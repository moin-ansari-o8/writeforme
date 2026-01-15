# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['W:/workplace-1/writeforme/frontend/dashboard_v2.py'],
    pathex=['W:/workplace-1/writeforme'],
    binaries=[],
    datas=[
        ('W:/workplace-1/writeforme/assets/wfm_logo.ico', 'assets'),
        ('W:/workplace-1/writeforme/assets/wfm main logo1.png', 'assets'),
        ('W:/workplace-1/writeforme/frontend/assets', 'assets'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['webrtcvad', 'speech_recognition', 'pyaudio', 'faster_whisper'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='WriteForMe',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='W:/workplace-1/writeforme/assets/wfm_logo.ico',
)
