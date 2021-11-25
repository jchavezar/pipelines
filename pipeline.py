
import kfp

from typing import NamedTuple

from kfp.v2.dsl import pipeline
from kfp.v2.dsl import component
from kfp.v2 import compiler
from google_cloud_pipeline_components import aiplatform as gcc_aip
import time

timestr = time.strftime("%H%M")
pipeline_name='pipe-{}'.format(timestr)
compiled_pipe='basic_pipeline_1'

PROJECT_ID='tron-302502'
BUCKET_NAME="gs://" + PROJECT_ID + "-bucket"
IMAGE_URI='gcr.io/tron-302502/kfp/custom:v1'
PIPELINE_ROOT = f"{BUCKET_NAME}/pipeline_root/"
REGION = 'us-central1'
BIGQUERY_DESTINATION = 'bq://{}'.format(PROJECT_ID)


@pipeline(name="{}".format(pipeline_name), description="A simple intro pipeline",
          pipeline_root='gs://tron-302502-bucket/basic-pipe')
def pipeline(
    bq_source: str = "bq://sara-vertex-demos.beans_demo.large_dataset",
    project: str = PROJECT_ID,
    gcp_region: str = REGION,
    container_uri: str = IMAGE_URI,
    bigquery_destination: str = BIGQUERY_DESTINATION,
):
    dataset_create_op = gcc_aip.TabularDatasetCreateOp(
        display_name="tabular-beans-dataset",
        bq_source=bq_source,
        project=project,
        location=gcp_region
    )

    training_op = gcc_aip.CustomContainerTrainingJobRunOp(
        display_name="pipeline-beans-custom-train",
        container_uri=container_uri,
        project=project,
        dataset=dataset_create_op.outputs["dataset"],
        staging_bucket=BUCKET_NAME,
        bigquery_destination=bigquery_destination
    )

    
if __name__ == '__main__':
    compiler.Compiler().compile(
        pipeline_func=pipeline, package_path="{}.json".format(compiled_pipe)
    )
