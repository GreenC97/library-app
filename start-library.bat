@echo off
echo Starting Library App...

:: Start MongoDB
start "MongoDB" mongod

:: Wait 3 seconds for MongoDB to start
timeout /t 3

:: Start Flask backend
start "Flask" cmd /k "cd C:\Users\pc\Desktop\library-app && python app.py"

:: Wait 2 seconds for Flask to start
timeout /t 2

:: Start Node frontend
start "Node" cmd /k "cd C:\Users\pc\Desktop\library-app && node server.js"

:: Wait 2 seconds then open browser
timeout /t 2
start http://127.0.0.1:3000

echo Library App is running!