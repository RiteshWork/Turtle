import mysql.connector
from mysql.connector import Error

class MySQL_Handler:
#CREATE TABLE feedbacks (
#	SUMM_INPUT_FILE VARCHAR(50),
#	USER_FEEDBACK CHAR(1),
#	SCENARIO_TYPE CHAR(20)
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

    def insertDB(self, summ_list, user_fb_list, types_list):
        v_row_list = []
        for i in range(len(summ_list)):
            summ_ = summ_list[i]
            u_fb = user_fb_list[i]
            t_type = types_list[i]
            temp_row = f"('{summ_}','{u_fb}','{t_type}')"
            v_row_list.append(temp_row)

        temp_q = """INSERT INTO feedbacks (SUMM_INPUT_FILE, USER_FEEDBACK, SCENARIO_TYPE) 
        VALUES
        {all_values}
        ;
        """
        t_ = ",\n".join([v for v in v_row_list])
        query = temp_q.format(all_values=t_)

        self.cursor.execute(query)
        self.conn.commit()

        if self.cursor.rowcount > 0:
            print(f"Data inserted successfully. {self.cursor.rowcount} got affected.")
        else:
            print(f"Insertion failed or affected 0 rows.")

    def selectQuery(self):
        query = """
            SELECT SUMM_INPUT_FILE, USER_FEEDBACK, SCENARIO_TYPE
                FROM feedbacks;
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        
        for row in rows:
            temp_summ, temp_fb, temp_type = row
            self.summ_list.append(temp_summ)
            self.fb_list.append(temp_fb)
            self.type_list.append(temp_type)
    
    def selectAll(self):
        if len(self.summ_list) == 0 and len(self.fb_list) == 0 and len(self.type_list) == 0:
            self.selectQuery()
        return self.summ_list, self.fb_list, self.type_list

#if __name__ == "__main__":
#    mysqlH = MySQL_Handler()
#    summ_inp = [' ', ' ', ' ', ' ', ' ']
#    user_fb = ['0','1','0','1','0']
#    t_type = ['error','valid input','invalid input','network','security']
#
#    #mysqlH.insertDB(summ_inp,user_fb,t_type)
#    mysqlH.selectAll()