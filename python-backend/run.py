
import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":

    port = int(os.environ.get("UVICORN_PORT", 8080))
    workers = int(os.environ.get("UVICORN_WORKERS", 1))
    root_path = str(os.environ.get("ROOT_PATH", ''))

    uvicorn.run(
        "source.app:wrapped_app",
        host="0.0.0.0",
        port=port,
        root_path=root_path,
        workers=workers
    )
