
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_curve
from sklearn.model_selection import train_test_split
from google.cloud import bigquery
from google.cloud import storage
from joblib import dump
import logging
import os
import pandas as pd

logging.basicConfig(level=logging.INFO)

bqclient = bigquery.Client()
storage_client = storage.Client()

def download_table(bq_table_uri: str):
    prefix = "bq://"
    if bq_table_uri.startswith(prefix):
        bq_table_uri = bq_table_uri[len(prefix):]

    table = bigquery.TableReference.from_string(bq_table_uri)
    rows = bqclient.list_rows(
        table,
    )
    return rows.to_dataframe(create_bqstorage_client=False)

# These environment variables are from Vertex AI managed datasets
training_data_uri = os.environ["AIP_TRAINING_DATA_URI"]
test_data_uri = os.environ["AIP_TEST_DATA_URI"]

logging.info('testing')
logging.info(training_data_uri)
logging.info(test_data_uri)
logging.info(os.environ["AIP_MODEL_DIR"])
# Download data into Pandas DataFrames, split into train / test
df = download_table(training_data_uri)
test_df = download_table(test_data_uri)
labels = df.pop("Class").tolist()
data = df.values.tolist()
test_labels = test_df.pop("Class").tolist()
test_data = test_df.values.tolist()

# Define and train the Scikit model
skmodel = DecisionTreeClassifier()
skmodel.fit(data, labels)
score = skmodel.score(test_data, test_labels)
logging.info('no logging out')
logging.info('accuracy is: {}'.format(score))
logging.info(os.environ["AIP_MODEL_DIR"])

# Save the model to a local file
dump(skmodel, "model.joblib")
