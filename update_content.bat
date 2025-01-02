
@echo off
REM Configurazione: Inserisci il tuo nome utente GitHub e il nome del repository
SET GITHUB_USERNAME=agaldri
SET REPO_NAME=marketingupdate

REM Naviga nella directory del repository
cd /d "%~dp0"

REM Aggiungi e committa i file
git add .
git commit -m "Aggiornato contenuto della pagina web"
git push

REM Messaggio di conferma
echo ===================================================
echo Il sito è stato aggiornato con il nuovo contenuto.
echo Visita il sito per vedere le modifiche.
echo ===================================================
pause
