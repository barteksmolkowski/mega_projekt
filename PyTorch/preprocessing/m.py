import subprocess

# Polecenie PowerShell zmieniające język na angielski (USA)
cmd = "Set-WinSystemLocale -SystemLocale en-US; Set-WinUserLanguageList -LanguageList en-US -Force"
subprocess.run(["powershell", "-Command", cmd], capture_output=True)
