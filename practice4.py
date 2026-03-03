from fastapi import FastAPI, Request

# Initialize the FastAPI app
app = FastAPI()

# Mock database of crew members
crew = [
    {"id": 1, "name": "Cosmo", "role": "Captain"},
    {"id": 2, "name": "Alice", "role": "Engineer"},
    {"id": 3, "name": "Bob", "role": "Scientist"}
]


# ✅ GET member by ID
@app.get("/members/{crew_id}")
async def read_crew_member(crew_id: int):
    for member in crew:
        if member["id"] == crew_id:
            return member

    return {"message": "Crew member not found"}


# ✅ POST add new member
@app.post("/members/")
async def add_crew_member(request: Request):

    data = await request.json()
    name = data.get("name")
    role = data.get("role")

    new_id = max([member["id"] for member in crew]) + 1 if crew else 1

    new_member = {
        "id": new_id,
        "name": name,
        "role": role
    }

    crew.append(new_member)
    return new_member


# ✅ PUT update member
@app.put("/members/{crew_id}")
async def update_crew_member(crew_id: int, request: Request):

    data = await request.json()
    new_name = data.get("name")
    new_role = data.get("role")

    for member in crew:
        if member["id"] == crew_id:
            member["name"] = new_name
            member["role"] = new_role
            return member

    return {"message": "Crew member not found"}


# ✅ DELETE member
@app.delete("/members/{crew_id}")
async def delete_crew_member(crew_id: int):

    for member in crew:
        if member["id"] == crew_id:
            crew.remove(member)
            return {"message": f"Crew member {crew_id} deleted"}

    return {"message": "Crew member not found"}