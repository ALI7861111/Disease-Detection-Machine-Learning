import pandas as pd
import argparse
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn import metrics

# Define command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, required=True, help="Model to use during training: 'decision_tree', 'random_forest', or 'svm'")
args = parser.parse_args()

# Create a dictionary of models
models = {
    'decision_tree': DecisionTreeClassifier(),
    'random_forest': RandomForestClassifier(),
    'svm': SVC(C=.1, kernel='linear', gamma=1)
}

model = models.get(args.model.lower())
if model is None:
    raise Exception(f"Model {args.model} not recognized. Choose either 'decision_tree', 'random_forest', or 'svm'.")

train_dataset_path = './dataset/Training.csv'
test_dataset_path  = './dataset/Testing.csv'

# reading the training data
train_csv = pd.read_csv(train_dataset_path)

del train_csv['Unnamed: 133']

# reading the test data
test_csv = pd.read_csv(test_dataset_path)

Y = train_csv[["prognosis"]]
X = train_csv.drop(["prognosis"],axis=1)

xtrain, xtest, ytrain, ytest = train_test_split(X, Y, test_size=0.2, random_state=42)

model.fit(xtrain, ytrain.values.ravel())

prediction = model.predict(xtest)
print(f"{args.model} model accuracy(in %):", metrics.accuracy_score(ytest, prediction)*100)

y_pred = model.predict(xtest)

print(classification_report(ytest, y_pred))

filename = f'{args.model}_model.sav'
pickle.dump(model, open(filename, 'wb'))