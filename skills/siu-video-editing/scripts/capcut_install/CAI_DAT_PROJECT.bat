@echo off
rem Double-click: installs the CapCut project next to this file into this computer's CapCut project folder.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0cai_dat_project.ps1" %*
