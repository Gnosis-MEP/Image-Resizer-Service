# FROM pytorch/pytorch:2.4.0-cuda12.4-cudnn9-runtime
FROM nvidia/cuda:11.6.2-base-ubuntu20.04

RUN apt-get update \
    && apt-get install -y \
        python3.8 python3.8-distutils python3.8-dev python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /service

ADD ./requirements.txt /service/requirements.txt
ADD ./requirements-torch.txt /service/requirements-torch.txt
ADD ./setup.py /service/setup.py
RUN mkdir -p /service/image_resizer_service/ && \
    touch /service/image_resizer_service/__init__.py

RUN pip install -r requirements-torch.txt && \
    pip install -r requirements.txt && \
    rm -rf /tmp/pip* /root/.cached
# pip install tornado==6.0.0 && \

## add all the rest of the code and install the actual package
## this should keep the cached layer above if no change to the pipfile or setup.py was done.
ADD . /service
RUN pip install -e . && \
    rm -rf /tmp/pip* /root/.cache