# nuitka-project-set: VERSION = __import__("tomllib").load(open("{MAIN_DIRECTORY}/../../pyproject.toml", "rb"))["project"]["version"]
# nuitka-project-set: MACOS_MIN = __import__("os").getenv("MACOSX_DEPLOYMENT_TARGET", "11.0")
# nuitka-project-set: ASSETS = "{MAIN_DIRECTORY}/../../.github/assets"

# nuitka-project-if: {OS} == "Darwin":
#    nuitka-project: --mode=app
#    nuitka-project: --macos-app-icon={ASSETS}/icon.icns
#    nuitka-project: --macos-app-macos-min-version={MACOS_MIN}
#    nuitka-project: --include-module=webview.platforms.cocoa
# nuitka-project-else:
#    nuitka-project: --mode=standalone
#
# nuitka-project-if: {OS} == "Linux":
#    nuitka-project: --enable-plugin=pyqt6
#    nuitka-project: --include-module=webview.platforms.qt
#    nuitka-project: --include-package=qtpy
# nuitka-project-if: {OS} == "Windows":
#    nuitka-project: --msvc=latest
#    nuitka-project: --windows-console-mode=attach
#    nuitka-project: --windows-icon-from-ico={ASSETS}/app.png
#    nuitka-project: --include-module=webview.platforms.winforms
#    nuitka-project: --include-module=webview.platforms.edgechromium
# nuitka-project-if: {OS} != "Linux":
#    nuitka-project: --nofollow-import-to=PyQt6
#    nuitka-project: --nofollow-import-to=qtpy
#    nuitka-project: --nofollow-import-to=webview.platforms.qt
#
# nuitka-project: --assume-yes-for-downloads
# nuitka-project: --product-name=Uniclare
# nuitka-project: --company-name=viraj-sh
# nuitka-project: --product-version={VERSION}
# nuitka-project: --file-description="Uniclare desktop client"
# nuitka-project: --output-dir=build/nuitka
# nuitka-project: --include-package=uniclare_client
# nuitka-project: --include-package-data=uniclare_client
# nuitka-project: --include-package-data=webview
# nuitka-project: --nofollow-import-to=uniclare_client.interfaces.cli
# nuitka-project: --nofollow-import-to=uniclare_client.interfaces.mcp
# nuitka-project: --nofollow-import-to=typer
# nuitka-project: --nofollow-import-to=fastmcp
# nuitka-project: --nofollow-import-to=keyring
# nuitka-project: --nofollow-import-to=webview.platforms.gtk
# nuitka-project: --nofollow-import-to=webview.platforms.cef
# nuitka-project: --nofollow-import-to=webview.platforms.android
# nuitka-project: --noinclude-pytest-mode=nofollow
# nuitka-project: --noinclude-setuptools-mode=nofollow
# nuitka-project: --noinclude-unittest-mode=nofollow
# nuitka-project: --lto=no
# nuitka-project: --report=build/nuitka/compilation-report.xml

from uniclare_client.interfaces.desktop.entry import run

if __name__ == "__main__":
    run()
