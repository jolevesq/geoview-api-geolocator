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
SET q=%1
SET lang=en
SET keys=nominatim
SET filename=%keys%_log.log
ECHO Service: %keys% >> %filename%
ECHO Query: %q% >> %filename%
echo off
REM ===========================================================================
REM Building the command expresion.
REM ===========================================================================
SET curl_command=%NomApp% %modifier% %method%
REM ===========================================================================
REM ===================== call the service url ======================
REM ===========================================================================
SET urlService=https://nominatim.openstreetmap.org/search?
SET command=%curl_command% "%urlService%q=%q%%ampers%accept-language=%lang%%ampers%format=jsonv2"
ECHO Start %keys% service time: %Time% >> %filename%
%command%
ECHO Stop %keys% service time: %Time% >> %filename%
ECHO. >> %filename%
