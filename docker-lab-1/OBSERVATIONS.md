## 📝 OBSERVATIONS.md

You must include an **`OBSERVATIONS.md`** file inside your `docker-lab-1/` folder. This file must answer the following questions **in your own words**:

1. What is the size of your image? Is it large or small — and why do you think that is?

the size is 179MB 
and it is small because the slim version and it removes unnecessary tools and it makes the image faster and very light 

2. How many layers does your image have? What does each major layer add?

9 layers 
installing python and setting env variables and adding required dependencies and configuring system and adding system tools setting the default command to ran python

3. What operating system and architecture does your image use? (from `docker inspect`)

linux and amd64 architecture

4. **Image-specific question:**
  
   - 🐍 Python: What error did you get when trying `import requests`? What does this tell you about how Docker containers work?
   
   I got a ModuleNotFoundError and it tells me that the containers are isolated and do not include extra python packages 

5. In one paragraph: what surprised you most about this lab?
doker containers are isolated so, each container runs independently also it does not include additional tools also how fast to run 