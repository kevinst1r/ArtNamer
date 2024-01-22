@echo off

:: Check for Python installation and install if not present
python -V >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Installing Python...
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; iwr -Uri 'https://www.python.org/ftp/python/3.10.4/python-3.10.4-amd64.exe' -OutFile 'python_installer.exe'; Start-Process -FilePath 'python_installer.exe' -Args '/quiet InstallAllUsers=1 PrependPath=1' -Wait; Remove-Item -Path 'python_installer.exe'}"
    echo Python installed.
) ELSE (
    echo Python is already installed.
)

:: Install PyQt5
echo Installing PyQt5...
python -m pip install PyQt5
echo PyQt5 installation complete.

:: Install OpenAI library
echo Installing OpenAI library...
python -m pip install openai
echo OpenAI installation complete.

:: Install dotenv library
echo Installing dotenv...
python -m pip install python-dotenv
echo Dotenv installation complete.

:: Install PyEnchant library
echo Installing PyEnchant...
python -m pip install pyenchant
echo PyEnchant installation complete.

echo Script finished. You can now run Art Namer!
pause
