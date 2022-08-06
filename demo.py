from store.pipeline.pipeline import Pipeline
from store.exception import StoreException
from store.logger import logging
import sys,os


def main():
    try:
        pipeline = Pipeline()
        pipeline.run_pipeline()


    except Exception as e:
    
        raise StoreException(e,sys) from e


        print(e)




if __name__=="__main__":
    main()
