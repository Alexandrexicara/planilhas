# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [
    ('templates', 'templates'),
    ('static', 'static'),
    ('banco_plus.db', '.'),
    ('banco.db', '.'),
    ('usuarios.db', '.'),
]
binaries = []
hiddenimports = [
    'sistema',
    'sistema_plus',
    'menu_principal',
    'usuarios_db',
    'gerenciamento_usuarios',
    'sistema_online_offline',
    'banco_offline',
    'flask',
    'werkzeug',
    'jinja2',
    'openpyxl',
    'PIL',
    'sqlite3',
]

for pkg in ('flask', 'werkzeug', 'jinja2', 'openpyxl'):
    pkg_datas, pkg_binaries, pkg_hidden = collect_all(pkg)
    datas += pkg_datas
    binaries += pkg_binaries
    hiddenimports += pkg_hidden

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Planilhas',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
