@echo off
cd /d "%~dp0"
python "debit_certificates_manager.py"
echo.
echo -----------------------------------------
echo Script finalizado. Pressione qualquer tecla para sair.
pause >nul
