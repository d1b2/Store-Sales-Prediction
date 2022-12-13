from store.entity.config_entity import DataIngestionConfig
from store.entity.artifact_entity import *
import sys,os
from store.exception import StoreException
from store.logger import logging
import tarfile
import numpy as np
from six.moves import urllib
import pandas as pd
import sys,os

class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig ):
        try:
            logging.info(f"{'>>'*20}Data Ingestion log started.{'<<'*20} ")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise StoreException(e,sys)





    def download_store_data(self,) -> str:
        try:
            #extraction remote url to download dataset
            download_url = self.data_ingestion_config.dataset_download_url

            #folder location to download file
            tgz_download_dir = self.data_ingestion_config.tgz_download_dir
            os.makedirs(tgz_download_dir,exist_ok=True)
            store_file_name = os.path.basename(download_url)
            tgz_file_path = os.path.join(tgz_download_dir, store_file_name)

            logging.info(f"Downloading file from :[{download_url}] into :[{tgz_file_path}]")

            urllib.request.urlretrieve(download_url, tgz_file_path)
            logging.info(f"File :[{tgz_file_path}] has been downloaded successfully.")

            return tgz_file_path



        except Exception as e:
                raise StoreException(e,sys) from e



    def extract_tgz_file(self,tgz_file_path:str):

        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)
            
            os.makedirs(raw_data_dir,exist_ok=True)
            logging.info(f"Extracting tgz file: [{tgz_file_path}] into dir: [{raw_data_dir}]")

            with tarfile.open(tgz_file_path) as store_tgz_file_obj:
                
                import os
                
                def is_within_directory(directory, target):
                    
                    abs_directory = os.path.abspath(directory)
                    abs_target = os.path.abspath(target)
                
                    prefix = os.path.commonprefix([abs_directory, abs_target])
                    
                    return prefix == abs_directory
                
                def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                
                    for member in tar.getmembers():
                        member_path = os.path.join(path, member.name)
                        if not is_within_directory(path, member_path):
                            raise Exception("Attempted Path Traversal in Tar File")
                
                    tar.extractall(path, members, numeric_owner=numeric_owner) 
                    
                
                safe_extract(store_tgz_file_obj, path=raw_data_dir)

            logging.info(f"Extraction completed")

        except Exception as e:
            raise StoreException(e,sys) from e

    def data_as_train_test(self) -> DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            train_file_name = os.listdir(raw_data_dir)[0]
            store_train_file_path = os.path.join(raw_data_dir,train_file_name)


            logging.info(f"Reading Train.csv file: [{store_train_file_path}]")
            store_train_data_frame = pd.read_csv(store_train_file_path)

            store_train_data_frame.replace({'Item_Fat_Content': 
                {'low fat':'Low Fat','LF':'Low Fat', 'reg':'Regular'}}, inplace=True)
            
            train_set=store_train_data_frame.drop(['Outlet_Establishment_Year'],axis=1)


            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,
                                            train_file_name)
            
            if train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                logging.info(f"Exporting training datset to file: [{train_file_path}]")
                train_set.to_csv(train_file_path,index=False)

            test_file_name = os.listdir(raw_data_dir)[1]
            store_test_file_path = os.path.join(raw_data_dir,test_file_name)


            logging.info(f"Reading Test.csv file: [{store_test_file_path}]")
            store_test_data_frame = pd.read_csv(store_test_file_path)

            store_test_data_frame.replace({'Item_Fat_Content': 
                {'low fat':'Low Fat','LF':'Low Fat', 'reg':'Regular'}}, inplace=True)

            test_set=store_test_data_frame.drop(['Outlet_Establishment_Year'],axis=1)


            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,
                                        test_file_name)
            
            if test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                logging.info(f"Exporting testing datset to file: [{test_file_path}]")
                train_set.to_csv(train_file_path,index=False)

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                test_file_path=test_file_path,
                is_ingested=True,
                message=f"Data ingestion completed successfully."
                )
            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact


        except Exception as e:
            raise StoreException(e,sys) from e

    
    def data_as_train_test(self)-> DataIngestionArtifact:
        try:
            tgz_file_path = self.download_store_data()
            self.extract_tgz_file(tgz_file_path=tgz_file_path)
            return self.split_data_as_train_test()

        except Exception as e:
            raise StoreException(e,sys) from e



    def __del__(self):
        logging.info(f"{'>>'*20}Data Ingestion log completed.{'<<'*20} \n\n")
