from PIL import Image
import threading
import numpy as np


class OCREngine:
    def __init__(self, apis, ocr):
        self.ocr = ocr
        self.apis = apis
    
    def get_crops(self, img: Image):
        if img.mode != 'RGB':
            img = img.convert('RGB')

        result = self.ocr(np.array(img), progress_bar=False)
        predictions = result['predictions']
        crops = []
        for pol, prec in zip(predictions[0]['polygons'], predictions[0]['scores']):
            if prec > 0.5:
                max_x, max_y = max(pol[::2]), max(pol[1::2])
                min_x, min_y = min(pol[::2]), min(pol[1::2])
                area = (min_x, min_y, max_x, max_y)
                crop = img.crop(area)
                crops.append(crop)
        return crops
    
    def get_batch_result(self, crops: list, thread_mask) -> int:
        apis = self.apis
        apis_count = len(apis)
        counts = [0] * apis_count
        scores = [[] for _ in range(apis_count)]
        texts = [[] for _ in range(apis_count)]

        def script_worker(api, index):
            for crop in crops:
                try:
                    api.SetImage(crop)
                    word_confs = api.AllWordConfidences()
                    text = api.GetUTF8Text()
                    while "\n" in text:
                        text = text.replace("\n", "")
                    text = text.strip()
                    if len(text) < 3:
                        scores[index].append(0)
                        texts[index].append("")
                        continue
                    if word_confs:
                        best_conf = np.mean(sorted(word_confs, reverse=True)[:10])
                    else:
                        best_conf = 0
                    scores[index].append(best_conf)
                    texts[index].append(text)
                except:
                    scores[index].append(0)
                    texts[index].append("")

        thr_list = []

        for i, flag in enumerate(thread_mask):
            if flag:
                thr_list.append(threading.Thread(target=script_worker, args=(apis[i], i)))
            else:
                for _ in range(len(crops)):
                    scores[i].append(0)
                    texts[i].append("")

        for thread in thr_list:
            thread.start()
        for thread in thr_list:
            thread.join()

        for c in range(len(crops)):
            crop_scores = []
            for api in range(len(apis)):
                score = scores[api][c]
                crop_scores.append(score)
            counts[np.argmax(crop_scores)] += 1
        for i in range(apis_count):
            texts[i] = " ".join(texts[i])
        return {'counts': counts, 'texts': texts}
    
    def predict(self, img: Image, crop_batch=20):
        return self.__call__(img, crop_batch)

    def __call__(self, img: Image, crop_batch=20):
        crops = self.get_crops(img=img)
        counts = np.array([0] * len(self.apis))
        texts = [[] for _ in range(len(self.apis))]
        thread_mask = [1] * len(self.apis)
        i = 0

        while i + crop_batch < len(crops):
            batch_result = self.get_batch_result(crops[i:i+crop_batch], thread_mask)
            counts += np.array(batch_result['counts'])

            for j, text in enumerate(batch_result['texts']):
                texts[j].append(text)

            s_counts = sorted(counts)
            if s_counts[-1] > s_counts[-2] * 1.5:
                res_id = np.argmax(counts)
                return {'label': res_id, 'text': " ".join(texts[res_id])}
            
            for j in range(len(counts)):
                if counts[i] * 2.5 < s_counts[-1]:
                    thread_mask[i] = 0
            i += crop_batch

        if i < len(crops):
            batch_result = self.get_batch_result(crops[i:], thread_mask)
            counts += np.array(batch_result['counts'])
            for j, text in enumerate(batch_result['texts']):
                texts[j].append(text)
        
        res_id = np.argmax(counts)
        return {'label': res_id, 'text': " ".join(texts[res_id])}