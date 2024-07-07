# Emotion Recognition in Music using Deep Learning
## Project Overview
This project is focused on emotion recognition in music using deep learning techniques. It aims to classify musical signals into specific emotional categories using various artificial intelligence algorithms.

# Introduction
What is Emotion Recognition in Music?
Emotion recognition in music is the task of classifying musical signals into specific emotional categories. This is challenging because the association of emotions with music is highly subjective, varying greatly from person to person.

# Previous Approaches
Researchers have previously focused on smaller, more specific datasets to reduce subjectivity, such as Turkish, Chinese, Japanese, and instrumental music.

# Dataset
The dataset's name is Moodify and consists of 1,200 songs classified into four emotions. The songs were downloaded and truncated to retain the most important 30 seconds. Features are provided by Spotify and extracted using the Python library Librosa.

# Models and Experiments
ResNet
Using PyTorch, we trained a predefined ResNet18 model with combined features into an image. After 25 epochs, I achieved an accuracy of 80%.

# ANN
I modeled a simple neural network with 4 hidden layers using Spotify's features, achieving an accuracy of 75%.

# CNN + LSTM
Inspired by a study, I combined convolutional blocks for attribute extraction and fed them to an LSTM. After 50 epochs, the model reached an accuracy of 80%.

# ResNet18 + BI-LSTM
Combining previous experiments, I used ResNet18 instead of convolutional blocks. Training for 50 epochs, the model achieved an accuracy of 86%.

# Music Journal Concept
The Music Journal concept involves a journal containing phrases describing daily life moments. Users associate these phrases with songs, which are then classified by the algorithm.

# Demo Application Details
I developed a client-server application using React for the frontend and Flask for the backend. The user logs in with their Spotify account and can see user information, statistics, and a music journal. Users can search for songs, which are then processed by the backend for classification. Data is persisted using MongoDB, and the backend follows the singleton service class pattern. Users remain logged in even if the session is interrupted. Two of the trained models are used. The main model is the one that uses ResNet18+BI-LSTM. In case it fails, the ANN is used.

# Model Details

The input is given as three 10-seconds sequences of the song to be classified. The ResNet is extracting the relevant features from the sequences and pass them to a Bi-LSTM layer. In the end, there are used two dense layers and a softmax to get the probability of each class.
![image](https://github.com/denisangel2k2/Licenta/assets/57831211/78bee68d-86e1-45a1-9c9f-673689d6fadd)


# Requirements
- Python 3.x
- Flask
- MongoEngine
- React, MUI, Bootstrap

# Architecture
![image](https://github.com/denisangel2k2/Licenta/assets/57831211/0bd4b9ec-7b8e-4e8f-b952-a4903c2db059)
![image](https://github.com/denisangel2k2/Licenta/assets/57831211/1bde44ae-8f14-45f2-8f66-dda47e2629b4)


# Run Locally
- You need to setup a spotify developer: app https://developer.spotify.com/dashboard
- Add .env attributes in the Backend/JournifyREST folder
```bash
  SPOTIFY_CLIENT_ID = 'your-spotify-client-id'
  SPOTIFY_CLIENT_SECRET = 'your-spotify-client-secret'
  FLASK_SECRET_KEY='the quick brown fox jumps over the lazy doggy'
```
- Run the backend server
- Run the frontend via npm start


# Application Demo
https://github.com/denisangel2k2/Licenta/assets/57831211/0a3f7e6b-a06d-49c0-ab25-ec4b8f1dc644



