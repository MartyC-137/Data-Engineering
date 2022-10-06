#!/usr/bin/env pwsh
foreach ($file in Get-ChildItem -Path C:\your\directory\here\*.py) {
    python $file.FullName
}