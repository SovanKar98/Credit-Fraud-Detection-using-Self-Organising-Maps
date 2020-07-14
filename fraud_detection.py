# Self Organizing Maps

# Importing the Libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Hybrid Deep Learnig Model


# Part 1 - Identify frauds using SOM

# Importing dataset
dataset  = pd.read_csv('Credit_Card_applications.csv')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

# Feature Scaling
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0,1))
X = sc.fit_transform(X)

# Training the SOM
from minisom import MiniSom
som = MiniSom(x = 10, y = 10, input_len = 15, sigma = 1.0, learning_rate = 0.5 )
som.random_weights_init(X)
som.train_random(data = X, num_iteration = 100)

# Visualizing the results
from pylab import bone, pcolor, colorbar, plot, show
bone()
pcolor(som.distance_map().T)
colorbar()
markers = ['o', 's']
colors = ['r', 'g']
for i, x in enumerate(X):
    w = som.winner(x)
    plot(w[0] + 0.5,
         w[1] + 0.5,
         markers[y[i]],
         markeredgecolor = colors[y[i]],
         markerfacecolor = 'None',
         markersize = 10,
         markeredgewidth = 2)
show()

# Finding the frauds
mappings = som.win_map(X)
frauds = np.concatenate((mappings[(2,8)], mappings[(7,5)]), axis = 0)
frauds = sc.inverse_transform(frauds)


# Part 2 - Going from Unsupervised to Supervised

# Creating Matrix of Features
customers = dataset.iloc[:, 1:].values

# Creating Dependent Variable
is_fraud = np.zeros(len(dataset))
for i in range(len(dataset)):
    if dataset.iloc[i,0] in frauds:
        is_fraud[i] = 1
        
# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
customers = sc.fit_transform(customers)

#Part 2 - Building the ANN

#Importing Keras libraries
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout

#Initialising the ANN
classifier = Sequential()
#Add Input Layer and First Hidden Layer with Dropout
classifier.add(Dense(output_dim = 6, init = 'uniform', activation = 'relu', input_dim = 15 ))
classifier.add(Dropout(rate = 0.1))
#Add Output Layer
classifier.add(Dense(output_dim = 1, init = 'uniform', activation = 'sigmoid'))
#Compiling the ANN
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Fitting classifier to the Training set
classifier.fit(customers, is_fraud, batch_size = 1, nb_epoch = 2)

# Predicting the Probabilities of Fraud
y_pred = classifier.predict(customers)
y_pred = np.concatenate((dataset.iloc[:,0:1].values, y_pred), axis = 1)
y_pred = y_pred[y_pred[:, 1].argsort()]











 