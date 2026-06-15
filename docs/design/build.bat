@echo off

REM The documentation build process has the following dependencies:
REM python
REM pandoc
REM MiKTeX
REM pandoc-include
REM
REM Install using:
REM choco install rsvg-convert python miktex pandoc
REM pip install pandoc-include

setlocal
set FORMAT=%1
set INFILE=src.md
set OUTFILE=design.%FORMAT%
set INCLUDE_SRC=incl_%FORMAT%
set INCLUDE_DIR=incl
set FILTERS=--filter=pandoc-include

REM PDF constants
set SETTINGS=meta\default.yml
set HEADER=meta\header.tex

for %%i in ("%~dp0.") do set "ROOTDIR=%%~fi"

if [%FORMAT%] == [pdf] goto pdf
if [%FORMAT%] == [md] goto md

echo "Choose output format: pdf or md"
goto error

:pdf
    set PANDOC_ARGS=%FILTERS% %SETTINGS% -H %HEADER% -s %INFILE% -o %OUTFILE%
    goto exec

:md
    set PANDOC_ARGS=%FILTERS% -s %INFILE% -o %OUTFILE%
    goto exec

:exec
    pushd %ROOTDIR%

    rmdir /Q /S %INCLUDE_DIR% 2>NUL
    mkdir %INCLUDE_DIR%
    copy %INCLUDE_SRC%\* %INCLUDE_DIR% >NUL

    pandoc %PANDOC_ARGS%

    rmdir /Q /S %INCLUDE_DIR%

    popd
    goto eof

:eof
    exit /B 0

:error
    exit /B 1
