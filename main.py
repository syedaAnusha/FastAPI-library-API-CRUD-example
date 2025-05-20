from library_api.main import app

# This file re-exports the FastAPI app from library_api/main.py
# This allows the application to be run from the root directory
app = app  # This makes the app available at the root level