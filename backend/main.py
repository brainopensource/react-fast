from fastapi import FastAPI
import requests


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/external")
def get_external_data():
    response = requests.get("https://google.com")
    if response.headers.get("Content-Type") == "application/json":
        return response.json()
    else:
        return {"error": "Response is not JSON", "content": response.text}
    
@app.get("/external_2")
def get_external_data():
    response = requests.get("https://jsonplaceholder.typicode.com/posts/2")
    return response.json()
