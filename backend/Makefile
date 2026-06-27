nuitka-linux:
	uv run nuitka \
	--standalone \
	--remove-output \
	--lto=yes \
	--jobs=4 \
	--prefer-source-code \
	--assume-yes-for-downloads \
	--product-name="UniclareClient" \
	--company-name="viraj-sh" \
	--file-description="View end-semester marks from the Uniclare App" \
	--copyright="Copyright © 2025 github.com/viraj-sh" \
	--file-version=2.0.0 \
	--follow-imports \
	--no-deployment-flag=excluded-module-usage \
	--enable-plugin=pyqt6 \
	--include-package-data=fastapi \
	--include-package-data=uvicorn \
	--include-package-data=pydantic_settings \
	--include-package-data=httpx \
	--include-package-data=qtpy \
	--include-package-data=webview \
	--include-data-dir=app/static=static \
	desktop.py


nuitka-mac:
	uv run nuitka \
	--mode=app \
	--macos-app-name="UniclareClient" \
	--macos-app-icon=../.github/assets/icon.icns \
	--remove-output \
	--lto=yes \
	--jobs=4 \
	--prefer-source-code \
	--assume-yes-for-downloads \
	--product-name="UniclareClient" \
	--company-name="viraj-sh" \
	--file-description="View end-semester marks from the Uniclare App" \
	--copyright="Copyright © 2025 github.com/viraj-sh" \
	--file-version=2.0.0 \
	--product-version=2.0.0 \
	--follow-imports \
	--no-deployment-flag=excluded-module-usage \
	--enable-plugin=pyqt6
	--include-package-data=fastapi \
	--include-package-data=uvicorn \
	--include-package-data=pydantic_settings \
	--include-package-data=httpx \
	--include-package-data=qtpy \
	--include-package-data=webview \
	--include-data-dir=app/static=static \
	desktop.py


nuitka-win:
	uv run nuitka \
	--standalone \
	--remove-output \
	--lto=yes \
	--jobs=4 \
	--prefer-source-code \
	--assume-yes-for-downloads \
	--no-deployment-flag=excluded-module-usage \
	--product-name="UniclareClient" \
	--company-name="viraj-sh" \
	--file-description="View end-semester marks from the Uniclare App" \
	--copyright="Copyright © 2025 github.com/viraj-sh" \
	--file-version=2.0.0 \
	--follow-imports \
	--enable-plugin=pyqt6
	--include-package-data=fastapi \
	--include-package-data=uvicorn \
	--include-package-data=pydantic_settings \
	--include-package-data=httpx \
	--include-package-data=qtpy \
	--include-package-data=webview \
	--include-data-dir=app/static=static \
	desktop.py

desktop:
	uv run desktop.py

sync:
	uv sync --dev --extra desktop