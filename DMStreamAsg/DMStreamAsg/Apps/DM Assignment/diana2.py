import numpy as np
import math
import matplotlib.pyplot as plt

from scipy.cluster import hierarchy
from sklearn import datasets
from random import randint
import random

# iris = datasets.load_iris()
# X = iris.data
# arr = []
# n=0
# for i in X:
#   arr.append([i[0],i[1], i[2], i[3]])
# n = len(arr)
# print(n)

# # for i in arr:
# #   print(i)

iris = datasets.load_iris()
X = iris.data
arr = []
n=0
for i in X:
  arr.append([i[0],i[1]])
  n += 1

# print(X)
print("------------")
print(arr[0], arr[1])
print("------------")
# print(atr2)




# arr = np.array([[1, 2],[3,2],[2,5],[1,3],[6,5],[7,5],[4,6],[3,5],[4,1],[5,6],[3,8],[8,5]])
k = 3
minPoints = 0
if len(arr)%k==0:
  minPoints=len(arr)//k
else:
  minPoints = (len(arr)//k)+1
# print(len(arr))
print(minPoints)

def Euclid(a,b):
  # print(a,b)
# finding sum of squares
  sum_sq = np.sum(np.square(a - b))
  return np.sqrt(sum_sq)


# a=[]
# b=[]
# for i in arr:
#   a.append(i[0])
#   b.append(i[1])
# print(a)
# print(b)


# dismatrix =[]
# for i in range(len(arr)):
#     for j in range(i+1, len(arr)):
#       # print(arr[i], arr[j])
#       # print(arr[j])
#       dismatrix.append([i,j,Euclid(arr[i],arr[j])])


# print(dismatrix)

# from typing_extensions import IntVar
# min = 100000
# point=[]
# for i in dismatrix:
#   # print(i)
#   if i[2] < min:
#     min = i[2]
#     point = i[:2]
# point

points=[[0]]
def findPoints(point):
  min = 0
  pt=-1
  for i  in point:
    for j in range(len(arr)):
      if j in point:
        continue
      else:
        # print(arr[i], arr[j])
        dis = Euclid(np.array(arr[i]),np.array(arr[j]))
        if min < dis:
          min = dis
          # print(min)
          pt=j
  return pt

travetsedPoints=[0]
for i in range(0,k):
  if len(travetsedPoints) >= len(arr):
    break
   
  # if len(points)>=k:
  #   break

  while(len(points[i])<minPoints):
  # while(True):
    pt = findPoints(travetsedPoints)
    if pt in travetsedPoints:
      break
    travetsedPoints.append(pt)
    points[i].append(pt)
  points.append([])
points.remove([])
print(points)



# colarr = ['blue','green','red','black']

colarr = []

for i in range(k):
    colarr.append('#%06X' % randint(0, 0xFFFFFF))

# no_of_colors=k
# colarr=["#"+''.join([random.choice('0123456789ABCDEF') for i in range(6)])
#        for j in range(no_of_colors)]
# print(color)
i=0
cluster=[]
for j in range(k):
  cluster.append(j)

annotations=["Point-1","Point-2","Point-3","Point-4","Point-5"]
fig, axes = plt.subplots(1, figsize=(15, 20))
for atr in points:
  for j in range(minPoints):
    if atr[j]==-1:
      continue
    pltY = atr[j]
    pltX = cluster[i%(k+1)]
    # pltX = arr[atr[j]][0]
    # pltY = arr[atr[j]][1]
    # pltY = data.loc[:,classatr]
    plt.scatter(pltX, pltY, color=colarr[i])
    label = str("(" + str(arr[atr[j]][0]) + "," + str(arr[atr[j]][1]) + ")")
    plt.text(pltX, pltY, label)

  i += 1

plt.legend(loc=1, prop={'size':4})
plt.show()
# st.pyplot()

# colarr = ['blue','green','red','black']
j=0
def findIndex(ptarr):
  # print("Ptarr: ", ptarr)
  for j in range(len(points)):
    if ptarr in points[j]:
      return j
    
fig, axes = plt.subplots(1, figsize=(10, 7))
clusters=[]
for i in range(k):
  clusters.append([[],[]])

for i in range(len(arr)):
  j = findIndex(i)
  clusters[j%k][0].append(arr[i][0])
  clusters[j%k][1].append(arr[i][1])

  # print(i)
  # plt.scatter(arr[i][0],arr[i][1], color = colarr[j])
for i in range(len(clusters)):
  plt.scatter(clusters[i][0],clusters[i][1], color = colarr[i%k], label=cluster[i])
plt.title("Sample plot")
plt.xlabel("X Cordinate")
plt.legend(loc=1, prop={'size':15})

# plt.legend(["x*2" , "x*3"])
plt.ylabel("Y Cordinate")
plt.show()

dismatrix =[]
for i in range(len(arr)):
    for j in range(i+1, len(arr)):
      # print(arr[i], arr[j])
      # print(arr[j])
      dismatrix.append([Euclid(np.array(arr[i]),np.array(arr[j]))])
ytdist = dismatrix
Z = hierarchy.linkage(ytdist, 'ward')
plt.figure()
dn = hierarchy.dendrogram(Z)
plt.show
# hierarchy.set_link_color_palette(['m', 'c', 'y', 'k'])
# fig, axes = plt.subplots(1, 2, figsize=(8, 3))
# dn1 = hierarchy.dendrogram(Z, ax=axes[0], above_threshold_color='y',
#                            orientation='top')
# dn2 = hierarchy.dendrogram(Z, ax=axes[1],
#                            above_threshold_color='#bcbddc',
#                            orientation='right')
# hierarchy.set_link_color_palette(None)  # reset to default after use
# plt.show()