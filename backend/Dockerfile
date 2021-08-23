FROM python:3.8.5-slim-buster

ARG CHROME_VERSION="google-chrome-stable"

WORKDIR /usr/src/app

COPY ./backend ./
COPY ./metrics.json ../

RUN export DEBIAN_FRONTEND=noninteractive \
  && apt-get update \
  && apt-get install -y --no-install-recommends wget unzip gnupg2 \
  libglib2.0-0 libnss3 libgconf-2-4 libxcb1 libfontconfig1 xvfb \
  # Add aim user
  && useradd --system -s /sbin/nologin aim \
  && mkdir -p /home/aim \
  # Install Chrome for Selenium
  && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update -qqy \
  && apt-get -qqy install ${CHROME_VERSION:-google-chrome-stable} \
  && rm /etc/apt/sources.list.d/google-chrome.list \
  # Upgrade pip
  && python -m pip install --no-cache-dir --upgrade pip \
  # Install requirements
  && pip install --no-cache-dir -r requirements.txt \
  # Install chromedriver for Selenium
  && VERSION=$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE) \
  && wget -q "https://chromedriver.storage.googleapis.com/${VERSION}/chromedriver_linux64.zip" -O driver.zip \
  && unzip driver.zip \
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
  && chown -R aim /home/aim \
  # delete unnecessary sources
  && rm -rf driver.zip /etc/apt/sources.list.d/google-chrome.list /var/lib/apt/lists/* /var/cache/apt/*

USER aim

CMD [ "python", "./server.py" ]
