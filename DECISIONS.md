- Why did you choose each Pydantic field type?
1- id ---int /// I used it like this because every book in my library has to have a unique number

2- title---str /// I used it like this to save or store the title as text

3-author---str /// because it is name and we have to store it as text

4-year ---int /// the year of publication must must be less than 2026 can not be in the futrue 

5-copies ---int /// because i want to know how many copy of the book we have in the library 

6- borrow_records---////to save or have all records of the book in my library 

################################################

- What does each validation rule protect against?

gt for the id can not be 0

ge and le i used yhem for prevent impossible valuse like 0 
copies or a year in futuer 

min_len  and max_len prevents empty or very short/long titles and author names.

return_date allow leaving it empty if the book is not returned yet.

@model_validator ensures the publishing year is not in the future. 



###########################################################

- Which endpoint uses `async` in a meaningful way, and why?


-endpoints that i used are get/post/put/delete and all of them used async    
-why?
-- if we have a huge DB id going to take time 
--so using async help the server to handle other req
##############################################################################################
<<database>>

1. What is `@contextmanager` and why do we use it instead of a plain function here?

contextmanager is used to define this function managed_db() and it helps us when we want to use         <<with managed_db() >> and i used it in my all endpoints in the file book.py no need to open and close the database connection 

plain function we have to call the functions db.connect_to_db() and db.close() every time when we write an endpoint and it is not good not because it is wrong to use it but because when we open a connection we might forget to close it 


################################################################################################
2. What does `check_same_thread=False` do and why is it necessary in a FastAPI application?

This lets SQLite be used by more than one thread at the same time. FastAPI can handle multiple requests at once FastAPI will raise an error when trying to access the same database connection from a different thread.
##################################################################################################
3. What happens to your data when the server restarts — with the old list vs. with SQLite?

old list -if I am using python list to store the books in my library all the data no matter how big is it when I restart the server would be lost because list exists only in RAM

SQLite - here it not same python list because all data I maen books and borrowers will be saved in the sqlite.bd file even if we restart our server the data will be there 

################################################################################################





