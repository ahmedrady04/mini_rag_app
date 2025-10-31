from fastapi import FastAPI
app=FastAPI()

@app.get("/welcom")
def welcom():
    return{
        "message":"welcom to fastapi"
    }