from phising_domain.entity import artifact_entity,config_entity 
from phising_domain.logger import logging 
from phising_domain.exception import PhisingException 
from typing import Optional 
import os,sys 
from phising_domain import utils 
from sklearn.ensemble import RandomForestClassifier 
from sklearn.metrics import f1_score  
  



class ModelTrainer:
    def __init__ (self,model_trainer_config:config_entity.ModelTrainerConfig,data_transformation_artifact:artifact_entity.DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact  
        except Exceptionas as e:
            raise FraudException(e,sys)



    def train_model(self,x,y):
        try:
            rf=RandomForestClassifier()
            rf.fit(x,y)
            return rf
        except Exception as e:
            raise PhishingException(e,sys)


    def initiate_model_trainer(self):
        try:
            train_arr=utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_path)
            test_arr=utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_path)

            x_train,y_train=train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test=test_arr[:,:-1],test_arr[:,-1]


            model=self.train_model(x=x_train,y=y_train) 


            yhat_train=model.predict(x_train)
            f1_train_score=f1_score(y_true=y_train,y_pred=yhat_train)

            yhat_test=model.predict(x_test)
            f1_test_score=f1_score(y_true=y_test,y_pred=yhat_test)


            if f1_test_score<self.model_trainer_config.expected_score:
                raise Exception("model is not good ") 

            diff=abs(f1_train_score-f1_test_score)
            if diff>self.model_trainer_config.overfitting_threshold:
                raise Exception("model is overfitted")


            utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)


            model_trainer_artifact  = artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path, 
            f1_train_score=f1_train_score, f1_test_score=f1_test_score)

            return model_trainer_artifact


        except Exception as e:
            raise PhisingException(e,sys)
        
