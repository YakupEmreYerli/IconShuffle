# Installs the IconShuffle desktop app on Windows:
#
#   irm https://iconshuffle.app/install.ps1 | iex
#
# It downloads the latest installer from GitHub releases and runs it silently for the
# current user (no administrator rights; it goes to %LOCALAPPDATA%\Programs\IconShuffle).
#
# Settings (environment variables):
#   ICONSHUFFLE_VERSION  a release such as 0.2.0 instead of the latest
#   ICONSHUFFLE_REPO     the GitHub repository (default YakupEmreYerli/IconShuffle)
#
# Works in Windows PowerShell 5.1 and PowerShell 7.

& {
    $ErrorActionPreference = 'Stop'
    $ProgressPreference = 'SilentlyContinue'  # the progress bar makes 5.1 downloads crawl
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

    $repo = if ($env:ICONSHUFFLE_REPO) { $env:ICONSHUFFLE_REPO } else { 'YakupEmreYerli/IconShuffle' }
    $version = $env:ICONSHUFFLE_VERSION

    if (-not [Environment]::Is64BitOperatingSystem) {
        throw 'IconShuffle needs 64-bit Windows.'
    }
    # The build is x64; Windows 11 on ARM runs it through its x64 emulation.
    $arch = $env:PROCESSOR_ARCHITEW6432
    if (-not $arch) { $arch = $env:PROCESSOR_ARCHITECTURE }
    if ($arch -notin 'AMD64', 'ARM64') {
        throw "There is no IconShuffle build for $arch Windows."
    }

    if (-not $version) {
        $release = Invoke-RestMethod -UseBasicParsing "https://api.github.com/repos/$repo/releases/latest"
        $version = $release.tag_name
    }
    $version = $version -replace '^v', ''
    $file = "IconShuffle-$version-windows-x64-setup.exe"
    $url = "https://github.com/$repo/releases/download/v$version/$file"
    $setup = Join-Path ([IO.Path]::GetTempPath()) $file

    Write-Host "Downloading $file..."
    Invoke-WebRequest -UseBasicParsing -Uri $url -OutFile $setup
    try {
        Write-Host 'Installing for this user...'
        $run = Start-Process -FilePath $setup -Wait -PassThru -ArgumentList `
            '/VERYSILENT', '/SUPPRESSMSGBOXES', '/NORESTART', '/SP-', '/CLOSEAPPLICATIONS'
        if ($run.ExitCode -ne 0) { throw "The installer stopped with exit code $($run.ExitCode)." }
    } finally {
        Remove-Item -Force -ErrorAction SilentlyContinue $setup
    }

    $exe = Join-Path $env:LOCALAPPDATA 'Programs\IconShuffle\iconshuffle.exe'
    Write-Host "Installed IconShuffle $version. Open it from the Start menu, or: & '$exe'"
    if (-not (Get-Service -Name 'Apple Mobile Device Service' -ErrorAction SilentlyContinue)) {
        Write-Host 'For the USB cable, install Apple Devices from the Microsoft Store (iTunes works too).'
    }
}
