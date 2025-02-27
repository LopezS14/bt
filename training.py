import random
import json
import pickle
import numpy as np
import keras
from keras.layers import Dense, Activation, Dropout
from keras import Sequential
from keras.optimizers import SGD
import nltk
#nltk.download('punkt')
#nltk.download('wordnet')
#nltk.download('omw-1.4')
nltk.download('all')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

intents = json.loads(open('comands.json').read())



words = []
classes = []
documents = []
ignore_letters = ['?', '!', '¿', '.', ',']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent["tag"]))
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

training = []
output_empty = [0] * len(classes)
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)

# Convertir a listas separadas para train_x y train_y
train_x = []
train_y = []

for pattern, tag in training:
    train_x.append(pattern)
    train_y.append(tag)

# Convertir a matrices NumPy
train_x = np.array(train_x)
train_y = np.array(train_y)

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Utilizar el optimizador heredado SGD
sgd = SGD(learning_rate=0.001, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

train_process = model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)
model.save("chatbot_model.h5", train_process)
