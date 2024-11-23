@echo off
chcp 65001 > nul

REM Path to the compiled C# server executable
set SERVER_PATH="ServerC#\ServerC#\publish\GrpcFileTransfer.exe"

REM Start the C# server
echo Starting C# server...
start "" %SERVER_PATH%

REM Navigate to Python client directory
cd "ClientPython"

REM Activate Python virtual environment
echo Activating Python virtual environment...
call .venv\Scripts\activate

REM Start Python client
echo Starting Python client...
python testGRPCtoC#.py

REM Deactivate virtual environment
deactivate