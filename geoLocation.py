import urllib.request, urllib.parse, urllib.error
import json
import sqlite3
import ssl


class GeoData:
    api_key = 42
    serviceUrl = "http://py4e-data.dr-chuck.net/json?"

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    con = sqlite3.connect("geoData.sqlite")
    cur = con.cursor()

    cur.executescript('''
        CREATE TABLE IF NOT EXISTS location(address TEXT, geodata TEXT)
    ''')
    con.commit();

    with open("where.txt", "r") as file:
        for line in file.readlines():
            address = line

            cur.execute('''
                SELECT * FROM location WHERE address = ?
            ''', (address,))

            test = cur.fetchone()

            if test is None:
                parms = dict()
                parms['address'] = address
                parms['key'] = api_key

                url = serviceUrl + urllib.parse.urlencode(parms)
                print('Retrieving', url)

                requested = urllib.request.urlopen(url, context=ctx)
                requestDecoded = requested.read().decode()

                print('here', len(requestDecoded), 'characters', requestDecoded[:20].replace('\n', ' '))

                jsonData = json.loads(requestDecoded)

                if 'status' not in jsonData or jsonData['status'] == 'FAILED' or jsonData['status'] == 'ZERO_RESULTS':
                    print('==== Failure To Retrieve ====')
                    print(jsonData)
                else:
                    cur.execute('''
                                INSERT INTO location(address,geoData) VALUES (?,?)
                                ''', (address.encode(), requestDecoded.encode()))
            else:
                print("Found in database ", address)

    con.commit()
    con.close()
