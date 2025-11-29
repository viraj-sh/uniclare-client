import os
import sys
import uvicorn

if __name__ == "__main__":
    # Add app/ folder to python path
    app_dir = os.path.join(os.path.dirname(__file__), "app")
    sys.path.insert(0, app_dir)

    port = int(os.environ.get("PORT", 8000))

    uvicorn.run(
        "main:app",  # <-- This is the correct import style
        host="0.0.0.0",
        port=port,
        reload=True,
    )
