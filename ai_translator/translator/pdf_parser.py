import pdfplumber
from typing import Optional
from book import Book, Page, Content, ContentType, TableContent, ImageContent
from .exceptions import PageOutOfRangeException
from utils import LOG


class PDFParser:
    def __init__(self):
        pass

    def parse_pdf(self, pdf_file_path: str, pages: Optional[int] = None) -> Book:   #pages指定的是最后的页码
        book = Book(pdf_file_path)

        with pdfplumber.open(pdf_file_path) as pdf:
            if pages is not None and pages > len(pdf.pages):
                raise PageOutOfRangeException(len(pdf.pages), pages)

            if pages is None:
                pages_to_parse = pdf.pages
            else:
                pages_to_parse = pdf.pages[:pages]  #从第1页到指定的页码

            for pdf_page in pages_to_parse: #pdf_page从第1页开始
                page = Page()

                # Store the original text content
                raw_text = pdf_page.extract_text()  #抽取原始的文本
                tables = pdf_page.extract_tables()  #抽取原始的表格
                images = pdf_page.images            #抽取原始的图片
                LOG.debug(f"[raw_text]\n{raw_text}")

                # Remove each cell's content from the original text
                for table_data in tables:   #遍历表格
                    for row in table_data:  #遍历行
                        for cell in row:    #遍历单元格
                            raw_text = raw_text.replace(cell, "", 1)

                # Handling text
                if raw_text:
                    # Remove empty lines and leading/trailing whitespaces
                    raw_text_lines = raw_text.splitlines()  #将原始的文本分割成行的列表
                    cleaned_raw_text_lines = [line.strip() for line in raw_text_lines if line.strip()]  #如果不是空白行，则收集此行
                    cleaned_raw_text = "\n".join(cleaned_raw_text_lines)    #将收集到的有效行，用换行符拼接成字符串

                    text_content = Content(content_type=ContentType.TEXT, original=cleaned_raw_text)    #将字符串封装成Content对象
                    page.add_content(text_content)  #将Content对象添加到page对象
                    LOG.debug(f"[raw_text]\n{cleaned_raw_text}")

                # Handling tables
                if tables:
                    table = TableContent(tables)    #tables是3维度list，为什么table是2维
                    page.add_content(table)
                    LOG.debug(f"[table]\n{table}")

                # Handling images
                """
                if images:
                    for image in images:
                        pdf_stream = image['stream']
                        raw_data = pdf_stream['rawdata']
                        LOG.debug(f"[image]\n{pdf_stream}")
                        LOG.debug(f"[image_data]\n{raw_data}")
                    image_content = ImageContent(images)
                    page.add_content(image_content)
                """
                book.add_page(page)

        return book
