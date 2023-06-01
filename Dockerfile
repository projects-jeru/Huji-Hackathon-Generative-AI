FROM nvidia/cuda:11.7.1-base-ubuntu22.04
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y libgl1 libglib2.0-0 wget git git-lfs python3-pip python-is-python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .
RUN useradd -m -u 1000 user

USER user

ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=user . $HOME/app		
RUN chmod +x tests.sh && ./tests.sh

CMD ["streamlit", "run","app.py","--server.port" ,"7860"]
