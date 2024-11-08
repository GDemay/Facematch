from pydantic import BaseModel

class ImageBase(BaseModel):
    pass
    


class ImageCreate(ImageBase):
    path: str


class Image(ImageBase):
    id: int
    score: float = 1000
    path: str

    class Config:
        orm_mode = True
        
        
class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True