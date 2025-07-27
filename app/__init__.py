from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.tools.pdf_parser.pdf_reader import output_parsed_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    output_parsed_data()
    return {"message": "PDF parsing completed successfully."}