import pymysql

class Database:
    def connect(self):
        return pymysql.connect(charset="utf8mb4", db="defaultdb", host="nara-real-estate-mohamedzahi33-d182.a.aivencloud.com", password="AVNS_-rsuSdYWn_5K62hZiKS", port=19329, user="avnadmin")

    def get_callcenter_id(self, email, passwd):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('select id from callcenterusers where email = %s AND password = %s', (email, passwd))
            return cursor.fetchone()[0]
        except Exception as e:
            return None
        finally:
            con.close()


    def get_callcenter_email(self, callcenter_id):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('select email from callcenterusers where id = %s', (callcenter_id))
            return cursor.fetchone()[0]
        except Exception as e:
            return None
        finally:
            con.close()
