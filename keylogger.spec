# PyInstaller spec file for keylogger CLI and GUI

block_cipher = None

from PyInstaller.utils.hooks import collect_submodules

hiddenimports = collect_submodules('keylogger')

# CLI Analysis and EXE
cli_analysis = Analysis(
    ['keylogger/cli.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
cli_pyz = PYZ(cli_analysis.pure, cli_analysis.zipped_data, cipher=block_cipher)
cli_exe = EXE(
    cli_pyz,
    cli_analysis.scripts,
    [],
    exclude_binaries=True,
    name='keylogger',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)

# GUI Analysis and EXE
gui_analysis = Analysis(
    ['keylogger/gui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
gui_pyz = PYZ(gui_analysis.pure, gui_analysis.zipped_data, cipher=block_cipher)
gui_exe = EXE(
    gui_pyz,
    gui_analysis.scripts,
    [],
    exclude_binaries=True,
    name='keylogger-gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # GUI: no terminal window
)

coll = COLLECT(
    cli_exe,
    gui_exe,
    cli_analysis.binaries + gui_analysis.binaries,
    cli_analysis.zipfiles + gui_analysis.zipfiles,
    cli_analysis.datas + gui_analysis.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='keylogger'
)
