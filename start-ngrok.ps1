Write-Host "Starting external access tunnel..." -ForegroundColor Cyan

# Check if Docker is running (you had this for some reason — kept it if you need it)
docker ps > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker is not running. Start Docker first." -ForegroundColor Red
    exit 1
}

# Start ngrok in the background
Start-Process -WindowStyle Hidden -FilePath "ngrok" -ArgumentList "http", "8080"

Write-Host "Tunnel starting..." -ForegroundColor Green
Start-Sleep -Seconds 4   # ngrok needs a moment to create the tunnel

try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:4040/api/tunnels" -ErrorAction Stop
    $httpsUrl = $response.tunnels | Where-Object { $_.proto -eq "https" } | Select-Object -First 1 -ExpandProperty public_url

    if ($httpsUrl) {
        Write-Host "`n External Allure Reports URL:" -ForegroundColor Cyan
        Write-Host $httpsUrl -ForegroundColor Yellow
        Write-Host "`n Local URL: http://localhost:8080" -ForegroundColor Gray
        Write-Host "`n URL copied to clipboard!" -ForegroundColor Green
        Set-Clipboard -Value $httpsUrl
    } else {
        Write-Host "No HTTPS tunnel found yet." -ForegroundColor Yellow
    }
} catch {
    Write-Host "`n Could not retrieve tunnel info. Is ngrok running?" -ForegroundColor Red
    Write-Host "Check the ngrok web interface at: http://127.0.0.1:4040" -ForegroundColor Yellow
}