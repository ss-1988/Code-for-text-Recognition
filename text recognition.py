# -*- coding: utf-8 -*-
"""Phd_Thesis-v1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZlDD8X-9pqin96faxTxICWauzCoaZsUv
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import numpy as np
import os
import gc
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img, array_to_img
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.layers import Conv2D, Activation, BatchNormalization, MaxPooling2D, Dropout, Flatten, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras import backend as K

ls

# #path that contains folder you want to copy
# %cd /content/drive/MyDrive/data
# %cp -av /content/drive/MyDrive/data /content/data

IMG_WIDTH=64
IMG_HEIGHT=32
batch_size=4

train_dir = r'/content/drive/MyDrive/data' # For Colab
# train_dir = r'data'

import matplotlib.image as mpimg
from  matplotlib import pyplot as plt

train_datagen = ImageDataGenerator(rescale=1./255,
    # shear_range=0.2,
    # zoom_range=0.2,
    # horizontal_flip=True,
    validation_split=0.2) # set validation split

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
	color_mode="rgb",
    batch_size=batch_size,
    shuffle=True,
    seed=42,
    class_mode='categorical',
    subset='training') # set as training data

validation_generator = train_datagen.flow_from_directory(
    train_dir, # same directory as training data
    target_size=(IMG_HEIGHT, IMG_WIDTH),
	color_mode="rgb",
    shuffle=False,
    seed=42,
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation') # set as validation data

train_data_dict = train_generator.class_indices
val_data_dict = validation_generator.class_indices
train_data_labels = train_generator.labels
val_data_labels = validation_generator.labels

train_generator.class_indices.keys()

train_data_labels

print(len(train_data_labels))

val_data_labels

print(len(val_data_labels))

model = Sequential()
inputShape = (64,32, 3)
chanDim = -1
# if we are using "channels first", update the input shape
# and channels dimension
if K.image_data_format() == "channels_first":
    inputShape = (depth, height, width)
    chanDim = 1
# CONV => RELU => POOL
model.add(Conv2D(32, (3, 3), padding="same",input_shape=inputShape))
model.add(Activation("relu"))
model.add(BatchNormalization(axis=chanDim))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3), padding="same"))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, (3, 3), padding="same"))
model.add(Activation("relu"))
model.add(BatchNormalization(axis=chanDim))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(256, (3, 3), padding="same"))
model.add(Activation("relu"))
model.add(BatchNormalization(axis=chanDim))
model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(0.1))
# (CONV => RELU) * 2 => POOL
model.add(Flatten())
model.add(Dense(120))
model.add(Activation("relu"))
model.add(BatchNormalization())
# softmax classifier
model.add(Dense(22))
model.add(Activation('softmax'))
model.summary()

from tensorflow.keras.optimizers import Adam
EPOCHS = 30
INIT_LR = 1e-3
opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)

METRICS = [
    tf.keras.metrics.TruePositives(name='tp'),
    # tf.keras.metrics.SensitivityAtSpecificity(0.5, name="SensitivityAtSpecificity"),
    tf.keras.metrics.FalsePositives(name='fp'),
    tf.keras.metrics.TrueNegatives(name='tn'),
    tf.keras.metrics.FalseNegatives(name='fn'), 
    tf.keras.metrics.Precision(name='precision'),
    tf.keras.metrics.Recall(name='recall'),
    tf.keras.metrics.AUC(name='auc'),
]

model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy',METRICS])
gc.collect()


early_stop  = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=15)
check_point = tf.keras.callbacks.ModelCheckpoint('best_model.h5', monitor='val_loss', save_best_only=True)



# history = model.fit(train_generator,steps_per_epoch=len(train_generator)//4,validation_data=validation_generator, epochs=100, callbacks=[early_stop, check_point], verbose=1)
# history = model.fit(train_generator,steps_per_epoch=3000,validation_data=validation_generator, epochs=50, callbacks=[early_stop, check_point], verbose=1)
history = model.fit(train_generator,steps_per_epoch=3000,validation_data=validation_generator, epochs=60, callbacks=[check_point], verbose=1)
# history = model.fit(train_generator,steps_per_epoch=1000,validation_data=validation_generator, epochs=7, callbacks=[early_stop, check_point], verbose=1)




model.save_weights('model_wieghts_test.h5')
model.save('model_keras_test.h5')

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
# SensitivityAtSpecificity = history.history['SensitivityAtSpecificity']
# val_SensitivityAtSpecificity = history.history['val_SensitivityAtSpecificity']
val_loss = history.history['val_loss']
precision = history.history['precision']
val_precision = history.history['val_precision']
recall = history.history['recall']
val_recall = history.history['val_recall']
auc = history.history['auc']
val_auc = history.history['val_auc']
tp = history.history['tp']
val_tp = history.history['val_tp']
fp = history.history['fp']
val_fp = history.history['val_fp']
tn = history.history['tn']
val_tn = history.history['val_tn']
fn = history.history['fn']
val_fn = history.history['val_fn']

Sensitivity  = ((np.mean(tp) / (np.mean(tp) + np.mean(fn))))
print(Sensitivity)

print("Accuracy AVG: ",np.average(acc))
print("\n")
print("val_accuracy AVG: ",np.average(val_acc))
print("\n")
print("loss AVG: ",np.average(loss))
print("\n")
print("val_loss AVG: ",np.average(val_loss))
print("\n")
print("Sensitivity ((np.mean(tp) / (np.mean(tp) + np.mean(fn)))) ",Sensitivity)

epochs = range(1, len(acc) + 1)

#Train and validation accuracy
plt.plot(epochs, acc, 'b', label='Training accurarcy')
plt.plot(epochs, val_acc, 'r', label='Validation accurarcy')
titleB = 'Training and Validation accuracy - Accuracy :' + str(acc[-1]) + "," + " Valid. :" + str(val_acc[-1])
# plt.title('Training and Validation accuracy')
plt.title(titleB)
plt.legend()

plt.figure()
#Train and validation loss
plt.plot(epochs, loss, 'b', label='Training loss')
plt.plot(epochs, val_loss, 'r', label='Validation loss')
titleA = 'Training and Validation loss - Train :' + str(loss[-1]) + "," + " Valid. :" + str(val_loss[-1])
# plt.title('Training and Validation loss')
plt.title(titleA)
plt.legend()

plt.figure()
#Train and validation AUC
plt.plot(epochs, history.history['auc'], 'b', label='Training AUC')
plt.plot(epochs, history.history['val_auc'], 'r', label='Validation AUC')
titleA = 'Training and Validation AUC - Train :' + str(auc[-1]) + "," + " Valid. :" + str(val_auc[-1])
# plt.title('Training and Validation AUC')
plt.title(titleA)
plt.legend()

plt.figure()
#Train and validation precision
plt.plot(epochs, history.history['precision'], 'b', label='Training precision')
plt.plot(epochs, history.history['val_precision'], 'r', label='Validation precision')
titleA = 'Training and Validation precision - Train :' + str(precision[-1]) + "," + " Valid. :" + str(val_precision[-1])
# plt.title('Training and Validation precision')
plt.title(titleA)
plt.legend()

plt.figure()
#Train and validation recall
plt.plot(epochs, history.history['recall'], 'b', label='Training recall')
plt.plot(epochs, history.history['val_recall'], 'r', label='Validation recall')
titleA = 'Training and Validation recall - Train :' + str(recall[-1]) + "," + " Valid. :" + str(val_recall[-1])
# plt.title('Training and Validation recall')
plt.title(titleA)
plt.legend()

plt.figure()
#TP / FP / FN/ TN
plt.plot(epochs, history.history['tp'], 'b', label='Training TP')
plt.plot(epochs, history.history['val_tp'], 'r', label='Validation TP')
titleA = 'Training and Validation TP - Train :' + str(tp[-1]) + "," + " Valid. :" + str(val_tp[-1])
# plt.title('Training and Validation TP')
plt.title(titleA)
plt.legend()

plt.figure()
plt.plot(epochs, history.history['fp'], 'b', label='Training FP')
plt.plot(epochs, history.history['val_fp'], 'r', label='Validation FP')
titleA = 'Training and Validation FP - Train :' + str(fp[-1]) + "," + " Valid. :" + str(val_fp[-1])
# plt.title('Training and Validation FP')
plt.title(titleA)
plt.legend()

plt.figure()
plt.plot(epochs, history.history['tn'], 'b', label='Training TN')
plt.plot(epochs, history.history['val_tn'], 'r', label='Validation TN')
titleA = 'Training and Validation TN - Train :' + str(tn[-1]) + "," + " Valid. :" + str(val_tn[-1])
# plt.title('Training and Validation TN')
plt.title(titleA)
plt.legend()

plt.figure()
plt.plot(epochs, history.history['fn'], 'b', label='Training FN')
plt.plot(epochs, history.history['val_fn'], 'r', label='Validation FN')
titleA = 'Training and Validation FN - Train :' + str(fn[-1]) + "," + " Valid. :" + str(val_fn[-1])
# plt.title('Training and Validation FN')
plt.title(titleA)
plt.legend()


plt.show()

"""Saving the model and running the inference on the test data"""

def getList(dict): 
    list = [] 
    for key in dict.keys(): 
        list.append(key) 
          
    return list

train_labels = getList(train_data_dict)

val_labels = getList(val_data_dict)
val_labels

from sklearn.metrics import classification_report, confusion_matrix

import imutils
import cv2 
import os 
import glob

gc.collect()

gc.collect()

# y_predict = model.predict_generator(validation_generator, verbose=1)
y_predict = model.predict_classes(validation_generator, verbose=1)
# y_predict = model.predict(validation_generator, verbose=1)

print(len(y_predict))

y_predict

def plot_confusion_matrix(cm,
                          target_names,
                          title='Confusion matrix',
                          cmap=None,
                          normalize=False):
    """
    given a sklearn confusion matrix (cm), make a nice plot

    Arguments
    ---------
    cm:           confusion matrix from sklearn.metrics.confusion_matrix

    target_names: given classification classes such as [0, 1, 2]
                  the class names, for example: ['high', 'medium', 'low']

    title:        the text to display at the top of the matrix

    cmap:         the gradient of the values displayed from matplotlib.pyplot.cm
                  see http://matplotlib.org/examples/color/colormaps_reference.html
                  plt.get_cmap('jet') or plt.cm.Blues

    normalize:    If False, plot the raw numbers
                  If True, plot the proportions

    Usage
    -----
    plot_confusion_matrix(cm           = cm,                  # confusion matrix created by
                                                              # sklearn.metrics.confusion_matrix
                          normalize    = True,                # show proportions
                          target_names = y_labels_vals,       # list of names of the classes
                          title        = best_estimator_name) # title of graph

    Citiation
    ---------
    http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html

    """
    import matplotlib.pyplot as plt
    import numpy as np
    import itertools

    accuracy = np.trace(cm) / np.sum(cm).astype('float')
    misclass = 1 - accuracy

    if cmap is None:
        cmap = plt.get_cmap('Blues')

    plt.figure(figsize=(50, 50))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()

    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(tick_marks, target_names, rotation=45)
        plt.yticks(tick_marks, target_names)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]


    thresh = cm.max() / 1.5 if normalize else cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if normalize:
            plt.text(j, i, "{:0.4f}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")
        else:
            plt.text(j, i, "{:,}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")


    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label\naccuracy={:0.4f}; misclass={:0.4f}'.format(accuracy, misclass))
    plt.show()

len(val_data_labels)

# compute the confusion matrix
confusion_mtx = confusion_matrix(val_data_labels, y_predict)
# plot the confusion matrix
plot_labels = val_labels
plot_confusion_matrix(confusion_mtx, plot_labels)

b = classification_report(val_data_labels, y_predict, target_names=plot_labels)
print(b)

# test_dir = "/content/drive/MyDrive/data/Amritsar"

# import cv2 
# import os 
# import glob 
# img_dir = test_dir
# data_path = os.path.join(img_dir,'*g') 
# files = glob.glob(data_path) 
# test_imgs = [] 
# for f1 in files: 
#     img = cv2.imread(f1) 
#     test_imgs.append(img) 

# import imutils


# labels_list = train_generator.labels
# def getList(dict): 
#     return list(dict.keys()) 
# class_list = getList(train_generator.class_indices)

# output_path = "results"


# print(len(test_imgs))
# for l in range(len(test_imgs)):
#     image = test_imgs[l]
#     output = imutils.resize(image, width=400)
#     image = cv2.resize(image, (32,64))
#     image = image.astype("float") / 255.0    
#     image = img_to_array(image)
#     image = np.expand_dims(image, axis=0)
#     # No need for this print
#     # print("[INFO] classifying image...")
#     proba = model.predict(image)[0]
#     idxs = np.argsort(proba)[::-1][:2]
#     # loop over the indexes of the high confidence class labels
#     for (i, j) in enumerate(idxs):
#         # build the label and draw the label on the image
#         label = "{}: {:.2f}%".format(class_list[j], proba[j] * 100)
#         cv2.putText(output, label, (10, (i * 30) + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
#     # show the probabilities for each of the individual labels
#     # Un-Comment Code to view
#     # for (label, p) in zip(class_list, proba):
#     #     print("{}: {:.2f}%".format(label, p * 100))
#     cv2.imwrite('{!s}/{!s}.jpg'.format(output_path, l),output)