#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Correlation
"""

import sys
import arrow
import random
import numpy as np
import tensorflow as tf

class Correlation(object):
	"""
	Correlation

	It's the basic class for measuring the correlation between arbitrary query and document. 
	"""

	def __init__(self, feature_len, \
		         L1_scale=0.005, cost_w0=1.0, cost_w1=20.0, \
		         iters=5, lr=0.01, batch_size=1, display_step=1):
		# Model parameters
		self.iters        = iters
		# Note: batch size is not allowd to be larger than the size of the dataset
		self.batch_size   = batch_size
		self.display_step = display_step
		# TF graph input
		self.q = tf.placeholder(tf.float32, [None, feature_len], name="query")
		self.d = tf.placeholder(tf.float32, [None, feature_len], name="document")
		self.y = tf.placeholder(tf.float32, name="click")
		# Model weights
		w0 = tf.constant(cost_w0, dtype=tf.float32)
		w1 = tf.constant(cost_w1, dtype=tf.float32)
		W  = tf.Variable(tf.eye(feature_len), dtype=tf.float32)
		L1 = tf.contrib.layers.l1_regularizer(scale=L1_scale)

		# Construct model
		self.pred = tf.sigmoid(
			tf.reduce_sum(tf.multiply(tf.matmul(self.q, W), self.d), 1)/\
			(tf.norm(self.q, ord="euclidean", axis=1)*tf.norm(self.d, ord="euclidean", axis=1)))

		# Minimize error using cross entropy
		L1_loss        = tf.contrib.layers.apply_regularization(L1, [W])
		self.cost      = tf.reduce_mean(w0*self.y*tf.log(self.pred)+w1*(1-self.y)*tf.log(1-self.pred))+L1_loss
		# self.cost      = tf.reduce_sum(tf.pow(self.pred-self.y, 2))+L1_loss
		self.optimizer = tf.train.GradientDescentOptimizer(lr).minimize(self.cost)

		# Evaluate model
		correct_pred  = tf.equal(tf.round(self.pred), self.y)
		self.accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

	def train(self, sess, qs, ds, ys, test_qs, test_ds, test_ys, pretrained=False):
		"""
		Train

		
		"""

		# Set pretrained variable if it was existed
		if not pretrained:
			init = tf.global_variables_initializer()
			sess.run(init)

		step        = 1 # the step of the iteration
		start_index = 0 # the index of the start row of the batch
		# Keep training until reach max iterations
		while step * self.batch_size <= self.iters:
			# Fetch the next batch of the input data (q, d, y)
			# And update the start_indext in order to prepare for the next batch
			batch_qs, batch_ds, batch_ys, start_index = self._next_batch(qs, ds, ys, start_index)
			# Run optimization
			sess.run(self.optimizer, feed_dict={self.q: batch_qs, self.d: batch_ds, self.y: batch_ys})
			if step % self.display_step == 0:
				# Calculate batch loss and accuracy
				loss, acc = sess.run(
					[self.cost, self.accuracy], 
					feed_dict={self.q: batch_qs, self.d: batch_ds, self.y: batch_ys})
				test_loss, test_acc = sess.run(
					[self.cost, self.accuracy],
					feed_dict={self.q: test_qs, self.d: test_ds, self.y: test_ys})
				# Log information for each iteration
				print >> sys.stderr, "[%s] Iter: %d" % (arrow.now(), (step * self.batch_size)) 
				print >> sys.stderr, "[%s] Train:\tloss (%.5f)\tacc (%.5f)" % (arrow.now(), loss, acc)
				print >> sys.stderr, "[%s] Test:\tloss (%.5f)\tacc (%.5f)" % (arrow.now(), test_loss, test_acc)
				# print >> sys.stderr, "[%s] Test node value:", nodes[0].shape
			step += 1
		print >> sys.stderr, "[%s] Optimization Finished!" % arrow.now()

	def score(self, sess, qs, ds):
		"""
		Score

		Calculate the scores (prediction) between the pairs of (q, d)
		"""
		return sess.run(self.pred, feed_dict={self.q: qs, self.d: ds})

	def test_acc(self, sess, qs, ds, ys):
		"""
		Test Accuracy

		Calculate the accuracy of the predictions by testing multiple pairs of (q, d)
		"""
		return sess.run(self.accuracy, feed_dict={self.q: qs, self.d: ds, self.y: ys})
		
	def _next_batch(self, qs, ds, ys, start_index):
		"""
		Next Batch
		
		This is a private method for fetching a batch of data from the integral input data. 
		Each time you call this method, it would return the next batch in the dataset by indicating 
		the start index. Which means you have to keep the return start index of every invoking,
		and pass it to the next invoking for getting the next batch correctly. 
		"""

		# total number of rows of the input data (query and target)
		num_row, num_col = np.shape(qs)   
		# start index of the row of the input data
		start_row = start_index % num_row 
		# end index of the row of the input data
		end_row   = (start_row + self.batch_size) % num_row 
		# if there is not enought data left in the dataset for generating an integral batch,
		# then top up this batch by traversing back to the start of the dataset. 
		if end_row < start_row:
			batch_qs = np.append(qs[start_row: num_row], qs[0: end_row], axis=0).astype(np.float32)
			batch_ds = np.append(ds[start_row: num_row], ds[0: end_row], axis=0).astype(np.float32)
			batch_ys = np.append(ys[start_row: num_row], ys[0: end_row], axis=0).astype(np.float32)
		else:
			batch_qs = qs[start_row: end_row].astype(np.float32)
			batch_ds = ds[start_row: end_row].astype(np.float32)
			batch_ys = ys[start_row: end_row].astype(np.float32)
		# Update the start index
		start_index += self.batch_size
		return batch_qs, batch_ds, batch_ys, start_index
	