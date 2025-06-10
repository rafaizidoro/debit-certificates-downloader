@echo off
cd /d %~dp0
call .venv\Scripts\activate
streamlit run cda_webapp.py
pause