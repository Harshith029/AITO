from fastapi import FastAPI
from app.routes import sample_route, traffic_routes
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sample_route.router)
app.include_router(traffic_routes.router)

@app.get("/")
def read_root():
    return {"message": "AITO Backend is running 🚀"}

if __name__ == "__main__":

    uvicorn.run("app.main:app", host="127.0.0.1", port=5000, reload=True)   
