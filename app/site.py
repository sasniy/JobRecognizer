
import random

from fastapi import FastAPI, UploadFile, Request,File
from model import JobRecognizer
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from samples import samples_text
import pandas as pd
from fastapi.responses import StreamingResponse
from data_proccesing import DataWorker

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory='templates')
filename = 'data.xlsx'
model = None
df = None

@app.on_event("startup")
def startup_event():
    global model
    model = JobRecognizer('spacy')

class TextRequest(BaseModel):
    text: str


@app.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    global df
    contents = await file.read()
    df = DataWorker(contents)
    return {"filename": file.filename}

@app.get('/download')
async def download_file():
    df.get_need_columns(model)
    df._df.to_excel(filename)
    file_path = filename
    file_name = filename

    return StreamingResponse(open(file_path, "rb"), media_type="application/octet-stream",
                             headers={"Content-Disposition": f"attachment; filename={file_name}"})

@app.get('/', response_class=HTMLResponse)
async def test(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})

@app.post('/change_text')
def process_text(request: TextRequest):
    text = request.text
    processed_text = model.predict(text)
    processed_text = DataWorker.preprocessed_text(processed_text)
    return {'newText': processed_text}


@app.get('/sample')
def sample():
    index = random.randint(0,len(samples_text)-1)
    return {'sample':samples_text[index]}
