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