from surrealdb import Surreal
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import logging
from fastapi.responses import RedirectResponse


async def surreal_db_operations():
	async with Surreal("ws://localhost:8000/rpc") as db:
		await db.signin({"user": "root", "pass": "root"})
		await db.use("test", "test")
		logging.info("Connected to SurrealDB with namespace 'test' and database 'test'")
		print("Connected to SurrealDB with namespace 'test' and database 'test'")


		create_response = await db.create(
           "person",
           {
               "user": "me",
               "pass": "safe",
               "marketing": True,
               "tags": ["python", "documentation"],
           }
        )

		logging.info(f"Create response: {create_response}")
		print(f"Create response: {create_response}")



app = FastAPI()

@app.get("/surrealdb_operation", response_class=HTMLResponse)
async def surrealdb_handler():
	result = await surreal_db_operations()
	return result

@app.get("/surrealist")
async def surrealdb_handler():
    # Instead of returning the result, redirect to the desired URL
    print("test")
    return RedirectResponse(url="http://0.0.0.0:8000")

@app.get("/", response_class=HTMLResponse)
async def landing_page():
   html_content = """
   <html>
       <head>
           <title>Welcome</title>
       </head>
       <body>
           <h1>Welcome to the FastAPI App</h1>
           <p>To perform operations with SurrealDB, visit the following link:</p>
           <a href="/surrealdb_operation">Execute the surrealdb operation</a>
           <p>To check the result of the operation, visit the following link:</p>
           <a href="/surrealist">Visit Surrealist</a>
       </body>
   </html>
   """
   return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
