import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

from src.model.structures import Graph


class GraphGUI():
    def __init__(self,name="",x_label="",y_label=""):
        self.name=name
        self.__plt=plt
        self.graph_list=dict()
        self.__x_label=x_label
        self.__y_label=y_label


    def show(self):
        if len(self.graph_list)==0: return

        for graph in self.graph_list.values():
            self.__plt.plot(graph.x_values,graph.y_values,color=graph.line_color)
            self.__plt.fill_between(graph.x_values,graph.y_values,0,color=graph.fill_color,alpha=graph.alpha,label=graph.name)

        plt.legend(loc="upper center")
        plt.title(self.name)
        plt.ylabel(self.__y_label)
        plt.xlabel(self.__x_label)

        self.__plt.show()

    def add_graph(self,graph:Graph):
        self.graph_list[graph.name]=graph

    def delete_graph(self,name):
        if name in self.graph_list:
            del self.graph_list[name]