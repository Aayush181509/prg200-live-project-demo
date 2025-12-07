# Student Management System

A simple web application demonstrating FastAPI backend with Streamlit frontend for teaching purposes.

## Project Structure

```
live-project/
├── backend/
│   ├── main.py              # FastAPI application
│   └── requirements.txt     # Backend dependencies
├── frontend/
│   ├── app.py              # Streamlit application
│   └── requirements.txt    # Frontend dependencies
└── README.md
```

## Features

### Backend (FastAPI)
- RESTful API with CRUD operations
- Student management endpoints:
  - `GET /students` - Get all students
  - `GET /students/{id}` - Get student by ID
  - `POST /students` - Create new student
  - `PUT /students/{id}` - Update student
  - `DELETE /students/{id}` - Delete student
- Data validation with Pydantic
- CORS enabled for frontend communication
- In-memory database (for simplicity)

### Frontend (Streamlit)
- User-friendly interface for student management
- View all students in a table
- Add new students
- Update existing students
- Delete students
- API integration using requests library

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Docker and Docker Compose (for containerized deployment)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the FastAPI server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

You can also access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:
```bash
streamlit run app.py
```

The frontend will be available at `http://localhost:8501`

### Docker Setup (Recommended)

1. Make sure Docker and Docker Compose are installed on your system

2. From the project root directory, run:
```bash
docker-compose up --build
```

This will:
- Build both backend and frontend images
- Start both services in containers
- Backend will be available at `http://localhost:8000`
- Frontend will be available at `http://localhost:8501`
- API documentation at `http://localhost:8000/docs`

3. To stop the containers:
```bash
docker-compose down
```

4. To run in detached mode (background):
```bash
docker-compose up -d
```

5. To view logs:
```bash
docker-compose logs -f
```

## Usage

1. **Start the backend first** - Run the FastAPI server on port 8000
2. **Start the frontend** - Run the Streamlit app on port 8501
3. Use the sidebar navigation to:
   - View all students
   - Add new students
   - Update existing students
   - Delete students

## API Examples

### Create a Student
```bash
curl -X POST "http://localhost:8000/students" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "age": 20,
    "course": "Computer Science"
  }'
```

### Get All Students
```bash
curl "http://localhost:8000/students"
```

### Update a Student
```bash
curl -X PUT "http://localhost:8000/students/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "age": 21,
    "course": "Computer Science"
  }'
```

### Delete a Student
```bash
curl -X DELETE "http://localhost:8000/students/1"
```

## Teaching Notes

This project demonstrates:
- **REST API Design** - Standard CRUD operations
- **HTTP Methods** - GET, POST, PUT, DELETE
- **Request/Response Flow** - Client-server communication
- **Data Validation** - Pydantic models
- **Error Handling** - HTTP status codes and error messages
- **Frontend-Backend Integration** - API calls from UI
- **State Management** - In-memory data storage

## Technologies Used

- **Backend**: FastAPI, Uvicorn, Pydantic
- **Frontend**: Streamlit, Requests, Pandas
- **Python**: 3.8+

## License

This project is created for educational purposes.
