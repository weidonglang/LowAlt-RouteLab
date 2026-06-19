$ErrorActionPreference = 'Stop'

$adapterUrl = ${env:LOWALT_ADAPTER_URL}
if ([string]::IsNullOrWhiteSpace($adapterUrl)) {
  $adapterUrl = 'http://127.0.0.1:8081'
}

$scenarioPath = Join-Path (Resolve-Path (Join-Path $PSScriptRoot '..')) 'algorithm-service\demo_scenarios\east_district_inspection.json'
if (-not (Test-Path $scenarioPath)) {
  Write-Host "[LowAlt][FAIL] Scenario file not found: $scenarioPath" -ForegroundColor Red
  exit 1
}

function Invoke-Json($method, $url, $body=$null) {
  try {
    if ($body -ne $null) {
      return Invoke-RestMethod -Method $method -Uri $url -ContentType 'application/json' -Body ($body | ConvertTo-Json -Depth 20) -TimeoutSec 20
    }
    return Invoke-RestMethod -Method $method -Uri $url -TimeoutSec 20
  } catch {
    Write-Host "[LowAlt][FAIL] $method $url failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host 'Start algorithm-service, route-adapter-service, and SkyGrid. For real mode, run route-adapter-service with skygrid.mode=real and a valid skygrid.token.'
    exit 1
  }
}

function Require-Data($title, $response) {
  if ($response -eq $null -or $response.data -eq $null) {
    Write-Host "[LowAlt][FAIL] $title returned empty data." -ForegroundColor Red
    exit 1
  }
  return $response.data
}

$scenario = Get-Content $scenarioPath -Raw | ConvertFrom-Json

Write-Host '[LowAlt] Running real SkyGrid integration demo...'
Write-Host "[LowAlt] Adapter URL: $adapterUrl"
Write-Host "[LowAlt] Scenario: $($scenario.scenarioId)"

$taskResponse = Invoke-Json POST "$adapterUrl/api/tasks" $scenario
$task = Require-Data 'Task creation' $taskResponse
Write-Host 'Route task created: OK'

$planResponse = Invoke-Json POST "$adapterUrl/api/tasks/$($task.id)/plan"
$planned = Require-Data 'Route planning' $planResponse
if ($planned.status -ne 'PLANNED') {
  Write-Host "[LowAlt][FAIL] Route planning did not complete. Current status: $($planned.status)" -ForegroundColor Red
  exit 1
}
Write-Host 'Route planned: OK'
Write-Host 'Risk evaluated: OK'
Write-Host 'TimeSlot converted: OK'

$conflictResponse = Invoke-Json POST "$adapterUrl/api/tasks/$($task.id)/check-conflict"
$conflict = Require-Data 'SkyGrid conflict check' $conflictResponse
Write-Host "SkyGrid conflict checked: OK ($($conflict.conflictStatus))"

$submitResponse = Invoke-Json POST "$adapterUrl/api/tasks/$($task.id)/submit-skygrid"
$submit = Require-Data 'SkyGrid booking submit' $submitResponse
if (-not $submit.bookingId) {
  Write-Host '[LowAlt][FAIL] SkyGrid submit did not return bookingId.' -ForegroundColor Red
  exit 1
}
Write-Host "Booking submitted: OK ($($submit.bookingId))"

Write-Host 'Demo completed successfully.'
