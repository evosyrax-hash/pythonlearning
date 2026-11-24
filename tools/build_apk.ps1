# Build python-practice.apk from the current web app.   Usage: .\tools\build_apk.ps1
# Needs Android Studio installed (uses its bundled Java and the Android SDK).
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$android = Join-Path $root 'android'
$www = Join-Path $android 'app\src\main\assets\www'

$env:JAVA_HOME = 'C:\Program Files\Android\Android Studio\jbr'
$sdk = Join-Path $env:LOCALAPPDATA 'Android\Sdk'
if (-not (Test-Path $env:JAVA_HOME)) { throw 'Android Studio (with its bundled Java) was not found.' }
if (-not (Test-Path $sdk)) { throw "Android SDK was not found at $sdk" }

# 1. Copy the web app into the APK's assets.
if (Test-Path $www) { Remove-Item -Recurse -Force $www }
New-Item -ItemType Directory -Force $www | Out-Null
$files = 'index.html', 'app.js', 'py-worker.js', 'harness.py', 'exercises.json', 'manifest.webmanifest',
         'icon.svg', 'icon-192.png', 'icon-512.png', 'icon-maskable-512.png', 'apple-touch-icon.png'
foreach ($f in $files) { Copy-Item (Join-Path $root $f) $www }
Copy-Item -Recurse (Join-Path $root 'vendor') $www

# 2. Tell Gradle where the SDK is.
"sdk.dir=$($sdk -replace '\\', '/')" | Out-File (Join-Path $android 'local.properties') -Encoding ascii

# 3. Build. (Java's local sockets fail in some temp folders on Windows, so give it one of our own.)
$uds = Join-Path $android '.gradle\uds'
New-Item -ItemType Directory -Force $uds | Out-Null
$env:JAVA_TOOL_OPTIONS = "-Djdk.net.unixdomain.tmpdir=$uds"
Push-Location $android
try {
    & .\gradlew.bat --console=plain assembleDebug
    if ($LASTEXITCODE -ne 0) { throw "Gradle build failed with exit code $LASTEXITCODE" }
} finally {
    Pop-Location
}

$apk = Join-Path $root 'python-practice.apk'
Copy-Item (Join-Path $android 'app\build\outputs\apk\debug\app-debug.apk') $apk -Force
"Built $apk ({0:N1} MB)" -f ((Get-Item $apk).Length / 1MB)
