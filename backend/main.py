from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import router as auth_router
from routes.attendance import router as attendance_router

app = FastAPI(
    title="Attendance Management System",
    description="Office attendance tracking with face detection",
    version="1.0.0"
)

# Allow React frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(auth_router)
app.include_router(attendance_router)

@app.get("/")
def root():
    return {"message": "Attendance API is running", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "ok"}from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Attendance Management System")

# Allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Attendance API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}
