# -*- coding: utf-8 -*-
"""Sports Classification.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12gid0MFuuPW5IRP36Dc2dPUPM1tqZLhB
"""

!pip install kaggle

from google.colab import files
files.upload()

!mkdir ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets download -d gpiosenka/sports-classification

!unzip sports-classification.zip

pip install keras==2.15.0

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import tensorflow as tf
import matplotlib.pyplot as plt
import random
import warnings
warnings.simplefilter('ignore')

from matplotlib.pyplot import imshow
from keras.preprocessing import image
from keras import applications
import os
import glob
import cv2

import keras
from keras import layers
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Input,Dense,Activation,ZeroPadding2D,BatchNormalization,Flatten,Conv2D
from keras.layers import AveragePooling2D,GlobalAveragePooling2D,GlobalMaxPool2D,MaxPooling2D,MaxPool2D,Dropout
from keras.models import Model,Sequential

train=glob.glob('/content/train/*')
train

glob.glob('/content/train/sidecar racing/*')

img = cv2.imread('/content/train/sidecar racing/033.jpg')
print(img.shape)
img1 = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
plt.imshow(img1)

train_class=os.listdir('/content/train/')
train_class

count_dict1 = {}
img_dict1 = {}

# Loop through classes
for cls in train_class:  # Assuming class_names contains the list of dog classes
    image_path = glob.glob(f'/content/train/{cls}/*')
    count_dict1[cls] = len(image_path)

    if image_path:  # Check if image_path is not empty
        img_dict1[cls] = tf.keras.utils.load_img(random.choice(image_path))
count_dict1

df1 = pd.DataFrame(data={'label':count_dict1.keys(),'count':count_dict1.values()})
df1

plt.figure(figsize=(20,8))
sns.barplot(x='label',y='count',data=df1)
plt.xticks(rotation=90)
plt.show()

import math

num_items = len(img_dict1)
num_cols = 4
num_rows = math.ceil(num_items / num_cols)

plt.figure(figsize=(20, 5 * num_rows))  # Adjust the figure size based on the number of rows

for id, (label, img) in enumerate(img_dict1.items()):
    plt.subplot(num_rows, num_cols, id + 1)
    plt.imshow(img)
    plt.title(f"{label} {img.size}")
    plt.axis('off')

"""Test Data"""

test_dir=os.listdir('/content/test')
test_dir

img_dict={}
count_dict={}
for cls in test_dir:
    img_path=glob.glob(f'/content/test/{cls}/*')
    count_dict[cls]=len(img_path)
    if img_path:
        img_dict[cls]=tf.keras.utils.load_img(random.choice(img_path))
count_dict

num_items=len(img_dict)
num_cols=4
num_rows=math.ceil(num_items/num_cols)
plt.figure(figsize=(20, 5* num_rows))
for id ,(label,img) in enumerate (img_dict.items()):
    plt.subplot(num_rows,num_cols, id + 1)
    plt.imshow(img)
    plt.title(f'{label} {img.size}')
    plt.axis('off')

"""Data Preprecessing"""

train_data=tf.keras.utils.image_dataset_from_directory('/content/train',label_mode='categorical',shuffle=False)
test_data=tf.keras.utils.image_dataset_from_directory('/content/test',shuffle=False,label_mode='categorical')
validation_data=tf.keras.utils.image_dataset_from_directory('/content/valid',label_mode='categorical',shuffle=False)

width = 224
height = 224
channels = 3

data_preprocessing = tf.keras.Sequential([
    tf.keras.layers.Resizing(height, width),
    tf.keras.layers.Rescaling(1.0 / 255),

])
train_ds=train_data.map(lambda x,y:(data_preprocessing(x),y))
test_ds=test_data.map(lambda x,y:(data_preprocessing(x),y))
valid_ds=validation_data.map(lambda x,y:(data_preprocessing(x),y))
train_ds

"""Custom CNN Model

"""

model = Sequential()
# Convolutional layers with MaxPooling
model.add(Conv2D(input_shape=(224,224,3), filters=32, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=32, kernel_size=(3,3), padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2,2), strides=(2,2)))

# model.add(Conv2D(filters=64, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=64, kernel_size=(3,3), padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2,2), strides=(2,2)))

# model.add(Conv2D(filters=128, kernel_size=(3,3), padding="same", activation="relu"))
# model.add(Conv2D(filters=128, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=128, kernel_size=(3,3), padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2,2), strides=(2,2)))

# flatten the image into a 1D array using the Flatten layer
model.add(Flatten())
# Fully connected layers
# model.add(Dense(units=512, activation="relu"))
model.add(Dense(units=256, activation="relu"))

# Output layer with 100 units and softmax activation for multi-class classification
model.add(Dense(units=100, activation="softmax"))

model.summary()

model.compile(optimizer='adam',loss='categorical_crossentropy'
                 ,metrics=['accuracy','Precision','Recall'])
from keras.callbacks import EarlyStopping
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

"""Data Augmentation"""

datagen = ImageDataGenerator(
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest')

batch_size = 40
# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator()
test_datagen = test_datagen.flow_from_directory('/content/test',
                                      class_mode = "categorical",
                                      target_size = (224, 224),
                                      batch_size = batch_size,
                                      shuffle = False,
                                      seed = 42)

# batches of augmented image data
train_generator = train_datagen.flow_from_directory(
        '/content/train',  # this is the target directory
        target_size=(224, 224),  # all images will be resized
        batch_size=batch_size,
        class_mode='categorical',
shuffle = True,  seed = 42)
# this is a similar generator, for validation data

# Assuming validation_generator is your validation data generator
batch_images, batch_labels = next(train_generator)

# Print the shape of the batch
print("Batch images shape:", batch_images.shape)
print("Batch labels shape:", batch_labels.shape)

val_datagen = ImageDataGenerator()
validation_generator = val_datagen.flow_from_directory(
        '/content/valid',
        target_size=(224, 224),
        batch_size=batch_size,
        class_mode='categorical',
        shuffle = False,seed = 42 )

# Assuming validation_generator is your validation data generator
batch_images, batch_labels = next(validation_generator)

# Print the shape of the batch
print("Batch images shape:", batch_images.shape)
print("Batch labels shape:", batch_labels.shape)

history=model.fit_generator(
        train_generator,
        epochs=20,
        validation_data=validation_generator,
        validation_steps=500 // batch_size,callbacks=early_stopping)

import matplotlib.pyplot as plt
plt.plot(history.history["accuracy"])
plt.plot(history.history['val_accuracy'])
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title("model accuracy")
plt.ylabel("Accuracy")
plt.xlabel("Epoch")
plt.legend(["Accuracy","Validation Accuracy","loss","Validation Loss"])
plt.show()

"""Xception Model"""

# Import libaries
from keras.optimizers import RMSprop
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from keras.applications.xception import Xception
# Create Xception base model
base_model_xception = Xception(weights='imagenet', include_top=False, input_shape=(224,224,3))

# Create a Sequential model
model_xception = Sequential()

# Adding the Xception base model
model_xception.add(base_model_xception)

# Adding Global Average Pooling 2D layer
model_xception.add(GlobalAveragePooling2D())

# Adding a Dense layer with 1024 units and 'relu' activation
model_xception.add(Dense(1024, activation='relu'))

# Adding Dropout layer with a dropout rate of 0.5
model_xception.add(Dropout(0.25))

# Adding another Dense layer with 512 units and 'relu' activation
model_xception.add(Dense(512, activation='relu'))

# Adding Dropout layer with a dropout rate of 0.3
model_xception.add(Dropout(0.3))

# Adding the final Dense layer with 100 units and 'softmax' activation
model_xception.add(Dense(100, activation='softmax'))

# Define RMSprop optimizer with specific parameters
optimizer = RMSprop(learning_rate=0.001, rho=0.9, epsilon=1e-07)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=3, min_lr=1e-7)
model_xception.compile(optimizer='adam',loss='categorical_crossentropy'
                 ,metrics=['accuracy','Precision','Recall'])

model_xception.summary()

from keras.callbacks import EarlyStopping
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
history2=model_xception.fit_generator(
        train_generator,
        epochs=20,
        validation_data=validation_generator,
        callbacks=[early_stopping, reduce_lr])

import matplotlib.pyplot as plt
plt.plot(history2.history["accuracy"])
plt.plot(history2.history['val_accuracy'])
plt.plot(history2.history['loss'])
plt.plot(history2.history['val_loss'])
plt.title("model accuracy")
plt.ylabel("Accuracy")
plt.xlabel("Epoch")
plt.legend(["Accuracy","Validation Accuracy","loss","Validation Loss"])
plt.show()

"""ResNet50 Model"""

from tensorflow.keras.applications import EfficientNetB0
# Load the EfficientNetB0 model pre-trained on ImageNet
base_model = EfficientNetB0(weights="imagenet", include_top=False, input_shape=(229, 229, 3))

# Freeze the base model layers (optional, can be fine-tuned later)
for layer in base_model.layers:
    layer.trainable = False

# Create a new model
model = Sequential()

# Add the pre-trained VGG16 base model
model.add(base_model)
model.add(GlobalAveragePooling2D())
# Add a dense layer with 256 neurons and ReLU activation
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.25))

# Add a dense layer with the number of output classes and softmax activation
model.add(Dense(100, activation='softmax'))

model.compile(optimizer='adam',loss='categorical_crossentropy'
                 ,metrics=['accuracy','Precision','Recall'])
history2=model.fit_generator(
        train_generator,
        epochs=10,
        validation_data=validation_generator,
        callbacks=[early_stopping, reduce_lr])

plt.plot(history2.history["accuracy"])
plt.plot(history2.history['val_accuracy'])
plt.plot(history2.history['loss'])
plt.plot(history2.history['val_loss'])
plt.title("model accuracy")
plt.ylabel("Accuracy")
plt.xlabel("Epoch")
plt.legend(["Accuracy","Validation Accuracy","loss","Validation Loss"])
plt.show()