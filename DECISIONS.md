
1. **Connection Management** — How does your connection manager track connected clients? What happens if a client disconnects mid-vote? Does your app handle this gracefully, or does it crash?

I used a connection manager with a dictionary and the claint is added when they connect and removed when they disconnect
what if the client disconnect or let's say error happend 
i can catch it or handle it and remove it i mean the client 

Does your app handle this gracefully, or does it crash?
yes , it does not crash



2. **State Storage** — You are storing vote counts in memory. Why did you choose this over writing votes to a database? What breaks if you restart the server? What would need to change to make this production-ready?

because a real - time prototype focused on websockets 
if we restarts the server it cost all data is lost 
to change:
real data 
add monitoring and health checks
Use Redis pub/sub



3. **Concurrency** — What would happen if two users voted at exactly the same moment? Did you handle this in your implementation? If not, what is the risk?

one vote is lost without protection race condition 
yes, i used asyncio.look so ,Votes are processed one at a time
this just woks with a single process so , if we have multible workers the race will happen again 



4. **REST vs WebSocket** — You now have two ways to vote: `POST /polls/{id}/vote` and the WebSocket. What is the key difference in behavior between them? When would a client prefer one over the other?

first with rest ,rest is send request and recive response 
on the other hand websocket the server pushes updates in real 

rest one time action 
websocket real time updates