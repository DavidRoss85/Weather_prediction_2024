from src.model.g_naive_bayes import NaiveBayesModel
from src.model.structures import *
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

print("Check")
m=NaiveBayesModel()

m.import_data("../data/fake_data.csv")
d=DataSet()
d.features=m.get_data()[['Temperature', 'Humidity', 'Precipitation']]
d.labels=m.get_data()['Date']
d.threshold=0
d.input_ranges=[Range(70,75),Range(30,50),Range(0,5)]

m.train_model(d)

nd=m.run_prediction(d)
nd.gaussify()


plt.plot(nd.x_values,nd.y_values)
plt.fill_between(nd.x_values,nd.y_values,color="green",alpha=.2)

plt.show()

print("DONE")