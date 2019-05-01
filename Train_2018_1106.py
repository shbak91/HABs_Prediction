import tensorflow as tf
import pandas as pd
import numpy as np
import os
import datetime

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

tf.set_random_seed(608)

Data_Train_raw = pd.read_csv('Dataset_Train_2018_1106_add_noise(sampling_0.1)_n.csv')
Data_Test_raw = pd.read_csv('Dataset_Test_2018_1023_n.csv')

# Create Train & Test Dataset
name_col = Data_Train_raw.columns[0:59]

Data_Train = Data_Train_raw[name_col]
Data_Train_Class = Data_Train_raw[["ClassR", "ClassN"]]

Data_Test = Data_Test_raw[name_col]
Data_Test_Class = Data_Test_raw[["ClassR", "ClassN"]]

x_data = np.array(Data_Train.values, dtype=np.float32)
y_data = np.array(Data_Train_Class.values, dtype=np.float32)

x_data_test = np.array(Data_Test.values, dtype=np.float32)
y_data_test = np.array(Data_Test_Class.values, dtype=np.float32)

# Create Deep Neural Network Model(Multi-layer Neural Network)
n_node = 200
learning_rate = 1e-3

# Input layer
X = tf.placeholder(tf.float32, shape=[None, 59], name='X')
Y = tf.placeholder(tf.float32, shape=[None, 2], name='Y')

# Hidden Layer1
W1 = tf.Variable(tf.random_normal([59, n_node]), name='weight1')
b1 = tf.Variable(tf.random_normal([n_node]), name='bias1')
layer1 = tf.nn.relu(tf.add(tf.matmul(X, W1), b1), name='layer1')

# Hidden Layer2
W2 = tf.Variable(tf.random_normal([n_node, n_node]), name='weight2')
b2 = tf.Variable(tf.random_normal([n_node]), name='bias2')
layer2 = tf.nn.relu(tf.add(tf.matmul(layer1, W2), b2), name='layer2')

# Hidden Layer3
W3 = tf.Variable(tf.random_normal([n_node, n_node]), name='weight3')
b3 = tf.Variable(tf.random_normal([n_node]), name='bias3')
layer3 = tf.nn.relu(tf.add(tf.matmul(layer2, W3), b3), name='layer3')

# Hidden Layer4
W4 = tf.Variable(tf.random_normal([n_node, n_node]), name='weight4')
b4 = tf.Variable(tf.random_normal([n_node]), name='bias4')
layer4 = tf.nn.relu(tf.add(tf.matmul(layer3, W4), b4), name='layer4')

# Output layer
W5 = tf.Variable(tf.random_normal([n_node, 2]), name='weight5')
b5 = tf.Variable(tf.random_normal([2]), name='bias5')
hypothesis = tf.add(tf.matmul(layer4, W5), b5)
output = tf.sigmoid(hypothesis, name='output_layer')

# tf.train.Saver
saver = tf.train.Saver()

# Cost
cost = tf.losses.sigmoid_cross_entropy(Y, hypothesis)
train = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

# Predict
predict = tf.cast(output > 0.5, dtype=np.float32)
accuracy = tf.reduce_mean(tf.cast(tf.equal(predict, Y), dtype=np.float32))

# Start Training & Monitoring
print("Start Training!")
Time_Start = datetime.datetime.now()

with tf.Session() as sess:

    sess.run(tf.global_variables_initializer())

    x = 1
    step = 0
    cost_point = 0

    while x == 1:

        step = step + 1

        sess.run(train, feed_dict={X: x_data, Y: y_data})

        cost_train = sess.run(cost, feed_dict={X: x_data, Y: y_data})
        cost_test = sess.run(cost, feed_dict={X: x_data_test, Y: y_data_test})

        accuracy_train = sess.run(accuracy, feed_dict={X: x_data, Y: y_data})
        accuracy_test = sess.run(accuracy, feed_dict={X: x_data_test, Y: y_data_test})

        if step % 10 == 0:

            print("Epoch : ", step)
            print("Train Data Cost : ", cost_train)
            print("Test Data Cost : ", cost_test)

            # Accuracy Report
            print("Accuracy(Train) : ", accuracy_train)
            print("Accuracy(Test) : ", accuracy_test)
            print("============================================", "\n")

        if step == 1:

            memory_cost1 = cost_test

        elif step > 1:

            memory_cost2 = cost_test

            cost_index = memory_cost1 - memory_cost2

            if cost_index > 0.1:

                memory_cost1 = cost_test

            else:

                cost_point = cost_point + 1

        if cost_point == 10:

            x = 0

    saver.save(sess, "./HAB_Prediction_2018_1106_1")

    print("Stop Epoch : ", step)
    print("Stop Train Data Cost : ", cost_train)
    print("Stop Test Data Cost : ", cost_test)
    print("Stop Train Data Accuracy : ", accuracy_train)
    print("Stop Test Data Accuracy : ", accuracy_test)

Time_Finish = datetime.datetime.now()

Duration = Time_Finish - Time_Start

print(Duration.seconds)
