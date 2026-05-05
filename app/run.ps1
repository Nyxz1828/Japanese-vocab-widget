$ErrorActionPreference = "SilentlyContinue"

function Get-BaseDir {
    if ($PSScriptRoot -and (Test-Path $PSScriptRoot)) {
        return $PSScriptRoot
    }

    if ($MyInvocation.MyCommand.Path) {
        return Split-Path -Parent $MyInvocation.MyCommand.Path
    }

    return Split-Path -Parent ([System.Diagnostics.Process]::GetCurrentProcess().MainModule.FileName)
}

$BaseDir = Get-BaseDir
$AppDir = Join-Path $BaseDir "app"
$MainPy = Join-Path $AppDir "main.py"

if (!(Test-Path $MainPy)) {
    exit 1
}

# Use pyw first because it runs Tkinter without opening CMD.
$pyw = Get-Command "pyw.exe" -ErrorAction SilentlyContinue

if ($pyw) {
    Start-Process `
        -FilePath $pyw.Source `
        -ArgumentList @("-3", "`"$MainPy`"") `
        -WorkingDirectory $AppDir `
        -WindowStyle Hidden

    exit 0
}

# Fallback: try pythonw.exe.
$python = Get-Command "python.exe" -ErrorAction SilentlyContinue

if ($python) {
    $pythonw = $python.Source -replace "python.exe$", "pythonw.exe"

    if (Test-Path $pythonw) {
        Start-Process `
            -FilePath $pythonw `
            -ArgumentList "`"$MainPy`"" `
            -WorkingDirectory $AppDir `
            -WindowStyle Hidden

        exit 0
    }
}

exit 1