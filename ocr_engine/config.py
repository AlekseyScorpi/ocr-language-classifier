from mmocr.apis import TextDetInferencer
from tesserocr import PyTessBaseAPI, PSM, OEM
from .engine import OCREngine

def init_tesseract_apis(tessdata_dir: str):
    apis = []
    for script in ['script/Cyrillic', 'script/Georgian', 'script/HanS', 'script/Japanese', 'script/Latin', 'kor']:
        api = PyTessBaseAPI(path=tessdata_dir, lang=script, psm=PSM.SINGLE_LINE, oem=OEM.LSTM_ONLY)
        if script != 'script/Latin':
            api.SetVariable("tessedit_char_blacklist", "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
        else:
            api.SetVariable("tessedit_char_blacklist", "0123456789")
        apis.append(api)
    return apis

def get_ocr_engine(tessdata_dir: str):
    inferencer = TextDetInferencer(model='TextSnake')
    apis = init_tesseract_apis(tessdata_dir)
    return OCREngine(apis=apis, ocr=inferencer)