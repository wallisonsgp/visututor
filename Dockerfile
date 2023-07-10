FROM python:3.9-slim
# System update
RUN apt-get update -y && apt-get install -y libgomp1
RUN python -m pip install --upgrade pip
# Work directory and files application
WORKDIR /webapp
# Coping requirements
COPY /requirements.txt /webapp/
# Install python dependencies
RUN pip install --upgrade pip
RUN pip install -r /webapp/requirements.txt
# Delete unused files
COPY app /webapp/
RUN rm /webapp/requirements.txt

EXPOSE 5000

CMD ["python", "/webapp/main.py"]