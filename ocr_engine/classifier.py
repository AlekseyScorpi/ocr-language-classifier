import fasttext
from .utils import convert
from .config import OCRConfig

ocr_config = OCRConfig.load()

text_classifier = fasttext.load_model(ocr_config.fasttext_path)

def predict(result):
    if result['label'] not in (0, 4):
        label = convert[result['label']]
    else:
        text = result['text']
        labels, probs = text_classifier.predict(text, k=5)
        for l in labels:
            l = l.replace('__label__', '')
            if l in convert:
                label = convert[l]
                break
        else:
            label = convert['ru'] if result['label'] == 0 else convert['en']
    return label