@echo off
REM Run main.py using uv
uv run src/main.py
if %errorlevel% neq 0 (
    echo [ERROR] Gagal menjalankan uv run src/main.py
    pause
)
