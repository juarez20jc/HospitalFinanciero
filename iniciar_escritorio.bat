@echo off
cd /d "%~dp0"
set MYSQL_HOST=127.0.0.1
set MYSQL_PORT=3306
set MYSQL_USER=root
set MYSQL_PASSWORD=
set MYSQL_DATABASE=hospital_financiero
python desktop_app.py
pause
