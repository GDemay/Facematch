from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from fastapi import HTTPException
import random
from typing import List
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def create_image(db: Session, image: schemas.ImageCreate):
    db_image = models.Image(**image.dict())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def get_all_images(db: Session) -> List[schemas.Image]:

    images = db.query(models.Image).all()
    return images

def get_two_images(db: Session) -> List[schemas.Image]:
    # Count the total number of images
    total_images = db.query(func.count(models.Image.id)).scalar()

    if total_images < 2:
        raise HTTPException(status_code=400, detail="Not enough images in the database")

    # Fetch all image IDs
    image_ids = [image.id for image in db.query(models.Image.id).all()]
    
    # Select two unique random IDs
    random_ids = random.sample(image_ids, 2)
    
    # Fetch the images with the selected IDs
    random_images = db.query(models.Image).filter(models.Image.id.in_(random_ids)).all()
    
    return random_images

def delete_image(db: Session, image_id: int):
    # Fetch the image to ensure it exists
    db_image = db.query(models.Image).filter(models.Image.id == image_id).first()
    
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    # Delete the image
    db.delete(db_image)
    db.commit()
    return db_image


# Ensure you have the ELO calculation function in the same module
def calculate_elo(winner_score, loser_score, k=16):
    # Calculate expected scores
    expected_winner = 1 / (1 + 10 ** ((loser_score - winner_score) / 400))
    expected_loser = 1 / (1 + 10 ** ((winner_score - loser_score) / 400))
    
    # Update scores
    new_winner_score = winner_score + k * (1 - expected_winner)
    new_loser_score = loser_score + k * (0 - expected_loser)
    
    return new_winner_score, new_loser_score

def battle_images(db: Session, winner_id: int, loser_id: int) -> List[schemas.Image]:
    # Fetch the two images
    winner = db.query(models.Image).filter(models.Image.id == winner_id).first()
    loser = db.query(models.Image).filter(models.Image.id == loser_id).first()
    
    if not winner or not loser:
        raise HTTPException(status_code=404, detail="One or both images not found")
    
    # Calculate new ELO scores
    new_winner_score, new_loser_score = calculate_elo(winner.score, loser.score)
    
    # Update the scores
    winner.score = new_winner_score
    loser.score = new_loser_score
    
    # Commit the changes to the database
    db.commit()
    
    return[winner, loser]