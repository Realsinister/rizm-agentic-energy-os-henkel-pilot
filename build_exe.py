import os
import sys
import streamlit
import pulp

streamlit_dir = os.path.dirname(streamlit.__file__)
pulp_dir = os.path.dirname(pulp.__file__)

spec_content = f"""# -*- mode: python ; coding: utf-8 -*-
import os
import sys

block_cipher = None

streamlit_dir = r"{streamlit_dir}"
pulp_dir = r"{pulp_dir}"

added_files = [
    (r"src", "src"),
    (r"data", "data"),
    (r"site_config.json", "."),
    (os.path.join(streamlit_dir, "static"), os.path.join("streamlit", "static")),
    (os.path.join(streamlit_dir, "runtime"), os.path.join("streamlit", "runtime")),
]

a = Analysis(
    ['desktop_launcher.py'],
    pathex=['.'],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'streamlit',
        'streamlit.web.cli',
        'streamlit.runtime.caching',
        'streamlit.runtime.scriptrunner.magic_funcs',
        'pulp',
        'pulp.solverdir',
        'pulp.apis',
        'pulp.apis.coin_api',
        'plotly',
        'plotly.express',
        'plotly.graph_objects',
        'pandas',
        'numpy',
        'src',
        'src.app',
        'src.optimizer',
        'src.data_generator',
        'src.data_validator',
        'src.sensitivity_engine'
    ],
    hookspath=[],
    hooksconfig=dict(),
    runtime_hooks=[],
    excludes=[],
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
    name='Sample_Energy_OS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
"""

with open("Sample_Energy_OS.spec", "w", encoding="utf-8") as f:
    f.write(spec_content)

print("Spec file Sample_Energy_OS.spec created successfully.")
