DO $$ 
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'your_database') THEN
      CREATE DATABASE your_database;
   END IF;
END $$;

\c your_database

CREATE TABLE IF NOT EXISTS your_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);
