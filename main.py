from phising_domain.pipeline.training_pipeline import start_training_pipeliune
from phising_domain.pipeline.batch_porediction import start_batch_prediction 


file_path='/config/workspace/phising_dataset.csv'

print(__name__)
if __name__=="__main__":
     try:
          output_file = start_batch_prediction(input_file_path=file_path)
          print(output_file)
     except Exception as e:
          raise PhisingException(e,sys)