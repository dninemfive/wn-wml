from fastapi import FastAPI
import ndf_parse as ndf

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/csv")
async def export_csv(src_path: str, dst_path: str):
    """
    Exports the files in the selected folder (including subfolders) as CSVs organized by namespace and type, for analysis
    
    `src_path`: a `str` pointing to the local folder holding the files to export
    `dst_path`: a `str` pointing to a folder where the CSVs will be placed
    """
    return {"message": "not implemented"}

@app.post("/")
async def generate_mod():
    return {"message": "not implemented"}

