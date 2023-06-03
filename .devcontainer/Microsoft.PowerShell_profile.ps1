Import-Module posh-git
Import-Module PSFzf -ArgumentList 'Ctrl+t', 'Ctrl+r'
Import-Module z
Import-Module Terminal-Icons

Set-PSReadlineKeyHandler -Key Tab -Function MenuComplete

$env:POSH_GIT_ENABLED=$true
oh-my-posh init pwsh --config $env:POSH_THEME | Invoke-Expression

# NOTE: You can override the above env var from the devcontainer.json "args" under the "build" key.
function PassGen {
    param (
        [int]$Length = 20
    )
    
    $ValidCharacters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_-+='
    $Password = ''
    
    for ($i = 0; $i -lt $Length; $i++) {
        $RandomIndex = Get-Random -Minimum 0 -Maximum $ValidCharacters.Length
        $Password += $ValidCharacters[$RandomIndex]
    }
    
    return $Password
}

Set-Alias -Name pg -Value PassGen
# Aliases
Set-Alias -Name ac -Value Add-Content