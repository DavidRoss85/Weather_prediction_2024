from unittest.mock import inplace

from fontTools.subset import subset
from scipy.ndimage import gaussian_filter1d
import pandas as pd

# ------------------------DataSet----------------------------------
class DataSet:
    """
    Dataset Structure used for the Naive Bayes model
    """
    def __init__(self,name:str="",filename:str=""):
        self.name = name    #Name
        self.__features = []    #Variables to compare against the labels, usually multiple
        self.__labels = []  #Usually the date, but can be any 1 variable
        self.threshold = 0  #Ignore values below ths
        self.__probability_dist = [] #Used to chart probability [<Julian day>,<Sum of probabilities>, <Count of probabilities>]
        self.__data_filename=filename   #Data file
        self.__data=None    #Processed dataset
        self.input_data = []    #Specific values to perform prediction. Corresponds to features
        self.input_ranges=[]    #Range of inputs to use for each feature
        self.graph=Graph(name,[],[])    #Used by graphUI for charting
        self.__scale = 1    #Scale the graph bigger or smaller
        self.__filled_nan=False #Tracks if nan values were replaced by the fill_nan_value
        self.__fill_nan_value=None  #Can be used to replace NaN values
        self.__dropped_nan=False    #Tracks if NaN values were dropped

        #Import data
        if filename != "" and filename is not None:
            self.import_data(filename)

    ##################################################################################################
    def is_empty(self):
        """
        Checks if resulting dataset is empty (Prevents bugs)
        :return:
        """
        return self.__data.empty

    ##################################################################################################
    def get_category_list(self,category):
        """
        Creates a list for each unique value in the category
        :param category: Column to look for values in data
        :return: List of values
        """
        cat_list=list()
        if self.__data is not None:
            cat_list=self.__data[category].unique().tolist()
        return cat_list

    ##################################################################################################
    def get_data(self):
        """
        :return: The dataset data
        """
        return self.__data
    ##################################################################################################
    def get_labels(self):
        return self.__labels
    ##################################################################################################
    def get_features(self):
        return self.__features
    ##################################################################################################
    def get_probability_dist(self):
        return self.__probability_dist
    ##################################################################################################
    def set_features(self,categories:list):
        self.__features=self.__data[categories]
    ##################################################################################################
    def set_labels(self,category:str):
        self.__labels=self.__data[category]
    ##################################################################################################
    def set_scale(self,size:float=1):
        self.__scale=size
    ##################################################################################################
    def set_graph_color(self,line_color="black",fill_color="green",alpha=.2):
        """
        Change graph properties
        :param line_color: Line Color
        :param fill_color: Fill Color
        :param alpha: Transparency levl
        :return:
        """
        self.graph.line_color=line_color
        self.graph.fill_color=fill_color
        self.graph.alpha=alpha
    ##################################################################################################
    def set_probability_dist(self,new_dist):
        """
        Saves the new probability distribution to the dataset
        :param new_dist: New distribution
        :return:
        """
        self.__probability_dist=new_dist
        graph_probs = []
        graph_names = []
        for condition, prob, count in new_dist:
            adjusted_prob = prob / count * self.__scale
            graph_probs.append(adjusted_prob)
            graph_names.append(condition)
        self.graph.x_values=graph_names
        self.graph.y_values=graph_probs

    ##################################################################################################

    def set_name(self,name):
        """
        Change name of dataset or graph
        :param name: String
        :return:
        """
        self.name=name
        self.graph.name=name
    ##################################################################################################
    def import_data(self, filename):
        """
        Import datasheet and process
        :param filename: File location
        :return:
        """
        self.__data_filename = filename
        try:
            self.__data = pd.read_csv(filename,low_memory=False)
            self.__filled_nan=False
            self.__fill_nan_value=None
            self.__dropped_nan=False
        except Exception as err:
            self.__handle_error(err, f"Could not import {filename}", "import_data")
    ##################################################################################################
    def get_dictionary_from_data(self,index_key):
        """
        Creates a dictionary from imported data
        :param index_key: Category that acts as the main dictionary key
        :return: Dictionary
        """
        return self.__data.set_index(index_key).to_dict(orient='index')
    ##################################################################################################
    def filter_data(self,category,value):
        """
        Filters the data to those that match criteria
        :param category: column to search
        :param value: value to search for
        :return: filtered list
        """
        data=self.__data[self.__data[category]==value]
        self.__data=data
        return data
    ##################################################################################################
    def drop_duplicates(self,criteria_list:list=None,sort_list:list=None):
        """
        Drop data that have duplicates in all fields in the criteria list. If no list specified, will match all items
        :param criteria_list: Each field to check for an exact match before discarding data
        :param sort_list: Ensures that items in the sorted list that contain data are favored over those that are empty or NaN
        :return:
        """
        if criteria_list is None:
            self.__data.drop_duplicates()
        else:
            by_list=sort_list if sort_list is not None else criteria_list
            sorted_data=self.sort_data(by_list)
            self.__data = sorted_data.drop_duplicates(subset=criteria_list,keep='first')

        self.__show_message("Duplicate rows dropped")
    ##################################################################################################
    def drop_data(self, category: str):
        """
        Drops a column from the dataset
        :param category: Column to discard
        :return:
        """
        if self.__data is not None:
            try:
                self.__data = self.__data.drop(columns=category)
                self.__show_message(f"{category} column dropped.")
            except Exception as err:
                self.__handle_error(err, f"Could not drop data category {category}", "drop_data")
    ##################################################################################################
    def sort_data(self,sort_criteria:list=None):
        """
        Sort dataset
        :param sort_criteria: by category
        :return:
        """
        if sort_criteria is None: return
        self.__data= self.__data.sort_values(by=sort_criteria, na_position='last')
        return self.__data
    ##################################################################################################
    def convert_dates_to_julian(self,date_col):
        """
        Converts dates to julian days
        :param date_col: Specifies which column contains the dates to be converted
        :return:
        """
        #Adds a new column 'DATE_t', stores the date time there, then replaces original date column with Julian day:
        self.__data[f"{date_col}_t"]=pd.to_datetime(self.__data[date_col])
        self.__data[date_col]=self.__data[f"{date_col}_t"].dt.dayofyear
        return self.__data

    ##################################################################################################
    def fill_nan_values(self,replacement):
        """
        Fill NaN values with specified value
        :param replacement: Value to replace NaN
        :return:
        """
        self.__filled_nan=True
        self.__fill_nan_value=replacement
        self.__data.fillna(replacement,inplace=True)

    ##################################################################################################
    def drop_nan_values(self,categories:list=None):
        """
        Drops rows containing NaN values in the specified columns
        :param categories: Columns to search for NaN values
        :return:
        """
        if categories is None or categories == []:
            self.__data.dropna(inplace=True)
        else:
            self.__data.dropna(subset=categories,inplace=True)

        self.__dropped_nan=True
    ##################################################################################################
    def replace_nan_using_avg(self,nan_category,categories:list):
        """
        Search a column for NaN values and use the average from other columns to fill missing value
        :param nan_category: Column to search for NaN values
        :param categories: Columns used to form an average for nan_category
        :return:
        """
        self.__data[nan_category] = self.__data.apply(
            lambda row: row[categories].mean(skipna=True)
            if pd.isna(row[nan_category]) else row[nan_category], axis=1
        )
    ##################################################################################################
    def sort_probability_dist(self):
        """
        Sort the probability distribution so that it plots properly on the chart
        :return:
        """
        self.__probability_dist.sort(key=lambda item: item[0])
        graph_probs = []
        graph_names = []
        for condition, prob, count in self.__probability_dist:
            adjusted_prob = prob / count * self.__scale
            graph_probs.append(adjusted_prob)
            graph_names.append(condition)
        self.graph.x_values = graph_names
        self.graph.y_values = graph_probs
    ##################################################################################################
    def gaussify(self,sigma=2):
        """
        Smoothens curve by adding a gaussian filter
        Cannot be undone once executed
        :param sigma: adjust curve strength
        :return:
        """
        if len(self.graph.y_values)==0: return  #Don't do anything if there are no values to gaussify
        self.graph.y_values=gaussian_filter1d(self.graph.y_values,sigma=sigma)

    ##################################################################################################
    def __handle_error(self, err, msg: str = None, entry: str = None):
        print(f"Error{(' in ' + entry) if not None else ''}:\n"
              f"\t{msg}\n\t{err}")
    ##################################################################################################
    def __show_message(self,msg:str=""):
        print(msg)




#------------------------Range----------------------------------------
class Range:
    """
    Object used to store ranges for dataset features
    """
    def __init__(self,low,high,step=1):
        self.low=low
        self.high=high
        self.step=step

#------------------------Graph----------------------------------------
class Graph:
    """
    Object for storing graph data
    """
    def __init__(self,name,x_values:list,y_values:list):
        self.x_values=x_values
        self.y_values=y_values
        self.name=name
        self.line_color="black"
        self.fill_color='green'
        self.alpha=0.2