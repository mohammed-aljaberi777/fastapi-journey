### `[Reflect]` Task 6 — OBSERVATIONS.md



1. What is the difference between a Pod and a Deployment? Why would you use a Deployment instead of a bare Pod?

pod / is samll thing in the Worker Node it runs a container
deployment / manages and control the pods

why
because the deployment restarts it if any thing happen






2. Why is a ConfigMap used for the MongoDB URL instead of hardcoding it in the Deployment YAML?

beacuse we have to edit the file when the url changes 





3. What happened to the original Pod when you scaled the WebApp to 3 replicas? Did it get replaced, or were new Pods added alongside it? 

nothing 

no, it added two new pods and they run at the same time 



4. What would happen to the application if the MongoDB Pod crashed? How would Kubernetes respond?

deployment will try to restrt it if managed by it 


how would kubernets respond?

The application will be affected because mongo pod crashed but it will work again if mongo is back 


5. What is one thing that surprised you or that you found confusing? How did you resolve it?

when i wtote  mongo.yaml i saw that container craeting  i though there was a problem then i ran it again it show me running so i learn it is not error  

---