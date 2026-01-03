FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "djangoo.wsgi:application", "--bind", "0.0.0.0:8000"]
