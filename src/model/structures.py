# ------------------------DataSet----------------------------------
from scipy.ndimage import gaussian_filter1d


class DataSet:
    def __init__(self):
        self.name = None
        self.features = []
        self.labels = []
        self.threshold = 0
        self.probability_dist = [] #all_conditions
        self.input_data = []
        self.input_ranges=[]
        self.y_values=[]
        self.x_values=[]
        self.scale = 1

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