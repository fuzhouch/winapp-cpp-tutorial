$VSInstallPath = &"${ENV:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe" -property installationPath
$DevShellDLL = "${VSInstallPath}\Common7\Tools\Microsoft.VisualStudio.DevShell.dll"
Import-Module "${DevShellDLL}"

${CurrentWorkingDirectory} = Get-Location
Enter-VsDevShell -VsInstallPath "${VSInstallPath}"
Set-Location ${CurrentWorkingDirectory}
