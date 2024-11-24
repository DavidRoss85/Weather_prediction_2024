import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

import time
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


# Step 1: Load the dataset
data = pd.read_csv('../data/fake_data.csv')

# Step 2: Preprocess the data
# Drop 'Date' column if it's not relevant for prediction
# data = data.drop(columns=['Date'])

# Encode categorical columns like 'Condition' and 'SoilCondition'
# data['Condition'] = data['Condition'].astype('category').cat.codes
# data['SoilCondition'] = data['SoilCondition'].astype('category').cat.codes

# Step 3: Separate features (X) and target labels (y)
X = data[['Temperature', 'Humidity', 'Precipitation']]
y = data['Date']

X2 = data[['Temperature']]

# Step 4: Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
X_train2, X_test2, y_train2, y_test2 = train_test_split(X2, y, test_size=0.3, random_state=42)

# Step 5: Initialize and train the Naive Bayes model
model = GaussianNB()
model.fit(X_train.values, y_train)

model2 = GaussianNB()
model2.fit(X_train2.values, y_train2)

# Step 6: Make predictions and evaluate accuracy
# predictions = model.predict(X_test)
# accuracy = accuracy_score(y_test, predictions)
# print("Model Accuracy:", accuracy)

# Example of predicting with new data
# new_data = [[200, 100, 500]]  # Example input for [Temperature, Humidity, SoilCondition]
# predicted_condition = model.predict(new_data)
# print("Predicted Condition:", predicted_condition)
#
#
# #___________________________________________________________________________________________
# # Example input data

# Get probabilities for each possible 'Condition' outcome

# Define a probability threshold
threshold =0

# Get the indices of the possible conditions that meet the threshold

# possible_conditions = [(model.classes_[i], prob) for i, prob in enumerate(probabilities[0]) if prob >= threshold]
start_time = time.time()  # Current time in seconds since the Epoch
formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
print(f"started: {formatted_time}")

#Approx 11,027 per minute
#multiply instructions by 0.0054409662487301 to get estimated seconds
all_conditions=[]
for temp_range in range(60,90):
    for humidity_range in range (30,50):
        for precipitation_range in range (5,10):

            new_data = [[temp_range,humidity_range,precipitation_range]]  # Example [Temperature, Humidity, SoilCondition]

            probabilities = model.predict_proba(new_data)

            new_conditions=[]
            for i, prob in enumerate(probabilities[0]):
                if prob>=threshold:
                    new_conditions.append([model.classes_[i],prob])
            for new_day, new_prob in new_conditions:
                day_found=False
                if len(all_conditions)>0:
                    # print(f"all conditions: {all_conditions}")
                    for i in range(len(all_conditions)):
                        if new_day==all_conditions[i][0]:
                            all_conditions[i][1]+=new_prob
                            all_conditions[i][2]+=1
                            day_found=True
                            break
                if not day_found:
                    all_conditions.append([new_day,new_prob,1])


all_conditions.sort(key=lambda item:item[0])

temp_conditions=[]
for temp_range in range(60,90):

    new_data2 = [[temp_range]]  # Example [Temperature, Humidity, SoilCondition]

    probabilities = model2.predict_proba(new_data2)

    new_conditions=[]
    for i, prob in enumerate(probabilities[0]):
        if prob>=threshold:
            new_conditions.append([model2.classes_[i],prob])
    for new_day, new_prob in new_conditions:
        day_found=False
        if len(temp_conditions)>0:
            # print(f"all conditions: {all_conditions}")
            for i in range(len(temp_conditions)):
                if new_day==temp_conditions[i][0]:
                    temp_conditions[i][1]+=new_prob
                    temp_conditions[i][2]+=1
                    day_found=True
                    break
        if not day_found:
            temp_conditions.append([new_day,new_prob,1])


temp_conditions.sort(key=lambda item:item[0])



# Print out the range of possible weather conditions and their probabilities
# print("OUTPUT 1:")
# print("Possible weather conditions within the threshold range:")
# for condition, prob in possible_conditions:
#     print(f"Condition: {condition}, Probability: {prob:.2f}")

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

graph_probs2=[]
graph_names2=[]
for condition, prob,count in temp_conditions:
    adjusted_prob=prob/count*1000
    graph_probs2.append(adjusted_prob)
    graph_names2.append(condition)
    # print(f"Condition: {condition}, Probability: {adjusted_prob:.2f}")

gauss_probs2=gaussian_filter1d(graph_probs2,sigma=sig)




plt.plot(graph_names,gauss_probs)
plt.fill_between(graph_names,gauss_probs,color="green",alpha=.2)

plt.plot(graph_names2,gauss_probs2)
plt.fill_between(graph_names2,gauss_probs2,color="red",alpha=.2)

plt.ylabel("Probability")
plt.xlabel("Day of year")

end_time = time.time()  # Current time in seconds since the Epoch
formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time))
print(f"Ended: {formatted_time}")
print(f"Time Taken: {(end_time-start_time)/60:.2f} minutes")
plt.show()
#_____________
#2

# Define a range of temperatures
# temperature_range = range(70, 80, 2)  # Example range from 70 to 78 in increments of 2
# humidity = 65
# soil_condition = 2
#
# # Generate predictions for each temperature in the range
# for temp in temperature_range:
#     data_point = [[temp, humidity, soil_condition]]
#     predicted_condition = model.predict(data_point)
#     print(f"Temperature: {temp} -> Predicted Condition: {predicted_condition[0]}")