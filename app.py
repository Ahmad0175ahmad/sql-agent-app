import streamlit as st
import database_utils as db
import agent_logic as ai
import pandas as pd

# --- COLORS ---  #15173D
PRI_BG = "#F4F0E4"
ACC_PURPLE = "#982598"
SOFT_PINK = "#E491C9"
TEXT_GRAY = "#F1E9E9"
STATUS_RED = "#FF4B4B" # Standard Streamlit Red

st.markdown(f"""
    <style>
    /* 1. App Background */
    .stApp {{
        background-color: {PRI_BG};
    }}
    
    /* 2. Main Title & Subheaders (Database Preview, etc.) */
    h1, h2, h3 {{
        color: {ACC_PURPLE} !important;
    }}
    
    /* 3. Tab Text (Query Interface & Database Explorer) */
    .stTabs [data-baseweb="tab"] p {{
        color: {ACC_PURPLE} !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }}

    /* 4. Widget Labels (Editable SQL Query, Ask a query, etc.) */
    [data-testid="stWidgetLabel"] p {{
        color: {ACC_PURPLE} !important;
        font-weight: bold !important;
    }}

    /* 5. RED STATUS TEXT (Showing first 20 records...) */
    /* This targets the specific paragraph text in the main body */
    .stMarkdown p {{
        color: {ACC_PURPLE}; /* Default to purple */
    }}
    
    /* Specific override for the record count text */
    div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > em,
    div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > strong {{
        color: {STATUS_RED} !important;
    }}
    
    /* Generic catch-all for the status line if you use st.write */
    .status-text {{
        color: {STATUS_RED} !important;
        font-weight: bold;
    }}

    /* 6. Input & Text Area Boxes */
    .stTextInput input, .stTextArea textarea {{
        background-color: {TEXT_GRAY} !important;
        color: {ACC_PURPLE} !important;
        border: 2px solid {SOFT_PINK} !important;
    }}

    /* 7. Button Styling */
    .stButton>button {{
        background-color: {ACC_PURPLE} !important;
        color: white !important;
        border: 2px solid {SOFT_PINK} !important;
        border-radius: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

st.title("🚀 DataPulse: SQL AI Agent")

# --- NAVIGATION TABS ---
tab1, tab2 = st.tabs(["💬 Query Interface", "📊 Database Explorer"])

# --- TAB 1: QUERY INTERFACE ---
with tab1:
    # Query Input
    query_text = st.text_input("Ask a query", placeholder="e.g., give me first 5 products")
    
    if st.button("Generate SQL"):
        if query_text:
            content, content_type = ai.get_sql_from_query(query_text)
            st.session_state['gen_content'] = content
            st.session_state['gen_type'] = content_type
        else:
            st.warning("Please type a question first.")

    # Results Section
    if 'gen_content' in st.session_state:
        content = st.session_state['gen_content']
        content_type = st.session_state['gen_type']
        
        if content_type == "text":
            st.info(f"💡 {content}")
        else:
            st.markdown("---")
            st.subheader("🛠️ Editable SQL Query")
            # User can edit the generated SQL
            edited_sql = st.text_area("Edit SQL if needed:", value=content, height=150)
            
            if st.button("Run SQL"):
                try:
                    df = db.run_query(edited_sql)
                    st.success(f"Results Found: {len(df)}")
                    # width="stretch" is the new standard for 2026
                    st.dataframe(df, width="stretch")
                    
                    # CSV Export
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 Download results as CSV", data=csv, file_name='query_results.csv')
                except Exception as e:
                    st.error(f"Execution Error: {e}")

# --- TAB 2: DATABASE EXPLORER ---
with tab2:
    st.header("🔍 Database Preview")
    tables = db.get_all_tables()
    selected_table = st.selectbox("Select a Table:", tables)
    
    # Session State to handle 'Load All' logic correctly
    if "view_mode" not in st.session_state:
        st.session_state.view_mode = "preview"
    
    # Reset view mode if user changes the table selection
    if "last_selected_table" not in st.session_state or st.session_state.last_selected_table != selected_table:
        st.session_state.view_mode = "preview"
        st.session_state.last_selected_table = selected_table

    # Buttons for data loading
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("First 20 rows"):
            st.session_state.view_mode = "preview"
    with col2:
        if st.button("Load All Rows"):
            st.session_state.view_mode = "all"

    # Determine Query
    if st.session_state.view_mode == "all":
        final_query = f"SELECT * FROM {selected_table}"
        st.write(f"Showing **all** records from `{selected_table}`")
    else:
        final_query = f"SELECT * FROM {selected_table} LIMIT 20"
        st.write(f"Showing **first 20** records from `{selected_table}`")

    # Execute and Display
    try:
        df_db = db.run_query(final_query)
        st.dataframe(df_db, width="stretch")
        
        # Download button for the current table view
        csv_db = df_db.to_csv(index=False).encode('utf-8')
        st.download_button(f"📥 Download {selected_table} CSV", data=csv_db, file_name=f"{selected_table}.csv")
    except Exception as e:
        st.error(f"Error: {e}")