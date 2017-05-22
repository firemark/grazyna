FROM python:slim
LABEL Name=grazyna Version=dev 
WORKDIR /workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python setup.py install

CMD ["python","-m","grazyna","default_config.ini"]