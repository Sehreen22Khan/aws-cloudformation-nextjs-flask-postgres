# aws-cloudformation-nextjs-flask-postgres
A full-stack application template using Next.js for the frontend, Flask for the backend, and PostgreSQL as the database, all containerized using Docker. This project provides a complete setup to build, connect, and deploy a scalable web application, with Docker Compose for easy service orchestration.

### Prerequisites:
1. Install Node.js and npm (for Next.js).
2. Install Python and pip (for Flask).
3. Install PostgreSQL and set up a database.

### Step 1: Set Up the Frontend (Next.js)
1. Create a new Next.js project:
   ```bash
   npx create-next-app frontend
   ```
2. Navigate into the project directory:
   ```bash
   cd frontend
   ```
3. Start the development server:
   ```bash
   npm install
   npm run dev
   ```
   This will start the Next.js development server at `http://localhost:3000`.

4. Create pages and components as needed for your frontend. You can use Axios or Fetch API to communicate with your backend API.

### Step 2: Set Up the Backend (Flask)
1. Create a new directory for the backend:
   ```bash
   mkdir backend
   cd backend
   ```
2. Create a virtual environment and activate it:
   ```bash
   py -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install Flask and other dependencies:
   ```bash
   pip install Flask Flask-Cors psycopg2-binary
   ```
4. Create a Flask application (`app.py`):
   ```python
   from flask import Flask, request, jsonify
   from flask_cors import CORS
   import psycopg2

   app = Flask(__name__)
   CORS(app)

   # Connect to PostgreSQL
   conn = psycopg2.connect(
       host="localhost",
       database="your_database",
       user="your_user",
       password="your_password"
   )
   cursor = conn.cursor()

   @app.route('/api/data', methods=['GET'])
   def get_data():
       cursor.execute("SELECT * FROM your_table")
       rows = cursor.fetchall()
       return jsonify(rows)

   if __name__ == '__main__':
       app.run(debug=True, host='0.0.0.0')
   ```
5. Start the Flask server:
   ```bash
   python app.py
   ```
   This will start the Flask server at `http://localhost:5000`.

### Step 3: Connect Frontend to Backend
1. In your Next.js application, you can use Axios or Fetch API to make requests to your Flask backend.

2. Install Axios in your Next.js project:
   ```bash
   npm install axios
   ```
3. Create a function in a component to fetch data from the Flask API:
   ```javascript
   import axios from 'axios';
   import { useEffect, useState } from 'react';

   export default function HomePage() {
     const [data, setData] = useState([]);

     useEffect(() => {
       axios.get('http://localhost:5000/api/data')
         .then(response => {
           setData(response.data);
         })
         .catch(error => {
           console.error('Error fetching data:', error);
         });
     }, []);

     return (
       <div>
         <h1>Data from Flask API</h1>
         <ul>
           {data.map((item, index) => (
             <li key={index}>{item}</li>
           ))}
         </ul>
       </div>
     );
   }
   ```

### Step 4: Set Up PostgreSQL Database
1. Start PostgreSQL and create a database:
   ```sql
   CREATE DATABASE your_database;
   
   CREATE TABLE your_table (
       id SERIAL PRIMARY KEY,
       name VARCHAR(100)
   );
   
   INSERT INTO your_table (name) VALUES ('Sample Data 1'), ('Sample Data 2');
   ```
2. Update the connection parameters in `app.py` to match your PostgreSQL configuration.

### Step 5: Running the Full Stack Application
- Make sure your PostgreSQL server is running.
- Start the Flask backend by running `python app.py`.
- Start the Next.js frontend by running `npm run dev` in the `frontend` directory.

Now, your Next.js frontend should be able to fetch data from the Flask backend, which in turn is connected to the PostgreSQL database.

### Step 6: Dockerize the Application

#### Dockerfile for Frontend (Next.js)
Create a `Dockerfile` in the `frontend` directory:
```dockerfile
# frontend/Dockerfile
FROM node:16

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json ./
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the Next.js application
RUN npm run build

# Expose port 3000 and start the server
EXPOSE 3000
CMD ["npm", "start"]
```

#### Dockerfile for Backend (Flask)
Create a `Dockerfile` in the `backend` directory:
```dockerfile
# backend/Dockerfile
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 5000 and start the server
EXPOSE 5000
CMD ["python", "app.py"]
```

Create a `requirements.txt` file in the `backend` directory:
```
Flask
Flask-Cors
psycopg2-binary
```

#### Docker Compose
Create a `docker-compose.yml` file in the root directory to manage both services:
```yaml
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - POSTGRES_HOST=postgres
      - POSTGRES_DB=your_database
      - POSTGRES_USER=your_user
      - POSTGRES_PASSWORD=your_password
    depends_on:
      - postgres

  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: your_database
      POSTGRES_USER: your_user
      POSTGRES_PASSWORD: your_password
    ports:
      - "5432:5432"
```

### Step 7: Running the Application with Docker
1. Build and start the containers:
   ```bash
   docker-compose up --build
   ```
2. The Next.js frontend will be available at `http://localhost:3000` and the Flask backend at `http://localhost:5000`.

Now, both your frontend and backend are running in separate Docker containers, managed by Docker Compose, along with a PostgreSQL container.

### Step 8: Sample Fun App Code for `pages/index.tsx`
Create a fun component for your Next.js app that allows users to input their name and see it saved to the database. Update your `pages/index.tsx` file as follows:
```typescript
import axios from 'axios';
import { useEffect, useState } from 'react';

export default function HomePage() {
  const [data, setData] = useState([]);
  const [name, setName] = useState('');

  useEffect(() => {
    axios.get('http://localhost:5000/api/data')
      .then(response => {
        setData(response.data);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, []);

  const handleAddName = () => {
    axios.post('http://localhost:5000/api/data', { name })
      .then(() => {
        setData(prevData => [...prevData, { name }]);
        setName('');
      })
      .catch(error => {
        console.error('Error adding name:', error);
      });
  };

  return (
    <div>
      <h1>Welcome to the Fun App!</h1>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Enter your name"
      />
      <button onClick={handleAddName}>Add Name</button>
      <h2>Names in the Database:</h2>
      <ul>
        {data.map((item, index) => (
          <li key={index}>{item.name}</li>
        ))}
      </ul>
    </div>
  );
}
```
This component allows users to input their name, which gets saved to the PostgreSQL database through the Flask backend, and displays the list of names from the database.
