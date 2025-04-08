# define base image (miniconda3)
FROM continuumio/miniconda3

# set working directory for the project
WORKDIR /ocr-documents-system

# create conda environment
RUN conda create -n docs_language_classifier python=3.10 -y && \
    conda clean -afy

# needed system packages
RUN apt-get update && apt-get install -y \
tesseract-ocr \
libtesseract-dev \
build-essential \
gcc \
g++ \
make \
cmake \
libglib2.0-0 \
libsm6 \
libxext6 \
libxrender-dev \
libgl1 \
ffmpeg \
git \
curl \
&& rm -rf /var/lib/apt/lists/*

# mannualy packages installation
# tesserocr installation
RUN conda install -n docs_language_classifier \
-c conda-forge tesserocr -y && \
conda clean -afy

# mmocr installation
RUN conda install -n docs_language_classifier \
    -c pytorch -c conda-forge \
    pytorch==1.13.1 torchvision cpuonly -y && \
    conda clean -afy

RUN conda run -n docs_language_classifier \
pip install --no-cache-dir -U openmim

RUN conda run -n docs_language_classifier \
mim install "mmengine==0.10.7"

RUN conda run -n docs_language_classifier \
mim install "mmcv==2.0.0rc4"

RUN conda run -n docs_language_classifier \
mim install "mmdet==3.1.0"

RUN conda run -n docs_language_classifier \
mim install "mmocr==1.0.1"

RUN conda run -n docs_language_classifier \
pip install "numpy<2"

RUN conda run -n docs_language_classifier \
pip install aiogram

# fasttext installation
RUN conda run -n docs_language_classifier \
pip install fasttext-wheel

# check good libraries installation
RUN conda run -n docs_language_classifier python -c "from mmocr.apis import TextDetInferencer; TextDetInferencer(model='TextSnake');"
RUN conda run -n docs_language_classifier python -c "from tesserocr import PyTessBaseAPI; PyTessBaseAPI()"

# download tessdata
RUN mkdir -p /ocr-documents-system/data \
    && git clone https://github.com/AlekseyScorpi/tessdata.git /ocr-documents-system/data/tessdata

# download fasttext model
RUN mkdir -p /ocr-documents-system/data/models \
    && curl -Lo /ocr-documents-system/data/models/lid.176.bin https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin

COPY bot ./bot
COPY ocr_engine ./ocr_engine

CMD ["conda", "run", "-n", "docs_language_classifier", "python", "-m", "bot.main"]