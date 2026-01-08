@echo off
echo Starting the project...

:: 1. Start Django Backend with Virtual Environment
echo Starting Django Backend (djangooo)...
start cmd /k "cd /d djangooo && call "C:/Users/zanja/Documents/project/VS Code Project/smartDeci/.venv/Scripts/activate.bat" && python manage.py runserver"

:: 2. Start Vue Frontend
echo Starting Vue Frontend (web)...
start cmd /k "cd /d web && npm run dev"

echo Both processes are running in separate windows.
pause