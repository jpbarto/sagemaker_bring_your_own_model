#!/usr/bin/env python
# This is the file that implements a flask server to do inferences. It's the file that you will modify to
# implement the scoring for your own algorithm.

from __future__ import print_function

import os
import pickle
import StringIO
import sys
import signal
import traceback
import json
import flask


import tensorflow as tf

prefix = '/opt/ml/'
model_path = os.path.join(prefix, 'model')

# It has a predict function that does a prediction based on the model and the input data.

class ScoringService(object):

    @classmethod
    def predict(cls, input):
        _CSV_COLUMNS = [
            'age', 'workclass', 'fnlwgt', 'education', 'education_num',
            'marital_status', 'occupation', 'relationship', 'race', 'gender',
            'capital_gain', 'capital_loss', 'hours_per_week', 'native_country',
            'income_bracket'
        ]

        _CSV_COLUMN_DEFAULTS = [[0], [''], [0], [''], [0], [''], [''], [''], [''], [''],
                                [0], [0], [0], [''], ['']]

        _NUM_EXAMPLES = {
            'train': 32561,
            'validation': 16281,
        }

        def build_model_columns():
          """Builds a set of wide and deep feature columns."""
          # Continuous columns
          age = tf.feature_column.numeric_column('age')
          education_num = tf.feature_column.numeric_column('education_num')
          capital_gain = tf.feature_column.numeric_column('capital_gain')
          capital_loss = tf.feature_column.numeric_column('capital_loss')
          hours_per_week = tf.feature_column.numeric_column('hours_per_week')

          education = tf.feature_column.categorical_column_with_vocabulary_list(
              'education', [
                  'Bachelors', 'HS-grad', '11th', 'Masters', '9th', 'Some-college',
                  'Assoc-acdm', 'Assoc-voc', '7th-8th', 'Doctorate', 'Prof-school',
                  '5th-6th', '10th', '1st-4th', 'Preschool', '12th'])

          marital_status = tf.feature_column.categorical_column_with_vocabulary_list(
              'marital_status', [
                  'Married-civ-spouse', 'Divorced', 'Married-spouse-absent',
                  'Never-married', 'Separated', 'Married-AF-spouse', 'Widowed'])

          relationship = tf.feature_column.categorical_column_with_vocabulary_list(
              'relationship', [
                  'Husband', 'Not-in-family', 'Wife', 'Own-child', 'Unmarried',
                  'Other-relative'])

          workclass = tf.feature_column.categorical_column_with_vocabulary_list(
              'workclass', [
                  'Self-emp-not-inc', 'Private', 'State-gov', 'Federal-gov',
                  'Local-gov', '?', 'Self-emp-inc', 'Without-pay', 'Never-worked'])

          # To show an example of hashing:
          occupation = tf.feature_column.categorical_column_with_hash_bucket(
              'occupation', hash_bucket_size=1000)

          # Transformations.
          age_buckets = tf.feature_column.bucketized_column(
              age, boundaries=[18, 25, 30, 35, 40, 45, 50, 55, 60, 65])

          # Wide columns and deep columns.
          base_columns = [
              education, marital_status, relationship, workclass, occupation,
              age_buckets,
          ]

          crossed_columns = [
              tf.feature_column.crossed_column(
                  ['education', 'occupation'], hash_bucket_size=1000),
              tf.feature_column.crossed_column(
                  [age_buckets, 'education', 'occupation'], hash_bucket_size=1000),
          ]

          wide_columns = base_columns + crossed_columns

          deep_columns = [
              age,
              education_num,
              capital_gain,
              capital_loss,
              hours_per_week,
              tf.feature_column.indicator_column(workclass),
              tf.feature_column.indicator_column(education),
              tf.feature_column.indicator_column(marital_status),
              tf.feature_column.indicator_column(relationship),
              # To show an example of embedding
              tf.feature_column.embedding_column(occupation, dimension=8),
          ]

          return wide_columns, deep_columns

        def build_estimator(model_dir, model_type):
          """Build an estimator appropriate for the given model type."""
          wide_columns, deep_columns = build_model_columns()
          hidden_units = [100, 75, 50, 25]

          # Create a tf.estimator.RunConfig to ensure the model is run on CPU, which
          # trains faster than GPU for this model.
          run_config = tf.estimator.RunConfig().replace(
              session_config=tf.ConfigProto(device_count={'GPU': 0}))

          if model_type == 'wide':
            return tf.estimator.LinearClassifier(
                model_dir=model_dir,
                feature_columns=wide_columns,
                config=run_config)
          elif model_type == 'deep':
            return tf.estimator.DNNClassifier(
                model_dir=model_dir,
                feature_columns=deep_columns,
                hidden_units=hidden_units,
                config=run_config)
          else:
            return tf.estimator.DNNLinearCombinedClassifier(
                model_dir=model_dir,
                linear_feature_columns=wide_columns,
                dnn_feature_columns=deep_columns,
                dnn_hidden_units=hidden_units,
                config=run_config)


        def input_fn(data_file, num_epochs, shuffle, batch_size):
          """Generate an input function for the Estimator."""
          assert tf.gfile.Exists(data_file), (
              '%s not found. Please make sure you have either run data_download.py or '
              'set both arguments --train_data and --test_data.' % data_file)

          def parse_csv(value):
            print('Parsing', data_file)
            columns = tf.decode_csv(value, record_defaults=_CSV_COLUMN_DEFAULTS)
            features = dict(zip(_CSV_COLUMNS, columns))
            labels = features.pop('income_bracket')
            return features, tf.equal(labels, '>50K')

          # Extract lines from input files using the Dataset API.
          dataset = tf.data.TextLineDataset(data_file)

          if shuffle:
            dataset = dataset.shuffle(buffer_size=_NUM_EXAMPLES['train'])

          dataset = dataset.map(parse_csv, num_parallel_calls=5)

          # We call repeat after shuffling, rather than before, to prevent separate
          # epochs from blending together.
          dataset = dataset.repeat(num_epochs)
          dataset = dataset.batch(batch_size)

          iterator = dataset.make_one_shot_iterator()
          features, labels = iterator.get_next()
          return features, labels



        print('printing input to predict')
        print (input)
        TEST_INPUT = input
        testing_dir = '/notebooks/test'
        input_csv = '/notebooks/test/test.csv'
        
         # Create temporary CSV file
        if not tf.gfile.Exists(testing_dir):
            tf.gfile.MkDir(testing_dir)
            
        # Remove file if it exists already to avoid errors
        if tf.gfile.Exists(input_csv):
            os.remove(input_csv)
            print("File Removed!")
        
        with tf.gfile.Open(input_csv, 'w') as temp_csv:
                temp_csv.write(TEST_INPUT)

        # restore trained model with same model_dir and model_type
        model = build_estimator(model_path, 'wide')
        pred_iter = model.predict(input_fn=lambda: input_fn(input_csv, 1, False, 1))
        for pred in pred_iter:
                print(pred)
                print (type(pred['classes']))
                print('Based on the provided inputs, the individuals income (1 for >50K and 0 for <=50k) will be :'+  str(pred['classes']))

        return ('Based on the provided inputs, the individuals income will be : '+  str(pred['classes'])+ ' where, 1 is for >50k and 0 for <=50k')

# The flask app for serving predictions
app = flask.Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    """Check to see if the checkpoint file exists as a part of the package downloaded from s3 in the model directory"""
    if os.path.isfile('/opt/ml/model/checkpoint'):
        status = 200
    else:
        status = 404
    return flask.Response(response='\n', status=status)

@app.route('/invocations', methods=['POST'])
def transformation():
    """Do an inference on a single batch of data. In this sample server, we take data as CSV, convert
    it to a pandas data frame for internal use and then convert the predictions back to CSV (which really
    just means one prediction per line, since there's a single column.
    """
    #data = None
    data = flask.request.data
    print ('printing post data')
    print(data)
    print (str(data))
    print ('printing ml directory')
    print (os.listdir('/opt/ml'))
    print (os.listdir('/opt/ml/model'))


    # Do the prediction
    predictions = ScoringService.predict(data)


    return flask.Response(response=predictions, status=200)

