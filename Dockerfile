FROM python:3.8
COPY . /app
WORKDIR /app
RUN pip install --use-deprecated=legacy-resolver -r requirements.txt
CMD python -u ./app.py
