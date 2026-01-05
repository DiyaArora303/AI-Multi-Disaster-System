import uvicorn
import os
import sys

# Ensure the root directory is in the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    # The 'reload' is great for dev, but create_task handles the background loop
    uvicorn.run("backend.app:app", host="127.0.0.1", port=8000, reload=True)