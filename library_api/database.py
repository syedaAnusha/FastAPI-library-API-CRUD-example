import os
from fastapi import FastAPI
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()  # Load from .env

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)
