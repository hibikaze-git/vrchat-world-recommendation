#!/bin/sh

if [ ! -d "/tmp/check" ]; then
    mkdir /tmp/check
    #npm install @material-ui/core \
    # && npm install @material-ui/icons \
    # && npm install @material-ui/lab \
    # && npm install react-icons \
    # && npm install axios@0.21.1 \
    # && npm install formik --save \
    # && npm install formik-material-ui \
    # && npm install yup @types/yup \
    # && npm install @types/react-modal \
    # && npm install react-modal

    npm install

    exec "$@"
else
    exec "$@"
fi