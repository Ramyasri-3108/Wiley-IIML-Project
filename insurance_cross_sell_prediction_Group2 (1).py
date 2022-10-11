# -*- coding: utf-8 -*-
"""Insurance cross-sell prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1f1a7fcRFEh8m-02kWRywXAB67NVqHe8l
"""

from google.colab import files
upload = files.upload()

# Commented out IPython magic to ensure Python compatibility.
# Import libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline

df=pd.read_csv("G1&2_Project_Insurance_crosssell.csv")

df.head()

"""Observation:
1. id column can be dropped.
2. Demographic information: Gender, Age, Region_Code
3. Vehicle information: Vehicle_Age, Vehicle_Damage, Annual_Premium
4. Policy Information: Policy_Sales_Channel

"""

df.shape

df.columns

"""Response - Target/Dependent Variable"""

# Check data types of variables
df.dtypes

"""observation: Gender, Vehicle_Age and Vehicle_Damage are categorical variables.
(DT is string)
"""

# check if dataset is balanced or not
response_count=df['Response'].value_counts().reset_index()
print(response_count)
sns.barplot(x='index', y='Response',data=response_count)

"""observation:
1. The Dataset is imbalanced
2. The Number of records with Response '0' i.e customers not interested in Health insurance is more
3. This will cause ML model biased to predict the 'Response' to be 0
"""

df.describe()

"""Observation:
At least 50% of customers don't have Insurance
"""

df['Age'].corr(df['Region_Code'])

# To get number of unique values of each variable
df.nunique()

df['Gender'].unique()

df['Driving_License'].unique()

df['Vehicle_Age'].unique()

df['Previously_Insured'].unique()

df['Vehicle_Damage'].unique()

df['Response'].unique()

df['Policy_Sales_Channel'].unique()

df['Region_Code'].unique()

# Age and Annual_Permium stats
df[["Age","Annual_Premium"]].describe()

"""Inference: Atleast 75% of customers are below the age of 50

# Data Preparation and Cleaning
"""

# check for missing values
df.isnull().sum()

"""observation: No missing values."""

# check for duplicate entries in the dataset
columns=df.columns
print(columns)
duplicates=df[df.duplicated(subset=columns[:])]

duplicates.sum()

"""observation: No duplicate entries."""

df.skew()



# check for ouliers
df.id.plot(kind='box')

df.Age.plot(kind='box')

df.Annual_Premium.plot(kind='box')

df.shape

"""# Exploratory Data Analysis

Univariate Analysis
"""

# Univariate Analysis
categorical_vars=['Gender', 'Vehicle_Age', 'Vehicle_Damage','Driving_License','Previously_Insured']
for var in categorical_vars:
  plt.figure(figsize=(6,4))
  sns.set_style('whitegrid')
  sns.countplot(x=var,data=df,hue='Response')

# Variables with more categories eg: 'Policy_Sales_Channel','Region_Code'
plt.figure(figsize=(15,4))
sns.set_style('whitegrid')
sns.histplot(x='Policy_Sales_Channel',data=df,hue='Response')
plt.figure(figsize=(15,4))
sns.set_style('whitegrid')
sns.histplot(x='Region_Code',data=df,hue='Response')

"""Observation:
1. Male customers are more
2. Majority of the customers are with Vehicle age between 1-2 yrs followed by Vehicles of age less than a year
3. There is no significance of Driving_License in response to the purchase of vehicle insurance.
4. Driving_License can be dropped due to imbalanced ratio of labels.
5. Customers who are previously insured don't have interest to buy insurance again.
6. There are only a few widely used Policy_Sales_Channels.

"""

numerical_vars=['Age','Annual_Premium','Vintage']
for var in numerical_vars:
  plt.figure(figsize=(8,4))
  sns.distplot(df[var])

"""Observation:

1. Age has skewed distribution, majority of customers are of middle-aged between 30 to 50 years
2. High peak at customers of age around 25 years
3. Vehicle Annual Premium is < 1,00,000
4. Vintage has uniform disttribution

Bivariate Analysis
"""

# Bivariate Analysis
sns.boxplot(x='Gender',y='Age',hue='Response',data=df)

"""observation: Female customers of age between 35 to 50 show more interest """

# Numeric vs Numeric - scatterplot
# Numeric vs Categorical - continuous probability density function - distplot
# Categorical vs Categorical - discrete probability density function - barplot

numerical_vars=['Age','Annual_Premium','Vintage']
for var in numerical_vars:
  plt.figure(figsize=(10,4))
  sns.displot(df,x=var,hue='Response',bins=10,multiple="dodge",kde=True)

"""Observation: 
1. Probability density of customers of age 30-50 years not showing interest towards health insurance is more.
2. Vintage column can be dropped as the data is uniformly distributed.
3. Customers with Vehicle Annual Premium between 5Lakh to 10Lakh show interest towards Health Insurance, but this can also be dropped as per the correlation matrix 
3. Widely used policy sales channel are between for customers showing interest towards Health Insurance are between 20 to 35, 120 to 135, 150 to 160


"""

plt.figure(figsize=(10,4))
df.plot.scatter('Age','Annual_Premium')

sns.displot(df,x='Age',hue='Vehicle_Age',bins=10,multiple="dodge",kde=True)

"""Inference: Customers of age 20 to around 35 years are using new vehicles"""

sns.displot(df,x='Age',hue='Vehicle_Damage',kde=True)

"""Inference: Distribution of customers with middle age who does vehicle damage is more"""

# Categorical vs Categorical

#categorical_vars=['Gender', 'Vehicle_Age', 'Vehicle_Damage','Driving_License','Previously_Insured','Response']
# Gender vs Response
pivot=pd.crosstab(df.Gender,df.Response,margins=True)
pivot

pivot[1]/pivot['All']

"""Observation: Male customers are 3% more who show interest to buy Insurance when compared to Female customers"""

# Vehicle_Age vs Response
pivot=pd.crosstab(df.Vehicle_Age,df.Response,margins=True)
pivot

pivot[1]/pivot['All']

"""Observation:
1. 29% of customers with vehicle age > 2 years show more interest to buy Insurance
"""

# Vehicle_Damage vs Response
pivot=pd.crosstab(df.Vehicle_Damage,df.Response,margins=True)
pivot

pivot[1]/pivot['All']

"""Observation: Customers with vehicles that are previously damaged show interest to buy insurance.
Vehicle_Damage More significant variable 
"""

# Driving_License vs Response
pivot=pd.crosstab(df.Driving_License,df.Response,margins=True)
pivot

pivot[1]/pivot['All']

"""Observation: 12% of customers who possess driving license show interest to buy  Insurance"""

# Previously Insured vs Response
pivot=pd.crosstab(df.Previously_Insured,df.Response,margins=True)
pivot

pivot[1]/pivot['All']

"""Observation: Customers who are previously insured don't have insterest to buy  Insurance again"""

df.head()

plt.figure(figsize=(12,8))
sns.heatmap(df.corr(),annot=True)
plt.show()

"""Important Features:
1. Age
2. Vehicle_Age
3. Vehicle_Damage
4. Policy_Sales_Channel 


Dropped Features:
1. Id
2. Gender
3. Previously_Insured
4. Driving_License
5. Region_Code
6. Vintage
7. Annual_Premium

# Feature pre-processing
"""

df=df.drop(columns=['id','Gender','Driving_License','Previously_Insured','Region_Code','Vintage','Annual_Premium'])
x=df[['Age','Vehicle_Age','Vehicle_Damage','Policy_Sales_Channel']]
y=df.Response
print(x.shape,y.shape)

x.head()

x.info()

x.nunique()

"""### Encoding Policy_Sales_Channel feature"""

top_20_policy_sales_channels=x.Policy_Sales_Channel.value_counts().sort_values(ascending=False).reset_index().head(20)

print(top_20_policy_sales_channels)

top_20_policy_sales_channels=x.Policy_Sales_Channel.value_counts().sort_values(ascending=False).head(20).index

print(top_20_policy_sales_channels)

# Feature pre-processing for widely used policy sales channel
tmp_df = pd.DataFrame()
for channel in top_20_policy_sales_channels:
  tmp_df[channel] = np.where(x['Policy_Sales_Channel']==channel,1,0)
tmp_df[top_20_policy_sales_channels]
tmp_df=tmp_df.add_prefix('Policy_Sales_Channel_')

tmp_df

# join to previous dataframe after feature encoding of Policy_Sales_Channel
x=x.join(tmp_df)

x.columns

# drop Policy_Sales_Channel after encoding
x=x.drop(columns=['Policy_Sales_Channel'])

x.head()

"""Encoding Vehicle_Damage Feature using LabelEncoder()"""

from sklearn import preprocessing
le = preprocessing.LabelEncoder()
#x.Gender=le.fit_transform(x.Gender)
x.Vehicle_Damage=le.fit_transform(x.Vehicle_Damage)
x.head()

"""Encoding Vehicle_Age using OneHotEnoder()"""

from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.compose import ColumnTransformer
#preprocessor = ColumnTransformer([('ohe',OneHotEncoder(drop='first'),[3])],remainder='passthrough')
preprocessor = ColumnTransformer([('ohe',OneHotEncoder(drop='first'),[1])],remainder='passthrough')
x = preprocessor.fit_transform(x)

final_df=pd.DataFrame(x)

final_df.head()

"""Splitting into Train, Test Data"""

# Splitting Data into Train, Test Data
from sklearn.model_selection import train_test_split
xtrain,xtest,ytrain,ytest=train_test_split(x,y,test_size=0.2)
print(xtrain.shape, xtest.shape)
print(ytrain.shape, ytest.shape)

"""### Model Building"""

# Logistic Regression
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(xtrain,ytrain)

ypredict = model.predict(xtest)

len(ypredict)
b=np.where(ypredict==1)
b

"""Observation: Model didn't predict any customers with class 1 (customers who are interested to buy insurance)"""

ypredict=model.predict(xtest)
from sklearn import metrics
print("Logistic Regression: ")
print("Accuracy: ",metrics.accuracy_score(ytest,ypredict))
print("Recall: ",metrics.recall_score(ytest,ypredict))
print("F1-Score: ",metrics.f1_score(ytest,ypredict))
print("Confusion Matrix: ",metrics.confusion_matrix(ytest,ypredict))

"""Recall is 0 - Bad Model for prediction

# Handling Imbalanced Dataset
"""

df=pd.read_csv("G1&2_Project_Insurance_crosssell.csv")

#df=df.drop(columns=['Gender','id','Driving_License','Previously_Insured','Region_Code','Vintage','Policy_Sales_Channel'])
x=df[['Age','Vehicle_Age','Vehicle_Damage','Policy_Sales_Channel']]
y=df.Response
print(x.shape,y.shape)

x.head()

# Feature pre-processing of Policy_Sales_Channel
top_20_policy_sales_channels=x.Policy_Sales_Channel.value_counts().sort_values(ascending=False).head(20).index

top_20_policy_sales_channels

# Feature encoding for widely used policy sales channel
tmp_df = pd.DataFrame()
for channel in top_20_policy_sales_channels:
  tmp_df[channel] = np.where(x['Policy_Sales_Channel']==channel,1,0)
tmp_df[top_20_policy_sales_channels]
tmp_df=tmp_df.add_prefix('Policy_Sales_Channel_')

tmp_df

x=x.join(tmp_df)

x=x.drop(columns=['Policy_Sales_Channel'])

x.head()

# Encoding Vehicle_Damage Feature
from sklearn import preprocessing
le = preprocessing.LabelEncoder()
#x.Gender=le.fit_transform(x.Gender)
x.Vehicle_Damage=le.fit_transform(x.Vehicle_Damage)
x.head()

# Encoding Vehicle_Age
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.compose import ColumnTransformer
preprocessor = ColumnTransformer([('ohe',OneHotEncoder(drop='first'),[1])],remainder='passthrough')
x = preprocessor.fit_transform(x)

final_df=pd.DataFrame(x)

final_df.head()

"""Splitting into Train,Test Data"""

from sklearn.model_selection import train_test_split
xtrain,xtest,ytrain,ytest=train_test_split(x,y,test_size=0.3)
print(xtrain.shape, xtest.shape)
print(ytrain.shape, ytest.shape)
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.30 ,random_state = 5)

from imblearn.over_sampling import SMOTE
smote = SMOTE()
x_balanced, y_balanced = smote.fit_resample(x, y)
x_train_balanced,x_test_balanced,y_train_balanced,y_test_balanced=train_test_split(x_balanced,y_balanced,test_size=0.3,random_state=5)

"""### Logistic Regression"""

# Logistic Regression
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(x_train_balanced,y_train_balanced)

ypredict = model.predict(x_test_balanced)

from sklearn import metrics
print("Logistic Regression: ")
print("Accuracy: ",metrics.accuracy_score(y_test_balanced,ypredict))
print("Recall: ",metrics.recall_score(y_test_balanced,ypredict))
print("F1-Score: ",metrics.f1_score(y_test_balanced,ypredict))
print("Confusion Matrix: ",metrics.confusion_matrix(y_test_balanced,ypredict))

"""### Decision Tree"""

from sklearn import tree

model3 = tree.DecisionTreeClassifier(criterion='gini')

# train the model using train data
model3.fit(x_train_balanced,y_train_balanced)

ypredict = model3.predict(x_test_balanced)

print("Accuracy: ",metrics.accuracy_score(y_test_balanced,ypredict))
print("Recall: ",metrics.recall_score(y_test_balanced,ypredict))
print("Precision: ",metrics.precision_score(y_test_balanced,ypredict))
print("F1 Score: ",metrics.f1_score(y_test_balanced,ypredict))
print("Confusion Matrix: ",metrics.confusion_matrix(y_test_balanced,ypredict))

from sklearn.model_selection import train_test_split,cross_val_score,KFold
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier

models=[]
models.append(('LogisticRegression',LogisticRegression(solver="liblinear", random_state=5)))
models.append(('DecisionTree',DecisionTreeClassifier(random_state=5)))
models.append(('RandomForest',RandomForestClassifier(random_state=5)))

results=[]
accuracies = []
recalls = []
names=[]
precisions= []
f1_scores=[]
for name,model in models:   
    kf=KFold(n_splits=5,shuffle=True,random_state=5)
    cv_score=cross_val_score(model,x_train_balanced,y_train_balanced,cv=kf,scoring='roc_auc',verbose=1)
    accuracy = cross_val_score(model,x_train_balanced,y_train_balanced,cv=kf,scoring='accuracy',verbose=1).mean()
    recall = cross_val_score(model,x_train_balanced,y_train_balanced,cv=kf,scoring='recall',verbose=1).mean()
    precision = cross_val_score(model,x_train_balanced,y_train_balanced,cv=kf,scoring='precision',verbose=1).mean()
    f1_score = cross_val_score(model,x_train_balanced,y_train_balanced,cv=kf,scoring='f1',verbose=1).mean()
    accuracies.append(accuracy)
    recalls.append(recall)
    precisions.append(precision)
    f1_scores.append(f1_score)
    results.append(cv_score)
    names.append(name)
    msg = "%s: Accuracy: %f , Recall: %f, F1-Score: %f ,Mean: %f , Std: (%f)" % (name, accuracy, recall, f1_score, cv_score.mean(), cv_score.std())
    print(msg)

#roc_curve

for name,model in models:
#     model = m['model'] # select the model
    model.fit(x_train_balanced, y_train_balanced) # train the model
    y_pred=model.predict(x_test_balanced) # predict the test data
# Compute False postive rate, and True positive rate
    fpr, tpr, thresholds = roc_curve(y_test_balanced, model.predict_proba(x_test_balanced)[:,1])
# Calculate Area under the curve to display on the plot
    auc =roc_auc_score(y_test_balanced,model.predict(x_test_balanced))
# Now, plot the computed values
    plt.plot(fpr, tpr, label='%s ROC (area = %0.2f)' % (name, auc))
# Custom settings for the plot 
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('1-Specificity(False Positive Rate)')
plt.ylabel('Sensitivity(True Positive Rate)')
plt.title('Receiver Operating Characteristic')
plt.legend(loc="lower right")
plt.show()   # Display

import matplotlib.pyplot as plt
  
X_axis = np.arange(len(names))

plt.bar(X_axis - 0.2, accuracies, 0.4, label = 'Accuracy')
plt.bar(X_axis + 0.2, recalls, 0.4, label = 'Recall')

plt.xticks(X_axis, names)
plt.xlabel("Classification Algorithms")
plt.ylabel("Values")
plt.title("Accuracy and Recall bar chart")
plt.legend()
plt.show()

