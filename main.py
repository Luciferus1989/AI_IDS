import os
from openread import open_csv_file, combine_normal, combine_attack
import pandas as pd

if os.path.isfile('normal.cvs'):
    print('Fail {} is founded in dir.'.format('normal.cvs'))
    df_normal = pd.read_csv('normal.cvs.csv')
else:
    df_normal = combine_normal()
    df_normal.to_csv('normal.cvs')

if os.path.isfile('attack.cvs'):
    print('Fail {} is founded in dir.'.format('attack.cvs'))
    df_attack = pd.read_csv('attack.cvs')
else:
    df_attack = combine_attack()
    df_attack.to_csv('attack.cvs')







# X, y = load_and_preprocess_data()
#
# # Encode categorical labels (if applicable)
# label_encoder = LabelEncoder()
# y = label_encoder.fit_transform(y)
#
# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#
# # Standardize features
# scaler = StandardScaler()
# X_train = scaler.fit_transform(X_train)
# X_test = scaler.transform(X_test)
#
# # Reshape the data for CNN input (assuming 1D features)
# X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
# X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)
#
# # Convert labels to one-hot encoding
# y_train_one_hot = tf.keras.utils.to_categorical(y_train, num_classes=num_classes)
# y_test_one_hot = tf.keras.utils.to_categorical(y_test, num_classes=num_classes)
#
# # Define the CNN model
# model = models.Sequential()
# model.add(layers.Conv1D(32, kernel_size=3, activation='relu', input_shape=(X_train.shape[1], 1)))
# model.add(layers.MaxPooling1D(pool_size=2))
# model.add(layers.Flatten())
# model.add(layers.Dense(64, activation='relu'))
# model.add(layers.Dense(num_classes, activation='softmax'))
#
# # Compile the model
# model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
#
# # Train the model
# model.fit(X_train, y_train_one_hot, epochs=10, batch_size=64, validation_data=(X_test, y_test_one_hot))
#
# # Evaluate the model on the test set
# loss, accuracy = model.evaluate(X_test, y_test_one_hot)
# print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')
#
# # Make predictions
# predictions = model.predict(X_test)
