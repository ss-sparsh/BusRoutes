f = open("stop_times.txt", "r")
lines = f.read().split('\n')
lis1 = []
for i in lines:
    lis1.append(i.split(','))
lis1 = lis1[1:-1]
f.close()

f = open("stops.txt","r")
lines = f.read().split('\n')
lis2 = []
for i in lines:
    lis2.append(i.split(','))
lis2 = lis2[1:-1]
f.close()

f = open("trips.txt","r")
lines = f.read().split('\n')
lis3 = []
for i in lines:
    lis3.append(i.split(','))
lis3 = lis3[1:-1]
f.close()

f = open("routes.txt","r")
lines = f.read().split('\n')
lis4 = []
for i in lines:
    lis4.append(i.split(','))
lis4 = lis4[1:-1]
f.close()

RouteNameRef= {}
for i in range(len(lis4)):
    RouteNameRef[lis4[i][3]] = lis4[i][1]

StopNameRef = {}
for i in range(len(lis2)):
    StopNameRef[lis2[i][0]] = lis2[i][2]

StopNameRefop = {}
for i in range(len(lis2)):
    StopNameRefop[lis2[i][2]] = lis2[i][0]

RouteTripRef = {}
for i in range(len(lis3)):
    RouteTripRef[lis3[i][2]]= lis3[i][0]


#empty dictionary with all trips IDs
dic = {}
for i in range(len(lis1)):
    dic[lis1[i][0]]=[]
#adding all stops on a trip to the dictionary
for i in range(len(lis1)):
    dic[lis1[i][0]].append(lis1[i][3])

#keeping only uniuqe trips in the dictionary
ResultDic = {}
for key, value in dic.items():
    if value not in ResultDic.values():
        ResultDic[key] = value
# There 533 unique Routes

# Replacing Trip ID with uniques trip IDs
Routes = {}
for i in ResultDic.keys():
    Routes[RouteTripRef[i]] = ResultDic[i]

#Now we find all trips through start and end
TripsThroughSE={}
TripsThrough= {}
def find(start,end):
    TripsThrough[start] = []
    TripsThrough[end] = []
    for i in range(len(lis1)):
        if start == lis1[i][3]:
            TripsThrough[start].append(lis1[i][0])
        if end == lis1[i][3]:
            TripsThrough[end].append(lis1[i][0])
    for i in TripsThrough.keys():
        TripsThroughSE[i] = []

    for i in TripsThroughSE.keys():
        for j in TripsThrough[i]:
            TripsThroughSE[i].append(RouteTripRef[j])
    #keeping unique Route IDs only
    for i in TripsThroughSE.keys():
        op=[]
        for j in TripsThroughSE[i]:
            if j not in op:
                op.append(j)
        TripsThroughSE[i]=op


find('978','105')
#print(TripsThroughSE)
sRoutes=[]
eRoutes=[]
flg=0
for i in TripsThroughSE.keys():
    if flg==0:
        sRoutes=TripsThroughSE[i]
    else:
        eRoutes=TripsThroughSE[i]
    flg+=1
print(eRoutes)
intersection = {}
common=[]

#init to []
for i in sRoutes:
    intersection[i]=[]
#getting intersections
for i in sRoutes:
    for j in eRoutes:
        if i!=j:
            common = list(set(Routes[i])&set(Routes[j]))
            #print(common)
            if common!=[]:
                if intersection[i]!=[]:
                    c = [j, common]
                    intersection[i].append(c)
                else:
                    c=[j,common]
                    intersection[i].append(c)

#intersection of the form key= RouteTillIntersection, Then 1st value is route after intersection, 2nd value contains listof intersectons bw i and j
#print(intersection)
direct = list(set(sRoutes)&set(eRoutes))
solution ={}
def ChangeToName(l):
    a=[]
    for i in l:
        a.append(StopNameRef[i])
    return a

for i in intersection.keys():
    solution[RouteNameRef[i]]=[]

for i in intersection.keys():
    c1=[]
    for j in range(len(intersection[i])):
        #print(intersection[i])
        c = [RouteNameRef[intersection[i][j][0]],ChangeToName(intersection[i][j][1])]
        c1.append(c)
    solution[RouteNameRef[i]] = c1
d=[]
for i in direct:
   d.append(RouteNameRef[i])

if d != []:
    solution["DIRECT"] = d
solnString = ''
for i in solution.keys():
    if i == "DIRECT":
        solnString+="Direct Route to destination is "+solution[i][0]+'\n'
    else:
        for j in solution[i]:
            for k in j[1]:
                solnString+="Take "+i+" till "+ k + " then change to "+ j[0]+" till the destination"+'\n'
print(solution.keys())
print(len(solution))
for i in solution.keys():
    print(len(solution[i]))