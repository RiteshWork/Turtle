import mysql.connector
from mysql.connector import Error

class MySQL_Handler:
#CREATE TABLE feedbacks (
#	SCENARIO_TYPE CHAR(20) PRIMARY KEY NOT NULL,
#   SUMMARY_INPUT_FILE VARCHAR(50),
#   USER_FEEDBACK CHAR(1)
#);

    def __init__(self):
        self.id_list = []
        self.summ_list = []
        self.fb_list = []
        self.type_list = []

        # DB variables
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'root'
        self.database = 'coginito'
        self.conn = None
        self.cursor = None

        self.makeConnection()
        


    def makeConnection(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        if self.conn.is_connected():
            self.cursor = self.conn.cursor()
            print("Successfully connected to MYSQL database.")
        else:
            print("Unable to conncet to MYSQL database.")

    def insertDB(self, types_list, summ_list, user_fb_list):
        v_row_list = []
        temp_q = """INSERT INTO feedbacks (SCENARIO_TYPE, SUMMARY_INPUT_FILE, USER_FEEDBACK) 
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
        SUMMARY_INPUT_FILE = VALUES(SUMMARY_INPUT_FILE),
        USER_FEEDBACK = VALUES(USER_FEEDBACK)
        ;
        """
        for i in range(len(summ_list)):
            summ_ = summ_list[i]
            u_fb = user_fb_list[i]
            t_type = types_list[i]
            temp_row = [t_type, summ_, u_fb]
            tup_row = tuple(temp_row)
            
            v_row_list.append(tup_row)

        #t_ = ",\n".join([v for v in v_row_list])
        #query = temp_q.format(all_values=t_)

        print(v_row_list)
        
        try:
            self.cursor.executemany(temp_q, v_row_list)
        except mysql.connector.Error as err:
            print(f"-- Error --\n {err}")
            print("--------------")     

        if self.cursor.rowcount > 0:
            print(f"Data upserted successfully. {self.cursor.rowcount} got affected.")
        
        self.conn.commit()
        
    

    def selectQuery(self):
        query = """
            SELECT SCENARIO_TYPE, SUMMARY_INPUT_FILE, USER_FEEDBACK
                FROM feedbacks;
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        
        for row in rows:
            temp_type, temp_summ, temp_fb = row
            self.type_list.append(temp_type)
            self.summ_list.append(temp_summ)
            self.fb_list.append(temp_fb)
    
    def selectAll(self):
        if len(self.summ_list) == 0 and len(self.fb_list) == 0 and len(self.type_list) == 0:
            self.selectQuery()
        return self.type_list, self.summ_list, self.fb_list

if __name__ == "__main__":
    mysqlH = MySQL_Handler()
    summ_inp = [' ', ' ', ' ', ' ', ' ']
    user_fb = ['1','0','0','1','1']
    #t_type = ['error','valid input','invalid input','network','security']
    t_type = ['G','B','H','I','K']


    mysqlH.insertDB(t_type,summ_inp,user_fb)
    #mysqlH.selectAll()