![interfacemetrics.aalto.fi](./aim_frontend/src/assets/workflow.png)

# Aalto Interface Metrics (AIM)

Aalto Interface Metrics (AIM) is a new service that lets you automatically test the usability and aesthetics of your websites using several verified user interface metrics. Simply enter a webpage URL or upload a screenshot, and select desired metrics to get started. AIM segments the page, and displays a preview. As results are computed, they are presented along with detailed explanations, and histograms for comparison. AIM is fully open-sourced, and we invite you to extend the service with your own contributions. Head over to [interfacemetrics.aalto.fi](https://interfacemetrics.aalto.fi/) to give it a try, and for more information.


## Architecture and Technologies

AIM's codebase is divided into four distinct parts:

* [Frontend - web application](./aim_frontend/)
* [Backend - web application](./aim_backend/)
* [Metrics library](./aim_metrics/)
* [Segmentation script](./aim_segmentation/)

The web application's frontend is built with [Vue.js](https://vuejs.org/), whereas the backend is based on [Tornado](http://www.tornadoweb.org/). The frontend and the backend communicate with each other via [WebSocket](https://tools.ietf.org/html/rfc6455).

### Depencencies

The metrics library and the segmentation script are both dependencies for the web application's backend. Other dependencies include [Node.js](https://nodejs.org/) + [npm](https://www.npmjs.com/) (frontend), **[Python 2.7](https://www.python.org/)** + [pip](https://pypi.org/project/pip/) (backend), and [MongoDB](https://www.mongodb.com/) (database). In addition, the backend depends on [Headless Chrome](https://www.google.com/chrome/) and [layout-learning](./aim_backend/bin/layout-learning). The former is used to capture web page screenshots and the latter offers an implementation for the visual search performance metric (needs to be compiled under the target platform, only Linux is available for now).


## Installation

### Database

Start by creating the `aim` database in MongoDB with the following two collections under it: `screenshots` and `results`.

### Backend

Configure backend environment variables for [development](./aim_backend/configs/development.conf), [test](./aim_backend/configs/test.conf), and [production](./aim_backend/configs/production.conf). Next, go to the [aim_backend](./aim_backend/) directory, and create and activate a new Python *virtual environment* (if needed). The final step involves running the following commands:

```bash
# Install required packages
pip install ../aim_metrics
pip install ../aim_segmentation
pip install -r requirements.txt
pip install opencv-python
```

### Frontend

Configure frontend environment variables for [development](./aim_frontend/config/dev.env.js), [test](./aim_frontend/config/test.env.js), and [production](./aim_frontend/config/prod.env.js). Then, go to the [aim_frontend](./aim_frontend/) directory and run the following command:

```bash
# Install required packages
npm install
```


## Usage

### Backend

To run the backend server, go to the [aim_backend](./aim_backend/) directory and execute:

```bash
# Start the server
python uimetrics_backend/main.py
```

### Frontend

Go to the [aim_frontend](./aim_frontend/) directory, and run the following command:

```bash
# Serve with hot reload at localhost:8080
npm run dev
```
To build the frontend for production:

```bash
# Build for production with minification
npm run build
```

After the build is complete, the files (for production) can be found under the newly created `dist` directory. These files are meant to be served over an HTTP server, such as [Apache HTTP Server](https://httpd.apache.org/).

It is highly recommended to use a *load balancer* (e.g., Apache HTTP Server) in a production environment, as certain metrics are extremely CPU intensive. This means that the backend needs to be launched with multiple instances, each listening to a different port. A process manager (e.g., [pm2](http://pm2.keymetrics.io/)) will come in handy at that point. Also, define the `AIM_ENV` environment variable on the production server and set its value to "production" (defaults to "development").


## AIM 2 Metrics

Go to the [aim2_metrics](./aim2_metrics/) directory and read [README.md](./aim2_metrics/README.md) for details.


## Contributing

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for details on contributing to AIM.


## Changelog

Detailed changes for each release are documented in the [release notes](https://github.com/aalto-ui/aim/releases).


## Funding Information and Contact

AIM and related research have been funded by the Technology Industries of Finland Future Makers project SOWP (2017-2019) and the European Research Council starting grant (COMPUTED 2015-2020).

For questions and further information, please contact us via email at <interfacemetrics@aalto.fi>.


## License

Copyright (c) 2018-present, [User Interfaces group](https://userinterfaces.aalto.fi/), [Aalto University](https://www.aalto.fi/), Finland

This software is distributed under the terms of the [MIT License](https://opensource.org/licenses/MIT). See [LICENSE.txt](./LICENSE.txt) for details.
