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
SET key1=nominatim
SET key2=geonames
SET filename=both_log.log
ECHO Service: %key1%,%key2% >> %filename%
ECHO Query: %q% >> %filename%
echo off
REM ===========================================================================
REM Building the command expresion.
REM ===========================================================================
SET curl_command=%NomApp% %modifier% %method%
REM ===========================================================================
REM ===================== call the service url NOMINATIM ======================
REM ===========================================================================
SET urlService=https://nominatim.openstreetmap.org/search?
SET command=%curl_command% "%urlService%q=%q%%ampers%accept-language=%lang%%ampers%format=jsonv2"
ECHO Start services time: %Time% >> %filename%
%command%
REM ===========================================================================
REM ===================== call the service url GEONAMES =======================
REM ===========================================================================
SET urlService=https://geogratis.gc.ca/services/geoname/%lang%/geonames.json?
SET command=%curl_command% "%urlService%q=%q%
%command%
ECHO Stop services time: %Time% >> %filename%
