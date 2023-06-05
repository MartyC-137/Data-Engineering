# This is an example of my Microsoft PowerShell profile. It sets up the Oh-My-Posh terminal theme,
# and contains the following user defined functions:
# PassGen: Generates random strong passwords
# Create-OpenInVSCode: Creates and opens a file in VS Code using one simple command

Set-Item -Path Env:TERMINAL_THEME -Value "https://raw.githubusercontent.com/JanDeDobbeleer/oh-my-posh/main/themes/night-owl.omp.json"

Import-Module Terminal-Icons

Set-PSReadlineKeyHandler -Key Tab -Function MenuComplete

oh-my-posh init pwsh --config $env:TERMINAL_THEME | Invoke-Expression

# Password Generator
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

# Alias for PassGen
Set-Alias -Name pg -Value PassGen

# Create and open file in VS Code

function Create-OpenInVSCode {
    param (
        [Parameter(Mandatory = $true)]
        [String]$newfile
    )
    
    # Create new file and open in VS Code
    code (new-item $newfile)
}
# Aliases for Create-OpenInVSCode
Set-Alias -Name new-file -Value Create-OpenInVSCode
Set-Alias -Name nf -Value Create-OpenInVSCode
