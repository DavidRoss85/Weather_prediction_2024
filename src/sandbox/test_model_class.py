from src.gui.Graph import GraphGUI
from src.model.g_naive_bayes import NaiveBayesModel
from src.model.structures import *
import matplotlib.pyplot as plt

print("Check")
m=NaiveBayesModel()

d=DataSet("Warm months","../data/fake_data.csv")
d.set_features(['Temperature', 'Humidity', 'Precipitation'])
d.set_labels('Date')
d.threshold=0
d.input_ranges=[Range(70,75),Range(30,50),Range(0,5)]
d.set_graph_color("black","red")

d2=DataSet("Cold Months","../data/fake_data.csv")
d2.set_features(['Temperature', 'Humidity', 'Precipitation'])
d2.set_labels('Date')
d2threshold=0
d2.input_ranges=[Range(20,35),Range(30,50),Range(0,5)]
d2.set_graph_color("black","blue")

m.train_model(d)

d=m.run_prediction(d)
d2=m.run_prediction(d2)

d.gaussify()
d2.gaussify()

g=GraphGUI("Weather","day of year","Likelihood")
g.add_graph(d.graph)
g.add_graph(d2.graph)
g.show()

# plt.show()
# plt.plot(d.graph.x_values,d.graph.y_values)
# plt.fill_between(d.graph.x_values,d.graph.y_values,color="green",alpha=.2)

plt.show()

print("DONE")