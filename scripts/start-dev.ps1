param(
    [switch]$SkipNpmInstall
)

$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$LogDir = Join-Path $Root "logs"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

function Test-PortListening {
    param([int]$Port)
    $connection = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
    return $null -ne $connection
}

function Start-ServiceProcess {
    param(
        [string]$Name,
        [int]$Port,
        [string]$WorkingDirectory,
        [string]$FilePath,
        [string[]]$Arguments
    )

    if (Test-PortListening -Port $Port) {
        Write-Host "[SKIP] $Name is already listening on port $Port" -ForegroundColor Yellow
        return
    }

    $stdout = Join-Path $LogDir "$Name.out.log"
    $stderr = Join-Path $LogDir "$Name.err.log"

    Write-Host "[START] $Name -> port $Port" -ForegroundColor Cyan
    Start-Process `
        -FilePath $FilePath `
        -ArgumentList $Arguments `
        -WorkingDirectory $WorkingDirectory `
        -WindowStyle Hidden `
        -RedirectStandardOutput $stdout `
        -RedirectStandardError $stderr
}

function Wait-Port {
    param(
        [string]$Name,
        [int]$Port,
        [int]$TimeoutSeconds = 45
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        if (Test-PortListening -Port $Port) {
            Write-Host "[OK] $Name is ready on port $Port" -ForegroundColor Green
            return
        }
        Start-Sleep -Seconds 1
    }

    Write-Host "[WARN] $Name did not open port $Port within $TimeoutSeconds seconds" -ForegroundColor Yellow
}

$AlgorithmDir = Join-Path $Root "algorithm-service"
$AdapterDir = Join-Path $Root "route-adapter-service"
$FrontendDir = Join-Path $Root "frontend"
$VenvPython = Join-Path $Root ".venv\Scripts\python.exe"

if (Test-Path $VenvPython) {
    $Python = $VenvPython
} else {
    $Python = "python"
}

if (-not $SkipNpmInstall -and -not (Test-Path (Join-Path $FrontendDir "node_modules"))) {
    Write-Host "[SETUP] frontend node_modules not found, running npm install..." -ForegroundColor Cyan
    Push-Location $FrontendDir
    npm install
    Pop-Location
}

Start-ServiceProcess `
    -Name "algorithm-service" `
    -Port 8001 `
    -WorkingDirectory $AlgorithmDir `
    -FilePath $Python `
    -Arguments @("-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8001")
Wait-Port -Name "algorithm-service" -Port 8001

Start-ServiceProcess `
    -Name "route-adapter-service" `
    -Port 8081 `
    -WorkingDirectory $AdapterDir `
    -FilePath "mvn.cmd" `
    -Arguments @("spring-boot:run")
Wait-Port -Name "route-adapter-service" -Port 8081 -TimeoutSeconds 90

Start-ServiceProcess `
    -Name "frontend" `
    -Port 5173 `
    -WorkingDirectory $FrontendDir `
    -FilePath "npm.cmd" `
    -Arguments @("run", "dev")
Wait-Port -Name "frontend" -Port 5173

Write-Host ""
Write-Host "LowAlt-RouteLab is ready:" -ForegroundColor Green
Write-Host "  Frontend:              http://127.0.0.1:5173/"
Write-Host "  algorithm-service:     http://127.0.0.1:8001"
Write-Host "  route-adapter-service: http://127.0.0.1:8081"
Write-Host ""
Write-Host "Logs are in: $LogDir"
Write-Host "If PowerShell blocks this script, run:"
Write-Host "  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass"

