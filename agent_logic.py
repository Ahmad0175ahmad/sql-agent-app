import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize the OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_sql_from_query(user_query):
    system_prompt = """
    You are an expert SQL Assistant for a database with: customers, products, orders, order_items.
    Return ONLY raw SQL. No markdown backticks. Limit queries to 100 rows.
    If the user greets you or asks unrelated questions, 
    return: 'REFUSAL: I am a SQL Specialist. Please ask about your data.'
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            temperature=0
        )
        
        raw_text = response.choices[0].message.content.strip()
        
        # Clean up any potential markdown backticks
        raw_text = raw_text.replace("```sql", "").replace("```", "").strip()
        
        if "REFUSAL:" in raw_text:
            return raw_text.replace("REFUSAL:", "").strip(), "text"
        return raw_text, "sql"
        
    except Exception as e:
        return f"OpenAI Error: {str(e)}", "text"