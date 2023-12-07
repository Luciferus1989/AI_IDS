from keras import Sequential, layers, models
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from sklearn.preprocessing import LabelEncoder, StandardScaler


class CNN:
    """
        Convolutional Neural Network (CNN) for classification.
    Attributes:
        model (Sequential): Keras Sequential model for the CNN.
        df (pd.DataFrame): Input dataframe containing features and labels.
        y (pd.Series): Target labels.
        X (pd.DataFrame): Feature matrix.
        trained_model : Trained CNN model.

    """
    def __init__(self, dataframe):
        """
        Initializes the CNN object.

        Parameters:
        dataframe (pd.DataFrame): Input dataframe containing features and labels.
        """
        self.model = Sequential()
        self.df = dataframe
        self.y = self.df['Label']
        self.X = self.df.drop(columns=['Label'])
        self.trained_model = None

    def train(self):
        """
        Trains the CNN model.
        :return: None for now.
        """

        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(self.y)

        X_train, X_test, y_train, y_test = train_test_split(self.X, y, test_size=0.2, random_state=42)

        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
        X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

        num_classes = len(np.unique(y))
        y_train_one_hot = tf.keras.utils.to_categorical(y_train, num_classes=num_classes)
        y_test_one_hot = tf.keras.utils.to_categorical(y_test, num_classes=num_classes)

        model = models.Sequential()
        model.add(layers.Conv1D(32, kernel_size=3, activation='relu', input_shape=(X_train.shape[1], 1)))
        model.add(layers.MaxPooling1D(pool_size=2))
        model.add(layers.Flatten())
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(num_classes, activation='softmax'))

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        model.fit(X_train, y_train_one_hot, epochs=10, batch_size=64, validation_data=(X_test, y_test_one_hot))
        loss, accuracy = model.evaluate(X_test, y_test_one_hot)
        print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')

        self.trained_model = model

        print('----------------------------------------')
        predictions_prob = model.predict(X_test)
        predictions = np.argmax(predictions_prob, axis=1)
        predicted_labels = label_encoder.inverse_transform(predictions)
        accuracy = np.mean(predictions == y_test)
        print(f'Test Accuracy: {accuracy}')

        loss, accuracy = model.evaluate(X_test, y_test_one_hot)
        print(f'Test Accuracy (using evaluate): {accuracy}')

        for i in range(10):
            actual_label = label_encoder.inverse_transform([y_test[i]])[0]
            predicted_label = predicted_labels[i]
            probabilities = predictions_prob[i]

            print(f'Actual: {actual_label}, Predicted: {predicted_label}')


