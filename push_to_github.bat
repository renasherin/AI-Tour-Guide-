@echo off
set PATH=%LOCALAPPDATA%\Programs\Git\cmd;%PATH%
echo ==============================================================
echo   Push Incredible Journeys to GitHub
echo ==============================================================
echo.
set /p REPO_URL="Enter your GitHub Repository URL (e.g. https://github.com/renasherin/incredible-journeys.git): "
if "%REPO_URL%"=="" (
    echo [!] No URL provided. Aborting.
    pause
    exit /b 1
)
git remote remove origin 2>nul
git remote add origin %REPO_URL%
git branch -M main
echo.
echo [*] Pushing to GitHub...
git push -u origin main
echo.
echo ==============================================================
echo   Done! Your code is now live on GitHub!
echo ==============================================================
pause
