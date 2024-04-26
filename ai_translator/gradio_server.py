import sys
import os
import time
import gradio as gr
from translator import PDFTranslator

root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_dir)


def translate(upload_file, source_language, target_language,
              file_format, model_name):
    new_file_path = upload_file.name.lower().strip('.pdf') + '_' + time.strftime("%Y%m%d-%H%M%S") + '_translated' + ('.pdf' if file_format == 'pdf' else '.md')

    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(model_name)
    output_file_path = translator.translate_pdf(pdf_file_path=upload_file.name, file_format=file_format,
                                                source_language=source_language if source_language else 'English',
                                                target_language=target_language if target_language else 'Chinese',
                                                output_file_path=new_file_path)
    return output_file_path


def launch_gradio():

    iface = gr.Interface(
        fn=translate,
        title="OpenAI-Translator v2.0(PDF 电子书翻译工具)",
        inputs=[
            gr.File(label="上传PDF文件"),
            gr.Textbox(label="源语言（默认：英文）", placeholder="英文", value="英文"),
            gr.Textbox(label="目标语言（默认：中文）", placeholder="中文", value="中文"),
            gr.Radio(label="目标文件格式", choices=["pdf", "markdown"], value="pdf"),
            gr.Radio(label="模型", choices=["gpt-3.5-turbo", "glm-4"], value="gpt-3.5-turbo")
        ],
        outputs=[
            gr.File(label="下载翻译文件")
        ],
        allow_flagging="never"
    )

    iface.launch(share=True, server_name="0.0.0.0")


if __name__ == "__main__":
    launch_gradio()
    print("Server started")
