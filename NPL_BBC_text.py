# -*- coding: utf-8 -*-
"""submition_1_Jeremy_Wijaya.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1W21SJ0WKIhCpZaoG0Xsmya2gPOIISZIy

# **Dataset : BBC text**

Kriteria :

Dataset minimal memiliki 1000 sampel, Harus menggunakan LSTM dalam arsitektur model sequential, Validation set sebesar 20% dari total dataset, Harus menggunakan Embedding, Harus menggunakan fungsi tokenizer dan Akurasi dari model minimal 75%.

data diri : Jeremy Wijaya
"""

# import libraries dan dataset bbc text
import pandas as pd
import tensorflow as tf
df = pd.read_csv('bbc-text.csv')

# cek dataset
df.info()

# gunakan one hot encoding untuk mengubah data kategrikal menjadi numerik
category = pd.get_dummies(df.category)
df_baru = pd.concat([df, category], axis=1)
df_baru = df_baru.drop(columns='category')
df_baru

# pisahkan label dengan fitur
news = df_baru['text'].values
label = df_baru[['business', 'entertainment', 'politics', 'sport', 'tech']].values

# lakukan pemecahan training dan validation data set
from sklearn.model_selection import train_test_split
news_latih, news_test, label_latih, label_test = train_test_split(news, label, test_size=0.2)

# lakukan fungsi tokenizer untuk mendapatkan sequence
# lalu gunakan padding agar sequence memiliki array yang sama
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
 
tokenizer = Tokenizer(num_words=5000, oov_token='x')
tokenizer.fit_on_texts(news_latih) 
tokenizer.fit_on_texts(news_test)
 
sekuens_latih = tokenizer.texts_to_sequences(news_latih)
sekuens_test = tokenizer.texts_to_sequences(news_test)
 
padded_latih = pad_sequences(sekuens_latih) 
padded_test = pad_sequences(sekuens_test)

padded_test[0]

# buatlah sebuah class anak dari callback
# buatlah dimana bila accuracy & val_accuracy > 90% 
# akan dilakukan callback
class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('accuracy')>0.9 and logs.get('val_accuracy')>0.9):
      print("\nAkurasi telah mencapai >90%!")
      self.model.stop_training = True
callbacks = myCallback()

# buatlah bentuk model sequential dengan 
import tensorflow as tf
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=5000, output_dim=16),
    tf.keras.layers.LSTM(64),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(5, activation='softmax')
])
model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

# traning set 1780 bacth size 100 agar mempercepat traning
# lakukan pembuatan model dengan epoch 30
num_epochs = 50
history = model.fit(padded_latih, label_latih, epochs=num_epochs,
                    batch_size = 100 , 
                    validation_data=(padded_test, label_test),
                    callbacks=[callbacks], 
                    verbose=1
                    )

# dapat dilihat bahwa fungsi callback tidak dilakukan
# dikarenakan accuracy dan val_accuracy tidak diatas

# buat grafik learn rate
import matplotlib.pyplot as plt
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train'], loc='lower right')
plt.show()