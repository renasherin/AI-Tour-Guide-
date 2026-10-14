@echo off
set PATH=%LOCALAPPDATA%\Programs\Git\cmd;%LOCALAPPDATA%\Programs\Git Credential Manager;%PATH%
cd /d "%~dp0"
echo ==============================================================
echo   Pushing Incredible Journeys to GitHub...
echo ==============================================================
echo Target: https://github.com/renasherin/AI-Tour-Guide-
echo.
git push -u origin main
echo.
echo ==============================================================
echo   Done! Check your repository at:
echo   https://github.com/renasherin/AI-Tour-Guide-
echo ==============================================================
pause
