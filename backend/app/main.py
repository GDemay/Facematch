import os
from fastapi import FastAPI, Depends, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS Middleware
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static files
app.mount("/static", StaticFiles(directory="uploaded_images"), name="static")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/images/", response_model=schemas.Image)
async def create_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    upload_dir = "uploaded_images"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    image_data = schemas.ImageCreate(path=f"/static/{file.filename}")
    return crud.create_image(db=db, image=image_data)

@app.get("/images/", response_model=List[schemas.Image])
async def get_all_images(db: Session = Depends(get_db)):
    return crud.get_all_images(db=db)

@app.get("/images/get_two_images", response_model=List[schemas.Image])
async def get_two_images(db: Session = Depends(get_db)):
    return crud.get_two_images(db=db)

@app.delete("/images/{image_id}", response_model=schemas.Image)
async def delete_image(image_id: int, db: Session = Depends(get_db)):
    return crud.delete_image(db=db, image_id=image_id)

@app.post("/images/battle/", response_model=List[schemas.Image])
async def battle_images_endpoint(winner_id: int, loser_id: int, db: Session = Depends(get_db)):
    return crud.battle_images(db=db, winner_id=winner_id, loser_id=loser_id)
