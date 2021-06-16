FROM python:3.8.5-slim-buster

WORKDIR /usr/src/app

COPY ./backend ./
COPY ./metrics.json ../

RUN apt-get update \
  && apt-get install -y curl unzip \
  libglib2.0-0 libnss3 libgconf-2-4 libxcb1 libfontconfig1 xvfb \
  # Add aim user
  && useradd --system -s /sbin/nologin aim \
  && mkdir /home/aim \
  # Install Chrome for Selenium
  && curl https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /chrome.deb \
  && (dpkg -i /chrome.deb || apt-get install -yf) \
  && rm /chrome.deb \
  # Upgrade pip
  && python -m pip install --no-cache-dir --upgrade pip \
  # Install requirements
  pip install --no-cache-dir -r requirements.txt \
  # Install chromedriver for Selenium
  && VERSION=$(curl https://chromedriver.storage.googleapis.com/LATEST_RELEASE) \
  && curl "https://chromedriver.storage.googleapis.com/${VERSION}/chromedriver_linux64.zip" -o driver.zip \
  && unzip driver.zip \
  && chmod +x chromedriver \
  && mv chromedriver ./webdrivers/chromedriver_linux \
  && rm driver.zip \
  # remove unwanted packages
  && apt-get remove --purge -y curl unzip \
  # change user permissions
  && chown -R aim . \
  && chown -R aim ../metrics.json \
  && chown -R aim /home/aim

USER aim

CMD [ "python", "./server.py" ]
