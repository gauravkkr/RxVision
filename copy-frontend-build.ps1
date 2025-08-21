# This script copies the latest frontend build to the backend static folder for Flask to serve.
# Usage: Run this after building the frontend (npm run build or yarn build)


$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$frontendDir = Join-Path $scriptDir 'frontend'
$frontendDist = Join-Path $frontendDir 'dist'
$backendDir = Join-Path $scriptDir 'backend'
$backendStaticDir = Join-Path $backendDir 'static'
$backendStatic = Join-Path $backendStaticDir 'frontend'

if (!(Test-Path $frontendDist)) {
    Write-Host "Frontend build folder not found: $frontendDist"
    exit 1
}

if (!(Test-Path $backendStatic)) {
    New-Item -ItemType Directory -Path $backendStatic | Out-Null
}

Copy-Item -Path (Join-Path $frontendDist '*') -Destination $backendStatic -Recurse -Force
Write-Host "Frontend build copied to backend static folder."
