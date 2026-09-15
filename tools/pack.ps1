# Builds the plugin and zips the release packages into dist/.
#
#   powershell -ExecutionPolicy Bypass -File tools\pack.ps1
#
# Two zips, because the two sites install differently. Thunderstore wants manifest.json,
# icon.png and README.md at the zip root, so package/ is zipped by its contents rather
# than as a folder. Nexus is installed by Vortex or by hand into the BepInEx folder, so
# that one is just the DLL at BepInEx/plugins/.

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$pkg = Join-Path $root "package"
$dist = Join-Path $root "dist"

$manifest = Get-Content (Join-Path $pkg "manifest.json") -Raw | ConvertFrom-Json
$version = $manifest.version_number

# The plugin version and the package version are read by different people in different
# places; if they drift, the listing lies about what is in the DLL.
$plugin = Get-Content (Join-Path $root "src\Plugin.cs") -Raw
if ($plugin -notmatch 'PluginVersion\s*=\s*"([^"]+)"') { throw "Could not read the plugin version from src\Plugin.cs" }
if ($Matches[1] -ne $version) { throw "manifest.json is $version but the plugin says $($Matches[1])" }

dotnet build (Join-Path $root "src\CarturFollowCommand.csproj") -c Release
if (-not $?) { throw "build failed" }

# Cleared, not just overwritten: a DLL left behind from an earlier build would otherwise
# ride along in the zip and get loaded next to the current one.
$plugins = Join-Path $pkg "plugins"
if (Test-Path $plugins) { Remove-Item $plugins -Recurse -Force }
New-Item -ItemType Directory -Force -Path $plugins | Out-Null
$dll = Join-Path $root "src\bin\Release\net472\CarturFollowCommand.dll"
Copy-Item $dll $plugins -Force

New-Item -ItemType Directory -Force -Path $dist | Out-Null

# Written entry by entry rather than with Compress-Archive: that cmdlet stores Windows
# backslashes in the entry names, and an installer reading the zip then creates a single
# file literally named "plugins\CarturFollowCommand.dll" instead of the folder.
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

function Write-Zip($path, $entries) {
    if (Test-Path $path) { Remove-Item $path }
    $archive = [System.IO.Compression.ZipFile]::Open($path, "Create")
    try {
        foreach ($e in $entries) {
            [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($archive, $e.Source, $e.Name) | Out-Null
        }
    }
    finally { $archive.Dispose() }
    Write-Host "packed $path"
}

$tsEntries = Get-ChildItem $pkg -Recurse -File | ForEach-Object {
    @{ Source = $_.FullName; Name = $_.FullName.Substring($pkg.Length + 1).Replace("\", "/") }
}
Write-Zip (Join-Path $dist "Carturs_Follow_Command-$version.zip") $tsEntries

Write-Zip (Join-Path $dist "Carturs_Follow_Command-$version-Nexus.zip") @(
    @{ Source = $dll; Name = "BepInEx/plugins/CarturFollowCommand.dll" }
)
