from supabase import create_client
import streamlit as st

url = "https://svejzpsygmjgscjwwmzz.supabase.co"
key = "SUA_KEY_AQUI" # Use a key que você me passou
supabase = create_client(url, key)

try:
    res = supabase.table("membros_core").select("*", count="exact").limit(1).execute()
    print("✅ CONEXÃO COM SUPABASE: OK")
    print(f"📊 Total de membros detectados: {res.count}")
except Exception as e:
    print(f"❌ ERRO DE CONEXÃO: {e}")
