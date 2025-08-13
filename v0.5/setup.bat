
@echo off
title MADZIN01 - Versao 0.5
color 0A
:MENU
cls
echo ===================================
echo       MADZIN01 - VERSAO 0.5
echo ===================================
echo.
echo [1] Jogar offline (2 jogadores no mesmo PC)
echo [2] Jogar online (modo P2P)
echo [3] Sair
echo.
set /p op=Escolha uma opcao:

if "%op%"=="1" (
    python main_offline.py
    pause
    goto MENU
)
if "%op%"=="2" (
    python main.py
    pause
    goto MENU
)
if "%op%"=="3" (
    exit
)
goto MENU
