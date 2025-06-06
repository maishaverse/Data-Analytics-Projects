# -*- coding: utf-8 -*-
"""Final_Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1iWgbTo1yBMAeNo263b3TMbdRE3G3f4HR
"""

# Commented out IPython magic to ensure Python compatibility.
#Load Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns

#Load Dataset
dataset=pd.read_csv('wireless_churn.csv')
dataset.head()

#Show Key Statistics
dataset.describe()

!pip install ydata-profiling

#Create Profile Report

from ydata_profiling import ProfileReport
import pandas as pd

df = pd.read_csv('wireless_churn.csv')
profile = ProfileReport(df, title="wireless_churn")
profile.to_notebook_iframe()
profile.to_file("wireless_churn.html")

from sklearn.ensemble import IsolationForest
# Select the relevant features
features = df[['AccountWeeks', 'ContractRenewal', 'DataPlan', 'DataUsage', 'CustServCalls',
               'DayMins', 'DayCalls', 'MonthlyCharge', 'OverageFee', 'RoamMins']]

# Initialize the Isolation Forest model
iso_forest = IsolationForest(contamination=0.05, random_state=42)

# Fit the model and predict outliers
df['outlier'] = iso_forest.fit_predict(features)

# Filter out the outliers
df_cleaned = df[df['outlier'] != -1]

# Optionally, drop the outlier column
df_cleaned.drop('outlier', axis=1, inplace=True)

# Display the cleaned dataset
print(df_cleaned.head())

from sklearn.model_selection import learning_curve
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load the dataset
df = df_cleaned

# Feature selection
X = df[['AccountWeeks', 'ContractRenewal', 'DataPlan', 'DataUsage', 'CustServCalls',
        'DayMins', 'DayCalls', 'MonthlyCharge', 'OverageFee', 'RoamMins']]
y = df['Churn']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Standardize features for Logistic Regression
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Initialize models
logistic_regression = LogisticRegression(solver='lbfgs', class_weight='balanced', max_iter=1000, random_state=100)
naive_bayes = GaussianNB()

# Function to plot learning curves
def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None, n_jobs=None, train_sizes=np.linspace(.1, 1.0, 5)):
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes, scoring='recall_weighted')
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r", label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g", label="Cross-validation score")

    plt.legend(loc="best")
    return plt

# Plot learning curve for Logistic Regression
plot_learning_curve(logistic_regression, "Learning Curves (Logistic Regression)", X_train, y_train, cv=5, n_jobs=-1)

# Plot learning curve for Naive Bayes
plot_learning_curve(naive_bayes, "Learning Curves (Naive Bayes)", X_train, y_train, cv=5, n_jobs=-1)

plt.show()

# Fit the Logistic Regression model
logistic_regression.fit(X_train, y_train)  # Add this line to train the model

# Predict with Logistic Regression
y_pred_lr = logistic_regression.predict(X_test)
y_pred_prob_lr = logistic_regression.predict_proba(X_test)[:, 1]

# ... (rest of the code)

# Predict with Logistic Regression
y_pred_lr = logistic_regression.predict(X_test)
y_pred_prob_lr = logistic_regression.predict_proba(X_test)[:, 1]

# Fit the Naive Bayes model before predicting
naive_bayes.fit(X_train, y_train)  # Add this line to train the Naive Bayes model

# Predict with Naive Bayes
y_pred_nb = naive_bayes.predict(X_test)
y_pred_prob_nb = naive_bayes.predict_proba(X_test)[:, 1]

# ... (rest of the code remains the same)

# Predict with Logistic Regression
y_pred_lr = logistic_regression.predict(X_test)
y_pred_prob_lr = logistic_regression.predict_proba(X_test)[:, 1]

# Predict with Naive Bayes
y_pred_nb = naive_bayes.predict(X_test)
y_pred_prob_nb = naive_bayes.predict_proba(X_test)[:, 1]

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report, roc_auc_score

# Logistic Regression Metrics
accuracy_lr = accuracy_score(y_test, y_pred_lr)
precision_lr = precision_score(y_test, y_pred_lr)
recall_lr = recall_score(y_test, y_pred_lr)
f1_lr = f1_score(y_test, y_pred_lr)
roc_auc_lr = roc_auc_score(y_test, y_pred_prob_lr)

# Naive Bayes Metrics
accuracy_nb = accuracy_score(y_test, y_pred_nb)
precision_nb = precision_score(y_test, y_pred_nb)
recall_nb = recall_score(y_test, y_pred_nb)
f1_nb = f1_score(y_test, y_pred_nb)
roc_auc_nb = roc_auc_score(y_test, y_pred_prob_nb)

# Confusion Matrices
conf_matrix_lr = confusion_matrix(y_test, y_pred_lr)
conf_matrix_nb = confusion_matrix(y_test, y_pred_nb)

# Classification Reports
class_report_lr = classification_report(y_test, y_pred_lr)
class_report_nb = classification_report(y_test, y_pred_nb)

# Display results for Logistic Regression
print("Logistic Regression Metrics:")
print(f"Accuracy: {accuracy_lr:.2f}")
print(f"Precision: {precision_lr:.2f}")
print(f"Recall: {recall_lr:.2f}")
print(f"F1 Score: {f1_lr:.2f}")
print(f"ROC AUC: {roc_auc_lr:.2f}")

print("\nConfusion Matrix for Logistic Regression:")
print(conf_matrix_lr)

print("\nClassification Report for Logistic Regression:")
print(class_report_lr)

# Display results for Naive Bayes
print("Naive Bayes Metrics:")
print(f"Accuracy: {accuracy_nb:.2f}")
print(f"Precision: {precision_nb:.2f}")
print(f"Recall: {recall_nb:.2f}")
print(f"F1 Score: {f1_nb:.2f}")
print(f"ROC AUC: {roc_auc_nb:.2f}")

print("\nConfusion Matrix for Naive Bayes:")
print(conf_matrix_nb)

print("\nClassification Report for Naive Bayes:")
print(class_report_nb)

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import roc_curve, roc_auc_score, auc
from sklearn.preprocessing import StandardScaler

# Load the dataset
df = df_cleaned
# Feature selection
X = df[['AccountWeeks', 'ContractRenewal', 'DataPlan', 'DataUsage', 'CustServCalls',
        'DayMins', 'DayCalls', 'MonthlyCharge', 'OverageFee', 'RoamMins']]
y = df['Churn']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Standardize features for Logistic Regression
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Initialize and train models
logistic_regression = LogisticRegression(solver='lbfgs', class_weight='balanced', max_iter=1000, random_state=100)
naive_bayes = GaussianNB()

# Fit the models
logistic_regression.fit(X_train, y_train)
naive_bayes.fit(X_train, y_train)

# Predict probabilities
y_pred_prob_lr = logistic_regression.predict_proba(X_test)[:, 1]
y_pred_prob_nb = naive_bayes.predict_proba(X_test)[:, 1]

# Compute ROC curve and AUC
fpr_lr, tpr_lr, _ = roc_curve(y_test, y_pred_prob_lr)
roc_auc_lr = auc(fpr_lr, tpr_lr)

fpr_nb, tpr_nb, _ = roc_curve(y_test, y_pred_prob_nb)
roc_auc_nb = auc(fpr_nb, tpr_nb)

# Plot ROC curves
plt.figure()

plt.plot(fpr_lr, tpr_lr, color='darkorange', lw=2, label='Logistic Regression (area = %0.2f)' % roc_auc_lr)
plt.plot(fpr_nb, tpr_nb, color='navy', lw=2, label='Naive Bayes (area = %0.2f)' % roc_auc_nb)
plt.plot([0, 1], [0, 1], color='gray', linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC)')
plt.legend(loc='lower right')
plt.show()

from sklearn.ensemble import GradientBoostingClassifier, VotingClassifier
from sklearn.metrics import roc_curve, roc_auc_score, auc

# Load the dataset
df = df_cleaned

# Feature selection
X = df[['AccountWeeks', 'ContractRenewal', 'DataPlan', 'DataUsage', 'CustServCalls',
        'DayMins', 'DayCalls', 'MonthlyCharge', 'OverageFee', 'RoamMins']]
y = df['Churn']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Standardize features for Logistic Regression
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Initialize models
logistic_regression = LogisticRegression(solver='lbfgs', class_weight='balanced', max_iter=1000, random_state=100)
gradient_boosting = GradientBoostingClassifier(n_estimators=100, random_state=100)

# Initialize and fit the Voting Classifier
voting_clf = VotingClassifier(estimators=[
    ('lr', logistic_regression),
    ('gb', gradient_boosting)
], voting='soft')

voting_clf.fit(X_train, y_train)

# Predict probabilities
y_pred_prob = voting_clf.predict_proba(X_test)[:, 1]

# Compute ROC curve and AUC
fpr, tpr, _ = roc_curve(y_test, y_pred_prob)
roc_auc = auc(fpr, tpr)

# Plot ROC curve
plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label='Ensemble Voting (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='gray', linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC)')
plt.legend(loc='lower right')
plt.show()

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

# Predict on test data
y_pred = voting_clf.predict(X_test)
y_pred_prob = voting_clf.predict_proba(X_test)[:, 1]

# Calculate performance metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred_prob)

# Confusion Matrix
conf_matrix = confusion_matrix(y_test, y_pred)

# Classification Report
class_report = classification_report(y_test, y_pred)

# Display results
print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1 Score: {f1:.2f}")
print(f"ROC AUC: {roc_auc:.2f}")

print("\nConfusion Matrix:")
print(conf_matrix)

print("\nClassification Report:")
print(class_report)

# Optionally, plot ROC curve if not already done
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

fpr_voting, tpr_voting, _ = roc_curve(y_test, y_pred_prob)
roc_auc_voting = auc(fpr_voting, tpr_voting)

plt.figure()
plt.plot(fpr_voting, tpr_voting, color='darkblue', lw=2, label='Ensemble Voting (area = %0.2f)' % roc_auc_voting)
plt.plot([0, 1], [0, 1], color='gray', linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC)')
plt.legend(loc='lower right')
plt.show()