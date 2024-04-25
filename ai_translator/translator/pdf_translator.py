from typing import Optional
from model import Model
from model.model import translate_prompt
from .pdf_parser import PDFParser
from .writer import Writer
from utils import LOG
from .translation_chain import TranslationChain


class PDFTranslator:
    def __init__(self, model: Model):
        self.model = model
        self.chain = TranslationChain() #TODO
        self.pdf_parser = PDFParser()
        self.writer = Writer()

    def translate_pdf(self, pdf_file_path: str, file_format: str = 'pdf',
                      source_language: str = 'English', target_language: str = 'Chinese',
                      output_file_path: str = None, pages: Optional[int] = None):
        self.book = self.pdf_parser.parse_pdf(pdf_file_path, pages)

        for page_idx, page in enumerate(self.book.pages):
            for content_idx, content in enumerate(page.contents):
                prompt = translate_prompt(content, source_language, target_language)
                LOG.debug(prompt)
                # translation, status = self.model.make_request(prompt)
                translation, status = self.chain.run(text=prompt, source_language=source_language, target_language=target_language)
                LOG.info("\n"+translation)

                # Update the content in self.book.pages directly
                self.book.pages[page_idx].contents[content_idx].set_translation(translation, status)

        self.writer.save_translated_book(self.book, output_file_path, file_format)
        return output_file_path
