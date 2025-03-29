from supabase import create_client, Client
from .config import settings

# Create Supabase client
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
