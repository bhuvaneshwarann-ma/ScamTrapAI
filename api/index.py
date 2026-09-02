import os
import sys

# Add project root directory to sys.path so 'backend' module can be imported
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Set database URL to /tmp/scamtrap.db when running in Vercel serverless environment
if os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
    os.environ["DATABASE_URL"] = "sqlite:////tmp/scamtrap.db"

from backend.app.main import app
from backend.app.db.engine import init_db

# Initialize DB tables on serverless function cold-start
try:
    init_db()
except Exception as e:
    print(f"[Vercel Startup] DB Init notice: {e}")

__all__ = ["app"]
