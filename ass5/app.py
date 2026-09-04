from fastapi import FastAPI, HTTPException
import json
import uvicorn

app = FastAPI()


with open("population.json", "r") as file:
    population_data = json.load(file)


@app.get("/")
def home():
    return {"message": "Population Finder API"}


@app.get("/population/{country}")
def find_population(country: str):

    for item in population_data:

        if item["country"].lower() == country.lower():
            return {
                "country": item["country"],
                "population": item["population"]
            }

    raise HTTPException(
        status_code=404,
        detail="Country not found"
    )

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )