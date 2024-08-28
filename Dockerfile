FROM pytorch/pytorch:2.4.0-cuda12.4-cudnn9-runtime

## install only stuff for ultralistic hard coupled requirements
WORKDIR /service

ADD ./requirements.txt /service/requirements.txt
ADD ./setup.py /service/setup.py
RUN mkdir -p /service/image_resizer_service/ && \
    touch /service/image_resizer_service/__init__.py

RUN pip install -r requirements.txt && \
    rm -rf /tmp/pip* /root/.cached

## add all the rest of the code and install the actual package
## this should keep the cached layer above if no change to the pipfile or setup.py was done.
ADD . /service
RUN pip install -e . && \
    rm -rf /tmp/pip* /root/.cache