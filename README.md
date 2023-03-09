1.Taking dataset from the given link and uploadinh into git hub repo.

2.Dumping the collected data into a mongo db database, cassandra and SQL data bases giving some issues so using MONGO DB data base.

3.Creating a folder phishing domain,inside these folder creating four folders Components, pipeline, Utils and entiy folder for every folder creating a __init__.py file .

4.In components folder creating data_ingestion, data_validation ,data transformation ,model trainer, model evaluation and model pusher python files.

5.In entity folder creating artifact entity and config entity files. The input giving to components are called as CONFIG ENTITY and the outputs of components file is called as artifact entity.

6. In config folder creating data ingestion config,data validation config, data transformation config , model building config,model evaluation config and model pusherconfig python files. Creating a training pipeline in config entity folder. using these pipeline creating a artifact folder in current working directory .

7.In data ingestion config , creating a feature store file path and data store file path. feature store file path is used to store collected data as  a .csv file. in dataset foldere storing train dataset and test dataset.

8.In data ingestiuon componenmt we collect the data as a dataframe and splitting data into train and test datsets , collecting data using a function written in utils folder .

9.In utils folder we can write some functions, whhen we want to call or need that function we directly import from the utils folder, like that get collection as data ftrame function written in utils folder is useful for collecting data as dataframe in data ingestion componenet.

10. In data ingestion component we collect the data as data frame and , if the data set contains any unwanted columns dropping them , if thge data set containd 'na' values then replacing them with 'np.nan' values , checking and dropping duplicate values, after that spliting the data set into train and test set storing these data sets in artifact directory data ingeastion folder , at last it returns whole data setr , train dataset and test dataset paths . 

11.data ingestion artifact file is used to hold the data ingestion component return values.

12.after completeing data ingestion componenet , next we need to create a data validation folder in artifact directory using data validation config file , it contains reeport.yaml file.

13. In data validation componenet , Dropping the columns in the dataset which have more tahn 30 percent , checking data drift , checkinhg is required columns exists , checking the client sended dataset columns , the serever side receve the same dataset or not , checking data drift for columns atr last it returns a yaml file which contains the information about the dataset.

14.Data transformation artifact returns a report yaml file which contains details about the data validation.

15.In data transformation config , create a data transformation folder in artifact directory , in this folder creating transformed path and transform train path and transform test paath.

16. Data transformtion compoinenet perform all preprocessing stps for example handling missing values , handling outliers, DScaling the dataset , featutre transformation, creating new features form existing features , label encoding for categorical target feature all the preprocessing will be done in data transformation componenet and it returns transformed path, transform train path , transform test path.

17. data transformation artifact holds the transfomed and transformer train and test path.

18. Model building componenet we build a model that best for given data set and it returs model object.

19.Mode3l evaluation componenet check and evaluation of the model checking the model is over fitted or underfitted like wise.

20. In real world cases the dataset is not constant the data change sover the time , so for new data the model accuracy is increases or decreases , so in model pusher componenet we check the accuracy score for both current train model anmd previous train model , if currently train model better than the previously trained model thgen we can pass current model as object, else we can place previous model a smodel object.

21.In pipeline folder we can create training pipeline and batch prediction pipeline , training pipeline is used to train the model and batch prediction pipeline is udsed to predictrion of data set.

22. It is possible to predict a batch of file or a single value , In batch prediction we can pass a mpore number of values in single prediction we pass a single value . In most cases we use batch prediction.

23. It is possible to store models in a folder like saved models and predictions in predictions folder.