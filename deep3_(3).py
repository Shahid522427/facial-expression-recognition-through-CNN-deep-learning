# -*- coding: utf-8 -*-
"""deep3 (3).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ooepaYVe1B_sadRxTETQUzh10lHm9B-8
"""

import numpy as np
import pandas as pd
import seaborn as sns
import os
import cv2
import matplotlib.pyplot as plt
import tensorflow as tf

# Importing Deep Learning Libraries
#from keras.preprocessing.image import load_img, img_to_array
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Dense,Input,Dropout,GlobalAveragePooling2D,Flatten,Conv2D,BatchNormalization,Activation,MaxPooling2D
from keras.models import Model,Sequential
from keras.optimizers import Adam,SGD,RMSprop
from tensorflow.keras import layers, models

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator


training_images = np.load(r"/content/drive/MyDrive/face_exp_dataset/train_images.npy")
training_labels = np.load(r"/content/drive/MyDrive/face_exp_dataset/train_labels.npy")
testing_images = np.load (r"/content/drive/MyDrive/face_exp_dataset/test_images.npy")
testing_labels = np.load(r"/content/drive/MyDrive/face_exp_dataset/test_labels.npy")

# Normalize the images to values between 0 and 1
training_images = training_images / 255.0
testing_images = testing_images / 255.0


#Define the CNN model structure
no_of_classes = 7
model = Sequential()

#1st CNN layer
model.add(Conv2D(64,(3,3),padding = 'same',  input_shape = (48,48,1)))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size = (2,2)))
model.add(Dropout(0.25))

#2nd CNN layer
model.add(Conv2D(128,(5,5),padding = 'same'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size = (2,2)))
model.add(Dropout (0.25))

#3rd CNN layer
model.add(Conv2D(512,(3,3),padding = 'same'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size = (2,2)))
model.add(Dropout (0.25))

#4th CNN layer
model.add(Conv2D(512,(3,3), padding='same'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())

#Fully connected 1st layer
model.add(Dense(256))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dropout(0.25))


# Fully connected layer 2nd layer
model.add(Dense(512))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dropout(0.25))

model.add(Dense(no_of_classes, activation='softmax'))



opt = Adam(lr = 0.0001)
model.compile(optimizer=opt,loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.summary()



cv2.ocl.setUseOpenCL(False)


# Compile the model

#model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.0001, decay=1e-6), metrics=['accuracy'])
model.compile(optimizer='adam',loss='sparse_categorical_crossentropy', metrics=['accuracy'])


#Reshape the training and testing data to include a single channel (grayscale)
training_images = training_images.reshape(training_images.shape[0], 48, 48, 1)
testing_images = testing_images.reshape(testing_images.shape[0], 48, 48, 1)

# Ensure that the label values are within the valid range [0, 6]
#training_labels = np.clip(training_labels, 0, 6)
#test_labels = np.clip(testing_labels, 0, 6)

# Train the model
m=model.fit(training_images, training_labels, epochs=30, batch_size=32, validation_split=0.2)

# Evaluate the model on the test set
test_loss, test_accuracy = model.evaluate(testing_images,testing_labels)
print("Test accuracy:", test_accuracy)

from google.colab import drive
drive.mount('/content/drive')

!pip install keras-tuner