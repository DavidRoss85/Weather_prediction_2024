from src.gui.Graph import GraphGUI
from src.model.g_naive_bayes import NaiveBayesModel
from src.model.structures import *
import matplotlib.pyplot as plt

print("Check")
m=NaiveBayesModel()

d=DataSet("Warm months","../data/final_combined_data.csv")
d.drop_data("SOURCE_FILE")
d.drop_data("VALUE")
d.drop_data('COMMODITY')
d.drop_duplicates()
d.drop_duplicates(['YEAR','COUNTY','DATE'],['TAVG','TMAX','TMIN','PRCP','AWND','SNOW'])
d.convert_dates_to_julian('DATE')
# d.filter_data('DATE',1)
d.sort_data(['YEAR'])
d.drop_nan_values(['TAVG', 'AWND', 'PRCP'])
x=d.get_category_list('COUNTY')
# d.fill_nan_values(-9999)
d.set_features(['TAVG', 'AWND', 'PRCP'])
d.set_labels('DATE')
d.threshold=0
d.input_ranges=[Range(70,75),Range(30,50),Range(0,5)]
d.set_graph_color("black","red")
# m.train_model(d)
print(f"{d.get_data()}")
print(x)