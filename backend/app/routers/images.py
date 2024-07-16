import os
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import SessionLocal
import uuid

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/images/", response_model=schemas.Image)
async def create_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    upload_dir = "uploaded_images"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(
        upload_dir, file.filename if file.filename else f"image_{uuid.uuid4().hex}.jpg"
    )
    with open(file_path, "wb") as f:
        f.write(await file.read())

    image_data = schemas.ImageCreate(path=f"/static/{file.filename}")
    return crud.create_image(db=db, image=image_data)


@router.get("/images/", response_model=List[schemas.Image])
async def get_all_images(db: Session = Depends(get_db)):
    return crud.get_all_images(db=db)


@router.get("/images/get_two_images", response_model=List[schemas.Image])
async def get_two_images(db: Session = Depends(get_db)):
    return crud.get_two_images(db=db)


@router.delete("/images/{image_id}", response_model=schemas.Image)
async def delete_image(image_id: int, db: Session = Depends(get_db)):
    return crud.delete_image(db=db, image_id=image_id)


@router.post("/images/battle/", response_model=List[schemas.Image])
async def battle_images_endpoint(
    winner_id: int, loser_id: int, db: Session = Depends(get_db)
):
    return crud.battle_images(db=db, winner_id=winner_id, loser_id=loser_id)
