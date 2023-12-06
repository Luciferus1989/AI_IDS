import os
from openread import open_csv_file

current_directory = os.path.dirname(os.path.abspath(__file__))


file_1 = 'Dataset_Iot/Normal/win7_normal_2.csv'
backdoor = [('Dataset_Iot/Backdoor/win7_backdoor_normal_1.csv', 'backdoor'),
            ('Dataset_Iot/Backdoor/win7_backdoor_normal_2.csv', 'backdoor')]
ddos = [('Dataset_Iot/DDos/win7_DDoS_normal_1.csv', 'DDoS'),
        ('Dataset_Iot/DDos/win10_DDoS_normal_1.csv', 'DDoS')]
dos = [('Dataset_Iot/Dos/win7_DoS_normal_1.csv', 'dos'),
       ('Dataset_Iot/Dos/win10_DoS_normal_1.csv', 'dos')]
infection = [('Dataset_Iot/Infection/win7_injection_normal_1.csv', 'infection'),
             ('Dataset_Iot/Infection/win10_injection_normal_1.csv', 'infection')]
mitm = [('Dataset_Iot/MITM/win7_MIMT_normal_1.csv', 'mitm'),
        ('Dataset_Iot/MITM/win10_MITM_normal_1.csv', 'mitm')]
password = [('Dataset_Iot/Password/win7_password_normal_1.csv', 'password'),
            ('Dataset_Iot/Password/win10_password_normal_1.csv', 'password')]
runsomware = [('Dataset_Iot/Runsomware/win7_runsomware_normal_1.csv', 'runsomware'),
              ('Dataset_Iot/Runsomware/win7_runsomware_normal_2.csv', 'runsomware'),
              ('Dataset_Iot/Runsomware/win7_runsomware_normal_3.csv', 'runsomware')]
scanning = [('Dataset_Iot/Scanning/win7_scanning_normal_1.csv', 'scanning'),
            ('Dataset_Iot/Scanning/win10_scanning_normal_1.csv', 'scanning'),
            ('Dataset_Iot/Scanning/win10_scanning_normal_2.csv', 'scanning'),
            ('Dataset_Iot/Scanning/win10_scanning_normal_3.csv', 'scanning')]
xss = [('Dataset_Iot/XSS/win7_XSS_normal_1.csv', 'xss'),
       ('Dataset_Iot/XSS/win10_XSS_normal_1.csv', 'xss')]
normal = [('Dataset_Iot/Normal/win7_normal_2.csv', 'normal'),
          ('Dataset_Iot/Normal/win7_normal_3.csv', 'normal'),
          ('Dataset_Iot/Normal/win10_normal_1.csv', 'normal'),
          ('Dataset_Iot/Normal/win10_normal_2.csv', 'normal'),
          ('Dataset_Iot/Normal/win10_normal_3.csv', 'normal'),
          ('Dataset_Iot/Normal/win10_normal_4.csv', 'normal')]

a = backdoor[0][0]

file_path = os.path.join(current_directory, a)

df = open_csv_file(file_path)


X, y = load_and_preprocess_data()

# Encode categorical labels (if applicable)
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Reshape the data for CNN input (assuming 1D features)
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

# Convert labels to one-hot encoding
y_train_one_hot = tf.keras.utils.to_categorical(y_train, num_classes=num_classes)
y_test_one_hot = tf.keras.utils.to_categorical(y_test, num_classes=num_classes)

# Define the CNN model
model = models.Sequential()
model.add(layers.Conv1D(32, kernel_size=3, activation='relu', input_shape=(X_train.shape[1], 1)))
model.add(layers.MaxPooling1D(pool_size=2))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(num_classes, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train_one_hot, epochs=10, batch_size=64, validation_data=(X_test, y_test_one_hot))

# Evaluate the model on the test set
loss, accuracy = model.evaluate(X_test, y_test_one_hot)
print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')

# Make predictions
predictions = model.predict(X_test)
