from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}




actor_skills = []
async def what_can_you_do(skills: str):
    for (skill) in actor_skills:
        actor_skills.append(skills)
    return {"skills": skills}
  
    