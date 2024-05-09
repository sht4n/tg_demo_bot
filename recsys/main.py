import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel

from ml.model import load_model


MODELS = {}

class OutputData(BaseModel):
    source_user_id: str
    form: dict


@asynccontextmanager
async def lifespan(app: FastAPI):
    MODELS["recsys"] = load_model()
    yield
    MODELS.clear()

app = FastAPI(lifespan=lifespan)


@app.get("/predict")
async def predict_recomendation(user_id: str) -> OutputData:
    model = MODELS["recsys"]
    predict = model(user_id)
    response = OutputData(
        source_user_id=user_id,
        form=predict.form,
    )
    return response

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        port=8000,
        reload=True
    )
