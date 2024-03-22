import sys
import os
import time

from fastapi import FastAPI, Form, UploadFile, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn

from model import OpenAIModel
from utils import ConfigLoader
from translator import PDFTranslator

root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_dir)

app = FastAPI()
# 设置静态文件路径
app.mount("/download", StaticFiles(directory="download"), name="download")


@app.get("/")
def index():
    with open("templates/index.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=status.HTTP_200_OK)


@app.post("/translate")
def translate(pages: int = Form('pages'), ai_model_type: str = Form('ai_model_type'),
              ai_model_version: str = Form('ai_model_version'), book: UploadFile = Form('book'),
              file_format: str = Form('file_format'), target_language: str = Form('target_language')):

    config_path = '../config.yaml'
    model_api_key = os.getenv("OPENAI_API_KEY")

    config_loader = ConfigLoader(config_path if config_path else "../config.yaml")
    config = config_loader.load_config()

    model_api_key = model_api_key if model_api_key else config[ai_model_type]['api_key']
    model = OpenAIModel(model=ai_model_version, api_key=model_api_key)

    book.filename = book.filename.lower()
    new_file_path = book.filename.strip('.pdf') + '_' + time.strftime("%Y%m%d-%H%M%S") + '.pdf'
    save_file_path = 'download/' + new_file_path
    with open(save_file_path, 'bw') as f:
        f.write(book.file.read())

    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(model)
    translator.translate_pdf(pdf_file_path=save_file_path, file_format=file_format, pages=pages if pages > 0 else None,
                             target_language=target_language if target_language else 'Chinese')

    new_file_path = new_file_path.strip('.pdf') + '_translated' + ('.pdf' if file_format == 'pdf' else '.md')
    return JSONResponse({"status": "success",
                         "message": '翻译完成！<a target="_blank" href="http://localhost:8000/download/'
                                    + new_file_path + '">请查阅</a>'},
                        status_code=status.HTTP_200_OK)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
    print("Server started")
