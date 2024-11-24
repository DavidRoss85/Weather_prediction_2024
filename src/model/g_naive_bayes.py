import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

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
    def __init__(self):
        self.__data_filename=None
        self.__data=None
        self.__data_sets=dict() #Stores all of the datasets
        self.__model=GaussianNB()
        self.__model_trained=False



    ##################################################################################################
    def set_dataset(self,key,dataset:DataSet):
        self.__data_sets[key]=dataset
        self.__show_message(f"Dataset: {dataset.name} added")

    ##################################################################################################
    def train_model(self, dataset:DataSet,test_size=0.3,random_state=40):
        if dataset.get_data() is None:
            self.__show_message("Data must be imported before training.")
            return

        # split data:
        x_train,xtest,y_train,y_test=train_test_split(
            dataset.get_features(),
            dataset.get_labels(),
            test_size=test_size,
            random_state=random_state
        )
        self.__model.fit(x_train.values,y_train)

        self.__show_message("Model training successful")
        self.__model_trained=True

    ##################################################################################################
    def drop_data(self,category:str):
        if self.__data is not None:
            try:
                self.__data=self.__data.drop(columns=category)
                self.__show_message(f"{category} dropped")
            except Exception as err:
                self.__handle_error(err,f"Could not drop data category {category}","drop_data")

    ##################################################################################################
    def run_prediction(self,dataset:DataSet)->DataSet:
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
        ranges_copy = all_ranges.copy()
        current_range = ranges_copy.pop(0)

        for i in range(current_range.low, current_range.high + 1):
            new_data = pre_list.copy()
            new_data.append(i)
            if len(ranges_copy) > 0:
                self.__recursive_predict(dataset,ranges_copy, new_data)
            else:
                dataset.input_data=new_data
                dataset=self.__make_prediction(dataset)

        return dataset

    ##################################################################################################
    def __make_prediction(self,dataset:DataSet)->DataSet:
        #MEAT AND POTATOES:
        all_conditions=dataset.get_probability_dist()
        new_data = dataset.input_data  # Example [Temperature, Humidity, SoilCondition]
        threshold=dataset.threshold

        probabilities = self.__model.predict_proba([new_data])
        new_conditions = []
        for i, prob in enumerate(probabilities[0]):
            if prob >= threshold:
                new_conditions.append([self.__model.classes_[i], prob])
        for new_day, new_prob in new_conditions:
            day_found = False
            if len(all_conditions) > 0:
                # print(f"all conditions: {all_conditions}")
                for i in range(len(all_conditions)):
                    if new_day == all_conditions[i][0]:
                        all_conditions[i][1] += new_prob
                        all_conditions[i][2] += 1
                        day_found = True
                        break
            if not day_found:
                all_conditions.append([new_day, new_prob, 1])
        dataset.set_probability_dist(all_conditions)
        # Sort dataset by day:
        dataset.sort_probability_dist()
        return dataset

    ##################################################################################################
    def __handle_error(self,err,msg:str=None,entry:str=None):
        print(f"Error{(' in '+ entry) if not None else ''}:\n"
              f"\t{msg}\n\t{err}")

    ##################################################################################################
    def __show_message(self,msg:str=""):
        print(msg)
