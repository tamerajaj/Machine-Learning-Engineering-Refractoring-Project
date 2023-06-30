from fastapi import Depends, FastAPI, HTTPException
import models
import schemas
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def index():
    return {"data": "houses list"}


# get all user
@app.get("/houses", response_model=list[schemas.HouseOutput])
def get_all_houses(db: Session = Depends(get_db)):
    house = db.query(models.House).all()
    if not house:
        raise HTTPException(status_code=404, detail="House not found")
    return house


# add user
@app.post("/houses", response_model=schemas.HouseOutput)
def create_house(request: schemas.HouseModel, db: Session = Depends(get_db)):
    house = models.House(date=request.date, price=request.price)
    db.add(house)
    db.commit()
    db.refresh(house)
    return house


# update user
@app.put("/houses/{id}")
def update_user(id: int, request: schemas.HouseUpdate, db: Session = Depends(get_db)):
    house = db.query(models.House).filter(models.House.id == id)
    if not house.first():
        raise HTTPException(status_code=404, detail="User not found")
    house.update(request.dict())
    db.commit()
    return "Updated successfully"


# delete user
@app.delete("/houses/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    house = db.query(models.House).filter(models.House.id == id)
    if not house.first():
        raise HTTPException(status_code=404, detail="User not found")
    house.delete(synchronize_session=False)
    db.commit()
    return "Deleted successfully"
