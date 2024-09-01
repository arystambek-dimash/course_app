import uvicorn
from pathlib import Path

from src.core.register import register_app

app = register_app()

if __name__ == '__main__':
    try:
        config = uvicorn.Config(app=f'{Path(__file__).stem}:app', reload=True)
        server = uvicorn.Server(config)
        server.run()
    except Exception:
        raise
