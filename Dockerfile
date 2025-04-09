FROM python:3.10.9

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim

RUN useradd -rms /bin/bash appuser && chmod 777 /opt /run 

WORKDIR /app

RUN mkdir /app/static && mkdir /app/media && chown -R appuser:appuser /app && chmod 755 /app

COPY --chown=appuser:appuser . .

RUN pip install -r requirements.txt

USER appuser

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


