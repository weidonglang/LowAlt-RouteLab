$ErrorActionPreference = "SilentlyContinue"

$Ports = @(5173, 8001, 8081)

foreach ($Port in $Ports) {
    $connections = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    foreach ($connection in $connections) {
        $processId = $connection.OwningProcess
        if ($processId) {
            Write-Host "[STOP] port $Port process $processId" -ForegroundColor Yellow
            Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
        }
    }
}

Write-Host "LowAlt-RouteLab dev services stopped." -ForegroundColor Green

