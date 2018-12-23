import csv
import random
from scipy.stats import multivariate_normal
import numpy as np
import matplotlib.pyplot as plt
from math import log

def load_data(filename):
    csv_reader = csv.reader(open(filename, encoding='utf-8'))
    raw_data=[]
    for row in csv_reader:
        for i in range(len(row)):
            row[i]=float(row[i])
        raw_data.append(row)
    return raw_data

def set_start_state(filename, k):
    p_weight=[]
    Mu=[]
    Sigma=[]
    raw_data = load_data(filename)
    for i in range(k):
        p_weight.append(1/k)
    for i in range(k):
        Mu.append(raw_data[random.randint(0, len(raw_data))])
        a=random.randint(1, 20)
        Sigma.append([[a, 0], [0, a]])

    return raw_data, Mu, Sigma, p_weight

def phi(Y, mu_k, cov_k):
    norm = multivariate_normal(mean=mu_k, cov=cov_k)
    return norm.pdf(Y)

def expectation(raw_data, Mu, Sigma, p_weight,k):
    cluster=[]
    for point in raw_data:
        down=[]
        parameter_dict=[]
        for i in range(k):
            down.append(p_weight[i]*phi(point,Mu[i],Sigma[i]))
        for i in range(k):
            parameter_dict.append(down[i]/sum(down))
        cluster.append(parameter_dict)
    return cluster

def maximization(cluster,raw_data,k):

    new_cluster=np.array(cluster)
    N_mean=np.sum(new_cluster,axis=0)
    new_Mu=[]
    for i in range(k):
        new_x=0
        new_y=0
        for j in range(len(raw_data)):
            new_x = new_x + raw_data[j][0] * cluster[j][i] / N_mean[i]
            new_y = new_y + raw_data[j][1] * cluster[j][i] / N_mean[i]
        new_Mu.append([new_x,new_y])

    new_Sigma=[]
    for i in range(k):
        new_sigma = np.array([[0, 0], [0, 0]])
        a=0
        b=0
        c=0
        d=0
        for j in range(len(raw_data)):
            a=a+(raw_data[j][0]-new_Mu[i][0])*(raw_data[j][0]-new_Mu[i][0])*cluster[j][i]/N_mean[i]
            b=b+(raw_data[j][0]-new_Mu[i][0])*(raw_data[j][1]-new_Mu[i][1])*cluster[j][i]/N_mean[i]
            c=c+b*cluster[j][i]/N_mean[i]
            d=d+(raw_data[j][1]-new_Mu[i][1])*(raw_data[j][1]-new_Mu[i][1])*cluster[j][i]/N_mean[i]

        new_Sigma.append([[a,b],[c,d]])

    new_p=[]
    for i in range(k):
        new_p.append(N_mean[i]/len(cluster))

    return new_p, new_Sigma, new_Mu

def EM_basic(filename,k,esp):
    raw_data, Mu, Sigma, p_weight = set_start_state(filename, k)
    j=1
    log_lhod=[]
    while(True):
        delta_mu=0
        old_mu = Mu.copy()
        cluster = expectation(raw_data, Mu, Sigma, p_weight, k)
        num=float(1)
        for i in range(len(raw_data)):
            num+=log(cluster[i][1])
        log_lhod.append(num)
        p_weight, Sigma, Mu = maximization(cluster, raw_data, k)
        for i in range(k):
            delta_mu = delta_mu+abs(old_mu[i][0]-Mu[i][0])+abs(old_mu[i][1]-Mu[i][1])
        if delta_mu < k*esp:
            break

    return p_weight, Sigma, Mu, log_lhod

def EM_extend(filename, esp):
    k=1
    BIC=[]
    while(True):
        k=k+1
        raw_data, Mu, Sigma, p_weight = set_start_state(filename, k)
        log_lhod = []
        while(True):
            delta_mu = 0
            old_mu = Mu.copy()
            cluster = expectation(raw_data, Mu, Sigma, p_weight, k)
            num = float(1)
            for i in range(len(raw_data)):
                num += log(cluster[i][1])
            log_lhod.append(num)
            p_weight, Sigma, Mu = maximization(cluster, raw_data, k)
            for i in range(k):
                delta_mu = delta_mu + abs(old_mu[i][0] - Mu[i][0]) + abs(old_mu[i][1] - Mu[i][1])
            if delta_mu < k * esp:
                BIC_single=-2*log_lhod[-1]+log(len(raw_data))*k
                break
        BIC.append(BIC_single)
        if len(BIC)>1:
            if BIC[-1]<BIC[-2]:
                k_best=1+len(BIC)-1
                break
    return k_best,BIC

mode=input('Basic EM, enter 1; Extending EM, enter 2:')
filename= "sample EM data v2.csv"#input('enter the name of the file:')

if mode =='1':
    k = int(input('enter the k:'))
    p_weight, Sigma, Mu, log_lhod = EM_basic(filename, k, 0.1)
    print(Mu)
    print(Sigma)
    f1 = plt.figure(1)
    plt.plot(log_lhod)
    plt.show()
elif mode=='2':
    k_best, BIC= EM_extend(filename, 0.1)
    print(k_best)
    print(BIC)
else: print('Error enter')