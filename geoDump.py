import codecs
import sqlite3
import json


class GeoDump:
    con = sqlite3.connect("geoData.sqlite")
    cur = con.cursor()

    cur.execute('''
        SELECT * FROM location
    ''')

    fhand = codecs.open('where.js', 'w', "utf-8")
    fhand.write("myData = [\n")
    count = 0
    for row in cur:
        rowData = row[1].decode()

        try:
            js = json.loads(rowData)
        except:
            pass

        if 'status' not in js or js['status'] != 'OK' : continue

        lat = js["results"][0]["geometry"]["location"]["lat"]
        lng = js["results"][0]["geometry"]["location"]["lng"]

        if lat == 0 and lng == 0: continue

        locationDetail = js["results"][0]['formatted_address']
        where = locationDetail.replace("'", "")

        try:
            print(where, lat, lng)

            count = count + 1
            if count > 1: fhand.write(",\n")
            output = "[" + str(lat) + "," + str(lng) + ", '" + where + "']"
            fhand.write(output)
        except:
            continue

    fhand.write("\n];\n")
    cur.close()
    fhand.close()
    print(count, "records written to where.js")
    print("Open where.html to view the data in a browser")