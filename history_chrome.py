import sqlite3
from datetime import datetime, timedelta
import webbrowser
import numpy as np
from urlparse import urlparse
from NN3 import *
import os
from shutil import copyfile

def dayToTimestamp(y=1970, m=1, d=1, h = 0, dt =0):
    startTime = datetime(year=1601, month=1,day=1)
    endTime = datetime(year = y, month = m, day = d, hour = h)
    if dt <>0:
        endTime =dt
    return long((endTime-startTime).total_seconds()*1000000//1)

def task(urls):
    url = urls
    webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open(url)

def timestampToDay(ts):
    #timestamp =13127085219994151
    epoch = datetime(1601, 1, 1)
    day = epoch+ timedelta(microseconds=ts)
    return day
    
def getTableCol(cursor, tbName):
    rows = cursor.execute("select * from "+tbName)
    #names = list(map(lambda x: x[0], cursor.description))
    names = [description[0] for description in cursor.description]
    return names
                   
def lastVisitSinceNow(ts, tnow=0): #hours since last visit
    lv=timestampToDay(ts)
    if tnow==0:
        c = datetime.utcnow()
    else:
        c = tnow
    delta = c-lv
    return delta.total_seconds()/3600
    

def getDayFN(d=100):
    c = datetime.utcnow()
    c= c-timedelta(days=d)
    return c

#C:\Users\%%USER%%\AppData\Local\Google\Chrome\User Data\Default\History


filename = "C:\Users\%%USER%%\AppData\Local\Google\Chrome\User Data\Default\History"

copyfile(filename, "History_T")
fd = os.open(filename, os.O_RDONLY)
#print "???", os.read(fd, 2000)
conn = sqlite3.connect("History_T")
#conn = sqlite3.connect('3')
#c = sqlite3.connect('/dev/fd/%d' %fd)
#conn = sqlite3.connect(fd)
#os.close(fd)
 
#conn = sqlite3.connect('file:History',uri=True)
c = conn.cursor()


d = getDayFN(100)
d100ts = dayToTimestamp(d.year, d.month, d.day)

######inputs for NN: website had not visited in last 100days considered not important
VC = {}
HSLV = {}
qsHSLV = "SELECT id, url, visit_count, last_visit_time FROM urls "\
         "WHERE last_visit_time > " + str(d100ts)
print qsHSLV

VCLW = {}
qsVCLW = "SELECT urls.id, urls.url, urls.visit_count, count(*) as vct FROM urls INNER JOIN visits "\
         "WHERE urls.id == visits.url AND visits.visit_time < " \
         ""+str(dayToTimestamp(dt=datetime.utcnow()))+" AND visits.visit_time >"+ str(dayToTimestamp(dt = datetime.utcnow()-timedelta(days=7))) + " group by visits.url order by vct DESC"



######outputs for NN
# website visited last three days sort by visit count in that peroid
DWS={}
qsDWS = "SELECT urls.id, urls.url, urls.visit_count, count(*) as vct FROM urls INNER JOIN visits "\
      "WHERE urls.id == visits.url AND visits.visit_time < " \
      ""+str(dayToTimestamp(dt=datetime.utcnow()))+" AND visits.visit_time >"+ str(dayToTimestamp(dt = datetime.utcnow()-timedelta(days=3))) + " group by visits.url order by vct DESC"

# visiting ocurance between time stamps _END_TIME_STAMP_, _START_TIME_STAMP_ to be replaced at before sql query
TSWC={}
qsTSWC = "SELECT urls.id, urls.url, urls.visit_count, count(*) as vct FROM urls INNER JOIN visits "\
      "WHERE urls.id == visits.url AND visits.visit_time < " \
      "_END_TIME_STAMP_ AND visits.visit_time > _START_TIME_STAMP_ " + " group by visits.url order by vct DESC"



# Training Data Set: history before July 1st 2016
d100tsT=dayToTimestamp(2016,10,05)

Lookup={}

VC_Tr = {}
HSLV_Tr = {}
qsHSLV_Tr = "SELECT urls.id, urls.url, urls.visit_count, visits.visit_time FROM urls INNER JOIN visits "\
            "WHERE urls.id = visits.url AND visits.visit_time > " + str(d100tsT)  +  " AND visits.visit_time"\
            " < " +str(dayToTimestamp(2016,12,1)) +" order by visits.visit_time"

VCLW_Tr = {}
qsVCLW_Tr = "SELECT urls.id, urls.url, urls.visit_count, count(*) as vct FROM urls INNER JOIN visits "\
         "WHERE urls.id == visits.url AND visits.visit_time < " \
         ""+str(dayToTimestamp(2016,12,1))+" AND visits.visit_time > "+ str(dayToTimestamp(2016,11,25)) + " group by visits.url order by vct DESC"

DWS_Tr ={}
qsDWS_Tr = "SELECT urls.id, urls.url, urls.visit_count, count(*) as vct FROM urls INNER JOIN visits "\
      "WHERE urls.id == visits.url AND visits.visit_time < " \
      ""+str(dayToTimestamp(2016,12,1))+" AND visits.visit_time > "+ str(dayToTimestamp(2016,11,28)) + " group by visits.url order by vct DESC"

DWS_Tr2 ={}
qsDWS_Tr2 = "SELECT urls.id, urls.url, urls.visit_count, count(*) as vct FROM urls INNER JOIN visits "\
      "WHERE urls.id == visits.url AND visits.visit_time < " \
      ""+str(dayToTimestamp(2016,12,1))+" AND visits.visit_time > "+ str(dayToTimestamp(2016,11,28)) + " group by visits.url order by vct DESC"



TSWC_Tr={}
qsTSWC_Tr = "SELECT urls.id, urls.url, urls.visit_count, count(*) as vct FROM urls INNER JOIN visits "\
      "WHERE urls.id == visits.url AND visits.visit_time < " \
      "A_END_TIME_STAMP_A AND visits.visit_time > A_START_TIME_STAMP_A " + " group by visits.url order by vct DESC"



sql_select = """ SELECT datetime(last_visit_time/1000000-11644473600,'unixepoch','localtime'),
                        url 
                 FROM urls
                 ORDER BY last_visit_time DESC
             """

'''
SELECT DATE(FROM_UNIXTIME(MyTimestamp)) AS ForDate,
        COUNT(*) AS NumPosts
 FROM   MyPostsTable
 GROUP BY DATE(FROM_UNIXTIME(MyTimestamp))
 ORDER BY ForDate
'''

print "hslv_tr",VC_Tr

for row in c.execute(qsHSLV_Tr):
    VC_Tr.update({str(row[0]):row[2]})    
    HSLV_Tr.update({str(row[0]):lastVisitSinceNow(row[3], datetime(year = 2016, month = 12, day = 1) )})
    VCLW_Tr.update({str(row[0]):0})
    DWS_Tr.update({str(row[0]):0})
    TSWC_Tr.update({str(row[0]):0})
for row in c.execute(qsVCLW_Tr):
    VCLW_Tr.update({str(row[0]):row[2]})
for row in c.execute(qsDWS_Tr):
    DWS_Tr.update({str(row[0]):row[3]})


for day in range(10):
    startTs = str(dayToTimestamp(dt = datetime(year = 2016, month = 12, day = 1)-timedelta(days=day+1)))
    endTs = str(dayToTimestamp(dt = datetime(year = 2016, month = 12, day = 1)-timedelta(days=day)))

    qsTSWC_Tr = qsTSWC_Tr.replace("A_END_TIME_STAMP_A", endTs)
    qsTSWC_Tr = qsTSWC_Tr.replace("A_START_TIME_STAMP_A", startTs)
    for row in c.execute(qsTSWC_Tr):
        #print "TTTTTTTTTTTTTT", TSWC_Tr[str(row[0])]
        TSWC_Tr[str(row[0])] +=1 
        #print TSWC_Tr[str(row[0])]



for row in c.execute(qsHSLV):
    Lookup.update({str(row[0]):str(row[1])})
    VC.update({str(row[0]):row[2]})    
    HSLV.update({str(row[0]):lastVisitSinceNow(row[3])})
    VCLW.update({str(row[0]):0})
    DWS.update({str(row[0]):0})
    TSWC.update({str(row[0]):0})

for row in c.execute(qsVCLW):
    VCLW.update({str(row[0]):row[2]})
for row in c.execute(qsDWS):
    DWS.update({str(row[0]):row[3]})

ci=0
cj=0

qsHSLV = "SELECT id, url, visit_count, last_visit_time FROM urls "\
         "WHERE last_visit_time > " + str(d100ts)


qsTSWC = "SELECT urls.id, urls.url, urls.visit_count, count(*) as vct FROM urls INNER JOIN visits "\
      "WHERE urls.id == visits.url AND visits.visit_time < " \
      "_END_TIME_STAMP_ AND visits.visit_time > _START_TIME_STAMP_ " + " group by visits.url order by vct DESC"


for day in range(10):
    startTs = str(dayToTimestamp(dt = datetime.utcnow()-timedelta(days=day+1)))
    print "test", datetime.utcnow()-timedelta(days=day+1)
    endTs = str(dayToTimestamp(dt = datetime.utcnow()-timedelta(days=day)))
    print "test", datetime.utcnow()-timedelta(days=day)
    
    qsTSWC=qsTSWC.replace("_END_TIME_STAMP_", endTs)
    qsTSWC= qsTSWC.replace("_START_TIME_STAMP_", startTs)
    print qsTSWC
    for row in c.execute(qsTSWC):
        try:
            TSWC[str(row[0])] +=1
        except:
            pass



print len(VC_Tr)
print len(HSLV_Tr)
print len(VCLW_Tr)
print len(DWS_Tr)


#conn.close()
#conn = sqlite3.connect('C:\Users\%%USER%%\AppData\Local\Google\Chrome\User Data\Default\History')#C:\Users\%%USER%%\AppData\Local\Google\Chrome\User Data\Default
#c = conn.cursor()

#print hoursSinceLastVisit_Tr


# Test Data Set: history before Oct 1st 2016
print getTableCol(c, "visits")
#print getTableCol(c, "segment_usage")
#where DateOrdered between '2011-11-01' and '2011-11-30' group by url
#SELECT url , visit_count, last_visit_time FROM urls
#ts = dayToTimestamp(2016,10,1,0)
#print timestampToDay(ts)



queryString = "SELECT url, id,visit_count, last_visit_time FROM urls WHERE last_visit_time > " +  str(dayToTimestamp(2016,10,6)) +" AND last_visit_time <"+ str(dayToTimestamp(2016,10,7)) +" ORDER BY last_visit_time"
queryStringTwo = "SELECT urls.url, urls.visit_count, count(*) as vct FROM urls INNER JOIN visits "\
                                "WHERE urls.id == visits.url AND visits.visit_time > " \
                                ""+str(dayToTimestamp(2016,10,1)) +" AND visits.visit_time <"+ str(dayToTimestamp(2016,10,7)) + " group by visits.url order by vct DESC"


queryString8 = "SELECT urls.url, urls.visit_count, count(*) as vct FROM urls INNER JOIN visits "\
                                "WHERE urls.id == visits.url AND visits.visit_time > " \
                                ""+str(dayToTimestamp(2016,10,6, 0)) +" AND visits.visit_time <"+ str(dayToTimestamp(2016,10,7,0)) + " group by visits.url order by vct desc"

#sql inject
#print queryStringTwo

queryString3 = "SELECT urls.url, urls.visit_count FROM urls  "\
                            "order by visit_count desc"
queryString6 = "SELECT urls.url, urls.visit_count FROM urls  "\
                            "WHERE urls.id=2024 and urls.last_visit_time > " \
                            ""+str(dayToTimestamp(2016,11,1)) +" AND urls.last_visit_time <"+ str(dayToTimestamp(2016,11,7)) + " "\
                            "order by visit_count desc"


                            # "WHERE urls.last_visit_time > " \
                            #""+str(dayToTimestamp(2008,10,1)) +" AND urls.last_visit_time <"+ str(dayToTimestamp(2016,12,7)) + " "\

queryString5= "select url, id, visit_count from urls where id =2024 order by visit_count desc"


queryString7 = "SELECT urls.url, segments.name, segments.id FROM urls INNER JOIN segments "\
                                "WHERE urls.id == segments.url_id "

q8 = "select * from visits order by visit_time "
i=0

for row in c.execute(q8):
    #  timestamp = long(row[2])
    #last_v = epoch + timedelta(microseconds=timestamp)
    #print (datetime.now() - last_v ).total_seconds()
    #last_v = str(last_v)

    #urlMatch.append(row[0])
    #visitCount.append(row[1])
    #lastVisitTime = row[2]    
    #print row[5]
    print row[0], "total count ", row[1], "time:", timestampToDay(row[2]), "last vist since now(hrs):", lastVisitSinceNow(row[5])    #,"TIMES, LAST VISTED AT", last_v
    #tasks(row[0])
    i =i+1
    if i >=2:
        break
conn.close()

def NN3_Step(a, b, HSLV, VC, VCLW, DWS, TSWC,thetaold =0, stru=[3,1,3], n =20000, test=0):
    thresh =0.1
    keys = np.asarray(HSLV.keys())
    hslv = np.asarray(HSLV.values())
    hslv = 1/(1+np.exp(-hslv/20+5)) #-hslv/20+5
    vc = np.asarray(VC.values())
    vc = 1/(1+np.exp(-vc/20+5))
    vclw = np.asarray(VCLW.values())
    tswc = np.asarray(TSWC.values())
    tswc = 1/(1+np.exp(-tswc/1.2+5))

    aaa= np.array([vc[a:b],hslv[a:b],vclw[a:b],tswc[a:b]])
    Xw = aaa.T
    Yw = np.array([DWS.values()[a:b]]).T
    Yw= 1/(1+np.exp(-Yw/2+3)) #-Yw/2+5
    XY = np.concatenate((Xw, Yw), axis=1)
    theta = networkStructure(stru, Xw, Yw)
    if thetaold<>0:
        theta[3] = thetaold[3]
        print "EE",theta[3]
        #print "here"
    for i in range(n):
        theta = runOnce(theta, test)
    res = theta[0][-1]
    #print res
    np.set_printoptions(suppress=True)
    np.set_printoptions(precision =3)

    compare =np.concatenate((XY, res), axis=1)
    #print compare.dtype
    #print res.T[0]

    keysF= keys[a:b]
    keyI =[]
    for key in keysF:
        keyI.append(int(key))
    print keysF
    #print keyI
    keyA = np.array([keyI])
    print keyA.T
    

    Result = np.concatenate((keyA.T,compare),axis=1)
    Resultf = np.compress((res.T[0]>thresh),Result, axis =0)
    cpp= np.compress((res.T[0]>thresh),compare,axis=0)
    cpp0 = np.compress((Yw.T[0]>thresh),compare,axis=0)
    if 0:
        1
        print compare
        print len(compare)
        print " "
        print cpp0
        print " "
        print cpp

    print len(cpp0), len(cpp)
    if test ==1:
        print "nn structure", stru
        print "test data", a, b
        print "threshhold", thresh
    print "missed =", len(np.compress((cpp0[:,5]<thresh),cpp0,axis=0))
    print "wrong predictions =", len(np.compress((cpp[:,4]<thresh),cpp,axis=0))
    return theta, len(cpp0), len(cpp), Resultf


def Prediction(HSLV, VC, VCLW, DWS,TSWC, Lookup={}):
    print len(VC)
    print len(HSLV)
    print len(VCLW)
    print len(DWS)

    synapse = [np.array([[ -0.032,   4.38 ,  -1.96 ,  -3.615,  -3.343],
       [ 17.744, -18.477,  39.245,  79.456,  39.633],
       [  0.307,   0.1  ,   0.107,  -4.589,   0.745]]), np.array([[ -8.057],
       [ 21.462],
       [ 30.849],
       [-57.632],
       [ 31.837]])]

    synapse = [np.array([[  0.871,  -2.049,  -2.153],
       [ 20.126,  10.431, -25.642],
       [  6.047,  -0.008,  -6.837],
       [  1.323,  -3.272,  -3.519]]), np.array([[ 1.629],
       [-4.497],
       [ 2.844]]), np.array([[ -1.521, -12.585,  -5.509]]), np.array([[ 1.214],
       [-9.002],
       [-1.299]])]       

    print synapse
    thetaold = [0,0,0,synapse,0,0]
    theta,o,f, r= NN3_Step(0,9200,HSLV, VC, VCLW , DWS, TSWC, thetaold, n=1, test =1)
    print theta[3]
    print r
    print int(r[0][0])
    '''
    i = 0
    for x in Lookup:
        print "lllllLLLL", x
        i+=1
        if i > 10:
            break
    '''
    
    domains =[]
    order =np.argsort(r, axis=0)
    ranka = np.argsort(order, axis =0)
    rank = ranka[:,1]
    rankL =[]
    print len(r)
    for i in range(len(r)):
        #print Lookup[str(int(r[i][0]))]
        parsed_uri = urlparse( Lookup[str(int(r[i][0]))] )
        #rank[i]
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        domain = domain[domain.find("//")+2:-1]
        if domain not in domains:
            domains.append(domain)
            rankL.append(rank[i])
        else:
            ind=domains.index(domain)
            rankL[ind] = rankL[ind] + rank[i]

    domainrank = zip(domains, rankL)
    
    domainrankS = sorted(domainrank, key=lambda x: x[1], reverse = True)

    i=0
    for x in domainrankS:
        print x[0]
        #task(x[0])
        i +=1
        if i >20:
            break
    print len(domains)
    
    


def Train_NN3(HSLV_Tr, VC_Tr, VCLW_Tr,DWS_Tr, TSWC_Tr):

    ast =0
    bst =99
    tsize =1000

    a=ast
    b=bst
    incrm=100
    thetaold =0

    auto =1
    rpt =0
    rptn=18
    conti = 1
    loop =0

    while auto:
        theta,o,f,r = NN3_Step(a,b,HSLV_Tr, VC_Tr, VCLW_Tr,DWS_Tr, TSWC_Tr, thetaold)
        #print "error", theta[1][2].T[0]
        print len(theta[1][2])
        #print len(theta[2])-1
        #print "ss", ss
        #print sum(abs(theta[1][len(theta[2])-1].T[0]))
        se = sum(pow(theta[1][len(theta[2])-1].T[0],2))
        print "sum", se
        if o==f:#(se<0.1 and o==f) or se<0.01:
            conti =1
            rpt = 0 
        else:
            print "r", rpt," ", b
            tehtaold =theta
            conti=0
            rpt +=1
            if rpt >rptn:
                conti =1
                rpt =0
        if conti ==1:
            print "c"
            a +=incrm
            b +=incrm
            conti =0
            print b
            if b >ast+tsize:
                print theta[3]
                if loop <0:
                    a=ast
                    b=bst
                    loop +=1
                else:
                    print "\ntrain data range", ast, ast+tsize
                    break
            thetaold=theta

        synapse = theta[3]
    if auto:
        theta,o,f, r= NN3_Step(0,5800,HSLV_Tr, VC_Tr, VCLW_Tr,DWS_Tr, TSWC_Tr, thetaold, n=1, test =1)
        print theta[3]

    while auto<>1:
        theta,o,f, r= NN3_Step(a,b,HSLV_Tr, VC_Tr, VCLW_Tr,DWS_Tr, TSWC_Tr, thetaold)
        key =raw_input("select q,r,c...")
        #print ("select q, c, r...")
        #key = m.getch()
        #print key
        if key == 'q':
            print theta[3]
            break
        if key == '':
            print "c"
            a +=incrm
            b +=incrm
            thetaold=theta
            #theta= NN3_Step(a,b,HSLV_Tr, VC_Tr, VCLW_Tr,DWS_Tr, thetaold)
            #print a, b
        if key == 'r':
            thetaold = theta
            #theta= NN3_Step(a,b,HSLV_Tr, VC_Tr, VCLW_Tr,DWS_Tr, thetaold)
        

def main():
    Prediction(HSLV, VC, VCLW, DWS, TSWC, Lookup)
    #Train_NN3(HSLV_Tr, VC_Tr, VCLW_Tr,DWS_Tr, TSWC_Tr)


if __name__== "__main__":
    main()



#### information from: https://digital-forensics.sans.org/blog/2010/01/21/google-chrome-forensics/

'''
The database file that contains the browsing history is stored under the Default folder as "History" and can be examined using any SQLlite browser there is (such as sqlite3). The available tables are:

downloads
presentation
urls
keyword_search_terms
segment_usage
visits
meta
segments




SELECT urls.url, urls.title, urls.visit_count, urls.typed_count, urls.last_visit_time, urls.hidden, visits.visit_time, visits.from_visit, visits.transitionFROM urls, visitsWHERE urls.id = visits.url




'''


'''
f = open('C:\Users\%%USER%%\AppData\Local\Google\Chrome\User Data\Default\History', 'rb')
data = f.read()
f.close()
f = open('your_expected_file_path.txt', 'w')
f.write(repr(data))
f.close()
1482616931
13126948354818121
'''


'''
nn = [5,1]
0-1000 train, 0-5000 predict
237 234
missed = 7
wrong predictions = 4
[array([[ -0.872,   2.979,  -0.348,  -1.423,   2.477],
       [ -4.734, -11.56 ,  -7.001,   5.243, -12.526],
       [ -0.046,   3.263,  -3.464,  -1.506,   3.298]]), array([[  0.531],
       [-22.892],
       [  5.288],
       [  0.318],
       [ 12.647]]), array([[-9.976]])]

0-2000 train, 2000-5000 test
112 115
missed = 0
wrong predictions = 3
[array([[ -0.164,  -2.176,  -0.029,   1.414,  -2.831],
       [-30.62 , -31.501,   0.18 , -20.833,   7.094],
       [  0.729,  -1.208,   0.732,   0.495,  -1.41 ]]), array([[-18.519],
       [ 17.277],
       [-11.851],
       [  1.55 ],
       [  7.576]]), array([[-3.997]])]

train data range 0 1000
237 249
nn structure [3, 1, 3]
test data 0 5000
missed = 0
wrong predictions = 12
[array([[  0.446,   0.981,   1.624],
       [-18.71 , -18.67 , -18.711],
       [  1.33 ,   0.266,   0.196]]), array([[ 15.497],
       [ 13.925],
       [ 15.09 ]]), array([[-0.804, -3.047, -3.107]]), array([[-4.092],
       [-4.579],
       [-3.113]])]


se = sum(abs(theta[1][2][0]))
if se<0.00001:
train data range 0 1000
237 236
nn structure [5]
test data 0 5000
threshhold 0.1
missed = 1
wrong predictions = 0
[array([[ -0.032,   4.38 ,  -1.96 ,  -3.615,  -3.343],
       [ 17.744, -18.477,  39.245,  79.456,  39.633],
       [  0.307,   0.1  ,   0.107,  -4.589,   0.745]]), array([[ -8.057],
       [ 21.462],
       [ 30.849],
       [-57.632],
       [ 31.837]])]

train data range 0 1000
237 236
nn structure [5]
test data 0 5000
threshhold 0.1
missed = 1
wrong predictions = 0
[array([[ -8.15 ,  -1.426,  -2.668,   2.581,  -0.798],
       [ 72.408,  40.308,  18.199,  38.857,  17.754],
       [-10.805,   1.946,  -3.84 ,   5.255,  -4.147]]), array([[-50.67 ],
       [ 38.129],
       [-18.909],
       [ 36.634],
       [ -8.186]])]


271 283
nn structure [3, 1, 3]
test data 0 5800
threshhold 0.1
missed = 0
wrong predictions = 12
[array([[  0.871,  -2.049,  -2.153],
       [ 20.126,  10.431, -25.642],
       [  6.047,  -0.008,  -6.837],
       [  1.323,  -3.272,  -3.519]]), array([[ 1.629],
       [-4.497],
       [ 2.844]]), array([[ -1.521, -12.585,  -5.509]]), array([[ 1.214],
       [-9.002],
       [-1.299]])]       
'''
