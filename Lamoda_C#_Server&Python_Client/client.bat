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