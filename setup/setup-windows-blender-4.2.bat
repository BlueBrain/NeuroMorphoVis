:: ####################################################################################################
:: # Copyright (c) 2016 - 2024, EPFL / Blue Brain Project
:: # Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
:: #
:: # This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
:: #
:: # This program is free software: you can redistribute it and/or modify it under the terms of the
:: # GNU General Public License as published by the Free Software Foundation, version 3 of the License.
:: #
:: # This Blender-based tool is distributed in the hope that it will be useful, but WITHOUT ANY
:: # WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
:: # PURPOSE.  See the GNU General Public License for more details.
:: #
:: # You should have received a copy of the GNU General Public License along with this program.
:: # If not, see <http://www.gnu.org/licenses/>.
:: ####################################################################################################

:: ####################################################################################################
:: This is a batch script for installing NeuroMorphoVis on Windows for a specific version of Blender.
:: For further details, please refer to the file name. Please do not modify the content of this script.
:: ####################################################################################################

@echo off

:: ####################################################################################################
:: Reference to the Blender version and OS and the online URL
:: ####################################################################################################
set "reference=blender-4.2.0-windows-x64"

:: ####################################################################################################
:: Download Blender and install it 
:: ####################################################################################################
REM Blender Zip file URL 
set "blender_url=https://download.blender.org/release/Blender4.2/%reference%.zip"

REM Path to save the downloaded Blender Zip file
set "blender_zip_file=%CD%\%reference%.zip"

REM Download the file using bitsadmin
echo Downloading ZIP file "%blender_url% ... 
bitsadmin /transfer myDownloadJob /download /priority normal "%blender_url%" "%blender_zip_file%"

REM Check if the Blender download was successful
echo Verifying the Blender archive .....
if exist "%blender_zip_file%" (
    echo Downloading Blender completed successfully!
) else (
    echo Download Blender failed. Please check your internet connection and run the batch file again.
    pause
    exit /b
)

REM Destination folder where the contents of the Blender zip file will be extracted
set "destination=%CD%"

REM Unzip the Blender Zip file using PowerShell
echo Extracting the Blender archive .....
powershell -command "Expand-Archive -Path '%blender_zip_file%' -DestinationPath '%destination%'"

REM Check if the extraction was successful
if exist "%destination%\%reference%" (
    echo Blender extraction completed successfully!
    echo Deleting the archive .....
    del "%destination%\%reference%.zip"
) else (
    echo Blender extraction failed! Please check the version of powershell.
)

:: ####################################################################################################
:: Download NeuroMorphoVis and install it 
:: ####################################################################################################
REM Check if curl is installed
echo Verifying curl ..... 
curl --version >nul 2>&1
if %errorlevel% neq 0 (
    echo curl is not installed on this system.
    pause
    exit /b
)

REM Set the URL for the ZIP archive of the master branch of NeuroMorphoVis
set "repoURL=https://github.com/BlueBrain/NeuroMorphoVis/archive/refs/heads/master.zip"

REM Set the output file path for the ZIP
set "neuromorphovis_zip_file=%CD%\NeuroMorphoVis-master.zip"

REM Download the ZIP file
echo Downloading NeuroMorphoVis .....
curl -L -o "%neuromorphovis_zip_file%" "%repoURL%"

REM Destination folder where the contents will be extracted
set "add_on_path=%CD%\%reference%\4.2\scripts\addons_core"

REM Unzip the file using PowerShell
echo Integrating NeuroMorphoVis to Blender [%reference%]...
powershell -command "Expand-Archive -Path '%neuromorphovis_zip_file%' -DestinationPath '%add_on_path%'"

REM Check if the extraction was successful
if exist "%add_on_path%\NeuroMorphoVis-master" (
    echo NeuroMorphoVis integration into Blender completed successfully!
    echo Deleting the archive ...
    del "%neuromorphovis_zip_file%"
) else (
    echo NeuroMorphoVis extraction failed.
)

:: ####################################################################################################
:: Download all the python dependencies 
:: ####################################################################################################
REM Python path
set "python_path= %CD%\%reference%\4.2\python\bin\python.exe"

REM 'enabledelayedexpansion' allows to use and modify environment variables within a for loop 
setlocal enabledelayedexpansion

REM Set the path to the text file
set "filePath=%CD%\deps.txt"

REM Check if the file exists
if not exist "%filePath%" (
    echo File not found: %filePath%
    pause
    exit /b
)

REM Read the file line by line
echo Reading %filePath% line by line:
for /f "delims=" %%i in (%filePath%) do (
    echo Installing %%i .....
    echo The package [%%i] is OPTIONAL. DO NOT WORRY IF NOT INSTALLED.
    %python_path% -m pip install %%i
)

:: ####################################################################################################
echo Installation completed!

pause
