from keras import Sequential, layers
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder, StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc

import logging

logging.basicConfig(level=logging.INFO)

class CNN:
    def __init__(self, dataframe):
        self.model = Sequential()
        self.df = dataframe
        self.y = self.df['Label']
        self.X = self.df.drop(columns=['Label'])
        self.trained_model = None

    def preprocess_data(self):
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(self.y)

        scaler = StandardScaler()
        X_train, X_test, y_train, y_test = train_test_split(self.X, y, test_size=0.2, random_state=42)

        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        X_train = np.expand_dims(X_train, axis=2)
        X_test = np.expand_dims(X_test, axis=2)

        return X_train, X_test, y_train, y_test, label_encoder



    def build_model(self, num_classes):
        self.model.add(layers.Conv1D(32, kernel_size=3, activation='relu', input_shape=(self.X.shape[1], 1)))
        self.model.add(layers.MaxPooling1D(pool_size=2))
        self.model.add(layers.Flatten())
        self.model.add(layers.Dense(64, activation='relu'))
        self.model.add(layers.Dense(num_classes, activation='softmax'))

        self.model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    def train(self, epochs, batch_size):
        X_train, X_test, y_train, y_test, label_encoder = self.preprocess_data()
        num_classes = len(label_encoder.classes_)

        self.build_model(num_classes)

        self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test))
        loss, accuracy = self.model.evaluate(X_test, y_test)
        logging.info(f'Test Loss: {loss}, Test Accuracy: {accuracy}')

        self.trained_model = self.model

        predictions_prob = self.model.predict(X_test)
        predictions = np.argmax(predictions_prob, axis=1)
        predicted_labels = label_encoder.inverse_transform(predictions)
        accuracy = np.mean(predictions == y_test)
        logging.info(f'Test Accuracy: {accuracy}')

        # Additional Metrics and Analysis
        logging.info("Classification Report:")
        logging.info(classification_report(y_test, predictions))

        # Confusion Matrix
        logging.info("Confusion Matrix:")
        logging.info(confusion_matrix(y_test, predictions))
        
        # Generate confusion matrix
        conf_matrix = confusion_matrix(y_test, predictions)

        # Display Confusion Matrix as a heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(confusion_matrix(y_test, predictions), annot=True, cmap='Blues', fmt='d', xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
        plt.xlabel('Predicted labels')
        plt.ylabel('True labels')
        plt.title('Confusion Matrix')
        plt.show()

        # ROC Curve
        fpr = {}
        tpr = {}
        roc_auc = {}

        for i in range(num_classes):
            fpr[i], tpr[i], _ = roc_curve((y_test == i).astype(int), predictions_prob[:, i])
            roc_auc[i] = auc(fpr[i], tpr[i])

        plt.figure(figsize=(10, 8))
        for i in range(num_classes):
            plt.plot(fpr[i], tpr[i], label=f'Class {i} (AUC = {roc_auc[i]:.2f})')

        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve')
        plt.legend(loc='best')
        plt.show()


        for i in range(10):
            actual_label = label_encoder.inverse_transform([y_test[i]])[0]
            predicted_label = predicted_labels[i]

            logging.info(f'Actual: {actual_label}, Predicted: {predicted_label}')

        classes = label_encoder.classes_
        return X_train, X_test, y_train, y_test, label_encoder, classes

    def cross_validate(self, folds):
        X, _, y, _, _ = self.preprocess_data()
        scores = cross_val_score(self.model, X, y, cv=folds)
        logging.info(f'Cross-validated Accuracy: {np.mean(scores)}')
