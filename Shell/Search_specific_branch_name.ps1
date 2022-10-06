#!/usr/bin/env pwsh
git branch -a | Select-String "string_youre_looking_for"