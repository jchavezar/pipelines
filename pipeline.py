
import kfp

from typing import NamedTuple

from kfp.v2.dsl import pipeline
from kfp.v2.dsl import component
from kfp.v2 import compiler
import time

timestr = time.strftime("%H%M")
pipeline_name='pipe-{}'.format(timestr)
compiled_pipe='basic_pipeline_1'

@component
def op(a: float, b: float) -> float:
    return a+b

@pipeline(name="{}".format(pipeline_name), description="A simple intro pipeline",
          pipeline_root='gs://tron-302502-bucket/basic-pipe')
def basic_pipeline(a: float=468, b: float=864):
    op_task = op(a,b)
    
if __name__ == '__main__':
    compiler.Compiler().compile(
        pipeline_func=basic_pipeline, package_path="{}.json".format(compiled_pipe)
    )
