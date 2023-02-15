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
SET keys=geonames
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
SET urlService=https://geogratis.gc.ca/services/geoname/%lang%/geonames.json?
SET command=%curl_command% "%urlService%q=%q%%ampers%lang=%lang%"
ECHO Start %keys% service time: %Time% >> %filename%
%command%
ECHO Stop %keys% service time: %Time% >> %filename%
ECHO. >> %filename%
