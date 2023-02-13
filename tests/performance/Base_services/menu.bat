echo off
REM ===========================================================================
REM Enable local variables 
REM ===========================================================================
SETLOCAL ENABLEDELAYEDEXPANSION

REM ===========================================================================
REM Initialize constants, parameters and status variable
REM ===========================================================================
SET NOMINATIM_LOG=.\nominatim_log.log
SET GEONAMES_LOG=.\geonames_log.log
SET BOTH_LOG=.\both_log.log
SET MERGED_LOG=.\merged_log.log
REM ===========================================================================
REM Remove old results
REM ===========================================================================
if exist %NOMINATIM_LOG% del %NOMINATIM_LOG%
if exist %GEONAMES_LOG% del %GEONAMES_LOG%
if exist %BOTH_LOG% del %BOTH_LOG%
if exist %MERGED_LOG% del %MERGED_LOG%
REM ===========================================================================
REM Get the string for the Query
REM ===========================================================================
:NEW_TEST
SET q=""
set /p q= Enter the text for the request (blank to finish) :
if %q%=="" goto EOF
call test_nominatim_url %q%
call test_geonames_url %q%
call test_both_url %q%
goto NEW_TEST
:EOF
set /p Y=Merge log files into one (y/n)? :
if %Y% NEQ y goto BYE
if exist %NOMINATIM_LOG% type %NOMINATIM_LOG% >>  %MERGED_LOG%
if exist %GEONAMES_LOG% type %GEONAMES_LOG% >>  %MERGED_LOG%
if exist %BOTH_LOG% type %BOTH_LOG% >>  %MERGED_LOG%
:BYE 
ECHO BYE
