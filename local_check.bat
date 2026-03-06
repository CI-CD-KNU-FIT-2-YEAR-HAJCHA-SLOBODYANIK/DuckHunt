@echo off
echo ==========================================
echo [1/2] Perevirka stylu kodu (Flake8)...
echo ==========================================
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=120 --statistics

echo.
echo ==========================================
echo [2/2] Zapusk testiv (Pytest)...
echo ==========================================
pytest --html=reports/local_report.html --self-contained-html

echo.
echo Perevirka zavershena! Zvit zberezheno v papku reports/
pause