import os
import pandas as pd

class HandleCSV:
    def __init__(self, file_path='data/feedback.csv'):
        self.file_path = file_path
        self.summ_input_file = []
        self.user_feedback = []
        self.scenario_type = []
        self.sep = ","

    def writeCSV_file(self,dataFrame, file_path='data/feedback.csv'):
        if not os.path.exists(file_path):
            dataFrame.to_csv(file_path, mode='w',index=True)
        else:
            dataFrame.to_csv(file_path, mode='a',index=False,header=False)

    def createDataFrame(self,summ_input_file, user_feedback, scenario_type):
        data = {"summary_input_file":summ_input_file,
                     "user_feedback":user_feedback,
                     "scenario_type":scenario_type
                     }
        dataFrame = pd.DataFrame(data)
        return dataFrame

    def readCSV_file(self):
        self.summ_input_file = []
        self.user_feedback = []
        self.scenario_type = []
        if os.path.exists(self.file_path):
            data = pd.read_csv(self.file_path, sep=self.sep)
            for index, row in data.iterrows():
                temp_summ = row['summary_input_file']
                temp_feedback = row['user_feedback']
                temp_type = row['scenario_type']

                self.summ_input_file.append(temp_summ)
                self.user_feedback.append(temp_feedback)
                self.scenario_type.append(temp_type)
        else:
            print("CSV file not present in the given path.")

    def returnCSVData(self):
        if len(self.summ_input_file) == 0 and len(self.user_feedback) == 0 and len(self.scenario_type) == 0:
            self.readCSV_file()
        return self.summ_input_file, self.user_feedback, self.scenario_type
    
if __name__ == '__main__':
    hc = HandleCSV()
    summ, feedback, st = hc.returnCSVData()
    print(summ)
    print(feedback)
    print(st)
