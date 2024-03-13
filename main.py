from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
from typing import List
from datetime import datetime

app = FastAPI()
r = redis.Redis(host="redis", port=6379)
class Meal(BaseModel):
    text: str
    cal_value: float
    meal_id: int = 0
    date: str = datetime.now().strftime("%d/%m/%Y")

class UpdateMealModel(BaseModel):
    text: str
    cal_value: float

@app.post("/meals")
def create_meal(meal_data: Meal):
    meal_id = r.incr("meal_counter")
    key = f"meal:{meal_id}"

    meal_data.meal_id = meal_id
    meal_data.date = datetime.now().strftime("%d/%m/%Y")

    r.hmset(key, meal_data.dict())

    return meal_data

@app.put("/meals/{meal_id}")
def update_meal(meal_id: int, update_data: UpdateMealModel):
    key = f"meal:{meal_id}"
    existing_meal_data = r.hgetall(key)

    if not existing_meal_data:
        raise HTTPException(status_code=404, detail=f"Meal {meal_id} not found")

    existing_meal_data.update({"text": update_data.text, "cal_value": update_data.cal_value})

    r.hmset(key, existing_meal_data)

    return existing_meal_data

@app.delete("/meals/{meal_id}")
def delete_meal(meal_id: int):
    key = f"meal:{meal_id}"
    existing_meal_data = r.hgetall(key)

    if not existing_meal_data:
        raise HTTPException(status_code=404, detail=f"Meal {meal_id} not found")

    r.delete(key)

    return {"message": f"Meal {meal_id} deleted"}

@app.get("/meals/{meal_id}", response_model=Meal)
def get_meal(meal_id: int):
    key = f"meal:{meal_id}"
    meal_data = r.hgetall(key)

    if not meal_data:
        raise HTTPException(status_code=404, detail=f"Meal {meal_id} not found")

    meal_data_typed = {key.decode(): float(value.decode()) if key == b'cal_value' else value.decode() for key, value in
                       meal_data.items()}

    return Meal(**meal_data_typed)

@app.get("/meals", response_model=List[Meal])
def get_all_meals():
    all_meals = []
    for key in r.keys("meal:*"):
        meal_data = r.hgetall(key)

        meal_data_typed = {key.decode(): float(value.decode()) if key == b'cal_value' else value.decode() for key, value
                           in meal_data.items()}
        meal_data_typed['meal_id'] = int(key.decode().split(":")[1])

        all_meals.append(Meal(**meal_data_typed))

    return all_meals

@app.get("/")
def root():
    return {"Temp": "Text"}
