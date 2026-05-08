from fastapi import FastAPI

app = FastAPI(title="ScholarAgent API")

@app.get("/")
def root():
    return {"message" : "ScholarAgent Backend Running"}