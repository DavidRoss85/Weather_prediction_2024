
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from src.model.structures import DataSet,Range


#Steps to running model
#   Import dataset
#   drop uneccessary columns - data=data.drop(columns=['']
#   Encode Columns with non number values data['']=data[''].astype('category').cat.codes
#   select features x=data[['','','']] y=['']
#   split into train and test, fortunately train_test_split does this:
#       X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
#   Train the model:
#       model=GaussianNB(), model.fit(X_train.values,y_train

class NaiveBayesModel:
    """
    First import the data using a Dataset object found in the structures.py
    Train model with train_model method and pass in the dataset
    Finally run_prediction. The returned value is a new dataset with chartable data
    """
    def __init__(self):
        self.__data_filename=None
        self.__data=None
        self.__data_sets=dict() #Stores all of the datasets
        self.__model=GaussianNB()   #sklearn GNB class
        self.__model_trained=False  #tracks if training has occurred


    def reset_model(self):
        """
        Resets the model to initial conditions
        :return:
        """
        self.__data_filename=None
        self.__data=None
        self.__data_sets=dict()
        self.__model=GaussianNB()
        self.__model_trained=False

    ##################################################################################################
    def add_dataset(self,key,dataset:DataSet):
        """
        Allows the saving and retrieval of multiple datasets
        :param key: Reference
        :param dataset: Dataset object
        :return:
        """
        self.__data_sets[key]=dataset
        self.__show_message(f"Dataset: {dataset.name} added")

    ##################################################################################################
    def train_model(self, dataset:DataSet,test_size=0.3,random_state=40):
        """
        Trains the model using provided data from the dataset
        :param dataset: Dataset object
        :param test_size: Size of test data vs training data
        :param random_state: Randomization
        :return:
        """
        if dataset.get_data() is None:
            self.__show_message("Data must be imported before training.")
            return

        # split data:
        x_train=0
        y_train=0
        x_test=0
        y_test=0
        try:
            x_train,x_test,y_train,y_test=train_test_split(
                dataset.get_features(),
                dataset.get_labels(),
                test_size=test_size,
                random_state=random_state
            )
        except ValueError as err:
            self.__handle_error(err,"Bad value passed to traiiner","train_model")


        #Train model
        self.__model.fit(x_train.values,y_train)

        self.__show_message("Model training successful")
        self.__model_trained=True

    ##################################################################################################
    def is_trained(self):
        return self.__model_trained
    ##################################################################################################
    def drop_data(self,category:str):
        """
        Call this method to drop a category from data to be processed
        :param category: Must match a title in the spreadsheet/data column
        :return:
        """
        if self.__data is not None:
            try:
                self.__data=self.__data.drop(columns=category)
                self.__show_message(f"{category} dropped")
            except Exception as err:
                self.__handle_error(err,f"Could not drop data category {category}","drop_data")

    ##################################################################################################
    def run_prediction(self,dataset:DataSet)->DataSet:
        """
        Performs prediction based on provided dataset
        :param dataset: Dataset object
        :return: new dataset with predictions
        """
        # Approx 11,027 per minute
        # multiply instructions by 0.0054409662487301 to get estimated seconds
        if not self.__model_trained:
            self.train_model(dataset)
        print("Prediction running")
        #Recursive function: O(i*n)
        dataset=self.__recursive_predict(dataset,dataset.input_ranges)
        return dataset

    ##################################################################################################
    def __recursive_predict(self,dataset:DataSet,all_ranges:list,pre_list:list=[])->DataSet:
        """
        Each variable must be calculated over a range of values.
        In the case where multiple variables have ranges, this recursion ensures that each
        combination is considered in the calculation
        :param dataset: Dataset object
        :param all_ranges: List of Range objects corresponding to each feature in the dataset
        :param pre_list: Used for recursion
        :return:
        """
        #Copy list of ranges
        ranges_copy = all_ranges.copy()
        #Grab first range in list:
        current_range = ranges_copy.pop(0)

        #While loop is used to handle floating point loops
        i=current_range.low
        #Cycle through the entire range
        while i < current_range.high:
            i+=current_range.step
            #Copy the recursive list passed in
            new_data = pre_list.copy()
            #Add the value of i to the end of the list
            new_data.append(i)

            #If there are still ranges in the list do recursion
            if len(ranges_copy) > 0:
                #Recursion
                self.__recursive_predict(dataset,ranges_copy, new_data)
            else:
                #If new_data has 1 number for each range, perform calculation:
                dataset.input_data=new_data
                dataset=self.__make_prediction(dataset)

        return dataset

    ##################################################################################################
    def __make_prediction(self,dataset:DataSet)->DataSet:
        """
        Takes a dataset and makes a prediction using the Naive Bayes Model
        Output is saved in the Dataset
        :param dataset: Dataset object
        :return: New Dataset
        """
        #This is the prior distribution curve saved to the dataset:
        #Nested list [[<Julian day>,<Sum of probabilities>, <Count of probabilities>]]
        #The prob. sum is divided by prob. count to give the average
        all_conditions=dataset.get_probability_dist()

        #Get the input data to make prediction
        new_data = dataset.input_data  # Example [Temperature, Humidity, SoilCondition]
        #Threshold can be controlled to only display meaningful values
        threshold=dataset.threshold

        #Makes a probability distribution in the form of a list:
        probabilities = self.__model.predict_proba([new_data])

        #Initialize new conditions list
        new_conditions = []

        #Cycles through the values in the new distribution and adds it to the new list
        # if it surpasses the threshold requirements:
        #self.__model.classes_[i] holds the julian day value associated with each prob
        for i, prob in enumerate(probabilities[0]):
            if prob >= threshold:
                new_conditions.append([self.__model.classes_[i], prob])

        #Compare each julian day/probability pair...
        #Increment the count if found, else add to list:
        for new_day, new_prob in new_conditions:
            day_found = False
            if len(all_conditions) > 0:
                for i in range(len(all_conditions)):
                    if new_day == all_conditions[i][0]:
                        all_conditions[i][1] += new_prob
                        all_conditions[i][2] += 1
                        day_found = True
                        break
            if not day_found:
                all_conditions.append([new_day, new_prob, 1])

        #Save the new distribution to the dataset:
        dataset.set_probability_dist(all_conditions)
        # Sort dataset by day:
        dataset.sort_probability_dist()

        #Return new dataset (Technically not necessary since lists are passed by ref)
        return dataset

    ##################################################################################################
    def __handle_error(self,err,msg:str=None,entry:str=None):
        print(f"Error{(' in '+ entry) if not None else ''}:\n"
              f"\t{msg}\n\t{err}")

    ##################################################################################################
    def __show_message(self,msg:str=""):
        print(msg)
