from app.main import app
import uvicorn

# Replit is able to pull in modules when our run script is run from the root.
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
