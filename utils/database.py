import os

from dotenv import load_dotenv
from supabase import create_client


# Load variables from the .env file
load_dotenv()


# Get Supabase credentials from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY")


# Create and export the Supabase client
supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)