# define base image (miniconda3)
FROM continuumio/miniconda3

# set working directory for the project
WORKDIR /ocr-documents-system

# create conda environment
COPY environment.yml .
RUN conda env create -f environment.yml

# overwrite default shell and use bash
SHELL ["conda", "run", "-n", "env", "/bin/bash", "-c"]

# checking good libraries installation
RUN echo "Check installation"
RUN python -c "from mmocr.apis import TextDetInferencer; TextDetInferencer(model='TextSnake');"
RUN python -c "from tesserocr import PyTessBaseAPI; PyTessBaseAPI()"

COPY 