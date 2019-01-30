import binascii
import nfc
import MySQLdb
import datetime
import requests
import subprocess

class MyCardReader(object):

    def on_connect(self, tag):
        print "touched"
# byte string to Hexadecimal
        self.idm = str(tag.identifier).encode('hex').upper()
        return True

    def read_id(self):
        clf = nfc.ContactlessFrontend('usb')
        try:
            clf.connect(rdwr={'on-connect': self.on_connect})
        finally:
            clf.close()

if __name__ == '__main__':

# Card read 
    cr = MyCardReader()
    while True:
        print "touch card:"
        cr.read_id()
        print "released"
        print cr.idm
        tt = datetime.datetime.now()
        f_id=cr.idm
        
# db connect  
        connector = MySQLdb.connect(host="localhost", 
                                    db="Wordrobe_db",
                                    user="yutani",
                                    passwd="*******", 
                                    charset="utf8mb4")
        cursor = connector.cursor()

        sql=u"update Wordrobe_tb set status = '0', date = '%s' where (idm = '%s' and status = '1')" %(tt , f_id)
        result = cursor.execute(sql)
# in status 0 to 1 update 
        if  result == 1 :
                    chk=u"select * from Wordrobe_tb where idm='%s'" %(f_id)
                    cursor.execute(chk)
                    records = cursor.fetchall()
                    for record in records:
                        stat=record[0]
                        name=record[1]
                        ttime=record[3]
                        st = str(stat)
                        nm= str(name)
                        time = str(ttime)
                        payload = {"value1": st, "value2": nm,"value3":time}
                        print(payload)
                        requests.post("https://maker.ifttt.com/trigger/Spreadsheet/with/key/jqVgiRKUt-3G63KNTYqSAhwUghW7te8KvieCZVXHFwx", json=payload)
                        subprocess.call("aplay /home/pi/nfcpy-0.13.5/music/kirameki02.wav", shell=True)
   # out status status 1 to 0                     
        if  result == 0 :
            sql=u"update Wordrobe_tb set status = '1', date = '%s' where (idm = '%s' and status = '0')" %(tt , f_id)
            result1=cursor.execute(sql)
            if  result1 == 1 :
                    chk=u"select * from Wordrobe_tb where idm='%s'" %(f_id)
                    cursor.execute(chk)
                    records = cursor.fetchall()
                    for record in records:
                        stat=record[0]
                        name=record[1]
                        idm=record[2]
                        ttime=record[3]
                        st = str(stat)
                        nm= str(name)
                        time = str(ttime)
                        payload = {"value1": st, "value2": nm,"value3":time}
                        print(payload)
                        requests.post("https://maker.ifttt.com/trigger/Spreadsheet/with/key/jqVgiRKUt-3G63KNTYqSAhwUghW7te8KvieCZVXHFwx", json=payload)
                        subprocess.call("aplay /home/pi/nfcpy-0.13.5/music/gundam08.wav", shell=True)
#  commit after update-chk  
        if result == 1 or result1 == 1 :
            connector.commit()

        cursor.close()
        connector.close()
