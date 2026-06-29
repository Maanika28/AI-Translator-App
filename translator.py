from deep_translator import GoogleTranslator

def translate_text(text, source_lang, target_lang):
    print("SOURCE =", source_lang)
    print("TARGET =", target_lang)

    translator = GoogleTranslator(
        source=source_lang,
        target=target_lang
    )

    result = translator.translate(text)

    print("RESULT =", result)

    return result