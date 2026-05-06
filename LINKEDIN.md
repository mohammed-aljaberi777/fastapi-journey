
https://www.linkedin.com/posts/mohammed-aljaberi-5a34323b3_fastapi-websockets-backenddevelopment-share-7457862638086217729-3BUl


Just built my first real-time polling app — and WebSockets finally
clicked for me 💡

Stack: FastAPI + vanilla HTML/JS, all containerised with Docker.
REST endpoints handle create/list/vote/delete, and a WebSocket at
/ws/polls/{poll_id} pushes updates to every connected client the
moment anyone votes. Two tabs side by side update within milliseconds
— no refresh, no setInterval.

The biggest lesson: concurrency. My first version just did
counter += 1. Then I imagined two voters clicking at the exact same
instant — both coroutines read the same count, both add one, both
write back, and one vote silently disappears. I added an asyncio.Lock
per poll inside the in-memory store so increments on the same poll
are serialised, while different polls don't block each other. Two
lines of code, but it was the moment WebSockets stopped feeling like
magic and started feeling like plumbing I have to think about
carefully.

Built as part of my Backend Engineering coursework at Final
International University. Demo + code in the comments 👇

#FastAPI #WebSockets #BackendDevelopment #Python #100DaysOfCode