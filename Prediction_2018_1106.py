import tensorflow as tf
import pandas as pd
import numpy as np
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Load Data
D = pd.read_csv('2018_0723.dat')

x_data = D[['d4ncpcp', 'd5ncpcp', 'd6ncpcp', 'd7ncpcp', 'd8ncpcp', 'd9ncpcp',
            'd4swdir', 'd5swdir', 'd6swdir', 'd7swdir', 'd8swdir', 'd9swdir',
            'd4w_spd', 'd5w_spd', 'd6w_spd', 'd7w_spd', 'd8w_spd', 'd9w_spd',
            'd4w_dir', 'd5w_dir', 'd6w_dir', 'd7w_dir', 'd8w_dir', 'd9w_dir',
            'd4w_tmp', 'd5w_tmp', 'd6w_tmp', 'd7w_tmp', 'd8w_tmp', 'd9w_tmp',
            'diff_swdir', 'diff_w_tmp',
            'd4diff_w_a', 'd5diff_w_a', 'd6diff_w_a', 'd7diff_w_a', 'd8diff_w_a', 'd9diff_w_a',
            'max_ncpcp', 'max_swdir', 'max_w_tmp', 'max_w_spd',
            'min_ncpcp', 'min_swdir', 'min_w_tmp', 'min_w_spd',
            'mean_ncpcp', 'mean_swdir', 'mean_w_tmp', 'mean_w_spd',
            'sum_ncpcp', 'sum_swdir', 'sum_w_tmp',
            'd4wci', 'd5wci', 'd6wci', 'd7wci', 'd8wci', 'd9wci']]

similarity = D[['similarity']]

# x_data for export
x_data2 = D[['d4ncpcp', 'd5ncpcp', 'd6ncpcp', 'd7ncpcp', 'd8ncpcp', 'd9ncpcp',
             'd4swdir', 'd5swdir', 'd6swdir', 'd7swdir', 'd8swdir', 'd9swdir',
             'd4w_spd', 'd5w_spd', 'd6w_spd', 'd7w_spd', 'd8w_spd', 'd9w_spd',
             'd4w_dir', 'd5w_dir', 'd6w_dir', 'd7w_dir', 'd8w_dir', 'd9w_dir',
             'd4w_tmp', 'd5w_tmp', 'd6w_tmp', 'd7w_tmp', 'd8w_tmp', 'd9w_tmp',
             'diff_swdir', 'diff_w_tmp',
             'd4diff_w_a', 'd5diff_w_a', 'd6diff_w_a', 'd7diff_w_a', 'd8diff_w_a', 'd9diff_w_a',
             'max_ncpcp', 'max_swdir', 'max_w_tmp', 'max_w_spd',
             'min_ncpcp', 'min_swdir', 'min_w_tmp', 'min_w_spd',
             'mean_ncpcp', 'mean_swdir', 'mean_w_tmp', 'mean_w_spd',
             'sum_ncpcp', 'sum_swdir', 'sum_w_tmp',
             'd4wci', 'd5wci', 'd6wci', 'd7wci', 'd8wci', 'd9wci']]

# Input Data Normalization
# ncpcp : Rain
x_data[['d4ncpcp']] = x_data[['d4ncpcp']]/73
x_data[['d5ncpcp']] = x_data[['d5ncpcp']]/73
x_data[['d6ncpcp']] = x_data[['d6ncpcp']]/73
x_data[['d7ncpcp']] = x_data[['d7ncpcp']]/73
x_data[['d8ncpcp']] = x_data[['d8ncpcp']]/73
x_data[['d9ncpcp']] = x_data[['d9ncpcp']]/73
# swdir : Sun
x_data[['d4swdir']] = x_data[['d4swdir']]/318
x_data[['d5swdir']] = x_data[['d5swdir']]/318
x_data[['d6swdir']] = x_data[['d6swdir']]/318
x_data[['d7swdir']] = x_data[['d7swdir']]/318
x_data[['d8swdir']] = x_data[['d8swdir']]/318
x_data[['d9swdir']] = x_data[['d9swdir']]/318
# w_spd : Wind Speed
x_data[['d4w_spd']] = x_data[['d4w_spd']]/10
x_data[['d5w_spd']] = x_data[['d5w_spd']]/10
x_data[['d6w_spd']] = x_data[['d6w_spd']]/10
x_data[['d7w_spd']] = x_data[['d7w_spd']]/10
x_data[['d8w_spd']] = x_data[['d8w_spd']]/10
x_data[['d9w_spd']] = x_data[['d9w_spd']]/10
# w_dir : Wind Direction
x_data[['d4w_dir']] = x_data[['d4w_dir']]/360
x_data[['d5w_dir']] = x_data[['d5w_dir']]/360
x_data[['d6w_dir']] = x_data[['d6w_dir']]/360
x_data[['d7w_dir']] = x_data[['d7w_dir']]/360
x_data[['d8w_dir']] = x_data[['d8w_dir']]/360
x_data[['d9w_dir']] = x_data[['d9w_dir']]/360
# w_tmp : Water Temperature
x_data[['d4w_tmp']] = (x_data[['d4w_tmp']]-6)/20
x_data[['d5w_tmp']] = (x_data[['d5w_tmp']]-6)/20
x_data[['d6w_tmp']] = (x_data[['d6w_tmp']]-6)/20
x_data[['d7w_tmp']] = (x_data[['d7w_tmp']]-6)/20
x_data[['d8w_tmp']] = (x_data[['d8w_tmp']]-6)/20
x_data[['d9w_tmp']] = (x_data[['d9w_tmp']]-6)/20

x_data[['diff_swdir']] = (x_data[['diff_swdir']]+45)/(34+45)
x_data[['diff_w_tmp']] = x_data[['diff_w_tmp']]

x_data[['d4diff_w_a']] = x_data[['d4diff_w_a']]/10
x_data[['d5diff_w_a']] = x_data[['d5diff_w_a']]/10
x_data[['d6diff_w_a']] = x_data[['d6diff_w_a']]/10
x_data[['d7diff_w_a']] = x_data[['d7diff_w_a']]/10
x_data[['d8diff_w_a']] = x_data[['d8diff_w_a']]/10
x_data[['d9diff_w_a']] = x_data[['d9diff_w_a']]/10

x_data[['max_ncpcp']] = x_data[['max_ncpcp']]/168
x_data[['max_swdir']] = (x_data[['max_swdir']]-103)/(329-103)
x_data[['max_w_tmp']] = (x_data[['max_w_tmp']]-6)/21
x_data[['max_w_spd']] = (x_data[['max_w_spd']]-2)/9

x_data[['min_ncpcp']] = x_data[['min_ncpcp']]
x_data[['min_swdir']] = x_data[['min_swdir']]/162
x_data[['min_w_tmp']] = (x_data[['min_w_tmp']]-5)/19
x_data[['min_w_spd']] = x_data[['min_w_spd']]/4

x_data[['mean_ncpcp']] = x_data[['mean_ncpcp']]/45
x_data[['mean_swdir']] = (x_data[['mean_ncpcp']]-40)/(249-40)
x_data[['mean_w_tmp']] = (x_data[['mean_w_tmp']]-5)/(25-5)
x_data[['mean_w_spd']] = (x_data[['mean_w_spd']]-1)/(8-1)

x_data[['sum_ncpcp']] = x_data[['sum_ncpcp']]/273
x_data[['sum_swdir']] = (x_data[['sum_swdir']]-241)/(1494-241)
x_data[['sum_w_tmp']] = (x_data[['sum_w_tmp']]-35)/(154-35)

x_data[['d4wci']] = (x_data[['d4wci']]-100)/832
x_data[['d5wci']] = (x_data[['d5wci']]-100)/832
x_data[['d6wci']] = (x_data[['d6wci']]-100)/832
x_data[['d7wci']] = (x_data[['d7wci']]-100)/832
x_data[['d8wci']] = (x_data[['d8wci']]-100)/832
x_data[['d9wci']] = (x_data[['d9wci']]-100)/832

# Location info
# test를 위해 임의로 "ClassR" 칼럼과 "ClassN" 칼럼을 불러 사용하였습니다.
# 실제 데이터에서는 "Lat"과 "Lon"을 사용해야 합니다.
Location1 = D[["lat"]]
Location1 = np.array(Location1.values, dtype=np.float32)

Location2 = D[["lon"]]
Location2 = np.array(Location2.values, dtype=np.float32)

# 예측결과가 저장될 변수 result와 차원을 맞춰주기 위해 Location의 shape 변경
Location1 = np.squeeze(Location1)
Location2 = np.squeeze(Location2)

# Define Model Structure
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

# Run Prediction
with tf.Session() as sess:

    saver.restore(sess, "./HAB_Prediction_2018_1106_1")

    p = tf.argmax(output, axis=1)
    result = sess.run(p, feed_dict={X: x_data})
    result = np.array(result, dtype=np.float32)

    h = sess.run(output, feed_dict={X: x_data})

r = np.c_[Location1, Location2, x_data2, h, result, similarity]
r2 = []

row_n = r.shape[0]

for i in range(row_n):
    # r[i,61] : ClassR
    # r[i,62] : ClassN
    # r[i,63] : Result

    # Result == 0
    # remove ClassR < 0.5 (Result : 0 -> 1)
    if r[i, 63] == 0 and r[i, 61] < 0.5:

        r[i, 63] = 1

for i in range(row_n):

    if r[i, 63] == 0:

        r2.append(r[i, ])

np.savetxt("Prediction_Result_2018_0723.csv", r,
           header="lat,lon,d4ncpcp,d5ncpcp,d6ncpcp,d7ncpcp,d8ncpcp,d9ncpcp,d4swdir,d5swdir,"
                  "d6swdir,d7swdir,d8swdir,d9swdir,d4w_spd,d5w_spd,d6w_spd,d7w_spd,d8w_spd,d9w_spd,"
                  "d4w_dir,d5w_dir,d6w_dir,d7w_dir,d8w_dir,d9w_dir,d4w_tmp,d5w_tmp,d6w_tmp,d7w_tmp,"
                  "d8w_tmp,d9w_tmp,diff_swdir,diff_w_tmp,d4diff_w_a,d5diff_w_a,d6diff_w_a,d7diff_w_a,"
                  "d8diff_w_a,d9diff_w_a,max_ncpcp,max_swdir,max_w_tmp,max_w_spd,min_ncpcp,min_swdir,"
                  "min_w_tmp,min_w_spd,mean_ncpcp,mean_swdir,mean_w_tmp,mean_w_spd,sum_ncpcp,sum_swdir,"
                  "sum_w_tmp,d4wci,d5wci,d6wci,d7wci,d8wci,d9wci,ClassR,ClassN,result,similarity",
           delimiter=",",
           comments="",
           fmt="%3.4f")

np.savetxt("Prediction_HAB_2018_0723.csv", r2,
           header="lat,lon,d4ncpcp,d5ncpcp,d6ncpcp,d7ncpcp,d8ncpcp,d9ncpcp,d4swdir,d5swdir,"
                  "d6swdir,d7swdir,d8swdir,d9swdir,d4w_spd,d5w_spd,d6w_spd,d7w_spd,d8w_spd,d9w_spd,"
                  "d4w_dir,d5w_dir,d6w_dir,d7w_dir,d8w_dir,d9w_dir,d4w_tmp,d5w_tmp,d6w_tmp,d7w_tmp,"
                  "d8w_tmp,d9w_tmp,diff_swdir,diff_w_tmp,d4diff_w_a,d5diff_w_a,d6diff_w_a,d7diff_w_a,"
                  "d8diff_w_a,d9diff_w_a,max_ncpcp,max_swdir,max_w_tmp,max_w_spd,min_ncpcp,min_swdir,"
                  "min_w_tmp,min_w_spd,mean_ncpcp,mean_swdir,mean_w_tmp,mean_w_spd,sum_ncpcp,sum_swdir,"
                  "sum_w_tmp,d4wci,d5wci,d6wci,d7wci,d8wci,d9wci,ClassR,ClassN,result,similarity",
           delimiter=",",
           comments="",
           fmt="%3.4f")
