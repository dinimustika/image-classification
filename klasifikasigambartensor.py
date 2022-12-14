# -*- coding: utf-8 -*-
"""KlasifikasiGambarTensor

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AdDoMDeXkzwznGw8r93PDOTn32-FdFGd

<h1>Data Diri</h1>
<p> Nama </t></t>: Dini Mustika</p>
<p> ID Group </t>: M07</p>
<p> ID SIB </t></t>: M319Y0855</p>
"""

#import tensorflow
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

#Print tensorflow version
print(tf.__version__)

!wget --no-check-certificate \
 https://github.com/dicodingacademy/assets/releases/download/release/rockpaperscissors.zip \
 -O /tmp/rockpaperscissors.zip

!pip install split-folders

import zipfile,os
import splitfolders

local_zip = '/tmp/rockpaperscissors.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('/tmp')
zip_ref.close()

splitfolders.ratio('/tmp/rockpaperscissors/rps-cv-images', 
                   output="/tmp/rockpaperscissors/data_split", 
                   seed=1337, 
                   ratio=(.6, .4))


data_dir = '/tmp/rockpaperscissors/data_split'
train_dir = os.path.join(data_dir, 'train')
validation_dir = os.path.join(data_dir, 'val')

train_paper_dir = os.path.join(train_dir, 'paper')
train_scissors_dir = os.path.join(train_dir, 'scissors')
train_rock_dir = os.path.join(train_dir, 'rock')

validation_paper_dir = os.path.join(validation_dir, 'paper')
validation_scissors_dir = os.path.join(validation_dir, 'scissors')
validation_rock_dir = os.path.join(validation_dir, 'rock')

train_datagen = ImageDataGenerator(rescale=1./255, 
                                  rotation_range=20,
                                  horizontal_flip=True,
                                  shear_range = 0.2)
validation_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size = (150, 150),
    batch_size = 20,
    class_mode = 'categorical'
)

valid_generator = validation_datagen.flow_from_directory(
    validation_dir,
    target_size = (150, 150),
    batch_size = 20,
    class_mode = 'categorical',
)

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(16, (3,3), activation='relu', input_shape=(150, 150, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Dropout(0.25),
    tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Dropout(0.25),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Dropout(0.25),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Dropout(0.25),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

model.summary()

model.compile(loss = 'categorical_crossentropy',
              optimizer= tf.keras.optimizers.Adam(), 
              metrics= ['accuracy'])

history = model.fit(train_generator, 
          steps_per_epoch=25, 
          epochs=20, 
          validation_data=valid_generator,
          validation_steps=5,
          verbose=2)

import matplotlib.pyplot as plt
plt.plot(history.history['accuracy'], color="red")
plt.plot(history.history['val_accuracy'], color="green")
plt.title('Accuracy')
plt.ylabel('accuracy')
plt.legend(['train', 'test'], loc='lower right')
plt.show()

plt.plot(history.history['loss'], color="red")
plt.plot(history.history['val_loss'], color="black")
plt.title('Loss')
plt.ylabel('loss')
plt.legend(['train', 'test'], loc='lower left')
plt.show()

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
from google.colab import files
from keras.preprocessing import image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# %matplotlib inline

uploaded = files.upload()

for fn in uploaded.keys():

    path = fn
    img = image.load_img(path, target_size=(150,150))
    imgplot = plt.imshow(img)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
 
    images = np.vstack([x])
    classes = model.predict(images, batch_size=32)
  
    print(fn)
    
    if classes[0,0] == 1.0:
      print('Paper')
    elif classes[0,1] == 1.0:
      print('Rock')
    else:
      print('Scissors')