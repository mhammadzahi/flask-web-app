import pymysql

class Database:
    def connect(self):
        return pymysql.connect(charset="utf8mb4", db="", host="", password="", port=123, user="")

    def get_callcenter_id(self, email, passwd):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('select id_ from call_center_users where email_ = %s AND password_ = %s', (email, passwd))
            return cursor.fetchone()[0]
        except Exception as e:
            return None
        finally:
            con.close()


    def get_agent_id(self, email, passwd):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('select id_ from agents where email_ = %s AND password_ = %s', (email, passwd))
            return cursor.fetchone()[0]
        except Exception as e:
            return None
        finally:
            con.close()


    def get_callcenter_email(self, callcenter_id):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('select email_ from call_center_users where id_ = %s', (callcenter_id))
            return cursor.fetchone()[0]
        except Exception as e:
            return None
        finally:
            con.close()
