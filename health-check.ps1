# Dual Core Caleon - Health Check Script (PowerShell)
# Usage: .\health-check.ps1

param(
    [string]$BaseUrl = "http://localhost"
)

Write-Host "🔍 Dual Core Caleon - Health Check" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

$Services = @(
    @{ Name = "nginx"; Url = "$BaseUrl/health" },
    @{ Name = "frontend"; Url = "$BaseUrl/" },
    @{ Name = "caleon-port"; Url = "$BaseUrl/api/health" },
    @{ Name = "caleon-core"; Url = "$BaseUrl/core/health" },
    @{ Name = "ollama"; Url = "$BaseUrl/ollama/api/tags" }
)

$OptionalServices = @(
    @{ Name = "tts-engine"; Url = "$BaseUrl/tts/health" }
)

$FailedServices = @()

function Test-Service {
    param(
        [string]$Name,
        [string]$Url
    )

    Write-Host "Checking $Name... " -NoNewline

    try {
        $response = Invoke-WebRequest -Uri $Url -TimeoutSec 10 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ OK" -ForegroundColor Green
            return $true
        } else {
            Write-Host "❌ FAILED (Status: $($response.StatusCode))" -ForegroundColor Red
            return $false
        }
    } catch {
        Write-Host "❌ FAILED ($($_.Exception.Message))" -ForegroundColor Red
        return $false
    }
}

Write-Host "`nCore Services:" -ForegroundColor Yellow
Write-Host "--------------" -ForegroundColor Yellow

foreach ($service in $Services) {
    if (-not (Test-Service -Name $service.Name -Url $service.Url)) {
        $FailedServices += $service.Name
    }
}

Write-Host "`nOptional Services:" -ForegroundColor Yellow
Write-Host "------------------"-ForegroundColor Yellow

foreach ($service in $OptionalServices) {
    Test-Service -Name $service.Name -Url $service.Url | Out-Null
}

Write-Host ""

if ($FailedServices.Count -eq 0) {
    Write-Host "🎉 All core services are healthy!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Access your Caleon instance at: http://localhost" -ForegroundColor Cyan
    exit 0
} else {
    Write-Host "❌ Some services are not healthy:" -ForegroundColor Red
    foreach ($service in $FailedServices) {
        Write-Host "   - $service" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "Check logs with: docker-compose logs $service" -ForegroundColor Yellow
    exit 1
}