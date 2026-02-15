import psycopg2
import os
import pandas as pd
import warnings
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# CRITICAL: Silence the pandas UserWarning regarding SQLAlchemy
# This keeps your terminal clean since we are using pure psycopg2
warnings.filterwarnings("ignore", category=UserWarning, module='pandas')

def get_db_connection():
    """
    Establishes a connection to the PostgreSQL database.
    Works for both local (.env) and Streamlit Cloud (st.secrets).
    """
    try:
        # Check for Streamlit Secrets first (Cloud), fallback to .env (Local)
        dbname = st.secrets.get("DB_NAME") or os.getenv("DB_NAME")
        user = st.secrets.get("DB_USER") or os.getenv("DB_USER")
        password = st.secrets.get("DB_PASSWORD") or os.getenv("DB_PASSWORD")
        host = st.secrets.get("DB_HOST") or os.getenv("DB_HOST")
        port = st.secrets.get("DB_PORT") or os.getenv("DB_PORT")

        return psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
    except Exception as e:
        print(f"Database Connection Error: {e}")
        return None

def run_query(sql):
    """
    Executes a SQL query and returns the result as a Pandas DataFrame.
    """
    conn = get_db_connection()
    if conn:
        try:
            # pd.read_sql_query works with psycopg2 but triggers a warning 
            # that we silenced at the top of this file.
            df = pd.read_sql_query(sql, conn)
            conn.close()
            return df
        except Exception as e:
            if conn:
                conn.close()
            raise e
    else:
        raise Exception("Could not establish database connection.")

def get_all_tables():
    """
    Returns a list of tables available in the schema.
    """
    return ["customers", "products", "orders", "order_items"]