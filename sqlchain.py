import psycopg2
import os
from dotenv import load_dotenv
from langchain.sql_database import SQLDatabase
from langchain.llms import GooglePalm
from langchain_experimental.sql import SQLDatabaseChain

def get_db_chain():
    load_dotenv()

    llm = GooglePalm(google_api_key=os.environ["GOOGLE_API_KEY"], temperature=0.1)

    # Initialize LangChain's database agent
    database = SQLDatabase.from_uri(
    "postgresql+psycopg2://sql_agent:password@localhost:5432/postgres", 
    include_tables=["products", "users", "purchases", "product_inventory"]);

    # Initialize LangChain's database chain agent
    db_chain = SQLDatabaseChain.from_llm(llm, db=database, verbose=True, use_query_checker=True, return_intermediate_steps=False)
    return db_chain

def prepare_agent_prompt(input_text):
    agent_prompt = f'''
    Query the database using PostgreSQL syntax.

    Use the shoe_color enum to query the color. Do not query this column with any values not found in the shoe_color enum.
    Use the shoe_width enum to query the width. Do not query this column with any values not found in the shoe_width enum.

    The color and width columns are array types. The name column is of type VARCHAR.
    An example query using an array columns would be:
    SELECT * FROM products, unnest(color) as col WHERE col::text % SOME_COLOR;
    or
    SELECT * FROM products, unnest(width) as wid WHERE wid::text % SOME_WIDTH;

    An example query using the name column would be:
    select * from products where name ILIKE %input_text%; It is not necessary to search on all columns, only those necessary for a query. 
    Generate a PostgreSQL query using the input: ''' + input_text + '''
    
    Answer needs to be in the format of a JSON object. 
    This object needs to have the key "query" with the SQL query and "query_response" as a JSON array of the query response.
    '''

    return agent_prompt