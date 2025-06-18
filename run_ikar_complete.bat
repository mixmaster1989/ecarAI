@echo off
echo ===================================================
echo        ИКАР-Ассистент 2.0 - Запуск программы
echo ===================================================

:: Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ОШИБКА] Python не установлен или отсутствует в PATH.
    echo Пожалуйста, установите Python 3.8 или выше.
    echo Скачать можно с сайта: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check Python version
python -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ОШИБКА] Требуется Python версии 3.8 или выше.
    echo Текущая версия:
    python --version
    pause
    exit /b 1
)

:: Create directory structure
echo [1/3] Создание структуры каталогов...
python create_dirs.py
if %ERRORLEVEL% NEQ 0 (
    echo [ОШИБКА] Не удалось создать структуру каталогов.
    pause
    exit /b 1
)

:: Check and install dependencies
echo [2/3] Проверка и установка зависимостей...
python check_deps.py
if %ERRORLEVEL% NEQ 0 (
    echo [ОШИБКА] Не удалось установить зависимости.
    echo Проверьте подключение к интернету и попробуйте снова.
    pause
    exit /b 1
)

:: Run the application
echo [3/3] Запуск приложения...
echo ===================================================
python run_ikar.py

if %ERRORLEVEL% NEQ 0 (
    echo ===================================================
    echo [ОШИБКА] Произошла ошибка при запуске приложения.
    echo Проверьте логи в папке ikar/logs для получения дополнительной информации.
    pause
)