@echo off
setlocal enabledelayedexpansion

:prompt_installation_type
REM Prompt user for installation type
set /p "installation_type=Enter 'server' or 'client' for installation: "

REM Validate user input
if /i "%installation_type%" neq "server" if /i "%installation_type%" neq "client" (
    echo Invalid input! Please enter either 'server' or 'client'.
    goto prompt_installation_type
)


if /i "%installation_type%" equ "client" (
    set "name_file=client_name"
    set "installation_path=./client/"
) else (
    set "name_file=server_name"
    set "installation_path=./server/"
)

REM Prompt user for the name
set /p "name=Enter the name for the %installation_type%: "

REM Save name to file
echo %name% > "%installation_path%%name_file%"

REM Delete the other folder
if /i "%installation_type%" equ "client" (
    rd /s /q .\test_server\
) else (
    rd /s /q .\test_client\
)

echo Installation completed for %installation_type%: %name%
