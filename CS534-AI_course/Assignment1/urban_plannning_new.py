import random
import copy
import queue
import numpy as np
import timeit
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

class Map:
    def __init__(self,industrial, commercial, residential):
        self.industrial = int(industrial)
        self.commercial = int(commercial)
        self.residential = int(residential)
        self.siteAmount = int(industrial) + int(commercial) + int(residential)

    def setToxicSite(self,cooridnates = None):
        if cooridnates is None:
            cooridnates =[]
        self.toxicCoord = copy.deepcopy(cooridnates)

    def setScenicView(self,sceCoord = None):
        if sceCoord is None:
            sceCoord = []
        self.scenicCoord = copy.deepcopy(sceCoord)

    def setCostMap(self,costMap = None):
        if costMap is None:
            costMap = []
        self.costMap = copy.deepcopy(costMap)

    def setParentNode(self,ParentNode):
        self.ParentNode = ParentNode

    def setScore(self,Score):
        self.score = Score

    def MapSize(self,iniMap):
        self.row = len(iniMap)-3
        self.column = len(iniMap[3])

# Read file through using a dialog

# File Dialog box

def ReadFromFile():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title = "Select Map File (text file only)",filetypes = (("text files","*.txt"),("all files","*.*")))
    fobj = open(file_path)

    # x is the total content reading from file
    x= []
    # the site number, [0] - industrial, [1] - commercial [2] - residential
    site_number = []
    # scenic view coordinates
    scenicPosition = []
    # toxic view coordinates
    toxicPosition = []

    for line in fobj:
        x.append(line.rstrip().replace(',',''))

    for i in range(0,3):
        temp = int(x[i])
        site_number.append(temp)

    cost_map = []
    for j in range(3,len(x)):
        line = []
        for m in range(len(x[j])):
            if x[j][m] == 'X':
                cost = 99
                line.append(cost)
                toxicPosition.append([j+1-3,m+1])
            elif x[j][m] == 'S':
                cost = -1
                line.append(cost)
                scenicPosition.append([j+1-3,m+1])
            elif x[j][m] != ',':
                cost = int(x[j][m])
                line.append(cost)
        cost_map.append(line)
    map2 = Map(site_number[0], site_number[1], site_number[2])
    map2.setToxicSite(toxicPosition)
    map2.setScenicView(scenicPosition)
    map2.setCostMap(cost_map)

    return map2


def printMap(result,map):

    row = len(map.costMap)
    column = len(map.costMap[0])
    ind = 0
    com = map.industrial
    res = map.commercial + map.industrial
    site_number = map.commercial + map.industrial + map.residential

    pb = [['O'] * column for i in range(row)]

    for i in range(len(map.toxicCoord)):
        pb[map.toxicCoord[i][0]-1][map.toxicCoord[i][1]-1] = 'X'

    for j in range(len(map.scenicCoord)):
        pb[map.scenicCoord[j][0]-1][map.scenicCoord[j][1]-1] = 'S'

    for k in range(ind,com):
        pb[result[k][0]-1][result[k][1]-1] = 'I'

    for l in range(com,res):
        pb[result[l][0] - 1][result[l][1] - 1] = 'C'

    for m in range(res,site_number):
        pb[result[m][0] - 1][result[m][1] - 1] = 'R'

    for i in range(row):
        if i != 0:
            print("")
        for j in range(column):
            print(str(pb[i][j]), end="")
    print("")


def iniPosition(map):
    position = []
    available_position = []
    num_indus = map.industrial
    num_comme = map.commercial
    num_resid = map.residential

    for i in range(len(map.costMap)):
        for j in range(len(map.costMap[i])):
            if map.costMap[i][j] == -1 or map.costMap[i][j] == 99:
                continue
            else:
                available_position.append((i+1,j+1))

    # choose the positions
    random_position = random.sample(range(0,len(available_position)),map.siteAmount)

    # get the coordinate
    for n in range(len(random_position)):
        position.append([available_position[random_position[n]][0],available_position[random_position[n]][1],0])

    #1 for industrial, 2 for commercial, 3 for residential
    for n in range(num_indus):
        position[n][2] = 1
    for n in range(num_comme):
        position[n+num_indus][2] = 2
    for n in range(num_resid):
        position[n+num_indus+num_comme][2] = 3

    return position

def ManhattanDistance(a,b):
    distance = abs(a[0]-b[0]) + abs(b[1]-a[1])
    return distance

def generateSuccessors (position,ini_avail_position):

    result_position = []
    ini_ap = copy.deepcopy(ini_avail_position)

    # Remove the element in position from initial available position
    for ele in position:
        temp = ele[:-1]
        while temp in ini_ap:
            ini_ap.remove(temp)

    for n in range(len(position)):
        for m in range(len(ini_ap)):
            temp_position = copy.deepcopy(position)
            temp_position[n][0] = ini_ap[m][0]
            temp_position[n][1] = ini_ap[m][1]
            result_position.append(temp_position)

    return result_position

# get the cost of each positions (except the X and S site)
def getAvailablePosition(map):
    available_position = []

    for i in range(len(map.costMap)):
        for j in range(len(map.costMap[i])):
            if map.costMap[i][j] == -1 or map.costMap[i][j] == 99:
                continue
            else:
                available_position.append([i + 1, j + 1])

    return available_position


# get the system time
def getTime():
    time = timeit.default_timer()
    return time

# In this progam the socre is the same as the fitness
def calculateScore(map,position):
    score = 0

    #pentaly for within 2 tiles from toxic site

    for ele in position:
        for ele_1 in map.toxicCoord:
            if ManhattanDistance(ele[:-1],ele_1) <=2:
                if ele[2] == 1:
                    score = score - 10
                elif ele[2] == 2:
                    score = score - 20
                elif ele[2] == 3:
                    score = score - 20

    #Bonus for near Scenic Site, Residental only
    for ele in position:
        if ele[2] == 3:
            for ele_1 in map.scenicCoord:
                if ManhattanDistance(ele[:-1],ele_1) <= 2:
                    score = score + 10

    # Construction cost on different sites:
    for ele in position:
        cost = map.costMap[ele[0]-1][ele[1]-1]
        score = score - cost

    # I,C,R sites points calculation
    ### First Record the index:
    indus_index = []
    comme_index = []
    resid_index = []

    for l in range(len(position)):
        if position[l][2] == 1:
            indus_index.append(l)
        elif position[l][2] == 2:
            comme_index.append(l)
        elif position[l][2] == 3:
            resid_index.append(l)

    ## industrial site benefit from other industrial sites, 2 tiles 3 points bonus:
    for in_l in range(0,len(indus_index)-1):
        for in_1_2 in range(in_l + 1, len(indus_index)):
            if ManhattanDistance(position[indus_index[in_l]][:-1],position[indus_index[in_1_2]][:-1]) <= 2:
                score = score + 3

    ## Commercial benefit from residential, <= 3, +5:
    for com_l in range(len(comme_index)):
        for res_l in range(len(resid_index)):
            if ManhattanDistance(position[comme_index[com_l]][:-1],position[resid_index[res_l]][:-1]) <= 3:
                score = score + 5

    ## Commercial compete with each other, <=2 , -5
    for com_l_1 in range(0,len(comme_index)-1):
        for com_l_2 in range(com_l_1+1,len(comme_index)):
            if ManhattanDistance(position[comme_index[com_l_1]][:-1],position[comme_index[com_l_2]][:-1]) <=2:
                score = score - 5


    ## Residential near industrial, penalty, <=3, -5
    for res_l_1 in range(len(resid_index)):
        for ind_l_1 in range(len(indus_index)):
            if ManhattanDistance(position[resid_index[res_l_1]][:-1],position[indus_index[ind_l_1]][:-1]) <= 3:
                score = score - 5

    return score

# On the following are functions for Genetic Algorithm

# used in the restart process
def upperBound(map):
    cost_list = []
    for i in range(len(map.costMap)):
        for j in range(len(map.costMap[i])):
            cost_list.append(map.costMap[i][j])
    cost_list.sort()
    while -1 in cost_list:
        cost_list.remove(-1)
    while 99 in cost_list:
        cost_list.remove(99)
    bonus_S = map.residential * len(map.scenicCoord)*10
    bonus_1 = map.residential * map.commercial*5
    if map.industrial >= 2:
        bonus_2 = int(map.industrial*(map.industrial-1)/2)*3
    else:
        bonus_2 = 0
    #print(bonus_2)
    #print(cost_list[:map.siteAmount])
    cost = sum(cost_list[:map.siteAmount])
    #print(cost)
    upper_final = bonus_S + bonus_1 + bonus_2 - cost
    return upper_final

# Hill Climbing
def hillClimbing (map,time_limit):

    temp_queue = queue.PriorityQueue()
    ini_position = iniPosition(map)
    available_position = getAvailablePosition(map)
    temp_queue.put((0,ini_position))
    score_list = []
    start = getTime()

    #function upper bound
    upper_bound = upperBound(map)

    #record the value of each restart.
    score_restart = queue.PriorityQueue()

    while True:

        currnt_position = temp_queue.get()[1] #the current position
        previous_score = calculateScore(map,currnt_position)
        temp_queue.queue.clear()

        current_successor = generateSuccessors(currnt_position,available_position)

        del score_list[:]

        for length in range(len(current_successor)):
            temp_score = calculateScore(map,current_successor[length])
            score_list.append(temp_score)
            temp_queue.put((10000-temp_score,current_successor[length]))

        score_list.sort(reverse=True)

        if score_list[0] <= previous_score:
            time_now = getTime()

            if time_now - start <= time_limit:

                if score_list[0] < upper_bound:
                    re_ini_pos = iniPosition(map)
                    temp_queue.put((0,re_ini_pos))
                    item = [previous_score,time_now-start]
                    score_restart.put((10000-previous_score,item))

            elif time_now - start > time_limit:
                result = copy.deepcopy(temp_queue.get()[1])
                item = [previous_score, time_now - start]
                score_restart.put((10000-previous_score,item))
                score = score_restart.get()[1]
                break

    return result,score

# Remove the same element:

def colonySize(map):
    row = len(map.costMap) - 3
    column = len(map.costMap[3])
    toxic = len(map.toxicCoord)
    scenic = len(map.scenicCoord)
    colonySize = map.siteAmount * (row * column - toxic - scenic)
    return colonySize

def RemoveSameElement(old_list):
    new_list = np.array(list(set([tuple(t) for t in old_list])))
    new_list = new_list.tolist()
    return new_list

def selection(scores,population):
    length = len(population)
    for i in range(len(scores)):
        scores[i] = 10000 + scores[i]
    scores = np.asarray(scores)
    pop_new = np.asarray(population)
    # according to the fitness, perform selection (through index)
    index = np.random.choice(np.arange(length), size=length, replace=True, p = scores/scores.sum())
    index = index.tolist()
    # filter duplicated elements
    index = list(set(index))
    pop_new = pop_new[index]
    pop_new = pop_new.tolist()

    return pop_new

def elitism_selection(population,map):

    score = 0
    index = 0
    # find the best fitness
    for i in range(len(population)):
        temp_score = calculateScore(map,population[i])
        if i == 0:
            score = temp_score
            index = i
        else:
            if temp_score > score:
                score = temp_score
                index = i

    elite = copy.deepcopy(population[index])

    #After elitism selection, the following elements
    del population[index]
    pop_sel = population

    return elite,pop_sel

def culling(population,map):
    score = 0
    index = 0
    # find the best fitness
    for i in range(len(population)):
        temp_score = calculateScore(map, population[i])

        if i == 0:
            score = temp_score
            index = i
        else:
            if temp_score < score:
                score = temp_score
                index = i

    # Remove the weakest element
    del population[index]
    pop_sel = population

    return pop_sel


# population: the colony for each generation
# map: the map
## population is a Queue

def crossover(pop_size,population,map):

    indp = 0
    comp = map.industrial
    resp = map.industrial + map.commercial
    site_number = map.industrial + map.commercial + map.residential
    child = []
    random.shuffle(population)

    temp_population = copy.deepcopy(population)

    #index = random.sample(range(0,len(population)),len(population))
    for i in range(len(population)-1):
        child_1 =[]
        child_2 =[]
        temp_chrom_ind = []
        temp_chrom_com = []
        temp_chrom_res = []

        for j in range(indp,comp):
            t1 = temp_population[i][j][:-1]
            temp_chrom_ind.append([t1[0],t1[1]])

        for j1 in range(indp, comp):
            t2 = temp_population[i+1][j1][:-1]
            temp_chrom_ind.append([t2[0],t2[1]])

        for m in range(comp,resp):
            # temp_chrom_com.append(temp_population[i][m][:-1])
            t3 = temp_population[i][m][:-1]
            temp_chrom_com.append([t3[0], t3[1]])

        for m2 in range(comp, resp):
            #temp_chrom_com.append(temp_population[i + 1][m2][:-1])
            t4 = temp_population[i + 1][m2][:-1]
            temp_chrom_com.append([t4[0], t4[1]])

        for n in range(resp,site_number):
            #temp_chrom_res.append(temp_population[i][n][:-1])
            t5 = temp_population[i][n][:-1]
            temp_chrom_res.append([t5[0], t5[1]])

        for n3 in range(resp, site_number):
            #temp_chrom_res.append(temp_population[i+1][n3][:-1])
            t6 = temp_population[i + 1][n3][:-1]
            temp_chrom_res.append([t6[0], t6[1]])


        # remove the duplicated elements for all the chromosome
        # industrial chromosome
        temp_chrom_ind = np.array(list(set([tuple(t) for t in temp_chrom_ind])))
        temp_chrom_ind = temp_chrom_ind.tolist()
        # commercial chromosome
        temp_chrom_com = np.array(list(set([tuple(t) for t in temp_chrom_com])))
        temp_chrom_com = temp_chrom_com.tolist()
        # residential chromsome
        temp_chrom_res = np.array(list(set([tuple(t) for t in temp_chrom_res])))
        temp_chrom_res = temp_chrom_res.tolist()

        test_ind_co_branch = 0
        # crossover on industrial site
        if len(temp_chrom_ind) < 2*map.industrial:
            #index_ind_1 = random.sample(range(0,len(temp_chrom_ind)),map.industrial)
            #index_ind_2 = random.sample(range(0,len(temp_chrom_ind)),map.industrial)

            if len(temp_chrom_ind) < map.industrial:

                remaining = map.industrial - len(temp_chrom_ind)
                child_1.extend(temp_chrom_ind)
                child_2.extend(temp_chrom_ind)

                #temp = [temp_chrom_ind[0][0],temp_chrom_ind[0][1]]
                for i in range(0,remaining):

                    index = random.sample(range(0,len(temp_chrom_ind)),1)
                    temp = [temp_chrom_ind[index[0]][0],temp_chrom_ind[index[0]][1]]
                    child_1.append(temp)
                    # index = random.sample(range(0, len(temp_chrom_ind)), 1)
                    child_2.append(temp)

                    test_ind_co_branch = 1
            elif len(temp_chrom_ind) >= map.industrial:
                index_ind_1 = random.sample(range(0, len(temp_chrom_ind)), map.industrial)
                index_ind_2 = random.sample(range(0, len(temp_chrom_ind)), map.industrial)
                temp_chrom_ind = np.asarray(temp_chrom_ind)
                ind_seg_1 = temp_chrom_ind[index_ind_1]
                ind_seg_2 = temp_chrom_ind[index_ind_2]
                ind_seg_1 = ind_seg_1.tolist()
                ind_seg_2 = ind_seg_2.tolist()
                child_1.extend(ind_seg_1)
                child_2.extend(ind_seg_2)

                test_ind_co_branch = 2

        else:
            test_ind_co_branch = 3
            # random crossover here
            length = map.industrial

            ind_seg_1 = []
            ind_seg_2 = []
            if length % 2 == 0:
                half = int(length/2)
            elif length % 2 == 1:
                half = int((length+1)/2)

            index_sample = random.sample(range(0,map.industrial),half)

            ind_seg_1.extend(temp_chrom_ind[0:map.industrial])
            ind_seg_2.extend(temp_chrom_ind[map.industrial:2*map.industrial])

            for ele in index_sample:
                temp_1 = copy.deepcopy(ind_seg_2[ele])
                temp_2 = copy.deepcopy(ind_seg_1[ele])
                ind_seg_1[ele] = copy.deepcopy(temp_1)
                ind_seg_2[ele] = copy.deepcopy(temp_2)
            child_1.extend(ind_seg_1)
            child_2.extend(ind_seg_2)

        test_com_branch = 0
        #cross over on commercial site:
        if len(temp_chrom_com) < 2 * map.commercial:
            #index_com_1 = random.sample(range(0, len(temp_chrom_com)), map.commercial)
            #index_com_2 = random.sample(range(0, len(temp_chrom_com)), map.commercial)
            if len(temp_chrom_com) < map.commercial:
                test_com_branch = 1
                remaining = map.commercial - len(temp_chrom_com)
                child_1.extend(temp_chrom_com)
                child_2.extend(temp_chrom_com)

                #temp = [temp_chrom_com[0][0], temp_chrom_com[0][1]]
                for i in range(0,remaining):
                    index = random.sample(range(0, len(temp_chrom_com)), 1)
                    temp = [temp_chrom_com[index[0]][0], temp_chrom_com[index[0]][1]]
                    #index_com_1 = random.sample(range(0,len(temp_chrom_com)),1)
                    # index = random.sample(range(0, len(temp_chrom_com)), 1)
                    child_1.append(temp)
                    #index_com_2 = random.sample(range(0, len(temp_chrom_com)), 1)
                    # index = random.sample(range(0, len(temp_chrom_com)), 1)
                    child_2.append(temp)

            elif len(temp_chrom_com) >= map.commercial:
                test_com_branch = 2
                index_com_1 = random.sample(range(0, len(temp_chrom_com)), map.commercial)
                index_com_2 = random.sample(range(0, len(temp_chrom_com)), map.commercial)
                temp_chrom_com = np.asarray(temp_chrom_com)
                com_seg_1 = temp_chrom_com[index_com_1]
                com_seg_2 = temp_chrom_com[index_com_2]
                com_seg_1 = com_seg_1.tolist()
                com_seg_2 = com_seg_2.tolist()
                child_1.extend(com_seg_1)
                child_2.extend(com_seg_2)

        else:
            test_com_branch = 3
            # random crossover here
            length = map.commercial

            com_seg_1 = []
            com_seg_2 = []
            if length % 2 == 0:
                half = int(length / 2)
            elif length % 2 == 1:
                half = int((length + 1) / 2)

            index_sample = random.sample(range(0, map.commercial), half)

            com_seg_1.extend(temp_chrom_com[0:map.commercial])
            com_seg_2.extend(temp_chrom_com[map.commercial:2 * map.commercial])

            for ele in index_sample:
                temp_1 = copy.deepcopy(com_seg_2[ele])
                temp_2 = copy.deepcopy(com_seg_1[ele])
                com_seg_1[ele] = copy.deepcopy(temp_1)
                com_seg_2[ele] = copy.deepcopy(temp_2)

            child_1.extend(com_seg_1)
            child_2.extend(com_seg_2)

        test_res_branch = 0
        # cross over on residential site:
        if len(temp_chrom_res) < 2 * map.residential:

            if len(temp_chrom_res) < map.residential:
                test_res_branch = 1

                remaining = map.residential - len(temp_chrom_res)
                child_1.extend(temp_chrom_res)
                child_2.extend(temp_chrom_res)

                #temp = [temp_chrom_res[0][0], temp_chrom_res[0][1]]

                for i in range(0,remaining):
                    index = random.sample(range(0, len(temp_chrom_res)), 1)
                    temp = [temp_chrom_res[index[0]][0], temp_chrom_res[index[0]][1]]
                    #index_res_1 = random.sample(range(0,len(temp_chrom_res)),1)
                    # index = random.sample(range(0, len(temp_chrom_com)), 1)
                    child_1.append(temp)
                    #index_res_2 = random.sample(range(0, len(temp_chrom_res)), 1)
                    child_2.append(temp)

            elif len(temp_chrom_res) >= map.residential:

                test_res_branch = 2
                index_res_1 = random.sample(range(0, len(temp_chrom_res)), map.residential)
                index_res_2 = random.sample(range(0, len(temp_chrom_res)), map.residential)
                temp_chrom_res = np.asarray(temp_chrom_res)
                res_seg_1 = temp_chrom_res[index_res_1]
                res_seg_2 = temp_chrom_res[index_res_2]
                res_seg_1 = res_seg_1.tolist()
                res_seg_2 = res_seg_2.tolist()
                child_1.extend(res_seg_1)
                child_2.extend(res_seg_2)

        else:
            test_res_branch = 3
            # random crossover here
            length = map.residential

            res_seg_1 = []
            res_seg_2 = []
            if length % 2 == 0:
                half = int(length / 2)
            elif length % 2 == 1:
                half = int((length + 1) / 2)

            index_sample = random.sample(range(0, map.residential), half)


            res_seg_1.extend(temp_chrom_res[0:map.residential])
            res_seg_2.extend(temp_chrom_res[map.residential:2 * map.residential])

            for ele in index_sample:
                # print("ele",ele)
                temp_1 = copy.deepcopy(res_seg_2[ele])
                temp_2 = copy.deepcopy(res_seg_1[ele])
                res_seg_1[ele] = copy.deepcopy(temp_1)
                res_seg_2[ele] = copy.deepcopy(temp_2)

            child_1.extend(res_seg_1)
            child_2.extend(res_seg_2)

        child_1 = RemoveSameElement(child_1)

        child_2 = RemoveSameElement(child_2)

        if len(child_1) == site_number:
            child.append(child_1)
            # print("child 1",child_1)

        if len(child_2) == site_number:
            child.append(child_2)
            # print("child 2",child_2)
    new_pop = []

    if len(child) != 0:
        if pop_size <= len(child):
            index = random.sample(range(0,len(child)),pop_size)
            for i in index:
                new_pop.append(child[i])
        else:
            new_pop.extend(child)
            diff = pop_size - len(child)

            # if the difference is smaller than the child length
            if diff < len(child):
                index = random.sample(range(0,len(child)),pop_size-len(child))
                for j in index:
                    new_pop.append(child[j])
            else:
            #if the difference is larger than the child length
                integer_part = int(diff/len(child))
                remaining = diff - integer_part*len(child)

                for k in range(0,integer_part):
                    index = random.sample(range(0, len(child)), len(child))
                    for j in index:
                        new_pop.append(child[j])

                index_2 = random.sample(range(0, len(child)), remaining)
                for j1 in index_2:
                    new_pop.append(child[j1])
    else:
        #After culling, the length may be short
        if len(new_pop) < pop_size:
            new_pop = copy.deepcopy(population)
            remain = pop_size - len(new_pop)
            for i in range(0,remain):
                index = random.sample(range(0,len(population)),1)
                new_pop.append(population[index[0]])
        else:
            new_pop = copy.deepcopy(population)
    # print("new pop without class",new_pop)

    for j in range (len(new_pop)):
        for ele in new_pop[j][0:map.industrial]:
            ele.append(1)
        for ele_1 in new_pop[j][map.industrial:map.industrial + map.commercial]:
            ele_1.append(2)
        for ele_2 in new_pop[j][map.industrial + map.commercial:map.industrial + map.commercial + map.residential]:
            ele_2.append(3)

    for length in range(len(new_pop)):
        for ele in new_pop[length]:
                ele[:3]

    # print("new_pop",new_pop)
    random.shuffle(new_pop)
    return new_pop

def mutation(population,ini_avail_position):

    pop_next = copy.deepcopy(population)

    ini_ap = copy.deepcopy(ini_avail_position)

    # Remove the element in position from initial available position
    for i in range(len(population)):
        for ele in population[i]:
            temp = ele[:-1]
            while temp in ini_ap:
                ini_ap.remove(temp)

        if len(ini_ap) > len(population[i]):
            index_sample = random.sample(range(0,len(ini_ap)),len(population[i]))

            for j in range(len(population[i])):
                pop_next[i][j][0] = ini_ap[index_sample[j]][0]
                pop_next[i][j][1] = ini_ap[index_sample[j]][1]
        else:
            index_sample = random.sample(range(0,len(ini_ap)),len(ini_ap))
            index_sample_2 = random.sample(range(0,len(population[i])),len(ini_ap))

            for n in range(len(index_sample)):
                pop_next[i][index_sample_2[n]][0] = ini_ap[index_sample[n]][0]
                pop_next[i][index_sample_2[n]][1] = ini_ap[index_sample[n]][1]

    for length in range(len(pop_next)):
        for ele in pop_next[length]:
                ele[:3]

    return pop_next

def GeneticAlgorithm(map,time_limit):

    colony_size = colonySize(map)
    score = []
    population = []
    temp_queue = queue.PriorityQueue()

    ini_available_position = getAvailablePosition(map)

    trial_use = []
    for _ in range(colony_size):
        temp_ini = iniPosition(map)
        population.append(temp_ini)

    start = timeit.default_timer()
    while True:
        #print("------- Loop -------" + str(__))

        del score[:]
        for index in range(len(population)):
            score.append(calculateScore(map,population[index]))

        #selection:
        population = copy.deepcopy(selection(score,population))

        #elitism:
        elite, population = elitism_selection(population,map)

        #culling:
        population = culling(population,map)
        #corss over:
        population = crossover(colony_size,population,map)

        #put elitism into it:
        population.append(elite)
        del population[0]

        #mutation:
        population = mutation(population,ini_available_position,)

        for l in range(len(population)):
            for  j in range(len(population[l])):
                population[l][j] = population[l][j][:3]

        timestamp = timeit.default_timer() - start
        for j in range(len(population)):
            temp_score = calculateScore(map, population[j])
            temp_queue.put((10000 - temp_score, [population[j],timestamp]))

        # for trial use:
        first = temp_queue.get()
        trial_use.append([10000-first[0],first[1][1]])
        temp_queue.put((first[0],[first[1][0],first[1][1]]))
        elapsedTime = timeit.default_timer() - start

        if elapsedTime > time_limit:
            break

    result = temp_queue.get()

    return result,elapsedTime,trial_use


# Genetic Algorithm:

print("------------ Urban Planning --------------")
print("Please Select Map File (text file only)")
map_trial = ReadFromFile()
# print("site number :",map_trial.siteAmount)
# print("cost Map ",map_trial.costMap)
# print("scenic view ",map_trial.scenicCoord)
# print("toxic view ",map_trial.toxicCoord)

print("Please choose: 1 for Hill Climbing. 2 for Genetic Algorithm:")
number = int(input())

if number == 1:
    print("Hill Climbing: ")
    start = timeit.default_timer()
    print("Please Input Running Time:")
    time_limit = int(input())

    result,score = hillClimbing(map_trial,time_limit)
    end = timeit.default_timer()

    print("The result: ")
    print(result)
    print("The score: "+str(score[0]))
    print("When achieved: " + str(score[1]))
    print("Elpased Time: " + str(end-start))
    printMap(result,map_trial)

elif number == 2:
    print("Genetic Algorithm:")
    print("Please Input Running Time:")
    time_limit = int(input())

    result,elapse_time,trial_use = GeneticAlgorithm(map_trial,time_limit)

    print("The result: ")
    print(result[1][0])
    print("The score: "+str(10000 - result[0]))
    print("Time acheived the score:",result[1][1])
    print("Elpased Time: " + str(elapse_time))
    printMap(result[1][0], map_trial)
else:
    print("Input Error. Please restart the program")
    exit()

x = []
y = []

for i in range(len(trial_use)):
    y.append(trial_use[i][0])
    x.append(trial_use[i][1])

###plot:
# print(trial_use)
plt.figure()

plt.plot(y, linewidth=1)  # linewidth决定绘制线条的粗细

plt.title('Genetic Algorithm (Full Version) ', fontsize=14)  # 标题
plt.xlabel('Iteration Number', fontsize=10)
plt.ylabel('Score', fontsize=10)

# plt.tick_params(axis='both', labelsize=14)  # 刻度加粗
plt.show()  # 输出图像
