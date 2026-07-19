"""Small offline translation fallback; replace with DeepL or an LLM in production."""

COMMON_TRANSLATIONS = {
    "Ich gehe mit dem Mann.": "I am going with the man.",
    "Ich gehe mit den Mann.": "I am going with the man.",
    "Ich bin ein Student.": "I am a student.",
    "Das ist ein gutes Buch.": "That is a good book.",
}


def translate_to_english(text: str) -> str:
    return COMMON_TRANSLATIONS.get(text.strip(), "English translation unavailable in offline mode.")
