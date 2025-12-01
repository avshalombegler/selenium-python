# Start ngrok for external access
Write-Host "Starting external access tunnel..." -ForegroundColor Cyan

# Check if Docker is running
docker ps > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Docker is not running. Start Docker first." -ForegroundColor Red
    exit 1
}

# Start ngrok
Start-Process -WindowStyle Hidden -FilePath "ngrok" -ArgumentList "http", "8080"

Write-Host "✓ Tunnel starting..." -ForegroundColor Green
Start-Sleep -Seconds 3

# Get and display URL
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:4040/api/tunnels"
    $httpsUrl = $response.tunnels | Where-Object {$_.proto -eq "https"} | Select-Object -ExpandProperty public_url
    
    if ($httpsUrl) {
        Write-Host "`n📊 External Allure Reports URL:" -ForegroundColor Cyan
        Write-Host $httpsUrl -ForegroundColor Yellow
        Write-Host "`n🏠 Local URL: http://localhost:8080" -ForegroundColor Gray
        Write-Host "`nURL copied to clipboard!" -ForegroundColor Green
        Set-Clipboard -Value $httpsUrl
    }
} catch {
    Write-Host "`nCheck status at: http://127.0.0.1:4040" -ForegroundColor Yellow
}