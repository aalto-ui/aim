FROM python:3.7.12-slim-buster

ARG CHROME_VERSION="google-chrome-stable"

WORKDIR /usr/src/app

COPY ./backend ./
COPY ./metrics.json ../

RUN export DEBIAN_FRONTEND=noninteractive \
  # Replace outdated mirror to archive mirror
  && sed -i 's/security.debian.org/archive.debian.org/g' /etc/apt/sources.list \
  && sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list \
  && apt-get update \
  && apt-get install -y --no-install-recommends wget unzip gnupg2 \
  libglib2.0-0 libnss3 libgconf-2-4 libxcb1 libfontconfig1 xvfb libc6-dev gcc \
  # Add aim user
  && useradd --system -s /sbin/nologin aim \
  && mkdir -p /home/aim \
  # Install Chrome for Selenium
  && apt-get update -qqy \
  && apt-get install -qqy /usr/src/app/vendor/deb/*.deb \
  # Upgrade pip
  && python -m pip install --no-cache-dir --upgrade pip \
  # Install requirements
  && pip install --no-cache-dir /usr/src/app/vendor/whl/*.whl \
  && pip --timeout=1000 install --no-cache-dir -r requirements.txt \
  # Install chromedriver for Selenium
  && unzip /usr/src/app/vendor/chromedriver/chromedriver_linux64.zip -d . \
  && chmod +x chromedriver \
  && mkdir -p webdrivers \
  && mv chromedriver ./webdrivers/chromedriver_linux \
  # remove unwanted packages
  # BUG: uninstalling wget removes chrome
  && apt-get remove --purge -y --auto-remove unzip gnupg2 \
  && apt-get clean \
  # change user permissions
  && chown -R aim . \
  && chown -R aim ../metrics.json \
  && chown -R aim /home/aim

USER aim

CMD [ "python", "./server.py" ]
