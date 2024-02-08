from langdetect import detect
from deep_translator import GoogleTranslator
import warnings
from jan_scraper import Unrecognizable_Language_Warning

LANGNAMES = {
    "Afrikaans": "af",
    "Arabic": "ar",
    "Bulgarian": "bg",
    "Bengali": "bn",
    "Catalan": "ca",
    "Czech": "cs",
    "Welsh": "cy",
    "Danish": "da",
    "German": "de",
    "Greek": "el",
    "English": "en",
    "Spanish": "es",
    "Estonian": "et",
    "Persian": "fa",
    "Finnish": "fi",
    "French": "fr",
    "Gujarati": "gu",
    "Hebrew": "he",
    "Hindi": "hi",
    "Croatian": "hr",
    "Hungarian": "hu",
    "Indonesian": "id",
    "Italian": "it",
    "Japanese": "ja",
    "Kannada": "kn",
    "Korean": "ko",
    "Lithuanian": "lt",
    "Latvian": "lv",
    "Macedonian": "mk",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Nepali": "ne",
    "Dutch": "nl",
    "Norwegian": "no",
    "Punjabi": "pa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Romanian": "ro",
    "Russian": "ru",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Somali": "so",
    "Albanian": "sq",
    "Swedish": "sv",
    "Swahili": "sw",
    "Tamil": "ta",
    "Telugu": "te",
    "Thai": "th",
    "Tagalog": "tl",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Vietnamese": "vi",
    "Chinese (Simplified)": "zh-cn",
    "Chinese (Traditional)": "zh-tw",
    "Amharic": "am",
    "Azerbaijani": "az",
    "Bosnian": "bs",
    "Chichewa": "ny",
    "Corsican": "co",
    "Esperanto": "eo",
    "Fijian": "fj",
    "Haitian Creole": "ht",
    "Hausa": "ha",
    "Hmong": "hmn",
    "Igbo": "ig",
    "Javanese": "jw",
    "Kazakh": "kk",
    "Khmer": "km",
    "Kurdish (Kurmanji)": "ku",
    "Kyrgyz": "ky",
    "Lao": "lo",
    "Luxembourgish": "lb",
    "Malagasy": "mg",
    "Maltese": "mt",
    "Maori": "mi",
    "Mongolian": "mn",
    "Pashto": "ps",
    "Samoan": "sm",
    "Scots Gaelic": "gd",
    "Shona": "sn",
    "Sindhi": "sd",
    "Sundanese": "su",
    "Tajik": "tg",
    "Uzbek": "uz",
    "Xhosa": "xh",
    "Yiddish": "yi",
    "Yoruba": "yo",
    "Zulu": "zu",
}


def supported_languages():
    """
    Prints a list of supported languages.
    """
    print(list(LANGNAMES.keys()))


class TranslateFunctions:
    """
    A class for translating text between languages using Google Translate.

    Attributes:
        text (str): The text to be translated.
        destination (str): The target language for translation.
        original (str): The detected or specified source language for translation.

    Methods:
        translatef(): Translates the text to the target language.

    Raises:
        Unrecognizable_Language_Warning: Warns if the provided language is not supported for auto-detection.
    """

    def __init__(self, text, destination):
        """
        Initializes the TranslateFunctions object.

        Args:
            text (str): The text to be translated.
            destination (str): The target language for translation.
        """
        self.text = text
        self.destination = destination
        try:
            self.original = detect(self.text)
        except Exception as e:
            self.original = "auto"
            warnings.warn(
                "Language provided is not among the ones supported by auto-detection... Switching to auto; errors may occur downstream",
                Unrecognizable_Language_Warning,
            )

    def translatef(self):
        """
        Translates the text to the target language.

        Returns:
            str: The translated text.
        """
        translator = GoogleTranslator(source=self.original, target=self.destination)
        translation = translator.translate(self.text)
        return translation
