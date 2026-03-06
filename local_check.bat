@echo off
echo ==========================================
echo [1/2] Perevirka stylu kodu (Flake8)...
echo ==========================================
:: Використовуємо python -m, щоб Windows точно знайшла встановлені бібліотеки
python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
python -m flake8 . --count --exit-zero --max-complexity=10 --max-line-length=120 --statistics

echo.
echo ==========================================
echo [2/2] Zapusk testiv (Pytest)...
echo ==========================================
:: Створюємо папку для звітів, якщо її немає
if not exist "reports" mkdir reports

:: Запускаємо тести через python -m
python -m pytest --html=reports/local_report.html --self-contained-html

echo.
echo ==========================================
echo Perevirka zavershena!
echo Zvit testiv: reports/local_report.html
echo ==========================================
pause