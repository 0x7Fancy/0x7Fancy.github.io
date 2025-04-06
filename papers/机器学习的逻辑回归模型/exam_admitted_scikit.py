import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

path = 'ex2data1.txt'
data = pd.read_csv(path, header=None, names=['Exam 1', 'Exam 2', 'Admitted'])
print(data.head())

X_train,X_test,y_train,y_test = train_test_split(
    data[["Exam 1", "Exam 2"]],
    data["Admitted"],
    test_size = 0.2)

#from sklearn.preprocessing import StandardScaler
#ss = StandardScaler()
#X_train = ss.fit_transform(X_train)
#X_test = ss.transform(X_test)

lr = LogisticRegression()
lr.fit(X_train,y_train)
predict = lr.predict(X_test)
print("predict_test:", predict)

score_train = lr.score(X_train, y_train)
score_test = lr.score(X_test, y_test)
print("score_train:", score_train)
print("score_test:", score_test)

print("Class:",lr.classes_)
print("Coef:",lr.coef_)
print("intercept:",lr.intercept_)
print("n_iter:",lr.n_iter_)

#
positive = data[data['Admitted'].isin([1])]
negative = data[data['Admitted'].isin([0])]

fig, ax = plt.subplots(figsize=(8,6))
ax.scatter(positive['Exam 1'], positive['Exam 2'], s=50, c='b', marker='o', label='Admitted')
ax.scatter(negative['Exam 1'], negative['Exam 2'], s=50, c='r', marker='x', label='Not Admitted')
ax.legend()
ax.set_xlabel('Exam 1 Score')
ax.set_ylabel('Exam 2 Score')

grid1 = np.arange(data["Exam 1"].min()-1, data["Exam 1"].max()+1, 0.2)
grid2 = np.arange(data["Exam 2"].min()-1, data["Exam 2"].max()+1, 0.2)
xx, yy = np.meshgrid(grid1, grid2)

Grid = np.vstack([xx.reshape(-1), yy.reshape(-1)]).T
zz = lr.predict(Grid).reshape(xx.shape)
plt.contourf(xx, yy, zz, cmap=plt.cm.Set1, alpha=0.5)

plt.show()
