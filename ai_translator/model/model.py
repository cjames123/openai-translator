from book import ContentType


def make_text_prompt(text: str, source_language: str, target_language: str) -> str:
    if target_language == "Chinese":
        target_language = "中文"
    elif target_language == "French":
        target_language = "法语"
    return f"从{source_language}翻译为{target_language}，每个句子，每个词都要翻译，尽量使语义简单易懂：{text}"


def make_table_prompt(table: str, source_language: str, target_language: str) -> str:
    if target_language == "Chinese":
        target_language = "中文"
    elif target_language == "French":
        target_language = "法语"
    return f"从{source_language}翻译为{target_language}，保持间距（空格，分隔符），以表格形式返回，单元格的文本都要翻译，数值除外：\n{table}"


def translate_prompt(content, source_language:str, target_language: str) -> str:
    if content.content_type == ContentType.TEXT:
        return make_text_prompt(content.original, source_language, target_language)
    elif content.content_type == ContentType.TABLE:
        return make_table_prompt(content.get_original_as_str(), source_language, target_language)


class Model:

    def make_request(self, prompt):
        raise NotImplementedError("子类必须实现 make_request 方法")
