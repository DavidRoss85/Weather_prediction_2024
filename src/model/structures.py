
from scipy.ndimage import gaussian_filter1d
import pandas as pd

# ------------------------DataSet----------------------------------
class DataSet:
    def __init__(self,name:str="",filename:str=""):
        self.name = name
        self.__features = []
        self.__labels = []
        self.threshold = 0
        self.__probability_dist = [] #all_conditions
        self.__data_filename=filename
        self.__data=None
        self.input_data = []
        self.input_ranges=[]
        self.graph=Graph(name,[],[])
        self.scale = 1
        if filename != "" and filename is not None:
            self.import_data(filename)

    ##################################################################################################
    def get_data(self):
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
    def set_graph_color(self,line_color="black",fill_color="green",alpha=.2):
        self.graph.line_color=line_color
        self.graph.fill_color=fill_color
        self.graph.alpha=alpha
    ##################################################################################################
    def set_probability_dist(self,new_dist):
        self.__probability_dist=new_dist
        graph_probs = []
        graph_names = []
        for condition, prob, count in new_dist:
            adjusted_prob = prob / count * self.scale
            graph_probs.append(adjusted_prob)
            graph_names.append(condition)
        self.graph.x_values=graph_names
        self.graph.y_values=graph_probs

    ##################################################################################################

    def import_data(self, filename):
        self.__data_filename = filename
        try:
            self.__data = pd.read_csv(filename)
        except Exception as err:
            self.__handle_error(err, f"Could not import {filename}", "import_data")

    ##################################################################################################
    def sort_probability_dist(self):
        self.__probability_dist.sort(key=lambda item: item[0])
        graph_probs = []
        graph_names = []
        for condition, prob, count in self.__probability_dist:
            adjusted_prob = prob / count * self.scale
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




#------------------------Range----------------------------------------
class Range:
    def __init__(self,low,high):
        self.low=low
        self.high=high

#------------------------Graph----------------------------------------
class Graph:
    def __init__(self,name,x_values:list,y_values:list):
        self.x_values=x_values
        self.y_values=y_values
        self.name=name
        self.line_color="black"
        self.fill_color='green'
        self.alpha=0.2