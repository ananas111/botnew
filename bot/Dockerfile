FROM python:3.8

WORKDIR /bot
ENV DONTWRITEBYTECODE 1
ENV PYTHONONBUFFERED 1

COPY requirements.txt /bot/requirements.txt

COPY . /bot

RUN pip install -r ./requirements.txt

CMD ["python", "bot.py"]