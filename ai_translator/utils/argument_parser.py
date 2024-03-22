import argparse
import os


class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Translate English PDF book to Chinese or French.')
        self.parser.add_argument('--config', type=str, default='../config.yaml',
                                 help='Configuration file with model and API settings.')
        self.parser.add_argument('--model_type', type=str, required=True, default='OpenAIModel',
                                 help='The type of translation model to use. Only support "OpenAIModel".')
        self.parser.add_argument('--glm_model_url', type=str, help='The URL of the ChatGLM model URL.')
        self.parser.add_argument('--timeout', type=int, help='Timeout for the API request in seconds.')
        self.parser.add_argument('--openai_model', type=str, default="gpt-3.5-turbo",
                                 help='The model name of OpenAI Model. Required if model_type is "OpenAIModel".')
        self.parser.add_argument('--openai_api_key', type=str,
                                 help='The API key for OpenAIModel. Required if model_type is "OpenAIModel".')
        self.parser.add_argument('--book', type=str, help='PDF file to translate.')
        self.parser.add_argument('--file_format', type=str,
                                 help='The file format of translated book. Now supporting PDF and Markdown')
        self.parser.add_argument('--pages', type=int, help='The page num to be translate')
        self.parser.add_argument('--target_language', type=str, required=True, choices=['Chinese', 'French'],
                                 help='The target language, only support "Chinese" and "French".')

    def parse_arguments(self):
        args = self.parser.parse_args()
        args.openai_api_key = args.openai_api_key if args.openai_api_key else os.getenv("OPENAI_API_KEY")
        if args.model_type == 'OpenAIModel' and not args.openai_model and not args.openai_api_key:
            self.parser.error("--openai_model and --openai_api_key is required when using OpenAIModel")
        return args
