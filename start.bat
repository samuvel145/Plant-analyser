@echo off
echo ==============================================
echo PlantMD Unified Server Startup
echo ==============================================

echo [1/3] Building the React Frontend...
cd frontend
call npm install
call npm run build
cd ..

echo [2/3] Installing Backend Dependencies...
cd backend
call pip install -r requirements.txt
cd ..

echo [3/3] Starting Unified FastAPI Server...
echo The site will be available at http://127.0.0.1:8000
echo Press Ctrl+C to stop the server.
echo.

cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000
