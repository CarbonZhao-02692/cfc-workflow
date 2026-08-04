; <项目名> — Inno Setup 安装脚本
; 功能: 离线安装（Python embeddable + pip 依赖 + 项目代码）
;       自定义安装目录 + 子文件夹选项 + 彻底卸载

#define MyAppName "<项目中文名>"
#define MyAppDirName "<AppDir>"
#define MyAppVersion "X.Y.Z"
#define MyAppVersionSuffix "beta"
#define MyAppPublisher "<Publisher>"
#define MyAppURL "http://localhost:5000"
#define MyAppExeName "start.bat"

[Setup]
AppId={{<GUID>}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}{#MyAppVersionSuffix}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppDirName}
DefaultGroupName={#MyAppName}
UninstallDisplayIcon={app}\start.bat
UninstallDisplayName={#MyAppName} {#MyAppVersion}{#MyAppVersionSuffix}
Compression=lzma2/ultra64
SolidCompression=yes
OutputDir=.
OutputBaseFilename={#MyAppName}_Setup_v{#MyAppVersion}{#MyAppVersionSuffix}
PrivilegesRequired=admin
DisableProgramGroupPage=yes
CloseApplications=force
; 版本升级：自动检测旧版本
UsePreviousAppDir=yes
ShowLanguageDialog=no
; 大文件支持
ExtraDiskSpaceRequired=300000000

[Languages]
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"

; ── 自定义页面：子文件夹选项 ──────────────────────────

[Code]
var
  SubfolderPage: TInputOptionWizardPage;
  InstallTypePage: TInputOptionWizardPage;

procedure InitializeWizard;
begin
  { 页面 1: 安装类型选择 — 直接安装还是创建子文件夹 }
  InstallTypePage := CreateInputOptionPage(
    wpSelectDir,
    '安装方式',
    '选择安装方式',
    '请选择是将程序直接安装到选定的目录，还是在其中新建一个子文件夹进行安装。',
    True, False);
  InstallTypePage.Add('直接安装到所选目录');
  InstallTypePage.Add('在所选目录中新建子文件夹');
  InstallTypePage.Values[0] := True;  { 默认选中直接安装 }

  { 页面 2: 子文件夹名称（仅在选择了新建子文件夹时有用）}
  SubfolderPage := CreateInputOptionPage(
    InstallTypePage.ID,
    '子文件夹名称',
    '输入子文件夹名称',
    '程序将安装到您选择的目录下的子文件夹中。',
    True, False);
  SubfolderPage.Add('使用默认名称: "{#MyAppDirName}"');
  SubfolderPage.Values[0] := True;
end;

function ShouldSkipPage(PageID: Integer): Boolean;
begin
  Result := False;
  if PageID = SubfolderPage.ID then
    Result := not InstallTypePage.Values[1];
end;

function GetCustomDirName(Param: String): String;
begin
  if InstallTypePage.Values[1] then
    Result := '{#MyAppDirName}'
  else
    Result := '';
end;

function UpdateDirName(Path: String): String;
begin
  if InstallTypePage.Values[1] then
    Result := AddBackslash(Path) + '{#MyAppDirName}'
  else
    Result := Path;
end;

{ 在用户点击"下一步"时更新安装目录 }
function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;
  if CurPageID = InstallTypePage.ID then
  begin
    if InstallTypePage.Values[1] then
      WizardForm.DirEdit.Text := AddBackslash(WizardDirValue) + '{#MyAppDirName}'
    else
      WizardForm.DirEdit.Text := WizardDirValue;
  end;
end;

[Files]
; ── Python embeddable ──
Source: "python\python-3.12.10-embed-amd64.zip"; DestDir: "{app}\python"; Flags: ignoreversion
Source: "python\get-pip.py"; DestDir: "{app}\python"; Flags: ignoreversion

; ── 离线依赖包（.whl 文件）──
Source: "packages\*.whl"; DestDir: "{app}\packages"; Flags: ignoreversion

; ── 项目代码 ──
Source: "..\run.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\config.yaml"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\requirements.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\src\*.py"; DestDir: "{app}\src"; Flags: ignoreversion recursesubdirs
Source: "..\src\*"; DestDir: "{app}\src"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\docs\*.md"; DestDir: "{app}\docs"; Flags: ignoreversion
Source: "..\docs\*.pdf"; DestDir: "{app}\docs"; Flags: ignoreversion

; ── 安装脚本和工具 ──
Source: "post_install.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "setup_pgsql.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "timescaledb.zip"; DestDir: "{app}"; Flags: ignoreversion
Source: "start.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "init_env.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "uninstall_tool.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "uninstall_tool.bat"; DestDir: "{app}"; Flags: ignoreversion

[Dirs]
Name: "{app}\logs"; Permissions: users-full
Name: "{app}\data"; Permissions: users-full
; PG 部署临时目录（setup_pgsql.py 在线下载安装包落地处）
Name: "{app}\pgcache"; Permissions: users-full

[Icons]
Name: "{autoprograms}\{#MyAppName}\启动系统"; Filename: "{app}\start.bat"; WorkingDir: "{app}"
Name: "{autoprograms}\{#MyAppName}\打开网页"; Filename: "http://127.0.0.1:5000"
Name: "{autoprograms}\{#MyAppName}\配置文件夹"; Filename: "{app}"
Name: "{autoprograms}\{#MyAppName}\卸载"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\start.bat"; WorkingDir: "{app}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "创建桌面快捷方式"; GroupDescription: "快捷方式:"

; ── 安装后操作 ──
[Run]
; 第一步：解压 Python embeddable
Filename: "powershell.exe"; Parameters: "-NoProfile -ExecutionPolicy Bypass -Command ""Expand-Archive -Path '{app}\python\python-3.12.10-embed-amd64.zip' -DestinationPath '{app}\python' -Force"""; StatusMsg: "正在解压 Python 运行环境..."; Flags: runhidden

; 第二步：配置环境和安装依赖
Filename: "{app}\init_env.bat"; StatusMsg: "正在安装依赖包（离线安装）..."; Flags: runhidden waituntilterminated

; 第三步：安装完成提示
Filename: "{app}\start.bat"; Description: "立即启动系统"; Flags: postinstall nowait skipifsilent unchecked shellexec

[UninstallRun]
Filename: "{app}\init_env.bat"; Parameters: "uninstall"; RunOnceId: "CleanupEnv"

[UninstallDelete]
Type: filesandordirs; Name: "{app}\python"
Type: filesandordirs; Name: "{app}\packages"
Type: filesandordirs; Name: "{app}\logs"
Type: filesandordirs; Name: "{app}\data"
Type: filesandordirs; Name: "{app}\__pycache__"
Type: dirifempty; Name: "{app}"

[Messages]
; 简体中文提示覆盖
SelectDirDesc=请选择安装目录（避免中文字符）
SelectDirLabel3=安装到以下文件夹：（避免中文字符，默认不含中文）
