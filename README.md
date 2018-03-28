# 50.003 Elements of Software Construction

This is our group project for the 50.003 module, Elements of Software Construction held in SUTD. It is a remote Know Your Customer application for identity verification.

This web server interfaces with an Android app for the frontend functionality. For more information on the Android code, please visit the [Android repository](https://github.com/smartlearner1520/Project).

## Functionality

This web server runs on the popular Python web framework, 

## Requirements

### Web Server

To install Django, simply run:

```
pip install Django
```

### Image Processing

Our image processing functionality is based off the wonderful toolkit, [dlib](https://github.com/davisking/dlib).

We use several libraries for face verification and image processing. To install this, several dependencies are required:

```
pip install numpy
pip install scipy
pip install scikit-image
pip install requests
pip install Pillow
pip install cmake
pip install dlib

```

### SMS Authentication

We make use of the [MQTT framework](http://mqtt.org) for SMS authentication.

```
pip install paho-mqtt python-etcd
```

## Tests

We implement several server side tests as well as stress tests for our web server.

* Blah
* TODO
* Blah

## Unimplemented Features


