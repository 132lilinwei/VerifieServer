# 50.003 Elements of Software Construction

This is our group project for the 50.003 module, Elements of Software Construction held in SUTD. It is a remote Know Your Customer application for identity verification.

This web server interfaces with an Android app for the frontend functionality. For more information on the Android code, please visit the [Android repository](https://github.com/smartlearner1520/Project).

## Functionality

This web server runs on the popular Python web framework, [Django](http://djangoproject.com). Our app mainly consists of 5 sections. These are sequential and the user will be unable to proceed to the next step if he does not complete any of the previous steps.

### Email verification

In this stage, an email is sent to the registered email address with a 4-digit code. The user is required to enter this code into the Android app to prove his ownership of the email address.

### SMS Verification

In this stage, we send an SMS containing a 4-digit code to the user's registered phone. The user is required to enter this code to proceed. For more information, please refer to our [SMS authentication repository](https://github.com/kuiqejw/MQTT-NEW).

### Image Verification

For this stage, we request a current photo of the user. This is uploaded from the Android app to our server, which processes it and verifies it against the user's previous photos. If it matches, the user may proceed to the final verification step. For more information, please refer to our dedicated [face verification repository](https://github.com/kohjingyu/face_verification).

### DigiCard Verification

For this step, we require the user to enter a unique code given two digits. This code is retrieved from the user's company issued card.

TODO: Insert image of card

### Verification Complete

After all previous steps are completed, the user has completed the verification process, and we believe to a high degree of certainty that the user is the true owner of the account.

## Requirements

Our code is tested only on **Python 3.6**. For other versions of Python, we make no guarantees that things will work as expected.

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

## Deployment

Verifie is currently deployed on a free Heroku dynos. We have observed that it requires approximately 200MB of disk space. During the verification process, it uses up to 300 MB of physical memory.

## Tests

We implement several server side tests as well as stress tests for our web server. For more info, please view `realapp/tests.py`.

* Unit tests: login, registration, username, user creation date
* System tests: DDoS login attack, incorrect permissions problems

## Unimplemented Features

Currently, all features that we have planned are implemented. However, we have a few features that we would like to work on should we be given the opportunity to make this into a production level app:

1. **Company branding:** it would be interesting for us to allow a company administrator to brand the app with their company colors and logo. This would let us "license" the app to a multitude of companies.
2. **Nonstatic image verification**: static images may be easy to fake. If we were to use video verification, it would allow us a way of ensuring that the user is currently using the verification app.

