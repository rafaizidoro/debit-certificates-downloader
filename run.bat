@echo off
cd /d "%~dp0"
python "CDA download.py"
echo.
echo -----------------------------------------
echo Script finalizado. Pressione qualquer tecla para sair.
pause >nul
