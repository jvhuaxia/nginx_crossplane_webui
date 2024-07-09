FROM python:3.8-slim-buster
WORKDIR /server
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install gunicorn -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY invoke_server.py .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "invoke_server:app"]