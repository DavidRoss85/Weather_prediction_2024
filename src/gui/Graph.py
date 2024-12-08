import matplotlib.pyplot as plt
from src.model.structures import Graph


class GraphGUI:
    """
    Class for plotting data
    """
    def __init__(self,name="",x_label="",y_label=""):
        self.name=name  #name of graph (Displayed in the legend)
        self.__plt=plt  #matplot lib
        self.graph_list=dict()  #List of all the graphs referenced by name
        self.__x_label=x_label  #X axis label
        self.__y_label=y_label  #Y axis label


    def show(self):
        """
        Cycle through all graphs and plot with varying colors
        :return:
        """
        if len(self.graph_list)==0: return  #Exit if no graphs in dictionary

        #Plot each graph in dictionary:
        for graph in self.graph_list.values():
            self.__plt.plot(graph.x_values,graph.y_values,color=graph.line_color)
            self.__plt.fill_between(graph.x_values,graph.y_values,0,color=graph.fill_color,alpha=graph.alpha,label=graph.name)

        #Set chart properties:
        plt.legend(loc="upper center")
        plt.title(self.name)
        plt.ylabel(self.__y_label)
        plt.xlabel(self.__x_label)

        #Display chart
        self.__plt.show()

    def add_graph(self,graph:Graph):
        """
        Add a graph to the list of charts to be drawn. Must be done before calling the show routine
        :param graph: A graph object used to draw on the chart
        :return:
        """
        self.graph_list[graph.name]=graph

    def delete_graph(self,name):
        """
        Remove a graph from the dictionary lis
        :param name: Key reference to the graph
        :return:
        """
        if name in self.graph_list:
            del self.graph_list[name]