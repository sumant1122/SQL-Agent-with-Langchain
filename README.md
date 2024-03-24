# SQL-Agent-with-Langchain
SQL Agent with Langchain Google PaLM as LLM

Run docker compose up 
```
docker compose up -d
```
Once Postgres container is up and running 
# Copy the schema and data files to the container
```
docker cp ./schema.sql postgres-demo-instance:/home 
docker cp ./data.sql postgres-demo-instance:/home
```

# Load the dataset into the database
```
docker exec -it postgres-demo-instance psql -U postgres -c '\i /home/schema.sql' \
docker exec -it postgres-demo-instance psql -U postgres -c '\i /home/data.sql'
```
# Run streamlit  
```streamlit run main.py```
