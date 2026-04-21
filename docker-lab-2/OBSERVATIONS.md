## 📝 OBSERVATIONS.md


1. What is the difference between running a container with `docker run` and deploying a pod with `kubectl run`? Both used the same image — what changed?

`docker run` this one is going to start one container on my computer 
`kubectl run` Management and also inside cluster is going to create a pod 


2. In `kubectl describe pod`, what is the role of the **Scheduler** event? Which control plane component does that correspond to?

He is the one who decides and he is the one who chooses which node to run the pod also where the pod will be inside the cluster 

3. In `kubectl get pods -n kube-system`, name two components you recognised from the lecture and describe what they do.
 
 i saw components like 
 etcd this one stores the data
 kube-scheduler this one assigns pods to nodes 



4. **Image-specific observation** (answer only the one relevant to your image):
   
   - 🐍 Python: Why does `platform.node()` return the pod name? What does this tell you about how Kubernetes assigns identities to pods?


     `platform.node()` because it has isolated env 
     this tell me that the pod has a unique name it has own identity 

    

   
5. Task 6 reflection: After deleting the pod, Kubernetes did **not** restart it. In one paragraph, explain why, and what Kubernetes object would change this behaviour.

  because it was not managed by a controller. Kubernetes only restarts pods automatically when they are part of a Deployment or ReplicaSet. If it was a Deployment, the pod would start again automatically.

  