# An example shell script to 'git mv' multiple files at once

# All files from one folder to new folder
mkdir my_new_folder
cd folder_your_files_are_in
foreach ($file in get-childitem *.sql) { git mv $file.name .\my_new_folder }

# Move all folders inside one folder to another folder
Get-ChildItem .\my_old_folder\ | ForEach-Object { git mv $_.FullName .\my_new_folder\ }