import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random




### Helper methods, you can use this or write your own.
def makeDistanceMatrix(data):
    distanceTriangle = [] #This will look like a lower diagnol matrix
    for i in range(1,len(data)): #for each instance but the first
        distances = [] #this will be a list of distances to location i
        for j in range(0,i): #only need to measure distance for objects before i
            distances.append(np.abs(data[i] - data[j]))
        distanceTriangle.append(distances)
    return distanceTriangle
    # print(data)


'''
changed this so it can update both single AND complete linkage depending on
boolean single.
'''
def updateMatrix(distances, i, j, typee):
    #create a new row
    row = []
    n = len(distances)+1
    # for single linkage
    if typee=='s':
        for col in range(n):
            if col == i+1 or col == j:
                continue
            if col > i+1:
                row.append(min(distances[col - 1][i+1], distances[col-1][j]))
            elif col > j:
                row.append(min(distances[i][col], distances[col-1][j]))
            else:
                row.append(min(distances[i][col], distances[j-1][col]))        
    # for complete linkage
    elif typee=='c':
        for col in range(n):
            if col == i+1 or col == j:
                continue
            if col > i+1:
                row.append(max(distances[col - 1][i+1], distances[col-1][j]))
            elif col > j:
                row.append(max(distances[i][col], distances[col-1][j]))
            else:
                row.append(max(distances[i][col], distances[j-1][col])) 
                
    #delete old cols
    for r in range(i+1,n-1):
        del distances[r][i+1]
    for r in range(j,n-1):
        del distances[r][j]
    #delete old rows
    del distances[i]
    del distances[max(j-1,0)]
    
    #Add row to Table
    distances.append(row)
    return distances
        

def updateGroups(groups, i, j):
    #Combine two groups
    #because table excludes first row add one to i when accessing groups which doesn't exclude first row
    newGroup = groups[i+1]+groups[j]
    #remove the old groups, start with higher number
    del groups[i+1]
    del groups[j]
    #add in the new group
    groups.append(newGroup)
    return groups

'''
Calculate the variance of a group 
- used in Ward's Minimimum Variance Clustering Method
'''
def calcVars(groups, i, j): 
    new = groups[i]+(groups[j])
    tot = 0
    avg = 0
    for x in new:
        avg += data[x]
    avg /= len(new)
    for thing in new:
        tot += (data[thing] - avg) ** 2
    return tot
        

      
    
### Five clustering methods (including additional clustering method). 
'''
Single Linkage Clustering
'''
def singleLinkage(data, k):
    group = []
    for x in data.index:
        group.append([x])
    d = makeDistanceMatrix(data)
    while len(group) > k:
        minimum=float('inf')
        row=0
        col=0
        # find minimum
        for i in range(len(d)):
            for j in range(len(d[i])):
                if d[i][j] < minimum:
                    minimum=d[i][j]
                    row=i
                    col=j
        group = updateGroups(group, row, col)
        # the 'typee='s'' updates matrix with minimum
        d = updateMatrix(d, row, col, typee='s')
    return group
 
        
 
'''
Complete Linkage Clustering
'''
def completeLinkage(data, k):
    group = []
    for x in data.index:
        group.append([x])
    d = makeDistanceMatrix(data)
    while len(group) > k:
        minimum=float('inf')
        row=0
        col=0
        # find the two clusters closest together
        for i in range(len(d)):
            for j in range(len(d[i])):
                if d[i][j] < minimum:
                    minimum=d[i][j]
                    row=i
                    col=j
        group = updateGroups(group, row, col)
        # the 'typee='c'' updates matrix with maximum rather than min
        d = updateMatrix(d, row, col, typee='c') 
    return group



'''
Average Linkage Clustering
'''
def averageLinkage(data, k):
    data = data.sort_values()
    group = []
    for x in data.index:
        group.append([x])

    #returns the average value of group
    calcAvg = lambda groups: [sum(data[group])/len(group) for group in groups]
        
    while len(group) > k:
        avgs = calcAvg(group)
        d = []
        # since data is sorted, we don't need to brute force every combination
        for i in range(len(group)-1):
            dd = avgs[i+1]-avgs[i]
            d.append(dd)
        minvalue = min(d)
        idx = d.index(minvalue)
        group[idx].extend(group[idx+1])
        group.pop(idx+1)
    return group



'''
K-Means Clustering
'''
def kMeans(data, k):
    val = []
    for idx in data.index:
        val.append(idx)
    
    group = []
    clusterNum = [] # store numeric values of the clusters
    for i in range(k):
        # pick initial guesses from the data to ensure no empty clusters in the end
        clusterNum.append( [ random.choice(data) ] ) 
        group.append([])
        
    #stores the last iterations groups
    old = []
    while True:
        # resetting groups
        for g in group:
            g.clear()
        
        for i in range(len(val)):
            low = 10000000
            for c in clusterNum:
                # if cluster is empty continue
                if not c:
                    continue                
                gap_dist = abs(c[0]-data[val[i]])
                if gap_dist < low:
                    low = gap_dist
                    g = c[0]
                    idx = clusterNum.index(c)
        
            group[idx].append(val[i])
            clusterNum[idx].append(data[val[i]])
        
        # recalculate the cluster average
        for cluster in clusterNum:
            # if cluster is empty continue
            if not cluster:
                continue            
            avg = sum(cluster)/len(cluster)
            cluster.clear()
            cluster.append(avg)
          
        # if groupings do not change two consecutive times, stop
        # make sure you have right number of final groups.
        if group == old and k == (len(group)-group.count([])):
            break
        old = group 
    return group




'''
Ward's Minimum Variance Clustering
'''
def wardMethod(data, k):
    group = []
    for x in data.index:
        group.append([x])
        
    while len(group) > k:            
        d = [[0 for x in range(len(group))] for y in range(len(group))]
  
        for i in range(len(group)):
            for j in range(i+1,len(group)):
                # stores variance after combining groups 'i' and 'j'
                d[i][j] = calcVars(group, i, j)
        ii = None
        jj = None
        minvalue = 100000000
        for i in range(len(group)):   # find min variance value
            for j in range(i+1, len(group)):
                if d[i][j] < minvalue:
                    minvalue = d[i][j]
                    ii = i
                    jj = j

        group[ii].extend(group[jj])
        group.pop(jj)
    return group




### Start Program and open file
print("\nHenry's Clustering Program.\n")
filename = input("Please enter the data-file's name: ")
# filename = "students.csv" 
dataFile = pd.read_csv(filename, index_col = 0)

### Allow User to select attribute
print("Here is a list of attributes:")
for name in dataFile.columns:
    print(name, end = "    ")
attribute = input("\nWhich attribute would you like to cluster?  ")
# attribute = 'Height'
data = dataFile.loc[:][attribute]

### Potentially plot data
toPlot = input("Would you like to plot this data? (y,n)  ")
# toPlot = 'y'
if toPlot.lower()[0] == 'y':
    plt.hist(data)
    plt.show()
#print(data)
    
### Select the Clustering Technique
print("\nWhich clustering technique would you like to use?")
print("(S)ingle linkage\n(C)omplete linkage\n(A)verage linkage\n(K)-means\n(W)ard's Variance minimizing")
clusterTechnique = input().lower()
# clusterTechnique = 'w'
k = int(input("How many clusters? "))
# k = 5
if clusterTechnique == 's':
    groups = singleLinkage(data, k)
elif clusterTechnique == 'c':
    groups = completeLinkage(data, k)
elif clusterTechnique == 'a':
    groups = averageLinkage(data, k)
elif clusterTechnique == 'k':
    groups = kMeans(data, k)
elif clusterTechnique == 'w':
    groups = wardMethod(data, k)

print("\nThe groups are:")
for g in groups:
    print()
    for name in g:
        print(name + ":", data[name])
toPlot = input("Would you like to plot the groups? (y/n)  ")
toPlot = toPlot.lower()[0]

if toPlot == 'y':
    for g in groups:
        groupData = [data[name] for name in g]
        plt.hist(groupData)
    plt.show()
  





    