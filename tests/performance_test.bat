REM ===========================================================================
REM Enable local variables 
REM ===========================================================================
SETLOCAL ENABLEDELAYEDEXPANSION

REM ===========================================================================
REM Initialize constants, parameters and status variable
REM ===========================================================================
SET NomApp=curl
SET modifier=-X
SET method=GET
SET ampers=^&
SET q=meech
SET lang=en
SET keys=nominatim

REM ===========================================================================
REM The number of calls is set. Never more than max
REM ===========================================================================
echo off
SET /a max=1000
SET /a param1=%max%
SET /a param1=%1
if %param1% LSS %max% (SET /a max=%param1%)
echo on
echo %param1%
echo %max%
SET status=0
REM ===========================================================================
REM Building the command expresion.
REM ===========================================================================
SET urlAPI=https://fr59c5usw4.execute-api.ca-central-1.amazonaws.com/dev?
SET curl_command=%NomApp% %modifier% %method% "%urlAPI%

REM ===========================================================================
REM =========================== Loop to call the url ==========================
REM ===========================================================================
SET command=%curl_command%q=%q%%ampers%lang=%lang%%ampers%keys=%keys%"
@FOR /L %%G IN (1,1,%max%) DO (
echo loop: %%G
@%command%
)

REM ================= Show the results at the end of the loop =================
ECHO completed %max% calls

REM ===========================================================================
REM We pause so that the window does not close 
REM in case we have to double-click on the.bat to execute it.
REM ===========================================================================
PAUSE
