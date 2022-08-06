
from datetime import datetime
import uuid
from store.config.configuration import Configuartion
from store.logger import logging #get_log_file_name
from store.exception import StoreException
from threading import Thread
from typing import List

from multiprocessing import Process
from store.entity.artifact_entity import  DataIngestionArtifact #,ModelPusherArtifact, ModelEvaluationArtifact
#from store.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact
from store.entity.config_entity import DataIngestionConfig #, ModelEvaluationConfig
from store.component.data_ingestion import DataIngestion
#from store.component.data_validation import DataValidation
#from store.component.data_transformation import DataTransformation
#from store.component.model_trainer import ModelTrainer
#from store.component.model_evaluation import ModelEvaluation
#from store.component.model_pusher import ModelPusher
import os, sys
from collections import namedtuple
from datetime import datetime
import pandas as pd
from collections import namedtuple
from store.constant import EXPERIMENT_DIR_NAME, EXPERIMENT_FILE_NAME

Experiment = namedtuple("Experiment", ["experiment_id", "initialization_timestamp", "artifact_time_stamp",
"running_status", "start_time", "stop_time", "execution_time", "message",
"experiment_file_path", "accuracy", "is_model_accepted"])



class Pipeline:
    def __init__(self,config: Configuartion = Configuartion()) -> None:

        try:
            self.config=config

        except Exception as e:
            raise StoreException(e,sys) from e



    def start_data_ingestion(self)->DataIngestionArtifact:

        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()

        except Exception as e:
            raise StoreException(e,sys) from e 




    def run_pipeline(self):
        try:
            #data ingestion
            data_ingestion_artifact = self.start_data_ingestion()
            
        except Exception as e:
            raise StoreException(e,sys) from e 
