
@echo off
REM Configurazione: Inserisci il tuo nome utente GitHub e il nome del repository
SET GITHUB_USERNAME=agaldri
SET REPO_NAME=marketingupdate

REM Inizializza Git nella directory corrente
git init
git remote add origin https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git

REM Aggiungi e committa i file
git add .
git commit -m "Initial commit for GitHub Pages"

REM Crea il branch principale e carica i file
git branch -M main
git push -u origin main

REM Istruzioni per abilitare GitHub Pages
echo ===================================================
echo Repository creato! Ora abilita GitHub Pages:
echo 1. Vai su: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%/settings/pages
echo 2. Seleziona la branch "main" e salva.
echo ===================================================
pause
