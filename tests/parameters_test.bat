REM ===========================================================================
REM Enable local variables 
REM ===========================================================================
SETLOCAL ENABLEDELAYEDEXPANSION

 
REM ===========================================================================
REM Allow accented characters
REM ===========================================================================
chcp 1252

REM ===========================================================================
REM Initialize constants, parameters and status variable
REM ===========================================================================
SET NomApp=curl
SET modifier=-X
SET method=GET
SET ampers=^&
SET percent=^%
rem q
SET q1=meech
SET q2=hilliardton
SET q_plus=meech+lake
SET q_percent=meech%percent%lake
SET q_percent20=meech%percent%20lake
SET q_not_ok=lake meech
rem lang
SET lang_e=en
SET lang_f=fr
SET lang_all=en,fr
SET lang_other=gr
rem keys
SET keys_g=geonames
SET keys_n=nominatim
SET keys_all=nominatim,geonames
SET keys_other=google
rem
SET invalidParam=anything
rem
SET status=0
REM ===========================================================================
REM Building the command expresion.
REM ===========================================================================
SET urlAPI=https://fr59c5usw4.execute-api.ca-central-1.amazonaws.com/dev?
SET curl_command=%NomApp% %modifier% %method% "%urlAPI%

REM 0X Set of tests with invalide parameters
REM ===========================================================================
REM ===================== Test 01. url without parameters =====================
REM ===========================================================================
SET command=%curl_command%
%command%
SET Statut=%Statut%%ERRORLEVEL%

REM ===========================================================================
REM ===================== Test 02. url with wrong query =======================
REM ===========================================================================
SET command=%curl_command%q=%q_not_ok%"
%command%
SET Statut=%Statut%%ERRORLEVEL%
echo %status%

REM ===========================================================================
REM ===================== Test 03. url with wrong language ====================
REM ===========================================================================
SET command=%curl_command%q=%q1%%ampers%lang=%lang_other%"
%command%
SET Statut=%Statut%%ERRORLEVEL%
echo %status%

REM ===========================================================================
REM ===================== Test 04. url with wrong service =====================
REM ===========================================================================
SET command=%curl_command%q=%q1%%ampers%keys=%keys_other%"
%command%
SET Statut=%Statut%%ERRORLEVEL%
echo %status%

REM 1X Set of tests with valid parameters
REM ===========================================================================
REM ===================== Test 11. url with all parameters ====================
REM ===========================================================================
SET command=%curl_command%q=%q1%%ampers%lang=%lang_e%%ampers%keys=%keys_n%"
%command%
SET Statut=%Statut%%ERRORLEVEL%
echo %status%

REM ===========================================================================
REM ===================== Test 12. url with lang other than default ===========
REM ===========================================================================
SET command=%curl_command%q=%q1%%ampers%lang=%lang_f%%ampers%keys=%keys_n%"
%command%
SET Statut=%Statut%%ERRORLEVEL%
echo %status%

REM ===========================================================================
REM ===================== Test 13. url without lang ===========================
REM ===========================================================================
SET command=%curl_command%q=%q1%%ampers%keys=%keys_n%"
%command%
SET Statut=%Statut%%ERRORLEVEL%
echo %status%

REM ===========================================================================
REM ===================== Test 14. url with service other =====================
REM ===========================================================================
SET command=%curl_command%q=%q1%%ampers%lang=%lang_f%%ampers%keys=%keys_g%"
%command%
SET Statut=%Statut%%ERRORLEVEL%
echo %status%

REM ===========================================================================
REM ===================== Test 15. url without service ========================
REM ===========================================================================
SET command=%curl_command%q=%q1%%ampers%lang=%lang_e%"
%command%
SET Statut=%Statut%%ERRORLEVEL%
echo %status%

REM ===========================================================================
REM ===================== Test 16. url with neither lang nor service ==========
REM ===========================================================================
SET command=%curl_command%q=%q1%"
%command%
SET Statut=%Statut%%ERRORLEVEL%
echo %status%

REM ===========================================================================
REM ===================== Test 17. url with differente query ==================
REM ===========================================================================
SET command=%curl_command%q=%q2%%ampers%lang=%lang_e%%ampers%keys=%keys_n%"
%command%
SET Statut=%Statut%%ERRORLEVEL%
echo %status%

REM ===========================================================================
REM ===================== Test 18. url with query with plus sign ==============
REM ===========================================================================
SET command=%curl_command%q=%q_plus%%ampers%lang=%lang_e%%ampers%keys=%keys_n%"
%command%
SET Statut=%Statut%%ERRORLEVEL%
echo %status%

REM ===========================================================================
REM ===================== Test 19. url with query with percent20 ==============
REM ===========================================================================
SET command=%curl_command%q=%q_percent20%%ampers%lang=%lang_e%%ampers%keys=%keys_n%"
%command%
SET Statut=%Statut%%ERRORLEVEL%
echo %status%

REM ===================== Compare status against expectations =================
@IF [%Statut%] EQU [0300000000003] (
 @ECHO INFORMATION : Metric test passed
 @COLOR A0
) ELSE (
 @ECHO ERROR: Metric test failed
 @COLOR CF
)

 
REM ===========================================================================
REM We pause so that the window does not close 
REM in case we have to double-click on the.bat to execute it.
REM ===========================================================================
PAUSE
COLOR
CLS
EXIT