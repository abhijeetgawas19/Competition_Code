# -*- coding: utf-8 -*-
"""Machine_Learning_Competition.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WW-p2r4OjC3wZ6W6INqGFP0Im9fsWz8c

### HackerEarth Machine Learning Challenge: How to not Lose Customer in 10 Days

Link: https://www.hackerearth.com/challenges/competitive/hackerearth-machine-learning-challenge-predict-customer-churn/

**Problem Statement**: No business can thrive without it’s customers. On the flip side, customers leaving the business is a nightmare that every business owner dreads!

In fact, one of the key metrics to measure a business’ success is by measuring its customer churn rate - the lower the churn, the more loved the company is. 

Typically, every user of a product or a service is assigned a prediction value that estimates their state of churn at any given time. This value may be based on multiple factors such as the user’s demographic, their browsing behavior and historical purchase data, among other details.

This value factors in unique and proprietary predictions of how long a user will remain a customer and is updated every day for all users who have purchased at least one of the products/services. The values assigned are between 1 and 5.

**Task**: An up-and-coming startup is keen on reducing its customer churn and has hired you as a Machine Learning engineer for this task. As an expert, you are required to build a sophisticated Machine Learning model that predicts the churn score for a website based on multiple features.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

dataset = pd.read_csv("/content/drive/MyDrive/dataset/train.csv")

dataset.head()

len(dataset)

dataset.shape

dataset.describe()

dataset.churn_risk_score.value_counts()

"""**Data Cleaning**"""

# Find the Null Values
dataset.isnull().sum()

dataset.shape

# Fill the NA values rather than dropping it
for i in dataset.columns:
    if dataset[i].dtype=='float64':
        dataset[i]=dataset[i].fillna(dataset[i].mean())
    else:
        dataset[i]=dataset[i].fillna(method='ffill')

dataset.shape

dataset.isnull().sum()

# Dropping the unimportant features of table
dataset.head()

def columnGetter():
  column_names = []
  for cols in dataset.columns:
    column_names.append(cols)
  return column_names

cols_name = columnGetter()

for i in range(0,len(cols_name)):
  print(cols_name[i])

"""### Features Selections and Dropping Other Features"""

dataset.head()

dataset = dataset.drop(["customer_id","Name","security_no","referral_id","last_visit_time"],axis=1)

dataset.head()

dataset.isnull().sum()

dataset.shape

"""#### Gender"""

dataset.gender.unique()

dataset.gender.value_counts()

from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()

dataset.head()

dataset["gender"] = le.fit_transform(dataset.gender)

dataset["gender"]

dataset.head()

"""#### Region_Category"""

dataset.region_category.unique()

dataset["region_category"] = le.fit_transform(dataset.region_category)

dataset.head(20)

"""#### Membership Category"""

dataset["membership_category"].value_counts()

dataset.membership_category.unique()

dataset["membership_category"] = le.fit_transform(dataset.membership_category)

dataset.head()

dataset["membership_category"].value_counts()

"""#### Joining Date"""

dataset["joining_date"].value_counts()

dataset["joining_date"].unique()

#df = df.replace('-', '', regex=True).astype(int)
dataset["joining_date"] = dataset["joining_date"].replace("-",'',regex=True).astype(int)

dataset.head()

"""#### Joined Through Referral"""

dataset["joined_through_referral"].value_counts()

dataset = dataset[dataset["joined_through_referral"]!="?"]

dataset["joined_through_referral"].value_counts()

dataset["joined_through_referral"] = le.fit_transform(dataset["joined_through_referral"])

dataset.shape

dataset["joined_through_referral"].value_counts()

"""#### Preferred Offer Types"""

dataset.head()

dataset["preferred_offer_types"].unique()

dataset["preferred_offer_types"].value_counts()

dataset["preferred_offer_types"] = le.fit_transform(dataset["preferred_offer_types"])

dataset.head()

"""#### Medium of Operation"""

dataset["medium_of_operation"].unique()

dataset = dataset[dataset["medium_of_operation"]!="?"]

dataset["medium_of_operation"].unique()

dataset["medium_of_operation"].value_counts()

dataset["medium_of_operation"] = le.fit_transform(dataset["medium_of_operation"])

dataset["medium_of_operation"].unique()

dataset["medium_of_operation"].value_counts()

"""#### Internet"""

dataset.head()

dataset["internet_option"].unique()

dataset["internet_option"] = le.fit_transform(dataset["internet_option"])

dataset["internet_option"].unique()

dataset["internet_option"].value_counts()

"""#### Used Special Discount"""

dataset["used_special_discount"].value_counts()

dataset["used_special_discount"] = le.fit_transform(dataset["used_special_discount"])

dataset["used_special_discount"].value_counts()

dataset.head()

"""#### Offer Application Preference"""

dataset["offer_application_preference"].value_counts()

dataset["offer_application_preference"] = le.fit_transform(dataset["offer_application_preference"])

dataset["offer_application_preference"].value_counts()

"""#### Past Complaint"""

dataset["past_complaint"].value_counts()

dataset["past_complaint"] = le.fit_transform(dataset["past_complaint"])

dataset["past_complaint"].value_counts()

"""#### Complaint Status"""

dataset["complaint_status"].value_counts()

dataset["complaint_status"] = le.fit_transform(dataset["complaint_status"])

dataset["complaint_status"].value_counts()

dataset.head()

"""#### Feedback"""

dataset["feedback"].unique()

dataset["feedback"] = le.fit_transform(dataset["feedback"])

dataset.head()

"""#### Churn Risk Score"""

dataset["churn_risk_score"].value_counts()

dataset.shape

"""### Outlier Detection and Removal for numeric values

#### Days Since Last Login
"""

dataset.head()

dataset["days_since_last_login"].value_counts()

# Its seen that day_since_last_login can't be negative so remove those values
dataset = dataset[dataset["days_since_last_login"]!=-999]

dataset["days_since_last_login"].value_counts()

dataset.shape

dataset.head()

"""#### Average Time Spend"""

dataset["avg_time_spent"].value_counts()

# Again Average Spent Time can't be negative
dataset = dataset[dataset["avg_time_spent"]>=0]

dataset.shape

"""#### Average Transaction Value"""

print(dataset["avg_transaction_value"].value_counts())

dataset.head()

"""#### Average Frequency Login Days"""

dataset["avg_frequency_login_days"].value_counts()

# Remove the Error Keyword which is not suitable for numerical value
dataset = dataset[dataset["avg_frequency_login_days"]!="Error"]

dataset["avg_frequency_login_days"] = pd.to_numeric(dataset["avg_frequency_login_days"])

dataset.shape

"""#### Points in Wallet"""

dataset["points_in_wallet"].unique()

dataset.info()

"""### Machine Learning Implementation

#### Logisitic Regression
"""

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

X = dataset.drop(["churn_risk_score"],axis=1)
y = dataset["churn_risk_score"]

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.20,random_state=42)

modelLR = LogisticRegression(max_iter=10000)

modelLR.fit(X_train,y_train)

y_pred = modelLR.predict(X_test)

# Accuracy Score
modelLR.score(X_test,y_test)

# Classification Report
print(classification_report(y_test,y_pred))

# Confusion Matrix
print(confusion_matrix(y_test,y_pred))

"""#### Random Forest"""

from sklearn.ensemble import RandomForestClassifier

modelRF = RandomForestClassifier()

modelRF.fit(X_train,y_train)

y_pred = modelRF.predict(X_test)

# Accurracy Score
modelRF.score(X_test,y_test)

# Classification Report
print(classification_report(y_test,y_pred))

# Confusion Matrix
print(confusion_matrix(y_test,y_pred))

"""#### XGBoost"""

from xgboost import XGBClassifier

modelXGB = XGBClassifier()

modelXGB.fit(X_train,y_train)

y_pred = modelXGB.predict(X_test)

# Accurracy Score
modelXGB.score(X_test,y_test)

# Classification Report
print(classification_report(y_test,y_pred))

# Confusion Matrix
print(confusion_matrix(y_test,y_pred))

"""### Test Data and Submission File"""

test = pd.read_csv("/content/drive/MyDrive/dataset/test.csv",na_values=['?','-999','Error','xxxxxxxx'])
test_1 = pd.read_csv("/content/drive/MyDrive/dataset/test.csv")

test.head()

test = test.drop(["customer_id","Name","security_no","referral_id","last_visit_time"],axis=1)

test.head()

"""#### Encoded Some values in training set so doing same in test set"""

for i in test.columns:
   if test[i].dtype=='float64':
     test[i]=test[i].fillna(test[i].mean())
   else:
     test[i]=test[i].fillna(method='ffill')

test["region_category"] = test.region_category.apply(str)

test["joined_through_referral"] = test.joined_through_referral.apply(str)

test["gender"] = le.fit_transform(test.gender)
test["region_category"] = le.fit_transform(test["region_category"])
test["membership_category"] = le.fit_transform(test.membership_category)
test["joined_through_referral"] = le.fit_transform(test["joined_through_referral"])
test["preferred_offer_types"] = le.fit_transform(test["preferred_offer_types"])
test["medium_of_operation"] = le.fit_transform(test["medium_of_operation"])
test["internet_option"] = le.fit_transform(test["internet_option"])
test["used_special_discount"] = le.fit_transform(test["used_special_discount"])
test["offer_application_preference"] = le.fit_transform(test["offer_application_preference"])
test["past_complaint"] = le.fit_transform(test["past_complaint"])
test["complaint_status"] = le.fit_transform(test["complaint_status"])
test["feedback"] = le.fit_transform(test["feedback"])

test["joining_date"] = test["joining_date"].replace("-",'',regex=True).astype(int)

result = modelRF.predict(test)

# result

submission = pd.DataFrame({
   'customer_id': test_1['customer_id'],
   'churn_risk_score': result,
})

submission.to_csv('/content/drive/MyDrive/dataset/randomforestresults.csv', index=False)