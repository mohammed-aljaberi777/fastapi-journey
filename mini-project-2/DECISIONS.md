### 7. DECISIONS.md

You must include a `DECISIONS.md` file that answers the following questions **in your own words**:

1. What is an ODM and why do we use Beanie instead of writing raw MongoDB queries?
ODM is Object Document Mapper and It lets you work with the database and also this Beanie lets us define database documents and  do CRUD operations easily.
it makes the code cleaner and fewer mistakes


2. What is the role of the `Database` class — why wrap Beanie methods inside it instead of calling them directly in routes?
It handles all CRUD operations and makes it easy to change database logic later


3. What happens if `initialize_database()` is not called on startup? What would break and why?
If we don’t call it, Beanie won’t start and database won’t connect.
for example if i did not call this initialize_database() the beanie will not start also our database will not work






4. What is the difference between the `Event` document and the `EventUpdate` model, and why are they two separate classes?
EventUpdate is used for updating an event because you might only want to change one or two fields.
and about (Even) full event, all fields required 



### 6. Update DECISIONS.md

Add a **Part B** section to your existing `DECISIONS.md` and answer these four questions in your own words:

1. Why does `DATABASE_URL` use `mongo` as the hostname instead of `localhost`? What would happen if you kept `localhost`? 

localhost it means the same container so if i used localhost fastapi is going to try to connect itself because each service has a name inside docker that is why we use the service name mongo 



2. What does `depends_on` in `docker-compose.yml` do? Does it guarantee MongoDB is fully ready before FastAPI starts — and if not, what would?

`depends_on` it does or it makes the doker run mongo and fastaoi but it runs mongo first but it does not mean that mongo is ready 100% because if fastapi starts first before the database is ready is going to give us error 



3. What is the purpose of the volume in the `mongo` service? What happens to your data if you remove it and run `docker compose down`?

volume we use it to save our data if we do not have volume (docker compose down) we are going to lost all data so, even after restarting data is save 


4. Why do we copy `requirements.txt` and run `pip install` before copying the rest of the app code in the Dockerfile?

it will not reinstall the packages if we did not change the `requirements.txt`so it makes the construction faster and faster after that we copy the rest of code so we need to copy the `requirements.txt` first then install the libraries because docker uses caching 
