from phising_domain.pipeline.training_pipeline import start_training_pipeliune


file_path="/config/workspace/phising_dataset.csv"
print(__name__)
if __name__=="__main__":
    try:
        start_training_pipeliune()
    except Exception as e:
        raise PhisingException(e,sys)
