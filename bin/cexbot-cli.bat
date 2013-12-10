@echo off
rem Windows wrapper script

setlocal
set CEXBOT=%~f0

if exist "%~dp0..\python.exe" (
    "%~dp0..\python" "%~dp0cexbot-cli" %*
) else (
    python "%~dp0cexbot-cli" %*
)
endlocal