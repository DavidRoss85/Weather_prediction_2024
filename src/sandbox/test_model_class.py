from src.gui.Graph import GraphGUI
from src.model.g_naive_bayes import NaiveBayesModel
from src.model.structures import *
import matplotlib.pyplot as plt

print("Check")
m=NaiveBayesModel()

d=DataSet("Warm months","../data/final_combined_data.csv")
# d.filter_data('Temperature',80)

d.drop_data("SOURCE_FILE")
d.drop_data("VALUE")
d.drop_data('COMMODITY')
d.drop_duplicates()
d.drop_duplicates(['YEAR','COUNTY','DATE'],['TAVG','TMAX','TMIN','PRCP','AWND','SNOW'])
d.convert_dates_to_julian('DATE')
# d.filter_data('DATE',1)
d.sort_data(['YEAR'])
# d.fill_nan_values(20)
d.drop_nan_values(['PRCP'])

d.set_features(['PRCP'])
d.set_labels('DATE')
d.threshold=0
d.input_ranges=[Range(0,.3,.01)]
d.set_graph_color("black","red")


d2=DataSet("Cold Months","../data/final_combined_data.csv")

d2.drop_data("SOURCE_FILE")
d2.drop_data("VALUE")
d2.drop_data('COMMODITY')
d2.drop_duplicates()
d2.drop_duplicates(['YEAR','COUNTY','DATE'],['TAVG','TMAX','TMIN','PRCP','AWND','SNOW'])
d2.convert_dates_to_julian('DATE')
# d.filter_data('DATE',1)
d2.sort_data(['YEAR'])

# d2.fill_nan_values(-10)
d2.set_features(['PRCP'])
d2.set_labels('DATE')
d2threshold=0
d2.input_ranges=[Range(.3,1,.01)]
d2.set_graph_color("black","blue")


m.train_model(d)

d=m.run_prediction(d)
d2=m.run_prediction(d2)

d.gaussify()
d2.gaussify()

g=GraphGUI("Weather","day of year","Likelihood")
g.add_graph(d.graph)
g.add_graph(d2.graph)

# mmm= d.get_category_list("Nada")
# print(f"THE LIST: {mmm}")
g.show()
# plt.show()
# plt.plot(d.graph.x_values,d.graph.y_values)
# plt.fill_between(d.graph.x_values,d.graph.y_values,color="green",alpha=.2)

# plt.show()

print("DONE")