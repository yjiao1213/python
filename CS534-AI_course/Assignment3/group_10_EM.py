import pandas as pd
import numpy as np
import math
import random
import matplotlib.pyplot as plt
import copy

def getPDF(value,mu,sigma):

    return (1/(2*math.pi*sigma[0][0]*sigma[1][1]))*np.exp(-math.pow(value[0]-mu[0],2)/(2*math.pow(sigma[0][0],2)))*np.exp(-math.pow(value[1]-mu[1],2)/(2*math.pow(sigma[1][1],2)))

def getCDF(value,mu,sigma):

    return 0.25*(1+math.erf((value[0]-mu[0])/(sigma[0][0]*math.sqrt(2)))) * (1+math.erf((value[1]-mu[1])/(sigma[1][1]*math.sqrt(2))))

def newGetPDF(data,Mu,sigma):

    sigma_sqrt = math.sqrt(np.linalg.det(sigma))
    sigma_inv = np.linalg.inv(sigma)
    data.shape = (2, 1)
    Mu.shape = (2, 1)
    minus_mu = data - Mu
    minus_mu_trans = np.transpose(minus_mu)
    res = (1.0 / (2.0 * math.pi * sigma_sqrt)) * math.exp(
        (-0.5) * (np.dot(np.dot(minus_mu_trans, sigma_inv), minus_mu)))

    return res

def Expectation(data,para_dict,prob_matrix):

    for i in range(len(data)):
        temp_prob = np.zeros(len(para_dict)-1)

        # important : multiply the weight
        for j in range(len(para_dict)-1):
            #temp_prob[j] = getPDF(data[i][:2],para_dict[j]['mu'],para_dict[j]['sigma']) * para_dict['weight'][j]
            temp_data = np.array([data[i][0],data[i][1]])
            temp_prob[j] = newGetPDF(temp_data,para_dict[j]['mu'],para_dict[j]['sigma']) * para_dict['weight'][j]
        temp_prob = temp_prob/np.sum(temp_prob)
        prob_matrix[i] = temp_prob

    ## Update the probability matrix directly
    return prob_matrix

def log_likelihood(prob_matrix):

    log_value = np.zeros(len(prob_matrix[0]))

    for i in range(len(prob_matrix)):
        for j in range(len(prob_matrix[0])):
            #log_value[j] += np.log(prob_matrix[i][j])
            #log_value[j] += prob_matrix[i][j]
            log_value[j] += np.log(prob_matrix[i][j])
        #log_value = log_value/len(prob_matrix[0])

    result = np.sum(log_value)
    #result = result / len(prob_matrix[0])
    #sum_log = np.sum(log_value)/len(log_value)

    return result

def Maximization(data,para_dict,prob_matrix):

    mean_ = np.zeros((len(para_dict)-1,2))
    std_ = np.zeros((len(para_dict)-1,2,2))
    denom_ = np.zeros(len(para_dict)-1)

    # calculate the denorminator
    for j in range(len(prob_matrix)):
        for i in range(len(para_dict)-1):
            denom_[i] += prob_matrix[j][i]

    ## update mu
    for i in range(len(data)):
        for j in range(len(para_dict)-1):
            mean_[j][0] += data[i][0] * prob_matrix[i][j] / denom_[j]
            mean_[j][1] += data[i][1] * prob_matrix[i][j] / denom_[j]

    ## update sigma
    for i in range(len(data)):
        for j in range(len(para_dict)-1):
            temp_data = np.array([data[i][0],data[i][1]])
            temp_data.shape = (2,1)
            temp_mean = np.array([para_dict[j]['mu'][0],para_dict[j]['mu'][1]])
            temp_mean.shape = (2,1)
            minus_mu = temp_data - temp_mean
            std_[j] += prob_matrix[i][j] * (minus_mu ) * np.transpose(minus_mu) / denom_[j]

    ## Update the weight parameter
    para_dict['weight'] = denom_ / len(data)

    ### Update other parameters
    for i in range(len(para_dict)-1):
        para_dict[i]['mu'] = mean_[i]#[mean_[i][0],mean_[i][1]]
        para_dict[i]['sigma'] = std_[i]#[[std_[i][0],0],[0,std_[i][1]]]

    ### Update the parameter dictionary directly
    return para_dict

def printVariance(para_dict):

    print("The parameter of the Clustering ")
    print("-----------------------")
    for j in range(len(para_dict)-1):
        print("*****")
        print("mu, ", para_dict[j]['mu'])
        print("sigma ", para_dict[j]['sigma'])
        print("*****")
    print("-----------------------")

def BICEquation(log_likelihood,K,N):

    return -2*log_likelihood + K*np.log(N)

def EM(data,para_dict,prob_matrix):

    log_value = 0
    log_list = []
    # for i in range(30):
    epsilon = 0.01
    difference = 10
    delta_mu = 300
    #cluster_number = len(para_dict) - 1

    while delta_mu > epsilon:
        #print("Weight vector, ", para_dict['weight'])

        delta_mu = 0
        last_para = copy.deepcopy(para_dict)

        prob_matrix = Expectation(data,para_dict,prob_matrix)
        para_dict = Maximization(data,para_dict,prob_matrix)
        log_value = log_likelihood(prob_matrix)
        #printVariance(para_dict)
        #print("log likelihood",log_value)
        log_list.append(log_value)

        now_para = copy.deepcopy(para_dict)

        for i in range(len(para_dict)-1):
            delta_mu += abs(now_para[i]['mu'][0] - last_para[i]['mu'][0]) + abs(now_para[i]['mu'][1] - last_para[i]['mu'][1])
            #delta_mu += math.sqrt(math.pow(now_para[i]['mu'][0] - last_para[i]['mu'][0],2) + math.pow(now_para[i]['mu'][1] - last_para[i]['mu'][1],2))
        #print(delta_mu)
        delta_mu = delta_mu / (len(para_dict)-1)

            #if len(log_list) > 2:
            #difference = log_list[len(log_list)-1] - log_list[len(log_list)-2]
    cluster_number = len(para_dict) - 1
    bic = BICEquation(log_list[-1], cluster_number, len(data))

    # plt.figure()
    # plt.plot(log_list)
    # plt.title("Log-Likelihood vs. Iteration")
    # plt.show()

    return log_list,bic

def _EM(data,para_dict,prob_matrix):
    log_value = 0
    log_list = []
    # for i in range(30):
    epsilon = 0.01
    difference = 10
    delta_mu = 300
    #cluster_number = len(para_dict) - 1

    while delta_mu > epsilon:
        #print("Weight vector, ", para_dict['weight'])

        delta_mu = 0
        last_para = copy.deepcopy(para_dict)

        prob_matrix = Expectation(data,para_dict,prob_matrix)
        para_dict = Maximization(data,para_dict,prob_matrix)
        log_value = log_likelihood(prob_matrix)
        #printVariance(para_dict)
        #print("log likelihood",log_value)
        log_list.append(log_value)

        now_para = copy.deepcopy(para_dict)

        for i in range(len(para_dict)-1):
            delta_mu += abs(now_para[i]['mu'][0] - last_para[i]['mu'][0]) + abs(now_para[i]['mu'][1] - last_para[i]['mu'][1])
            #delta_mu += math.sqrt(math.pow(now_para[i]['mu'][0] - last_para[i]['mu'][0],2) + math.pow(now_para[i]['mu'][1] - last_para[i]['mu'][1],2))
        #print(delta_mu)
        delta_mu = delta_mu / (len(para_dict)-1)

            #if len(log_list) > 2:
            #difference = log_list[len(log_list)-1] - log_list[len(log_list)-2]
    cluster_number = len(para_dict) - 1
    bic = BICEquation(log_list[-1], cluster_number, len(data))

    return log_list[-1], bic

def InitializeParameter(data,cluster_number):

    prob_matrix = np.ones((len(data),cluster_number))
    prob_matrix = prob_matrix / cluster_number

    # Initialize the parameters
    para_dict = dict()

    point = random.sample(data.tolist(),cluster_number)
    point = np.array(point)

    x_std = np.std(np.transpose(data)[0])
    y_std = np.std(np.transpose(data)[1])

    x_std_array = np.random.uniform(low=x_std,high=cluster_number*x_std,size=(cluster_number,))
    y_std_array = np.random.uniform(low=y_std,high=cluster_number*y_std,size=(cluster_number,))


    x_mean_array = np.zeros(cluster_number)
    y_mean_array = np.zeros(cluster_number)

    for j in range(cluster_number):
        x_mean_array[j] = point[j][0]
        y_mean_array[j] = point[j][1]


    ## Initialize the parameter dictionary
    for i in range(cluster_number):
        sub_dict = dict()
        sub_dict['mu'] = np.array([x_mean_array[i],y_mean_array[i]])
        sub_dict['sigma'] = np.array([[math.sqrt(x_std_array[i]),0],[0,math.sqrt(y_std_array[i])]])
        para_dict[i] = sub_dict

    para_dict['weight'] = np.ones(cluster_number) / cluster_number

    return data,para_dict,prob_matrix

def getEMResult(data,cluster_number):

    data, para_dict, prob_matrix = InitializeParameter(data, cluster_number)
    log_value, bic = EM(data,para_dict,prob_matrix)

    printVariance(para_dict)

    plt.figure()
    plt.plot(log_value)
    plt.title("Log-Likelihood vs. Iteration")
    plt.show()

    return log_value,bic

def _getEMResult(data,cluster_number):

    data, para_dict, prob_matrix = InitializeParameter(data, cluster_number)
    log_value, bic = _EM(data,para_dict,prob_matrix)

    #printVariance(para_dict)

    return log_value,bic

def ExtendedEM(data):

    BIC_list = []

    k = 1
    #k_best = 0

    while True:
        k = k + 1
        temp_log_value,temp_bic = _getEMResult(data,k)
        BIC_list.append(temp_bic)
        print("cluster number",k, "BIC ",temp_bic,"log-likelihood ",temp_log_value)

        if len(BIC_list) > 1:
            if BIC_list[-1] < BIC_list[-2]:
                k_best = len(BIC_list)
                break

    return k_best,BIC_list

def ExtendedEMResult(data):

    total_list = []

    for i in range(2, 7):

        sub_list = []
        for j in range(20):
            log_value, bic = _getEMResult(data, i)
            sub_list.append(bic)

        total_list.append(sub_list)

    x_ = []
    label_ = []
    for i in range(20):
        x_.append(i + 1)

    for j in range(2, 11):
        label_.append("cluster k = " + str(j))

    var_ = []
    for i in range(len(total_list)):
        arr_ = np.array(total_list[i])
        var_.append(np.var(arr_ / np.sum(arr_)))

    print("Variance ", var_)

    plt.figure()

    for i in range(len(total_list)):
        plt.plot(x_, total_list[i], label=str(label_[i]))
        plt.legend(loc='upper right')

    plt.show()


# file_read = pd.read_csv("sample EM data v2.csv")
# data = file_read.values

mode=input('Basic EM, enter 1; Extending EM, enter 2:')
filename= input('enter the Path of the file:')

if mode =='1':
    k = int(input('enter the k:'))
    data = pd.read_csv(filename).values
    #print(data)
    getEMResult(data,k)

elif mode=='2':
    data = pd.read_csv(filename).values
    k_best,BIC_list = ExtendedEM(data)
    print("Best cluster number K:",k_best)

else:
    print('Input Error. Please Re-input.')




