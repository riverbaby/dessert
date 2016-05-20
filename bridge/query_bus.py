# -*- coding: utf-8 -*-
import sys, urllib, urllib2, json
import csv

#please fill your baidu api store apikey here, http://apistore.baidu.com
apikey = ""

url_prefix= 'http://apis.baidu.com/xiaota/bus_lines/buses_lines?'
city= '杭州'
directions={'0','1'}
buslines = {'1','10','101','11','116','120','129','130','15','172','179','180','185','186','194','198','199','20','205','209','211','215','221','223','227','228','229','259','266','267','268','270','279','286','290','303','305','31','320','33','345','357','358','40','401','43','48','49','5','50','53','54','55','63','67','69','7','76','78','79','8','90','900','91','92','93','B8','B1','B8','Y2', 'Y6'}

data = []
newlines=[]
err = 0
num = 0
for bus in buslines:
    for direction in directions:
        url = url_prefix+'city='+city+'&bus='+bus+'&direction='+direction
        req = urllib2.Request(url)
        req.add_header("apikey", apikey)
        resp = urllib2.urlopen(req)
        content = resp.read()
        if(content):
            result = json.loads(content)
            if (result["code"] != 1000):
                err = err+1
                if "data" in result and result["data"] != None:
                    for new in result["data"]:
                        if new  not in  newlines:
                            newlines.append(new)
                else:
                    print url
                    print content
                    err = err+1
                continue
            stations = result["data"]["stations"]
            for station in stations:
                line = (bus, direction, station["station"],station["stateName"].encode('utf-8'))
                data.append(line)

print newlines
for bus in newlines:
    for direction in directions:
        url = url_prefix+'city='+city+'&bus='+bus.encode('utf-8')+'&direction='+direction
        req = urllib2.Request(url)
        req.add_header("apikey", apikey)
        resp = urllib2.urlopen(req)
        content = resp.read()
        if(content):
            result = json.loads(content)
            if (result["code"] != 1000):
                print url
                print content
                err = err+1
                continue
            stations = result["data"]["stations"]
            for station in stations:
                line = (bus.encode('utf-8'), direction, station["station"],station["stateName"].encode('utf-8'))
                data.append(line)


print err
csvfile=file('bus.csv','wb')
writer = csv.writer(csvfile)
writer.writerow(['Line', 'isUpStream', 'IndexInLine','StationName'])
writer.writerows(data)

csvfile.close()

