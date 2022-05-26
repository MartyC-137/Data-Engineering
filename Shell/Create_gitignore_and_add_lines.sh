#How to create a .gitignore file using bash

#Create .gitignore
cd /Users/johndoe/documents
touch .gitignore 

# zsh (Mac)
echo '.DS_Store' >> .gitignore

# Powershell (Windows)
Add-Content .gitignore '.DS_Store'