import fasttext
from .utils import convert

text_classifier = fasttext.load_model("models/lid.176.bin")

def predict(result):
    """
    result — результат вызова движка OCR: {'label': int, 'text': str}
    """
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