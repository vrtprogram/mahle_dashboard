#syntax=docker/dockerfile:1

FROM python:3.10.9

WORKDIR C:/Users/admin/Documents/GitHub/mahle_dashboard

COPY . .

RUN python -m venv venv
RUN . venv/bin/activate

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENV username=admin
ENV password=admin

EXPOSE 7070

CMD ["streamlit", "run", "./App.py"]
