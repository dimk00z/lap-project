# Set the base image using Python 3.12 and Debian Bookworm
FROM python:3.12-slim-bookworm

ARG LITESTAR_ENV \
  # Needed for fixing permissions of files created by Docker:
  UID=1000 \
  GID=1000


ENV LITESTAR_ENV=${LITESTAR_ENV} \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_DEFAULT_TIMEOUT=100

RUN apt-get update && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
    build-essential \ 
    curl

    # Set the working directory to /app
WORKDIR /code

COPY --chown=web:web ./requirements.txt /code/

RUN groupadd -g "${GID}" -r web \
&& useradd -d '/code' -g web -l -r -u "${UID}" web \
&& chown web:web -R '/code'

RUN pip install uv 
RUN python -m uv pip install --no-cache -r /code/requirements.txt

USER web

# Copy only the necessary files to the working directory
COPY --chown=web:web . /code

# CMD ["uvicorn", "--factory", "main:create_app"]