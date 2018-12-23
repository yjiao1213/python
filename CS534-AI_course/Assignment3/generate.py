import csv
import numpy as np

out = open('EM sample v3_test.csv','a', newline='')

csv_write = csv.writer(out,dialect='excel')

mean1=[0,0]
mean2=[10,10]
mean3=[20,20]
cov1= [[100, 1], [1, 100]]
cov2= [[10, 1], [1, 10]]
cov3= [[50, 1], [1, 50]]
for i in range(1119):
    if i<400:
        x, y = np.random.multivariate_normal(mean1, cov1, 1).T
        csv_write.writerow([x[0], y[0]])
    elif 400<i<800:
        x, y = np.random.multivariate_normal(mean2, cov2, 1).T
        csv_write.writerow([x[0], y[0]])
    else:
        x, y = np.random.multivariate_normal(mean3, cov3, 1).T
        csv_write.writerow([x[0], y[0]])

print ("write over")
