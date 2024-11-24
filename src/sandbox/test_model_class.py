from src.model.g_naive_bayes import NaiveBayesModel
from src.model.structures import *
import matplotlib.pyplot as plt


print("Check")
m=NaiveBayesModel()

m.import_data("../data/fake_data.csv")
d=DataSet()
d.features=m.get_data()[['Temperature', 'Humidity', 'Precipitation']]
d.labels=m.get_data()['Date']
d.threshold=0
d.input_ranges=[Range(70,75),Range(30,50),Range(0,5)]

# m.set_dataset("FirstData",d)
m.train_model(d)

nd=m.run_prediction(d)
all_conditions=nd.probability_dist

print("OUTPUT:")
print("Possible weather conditions within the threshold range:")
graph_probs=[]
graph_names=[]
for condition, prob,count in all_conditions:
    adjusted_prob=prob/count*1000
    graph_probs.append(adjusted_prob)
    graph_names.append(condition)
    # print(f"Condition: {condition}, Probability: {adjusted_prob:.2f}")

sig=2
gauss_probs=gaussian_filter1d(graph_probs,sigma=sig)

plt.plot(graph_names,gauss_probs)
plt.fill_between(graph_names,gauss_probs,color="green",alpha=.2)

print("DONE")