import xlrd
import xdrlib, sys
import random
import matplotlib as mpl
import matplotlib.pyplot as plt

def open_file():
    data = xlrd.open_workbook('CS534 assignment 2 network.xlsx')
    table = data.sheet_by_name('Sheet1')
    nrows = table.nrows
    colnames = table.row_values(0)
    list =[]
    for rownum in range(0, nrows):
        row = table.row_values(rownum)
        if row:
            app = []
            for i in range(len(colnames)):
                if row[i]:
                    app.append(row[i])
            list.append(app)
    return list

def load_input():
    str = input('Please input:').split()
    query_node=str[1]
    iteration_num=str[-3]
    discard_num=str[-1]
    evidence=str[2:-4]
    return query_node,iteration_num,discard_num,evidence

def set_start_state(level,state):
    if level[0]==0:
        state[0]=random.choice(['lots', 'little'])
    if level[1]==0:
        state[1]=random.choice(['bad', 'good'])
    if level[2]==0:
        state[2]=random.choice(['bad', 'good'])
    if level[3]==0:
        state[3]=random.choice(['old', 'new'])
    if level[4]==0:
        state[4]=random.choice(['good', 'bad', 'ugly'])
    if level[5]==0:
        state[5]=random.choice(['small', 'medium', 'large'])
    if level[6]==0:
        state[6]=random.choice(['bad', 'good'])
    if level[7]==0:
        state[7]=random.choice(['cheap', 'ok', 'expensive'])
    return state

def one_iteration(list, level, state):
    if level[0] == 0:
        for i in range(11, 15):
            if list[i][1] == state[1]:
                if list[i][0] == 'lots':
                    p1 = list[i][list[10].index(state[4])]
                if list[i][0] == 'little':
                    p2 = list[i][list[10].index(state[4])]
        p_lots1 = list[2][1]*p1
        p_little1 = list[3][1]*p2
        a = 1/(p_little1+p_lots1)
        p_lots = a*p_lots1
        p_little = a*p_little1
        state[0] = random.choices(['lots', 'little'], [p_lots, p_little])[0]

    if level[1] == 0:
        for i in range(11, 15):
            if list[i][0] == state[0]:
                if list[i][1] == 'bad':
                    p1 = list[i][list[10].index(state[4])]
                if list[i][1] == 'good':
                    p2 = list[i][list[10].index(state[4])]
        p_bad1 = list[6][1]*p1*list[18][list[17].index(state[2])]
        p_good1 = list[7][1]*p1*list[19][list[17].index(state[2])]
        a = 1 / (p_bad1 + p_good1)
        p_bad = a*p_bad1
        p_good = a*p_good1
        state[1] = random.choices(['bad', 'good'], [p_bad, p_good])[0]

    if level[2] == 0:
        p_bad1 = list[18][list[17].index(state[1])]*list[28][list[27].index(state[-2])]
        p_good1 = list[18][list[17].index(state[1])]*list[29][list[27].index(state[-2])]
        a = 1 / (p_bad1 + p_good1)
        p_bad = a*p_bad1
        p_good = a*p_good1
        state[2] = random.choices(['bad', 'good'], [p_bad, p_good])[0]

    if level[3]==0:
        for i in range(33, 36):
            if list[i][0] == state[4]:
                p1=list[i][1]
                p2=list[i][2]
        for i in range(39, 75):
            if list[i][0] == state[4]:
                if list[i][2] == state[-2]:
                    if list[i][3] == state[-3]:
                        if list[i][1] == 'old':
                            p11 = list[i][list[38].index(state[-1])]
                        if list[i][1] == 'new':
                            p22 = list[i][list[38].index(state[-1])]
        p_old1=p1*p11
        p_new1=p2*p22
        a = 1 / (p_old1 + p_new1)
        p_old = a*p_old1
        p_new= a*p_new1
        state[3] = random.choices(['old', 'new'], [p_old, p_new])[0]

    if level[4]==0:
        for i in range(11,15):
            if list[i][0] == state[0]:
                if list[i][1] == state[1]:
                    p1 = list[i][2]
                    p2 = list[i][3]
                    p3 = list[i][4]
        p11 = list[33][list[32].index(state[3])]
        p22 = list[34][list[32].index(state[3])]
        p33 = list[35][list[32].index(state[3])]
        for i in range(39, 75):
            if list[i][1] == state[3]:
                if list[i][2] == state[-2]:
                    if list[i][3] == state[-3]:
                        if list[i][0] == 'good':
                            p111 = list[i][list[38].index(state[-1])]
                        if list[i][0] == 'bad':
                            p222 = list[i][list[38].index(state[-1])]
                        if list[i][0] == 'ugly':
                            p333 = list[i][list[38].index(state[-1])]

        p_good1 = p1*p11*p111
        p_bad1 = p2*p22*p222
        p_ugly1 = p3*p33*p333
        a = 1 / (p_good1 + p_bad1+p_ugly1)
        p_good = a*p_good1
        p_bad = a*p_bad1
        p_ugly = a*p_ugly1
        state[4] = random.choices(['good', 'bad', 'ugly'], [p_good, p_bad, p_ugly])[0]

    if level[5] == 0:
        for i in range(39, 75):
            if list[i][0] == state[4]:
                if list[i][1] == state[3]:
                    if list[i][2] == state[-2]:
                        if list[i][3] == 'small':
                            p1 = list[i][list[38].index(state[-1])]
                        if list[i][3] == 'medium':
                            p2 = list[i][list[38].index(state[-1])]
                        if list[i][3] == 'large':
                            p3 = list[i][list[38].index(state[-1])]
        p_small1 = p1*list[22][1]
        p_medium1 = p2*list[23][1]
        p_large1 = p3*list[24][1]
        a = 1 / (p_small1 + p_medium1+p_large1)
        p_small = a*p_small1
        p_medium = a*p_medium1
        p_large = a*p_large1
        state[5] = random.choices(['small', 'medium', 'large'], [p_small, p_medium, p_large])[0]

    if level[6]==0:
        for i in range(39, 75):
            if list[i][0] == state[4]:
                if list[i][1] == state[3]:
                    if list[i][3] == state[-3]:
                        if list[i][2] == 'bad':
                            p1 = list[i][list[38].index(state[-1])]
                        if list[i][2] == 'good':
                            p2 = list[i][list[38].index(state[-1])]
        for i in range(28,30):
            if list[i][0] == state[2]:
                p11 = list[i][1]
                p22 = list[i][2]
        p_bad1 = p11*p1
        p_good1 = p22*p2
        a = 1 / (p_bad1 + p_good1)
        p_bad = a*p_bad1
        p_good= a*p_good1
        state[6] = random.choices(['bad', 'good'], [p_bad, p_good])[0]

    if level[7]==0:
        for i in range(39, 75):
            if list[i][0] == state[4]:
                if list[i][1] == state[3]:
                    if list[i][2] == state[-2]:
                        if list[i][3] == state[-3]:
                            p_cheap = list[i][4]
                            p_ok = list[i][5]
                            p_expensive = list[i][6]
        state[7] = random.choices(['cheap', 'ok', 'expensive'], [p_cheap, p_ok, p_expensive])[0]
    return state

def gibbs_sampling():
    list = open_file()
    query_node, iteration_num, discard_num, evidence = load_input()
    mk = ['amenities', 'neighborhood', 'children', 'age', 'location', 'size', 'schools', 'price']
    level=[0,0,0,0,0,0,0,0]
    state=[0,0,0,0,0,0,0,0]
    for i in range(len(evidence)):
        a = evidence[i].split('=')
        level[mk.index(a[0])]=1
        state[mk.index(a[0])]=a[1]
    state = set_start_state(level, state)
    discard = int(discard_num)
    m=0
    n=0
    k=0
    result=[]
    for i in range(int(iteration_num)):
        state = one_iteration(list, level, state)
        if discard == 0:
            if mk.index(query_node) == 0:
                if state[0] == 'lots':
                    m=m+1
                else:
                    n=n+1
                result.append([m/(m+n),n/(m+n)])
            if mk.index(query_node) == 1:
                if state[1] == 'bad':
                    m=m+1
                else:
                    n=n+1
                result.append([m/(m+n), n/(m+n)])
            if mk.index(query_node) == 2:
                if state[2] == 'bad':
                    m=m+1
                else:
                    n=n+1
                result.append([m/(m+n), n/(m+n)])
            if mk.index(query_node) == 3:
                if state[3] == 'old':
                    m=m+1
                else:
                    n=n+1
                result.append([m/(m+n), n/(m+n)])
            if mk.index(query_node) == 4:
                if state[4] == 'good':
                    m=m+1
                elif state[4] == 'bad':
                    n=n+1
                else:
                    k=k+1
                result.append([m/(m+n+k), n/(m+n+k), k/(m+n+k)])
            if mk.index(query_node) == 5:
                if state[5] == 'small':
                    m=m+1
                elif state[5] == 'medium':
                    n=n+1
                else:
                    k=k+1
                result.append([m/(m+n+k), n/(m+n+k), k/(m+n+k)])
            if mk.index(query_node) == 6:
                if state[6] == 'bad':
                    m=m+1
                else:
                    n=n+1
                result.append([m/(m+n), n/(m+n)])
            if mk.index(query_node) == 7:
                if state[7] == 'cheap':
                    m=m+1
                elif state[7] == 'ok':
                    n=n+1
                else:
                    k=k+1
                result.append([m/(m+n+k), n/(m+n+k), k/(m+n+k)])
        else:
            discard = discard-1

    return query_node, m, n, k, result

mk = ['amenities', 'neighborhood', 'children', 'age', 'location', 'size', 'schools', 'price']
query_node, m, n, k, result = gibbs_sampling()
if mk.index(query_node) == 0:
    print('P(amenities=lots)=', m / (m + n))
    print('P(amenities=little)=', n / (m + n))
    y1 = [x[0] for x in result]
    y2 = [x[1] for x in result]
    plt.plot(y1, "x-", label="P(amenities=lots)", linewidth=0.5)
    plt.plot(y2, "+-", label="P(amenities=little)", linewidth=0.5)
if mk.index(query_node) == 1:
    print('P(neighborhood=bad)=', m / (m + n))
    print('P(neighborhood=good)=', n / (m + n))
    y1 = [x[0] for x in result]
    y2 = [x[1] for x in result]
    plt.plot(y1, label="P(neighborhood=bad)", linewidth=0.5)
    plt.plot(y2, label="P(neighborhood=good)", linewidth=0.5)
if mk.index(query_node) == 2:
    print('P(children=bad)=', m / (m + n))
    print('P(children=good)=', n / (m + n))
    y1 = [x[0] for x in result]
    y2 = [x[1] for x in result]
    plt.plot(y1, label="P(children=bad)", linewidth=0.5)
    plt.plot(y2, label="P(children=good)", linewidth=0.5)
if mk.index(query_node) == 3:
    print('P(age=old)=', m / (m + n))
    print('P(age=new)=', n / (m + n))
    y1 = [x[0] for x in result]
    y2 = [x[1] for x in result]
    plt.plot(y1, label="P(age=old)", linewidth=0.5)
    plt.plot(y2, label="P(ge=new)", linewidth=0.5)
if mk.index(query_node) == 4:
    print('P(location=good)=', m / (m + n + k))
    print('P(location=bad)=', n / (m + n + k))
    print('P(location=ugly)=', k / (m + n + k))
    y1 = [x[0] for x in result]
    y2 = [x[1] for x in result]
    y3 = [x[2] for x in result]
    plt.plot(y1, label="P(location=good)", linewidth=0.5)
    plt.plot(y2, label="P(location=bad)", linewidth=0.5)
    plt.plot(y3, label="P(location=ugly)", linewidth=0.5)
if mk.index(query_node) == 5:
    print('P(size=small)=', m / (m + n + k))
    print('P(size=medium)=', n / (m + n + k))
    print('P(size=large)=', k / (m + n + k))
    y1 = [x[0] for x in result]
    y2 = [x[1] for x in result]
    y3 = [x[2] for x in result]
    plt.plot(y1, label="P(size=small)", linewidth=0.5)
    plt.plot(y2, label="P(size=medium)", linewidth=0.5)
    plt.plot(y3, label="P(size=large)", linewidth=0.5)
if mk.index(query_node) == 6:
    print('P(schools=bad)=', m / (m + n))
    print('P(schools=good)=', n / (m + n))
    y1 = [x[0] for x in result]
    y2 = [x[1] for x in result]
    plt.plot(y1, label="P(schools=bad)", linewidth=0.5)
    plt.plot(y2, label="P(schools=good)", linewidth=0.5)
if mk.index(query_node) == 7:
    print('P(price=cheap)=', m / (m + n + k))
    print('P(price=ok)=', n / (m + n + k))
    print('P(price=expensive)=', k / (m + n + k))
    y1 = [x[0] for x in result]
    y2 = [x[1] for x in result]
    y3 = [x[2] for x in result]
    plt.plot(y1, label="P(price=cheap)", linewidth=0.5)
    plt.plot(y2, label="P(price=ok))", linewidth=0.5)
    plt.plot(y3, label="P(price=expensive)", linewidth=0.5)
plt.xlabel('iteration')
plt.ylabel('probability')
plt.grid(True)
plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)
plt.show()