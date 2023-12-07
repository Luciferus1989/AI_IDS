import os
from openread import open_csv_file, combine_normal, combine_attack, clean_null_rows, clean_na, common_type
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if os.path.isfile('normal.csv'):
    print('Fail {} is founded in dir.'.format('normal.csv'))
    df_normal = pd.read_csv('normal.csv', low_memory=False)
else:
    df_normal = combine_normal()
    df_normal.to_csv('normal.csv', index=False)

if os.path.isfile('attack.csv'):
    print('Fail {} is founded in dir.'.format('attack.csv'))
    df_attack = pd.read_csv('attack.csv', low_memory=False)
else:
    df_attack = combine_attack()
    df_attack.to_csv('attack.csv', index=False)


df = pd.concat([df_normal, df_attack], ignore_index=True)
print(df.shape)
df = clean_null_rows(df)
df = common_type(df)
print(df.shape)

# for i in df_normal.columns:
#     same_data_type = df_normal[i].apply(type).nunique() == 1
#     if not same_data_type:
#         count += 1
#         print("{}  There is value with diff type".format(i))
#     else:
#         continue


for i in df.columns:
    main_data_type = df[i].apply(type).mode().iloc[0]

    different_data_rows = df[df[i].apply(type) != main_data_type]

    if not different_data_rows.empty:
        print(f"Column: {i}")
        print(f"  Main Data Type: {main_data_type}")
        print(f"  Rows with Different Data Type: {len(different_data_rows)}")

        sample_values = different_data_rows[i].head(5).tolist()
        print(f"  Sample Values: {sample_values}")
        print("\n")


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
