from flask import Flask, request, render_template
app = Flask(__name__)

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
    sRoutes = []
    eRoutes = []
    flg = 0
    for i in TripsThroughSE.keys():
        if flg == 0:
            sRoutes = TripsThroughSE[i]
        else:
            eRoutes = TripsThroughSE[i]
        flg += 1
    print(eRoutes)
    intersection = {}
    common = []

    # init to []
    for i in sRoutes:
        intersection[i] = []
    # getting intersections
    for i in sRoutes:
        for j in eRoutes:
            if i != j:
                common = list(set(Routes[i]) & set(Routes[j]))
                # print(common)
                if common != []:
                    if intersection[i] != []:
                        c = [j, common]
                        intersection[i].append(c)
                    else:
                        c = [j, common]
                        intersection[i].append(c)

    # intersection of the form key= RouteTillIntersection, Then 1st value is route after intersection, 2nd value contains listof intersectons bw i and j
    # print(intersection)
    direct = list(set(sRoutes) & set(eRoutes))
    solution = {}

    def ChangeToName(l):
        a = []
        for i in l:
            a.append(StopNameRef[i])
        return a

    for i in intersection.keys():
        solution[RouteNameRef[i]] = []

    for i in intersection.keys():
        c1 = []
        for j in range(len(intersection[i])):
            # print(intersection[i])
            c = [RouteNameRef[intersection[i][j][0]], ChangeToName(intersection[i][j][1])]
            c1.append(c)
        solution[RouteNameRef[i]] = c1
    d = []
    for i in direct:
        d.append(RouteNameRef[i])

    if d != []:
        solution["DIRECT"] = d
    solnString = ''
    for i in solution.keys():
        if i == "DIRECT":
            solnString += "Direct Route to destination is " + solution[i][0] + '\n'
        else:
            for j in solution[i]:
                for k in j[1]:
                    solnString += "Take " + i + " till " + k + " then change to " + j[
                        0] + " till the destination" + '\n'
    print(solution.keys())
    print(len(solution))
    for i in solution.keys():
        print(len(solution[i]))
    return solution

def CheckStop(name):
    name = name.lower()
    for i in range(len(lis2)):
        if lis2[i][2].lower() == name:
            print('Found')
            return lis2[i][0]

    return -1


@app.route('/')
def my_form():
    return render_template('Input.html')

@app.route('/', methods=['POST'])
def my_form_post():
    start = request.form['text']
    end = request.form['text2']
    if CheckStop(start)==-1:
        return ("Invalid Starting Point")
    if CheckStop(end)==-1:
        return ("Invalid Destination")
    s = StopNameRefop[start]
    print(s)
    e = StopNameRefop[end]
    print(e)
    result = find(s,e)
    #updated_dict = {'108DOWN': [['234CL_UP', ['INMAS', 'DCM Chemical', 'INS Hostel', 'Vishwa Vidyalaya Metro Station', 'Nehru Vihar Crossing', 'Police Station Timarpur', 'Roop Nagar / Kamla Nagar', 'Maurice Nagar II', 'Shastri Nagar Metro Station', 'CGHC Dispensary', 'DDA Flats Lucknow Road', 'ESI Dispensary/CGHS Dispensary', 'Shakti Nagar Nangia Park', 'Shastri Nagar Shiv Mandir', 'Balak Ram Hospital', 'Shastri Nagar A Block', 'Shastri Nagar E Block', 'Zakhira', 'Subhadra Colony', 'Patel Chest', 'Chowki No 2 / Gulabi Bagh Crossing', 'Campa Cola', 'Inderlok', 'Khalsa College', 'Shri Ram College', 'Police Station Roop Nagar / Banglow Road']], ['813CLDown', ['DCM Chemical', 'Moti Nagar Market', 'INS Hostel', 'Roop Nagar / Kamla Nagar', 'Maurice Nagar II', 'Shastri Nagar Metro Station', 'ESI Dispensary/CGHS Dispensary', 'Shakti Nagar Nangia Park', 'Shastri Nagar Shiv Mandir', 'Doulat Ram College', 'Shastri Nagar E Block', 'Zakhira', 'Subhadra Colony', 'Gulabi Bagh', 'Chowki No 2 / Gulabi Bagh Crossing', 'Inderlok', 'Kirti Nagar', 'Khalsa College', 'Shri Ram College', 'Moti Nagar', 'Police Station Roop Nagar / Banglow Road']], ['778DOWN', ['DCM Chemical', 'Moti Nagar Market', 'Campa Cola', 'Inderlok', 'F Block Kirti Nagar', 'ESI Dispensary/CGHS Dispensary', 'Mayapuri Depot', 'Kirti Nagar', 'Government Press', 'PS Kirti Nagar', 'Zakhira', 'Moti Nagar', 'Wood Market']], ['816ADOWN', ['Shastri Nagar Metro Station', 'DCM Chemical', 'Moti Nagar Market', 'Chowki No 2 / Gulabi Bagh Crossing', 'Campa Cola', 'Shastri Nagar Shiv Mandir', 'ESI Dispensary/CGHS Dispensary', 'Inderlok', 'Kirti Nagar', 'Shastri Nagar A Block', 'Shastri Nagar E Block', 'Shakti Nagar Nangia Park', 'Zakhira', 'Moti Nagar', 'Police Station Roop Nagar / Banglow Road', 'Roop Nagar / Kamla Nagar', 'Maurice Nagar II']], ['816Down', ['Shastri Nagar Metro Station', 'DCM Chemical', 'Chowki No 2 / Gulabi Bagh Crossing', 'Inderlok', 'Shastri Nagar Shiv Mandir', 'ESI Dispensary/CGHS Dispensary', 'Kirti Nagar', 'Shastri Nagar A Block', 'Shastri Nagar E Block', 'Shakti Nagar Nangia Park', 'Zakhira', 'Moti Nagar', 'Police Station Roop Nagar / Banglow Road', 'Roop Nagar / Kamla Nagar', 'Maurice Nagar II']], ['816ExtDown', ['Shastri Nagar Metro Station', 'DCM Chemical', 'Chowki No 2 / Gulabi Bagh Crossing', 'Inderlok', 'Shastri Nagar Shiv Mandir', 'ESI Dispensary/CGHS Dispensary', 'Kirti Nagar', 'Shastri Nagar A Block', 'Shastri Nagar E Block', 'Shakti Nagar Nangia Park', 'Zakhira', 'Moti Nagar', 'Police Station Roop Nagar / Banglow Road', 'Roop Nagar / Kamla Nagar', 'Maurice Nagar II']], ['817ADown', ['DCM Chemical', 'Moti Nagar Market', 'Campa Cola', 'Inderlok', 'ESI Dispensary/CGHS Dispensary', 'Kirti Nagar', 'Zakhira', 'Moti Nagar']], ['817BDown', ['DCM Chemical', 'Moti Nagar Market', 'Campa Cola', 'Inderlok', 'ESI Dispensary/CGHS Dispensary', 'Kirti Nagar', 'Zakhira', 'Moti Nagar']], ['817Down', ['DCM Chemical', 'Moti Nagar Market', 'Campa Cola', 'Inderlok', 'ESI Dispensary/CGHS Dispensary', 'Kirti Nagar', 'Zakhira', 'Moti Nagar']], ['832UP', ['DCM Chemical', 'Moti Nagar Market', 'Campa Cola', 'Inderlok', 'ESI Dispensary/CGHS Dispensary', 'Kirti Nagar', 'Zakhira', 'Moti Nagar']], ['234CLEUp', ['INMAS', 'DCM Chemical', 'INS Hostel', 'Vishwa Vidyalaya Metro Station', 'Nehru Vihar Crossing', 'Police Station Timarpur', 'Roop Nagar / Kamla Nagar', 'Maurice Nagar II', 'Shastri Nagar Metro Station', 'CGHC Dispensary', 'ESI Dispensary/CGHS Dispensary', 'Shakti Nagar Nangia Park', 'Balak Ram Hospital', 'Doulat Ram College', 'Shastri Nagar A Block', 'Shastri Nagar E Block', 'Lucknow Road', 'Zakhira', 'Subhadra Colony', 'Patel Chest', 'Chowki No 2 / Gulabi Bagh Crossing', 'Campa Cola', 'Inderlok', 'Khalsa College', 'Shri Ram College', 'Police Station Roop Nagar / Banglow Road']], ['847DOWN', ['Shastri Nagar Metro Station', 'DCM Chemical', 'Moti Nagar Market', 'Campa Cola', 'Inderlok', 'Shastri Nagar Shiv Mandir', 'ESI Dispensary/CGHS Dispensary', 'Kirti Nagar', 'Shastri Nagar E Block', 'Zakhira', 'Moti Nagar']]], '73DOWN': [['108DOWN', ['DDU Hospital', 'Mayapuri Depot', 'Beriwala Bagh', 'LIG Flats', 'Hari Nagar Clock Tower', 'Government Press', 'Swarg Ashram']], ['778DOWN', ['Mayapuri Depot', 'Government Press', 'Metal Forging']]], '751Down': [['108DOWN', ['DDU Hospital', 'Mayapuri Depot', 'Beriwala Bagh', 'Hari Nagar (Mohan Mandir) Mayapuri', 'LIG Flats', 'Government Press', 'Swarg Ashram', 'Hari Nagar Clock Tower']], ['813CLDown', ['Dabri Xing', 'Dwarka Puri', 'Mahaveer Enclave Part II  and  III', 'SFS Flats Sec-2 Power House', 'New Dwarka Road / Seetapuri', 'Dwarka Sec-1 Mahalaxmi Apartment']], ['778DOWN', ['J M International School', 'Dwarka Sec 2-6', 'Mayapuri Depot', 'Dwarka Puri', 'Madhu Vihar', 'Government Press', 'Mahaveer Enclave Part II  and  III', 'SFS Flats Sec-2 Power House', 'New Dwarka Road / Seetapuri', 'Dwarka Sec-1 Mahalaxmi Apartment']], ['832UP', ['C2B Janakpuri', 'C2D Janakpuri']]], 'DIRECT': ['108DOWN']}
    return render_template('Routes.html', templateData = result)

if __name__ == '__main__':
   app.run(debug=True)