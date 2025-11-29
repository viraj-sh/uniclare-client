from PyInstaller.utils.hooks import collect_submodules

hidden = collect_submodules("fastapi") + collect_submodules("uvicorn")

block_cipher = None

a = Analysis(
    ["launcher.py"],
    pathex=["."],
    binaries=[],
    datas=[
        ("static", "static"),
        ("services", "services"),
        ("core", "core"),
        ("api", "api"),
        ("schema", "schema"),
        ("static/src/favicon.ico", "static/src"),
    ],
    hiddenimports=hidden,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name="uniclare-client",
    console=True,
    icon="static/src/favicon.ico",
)

