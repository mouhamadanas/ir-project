from googletrans import Translator
from langdetect import detect

class TranslationService:
    def __init__(self):
        self.translator = Translator()

    def translate_text(self, text, src_lang='auto', dest_lang='en'):
        translated = self.translator.translate(text, src=src_lang, dest=dest_lang)
        return translated.text

    def detect_and_translate(self, query_text):
        detected_language = detect(query_text)
        if detected_language != 'en':
            query_text = self.translate_text(query_text, src_lang=detected_language, dest_lang='en')
        return query_text
