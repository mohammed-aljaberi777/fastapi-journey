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
