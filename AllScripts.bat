:: @Authors: Bilal Hayat Butt, Anas ur Rehman, Sufyan Faizi


@echo off
set csvFileName="DOI"
set dirName="COCI"
set graphFileName="DOIDirected"
set hashFileName="DOIMapping"
set mappingKeyId="10.1145/3277591"
set mappingKey="1"
set Start_Date="2003-01-01"
set End_Date="2013-12-31"
set ISSN="0138-9130"
set fileNameOfCsv=%ISSN%DOI_List
set doiAuthorCsv=%ISSN%DOI_Author_List
set articleCitationCsv=%ISSN%ArticleNetwork
set folderName=%Start_Date%__%End_Date%__%ISSN%
set collaborationNetworkCsv=%ISSN%collNet
set collaborationNetwork=%ISSN%CollaborationNetwork
set authorCitationNetworkCsv="AuthorCitationNetwork"
set authorCitation=%ISSN%AuthorCitationNetwork
set articleFolder="Article"
set authorFolder="Author"
set collaborationFolder="Collaboration"
set start=%time%

::Use first two for new COCI data only.
@echo StartTime: %time%
::python3 1.Edge_List.py %dirName% %csvFileName% || goto :error
@echo "1.Edge_List" & echo.EndTime: %time% & echo.

@echo StartTime: %time%
::python3 2.SNAP_Binary.py %csvFileName% %graphFileName% %hashFileName% %folderName% || goto :error
@echo "2.SNAP_Binary" & echo.EndTime: %time% & echo.

@echo StartTime: %time%
python3 3.JsonDump.py %Start_Date% %End_Date% %ISSN% %folderName% || goto :error
@echo "3.JsonDump" & echo.EndTime: %time% & echo.

@echo StartTime: %time%
python3 4.Extraction.py %doiAuthorCsv% %folderName% || goto :error
@echo "4.Extraction" & echo.EndTime: %time% & echo.

@echo StartTime: %time%
python3 5.DOIList.py %fileNameOfCsv% %folderName% || goto :error
@echo "5.DOIList" & echo.EndTime: %time% & echo.

@echo StartTime: %time%
python3 6.ArticleCit.py %hashFileName% %graphFileName% %fileNameOfCsv% %articleCitationCsv% %folderName% %articleFolder% || goto :error
@echo "6.ArticleCit" & echo.EndTime: %time% & echo.

@echo StartTime: %time%
python3 7.CollaborationNet.py %collaborationNetworkCsv% %doiAuthorCsv%  %collaborationNetwork% %collaborationFolder% %folderName% || goto :error
@echo "7.CollaborationNet" & echo.EndTime: %time% & echo.

@echo StartTime: %time%
python3 8.AuthorCit.py %articleCitationCsv% %authorCitation% %doiAuthorCsv% %articleFolder% %folderName% %authorFolder% %hashFileName% || goto :error
@echo "8.AuthorCit" & echo.EndTime: %time% & echo.

@echo StartTime: %time%
python3 9.ArticleCentrality.py %folderName% %articleFolder% %articleCitationCsv% %hashFileName% || goto :error
@echo "9.ArticleCentrality" & echo.EndTime: %time% & echo.

@echo StartTime: %time%
python3 10.AuthorCitCentr.py %folderName% %authorFolder% %authorCitation% || goto :error
@echo "10.AuthorCitCentr" & echo.EndTime: %time% & echo.

@echo StartTime: %time%
python3 11.CollaborationCent.py %folderName% %collaborationFolder% %collaborationNetwork% || goto :error
@echo "11.CollaborationCent" & echo.EndTime: %time% & echo.

@echo StartTime: %time%
python3 12.EgoNetCode.py %hashFileName% %graphFileName% %folderName% %articleFolder% %articleCitationCsv% || goto :error
@echo "12.EgoNetCode" & echo.EndTime: %time% & echo.

@echo StartTime: %time%
python2 13.CrossrefDumpForEgoNet.py %folderName% || goto :error
@echo "13.CrossrefDumpForEgoNet" & echo.EndTime: %time% & echo.

@echo StartTime: %time%
python2 14.DOIAUthorExtractionForEgoNet.py %folderName% || goto :error
@echo "14.DOIAUthorExtractionForEgoNet" & echo.EndTime: %time% & echo.

@echo StartTime: %time%
python2 15.CollaborationNetwork.py  %folderName% || goto :error
@echo "15.CollaborationNetwork" & echo.EndTime: %time% & echo.

@echo StartTime: %time%
python2 16.AuthorCitation.py  %folderName% || goto :error
@echo "16.AuthorCitation" & echo.EndTime: %time% & echo.

@echo StartTime: %time%
python3 17.CentralityArticle.py  %folderName% || goto :error
@echo "17.CentralityArticle" & echo.EndTime: %time% & echo.

@echo StartTime: %time%
python3 18.CentralityAuthorCitation.py  %folderName% || goto :error
@echo "18.CentralityAuthorCitation" & echo.EndTime: %time% & echo.

@echo StartTime: %time%
python3 19.CentralityCollaboration.py  %folderName% || goto :error
@echo "19.CentralityCollaboration" & echo.EndTime: %time% & echo.

:error
set end=%time%
set options="tokens=1-4 delims=:.,"
for /f %options% %%a in ("%start%") do set start_h=%%a&set /a start_m=100%%b %% 100&set /a start_s=100%%c %% 100&set /a start_ms=100%%d %% 100
for /f %options% %%a in ("%end%") do set end_h=%%a&set /a end_m=100%%b %% 100&set /a end_s=100%%c %% 100&set /a end_ms=100%%d %% 100

set /a hours=%end_h%-%start_h%
set /a mins=%end_m%-%start_m%
set /a secs=%end_s%-%start_s%
set /a ms=%end_ms%-%start_ms%
if %ms% lss 0 set /a secs = %secs% - 1 & set /a ms = 100%ms%
if %secs% lss 0 set /a mins = %mins% - 1 & set /a secs = 60%secs%
if %mins% lss 0 set /a hours = %hours% - 1 & set /a mins = 60%mins%
if %hours% lss 0 set /a hours = 24%hours%
if 1%ms% lss 100 set ms=0%ms%

set /a totalsecs = %hours%*3600 + %mins%*60 + %secs%
echo All Scipts execution time %hours%:%mins%:%secs%.%ms% (%totalsecs%.%ms%s total)

pause
