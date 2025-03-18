from fastapi import FastAPI, Query, Body, Path

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "stars": 4},
    {"id": 2, "title": "Dubai", "stars": 4},
]


@app.get("/hotels")
def get_hotels(
    title: str = Query(default=None, description="Название отеля"),
    stars: int = Query(default=None, description="Количество звёзд"),
):
    result = []
    for hotel in hotels:
        if title and hotel["title"] != title:
            continue
        if stars and hotel["stars"] != stars:
            continue
        result.append(hotel)

    return result


@app.get("/hotels/{id}")
def get_hotel(
    id: int = Path(description="ИД отеля")
):
    for hotel in hotels:
        if hotel["id"] == id:
            return hotel


@app.post("/hotels")
def create_hotel(
    title: str = Body(embed=True, description="Название отеля"),
    stars: int = Body(embed=True, description="Количество звёзд"),
):
    hotel = {"id": hotels[-1]["id"] + 1, "title": title, "stars": stars}
    hotels.append(hotel)

    return hotel


@app.put("/hotels/{id}")
def update_hotel(
    id: int = Path(description="ИД отеля"),
    title: str = Body(description="Название отеля"),
    stars: int = Body(description="Количество звёзд"),
):
    for hotel in hotels:
        if hotel["id"] == id:
            hotel["title"] = title
            hotel["stars"] = stars

            return hotel


@app.patch("/hotels/{id}")
def edit_hotel(
    id: int = Path(description="ИД отеля"),
    title: str = Body(default=None, description="Название отеля"),
    stars: int = Body(default=None, description="Количество звёзд"),
):
    for hotel in hotels:
        if hotel["id"] == id:
            hotel["title"] = title if title else hotel["title"]
            hotel["stars"] = stars if stars else hotel["stars"]

            return hotel


@app.delete("/hotels/{id}")
def delete_hotels(id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != id]
    return {"status": "OK"}
