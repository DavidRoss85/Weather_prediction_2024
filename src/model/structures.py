# ------------------------DataSet----------------------------------
from scipy.ndimage import gaussian_filter1d


class DataSet:
    def __init__(self):
        self.name = None
        self.features = []
        self.labels = []
        self.threshold = 0
        self.__probability_dist = [] #all_conditions
        self.input_data = []
        self.input_ranges=[]
        self.y_values=[]
        self.x_values=[]
        self.scale = 1

    def get_probability_dist(self):
        return self.__probability_dist

    def set_probability_dist(self,new_dist):
        self.__probability_dist=new_dist
        graph_probs = []
        graph_names = []
        for condition, prob, count in new_dist:
            adjusted_prob = prob / count * self.scale
            graph_probs.append(adjusted_prob)
            graph_names.append(condition)
        self.x_values=graph_names
        self.y_values=graph_probs

    def sort_probability_dist(self):
        self.__probability_dist.sort(key=lambda item: item[0])
        graph_probs = []
        graph_names = []
        for condition, prob, count in self.__probability_dist:
            adjusted_prob = prob / count * self.scale
            graph_probs.append(adjusted_prob)
            graph_names.append(condition)
        self.x_values = graph_names
        self.y_values = graph_probs

    def gaussify(self,sigma=2):
        """
        Smoothens curve by adding a gaussian filter
        Cannot be undone once executed
        :param sigma: adjust curve strength
        :return:
        """
        if len(self.y_values)==0: return  #Don't do anything if there are no values to gaussify
        self.y_values=gaussian_filter1d(self.y_values,sigma=sigma)

#------------------------Range----------------------------------------
class Range:
    def __init__(self,low,high):
        self.low=low
        self.high=high