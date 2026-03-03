from fastapi import FastAPI, Request

app = FastAPI()

# Mock database of crew members
crew = [
    {"id": 1, "name": "Cosmo", "role": "Captain"},
    {"id": 2, "name": "Alice", "role": "Engineer"},
    {"id": 3, "name": "Bob", "role": "Scientist"}
]

# PUT endpoint to update crew member
@app.put("/update_crew/{crew_id}")
async def update_crew(crew_id: int, request: Request):

    # Parse JSON body
    data = await request.json()
    new_name = data.get("name")
    new_role = data.get("role")

    # Find and update crew member
    for member in crew:
        if member["id"] == crew_id:
            member["name"] = new_name
            member["role"] = new_role
            return member

    # If crew member not found
    return {"message": "Crew member not found"}