FROM node:alpine

WORKDIR /firestore

RUN apk update && \
    apk add inotify-tools && \
    npm install -g npm && \
    npm install -g firebase-tools \
    && rm -rf /var/lib/apt/lists/*
