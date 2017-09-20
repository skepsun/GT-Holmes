import sys
import numpy as np
import tensorflow as tf

class Click2Score(object):
	"""
	
	"""

	def __init__(self, query_len, iter=20, lr=0.01, batch_size=1, display_step=1):
		# Model parameters

		# TF graph input
		pass
		
if __name__ == "__main__":

	query_len = 3
	lr = 0.1

	batch_q = [[1, 0, 0], [1, 1, 0], [0, 0, 1], [0, 0, 1], [0, 0, 0]]
	batch_d = [[1, 0, 0], [1, 0, 0], [0, 0, 1], [0, 1, 1], [0, 0, 1]]
	batch_y = [1, 1, 0, 0, 0]


	q = tf.placeholder(tf.float32, [None, query_len], name="query")
	d = tf.placeholder(tf.float32, [None, query_len], name="document")
	y = tf.placeholder(tf.float32, name="click")

	# Model weights
	w0 = tf.constant(1.0, dtype=tf.float32)
	w1 = tf.constant(1.0, dtype=tf.float32)
	W  = tf.Variable(tf.eye(query_len), dtype=tf.float32)
	# l1_regularizer = tf.contrib.layers.l1_regularizer(scale=0.005)

	# Construct model
	pred = tf.sigmoid(tf.matmul(tf.matmul(q, W), tf.transpose(d)))
	# l1_penalty = tf.contrib.layers.apply_regularization(l1_regularizer, W)

	# Minimize error using cross entropy
	cost = tf.reduce_mean(w0*y*tf.log(pred)+w1*(1-y)*tf.log(1-pred))#+l1_penalty

	optimizer = tf.train.GradientDescentOptimizer(lr).minimize(cost)

	init = tf.global_variables_initializer()

	# Start training
	with tf.Session() as sess:
		sess.run(init)
		sess.run(optimizer, feed_dict={q: batch_q, d: batch_d, y: batch_y})


    







