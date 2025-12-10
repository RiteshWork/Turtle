from VectorDB import VectorDB
from LLM_Model import LLM_Model
from Embedding import Embedding
from HandleCSV import HandleCSV
import Make_prompt
from MySQL_Handler import MySQL_Handler as MSQL_H
import os, json, copy
from datetime import datetime

# Query DB to get data now
def selectDB():
    mySQL = MSQL_H()
    summ_list, fb_list, type_list = mySQL.selectAll()
    return summ_list, fb_list, type_list

# Get positive negative feedback types for DB query.
def getPosNegTypesDB():
    summ_inp, db_0_1_list, types_list = selectDB()
    pos_list = []
    neg_list = []
    for i in range(len(db_0_1_list)):
        if db_0_1_list[i] == '0':
            neg_list.append(types_list[i])
        elif db_0_1_list[i] == '1':
            pos_list.append(types_list[i])
    return pos_list, neg_list
        
# Insert into DB
def insertToDB(summ_input_file, user_feedback, TS_types):
    mySQL = MSQL_H()
    mySQL.insertDB(summ_input_file, user_feedback, TS_types)

## Get desired subtexts from the large text 
def getTypesText(text, toSearch):
    search_index = text.find(toSearch)
    types_list = []
    if search_index > -1:
        search_index += len(toSearch)
        sub_text = text[search_index:]
        sub_text = sub_text.split("\n")[0]
        types_list = sub_text.split(',')
        types_list = [s.strip() for s in types_list]
    return types_list

## Save the feedback from the user into CSV
def saveFeedbackToCSV(summ_input, TS_list, types_list):
    hc = HandleCSV()
    df = hc.createDataFrame(summ_input, TS_list, types_list)
    hc.writeCSV_file(dataFrame=df)
    print("Data saved to CSV.")

## Get the positive, negative type feedback from CSV file
def getPosNegTypes(file_path='data/feedback.csv'):
    hc = HandleCSV()
    summ, feedback, scenario_types = hc.returnCSVData()
    positive_types = []
    negative_types = []

    for i in range(len(feedback)):
        if feedback[i] == 0: # Negative feedback
            negative_types.append(scenario_types[i])
        elif feedback[i] == 1: # Positive feedback
            positive_types.append(scenario_types[i])
    
    return positive_types, negative_types

## Write to txt file to check on the LLM response.
def writeToFile(content, comments, mode):
    with open('data/LLM_generated.txt', mode, encoding='utf-8') as f:
        f.write(comments + content)
    f.close()

## convert the LLM response Test scenarios to list.
def testscenariostoList(TS):
    ## First split the whole text by next line "\n"
    TS_list = TS.split("\n")
    filtered_TS_list = []
    # Go through each line in the list and check if first few char is numeric then put it in filtered TS list.
    for ts in TS_list:
        num_text = ""
        for ch in ts:
            if ch.isnumeric():
                num_text += ch
            else:
                break
        # To check num_text is not empty    
        if len(num_text) > 0 and num_text.isnumeric():
            splitter = ". "
            # get the index of the splitter and fetch only texts after splitter.
            start_index = ts.find(splitter) + len(splitter)
            temp_ts = ts[start_index:]
            filtered_TS_list.append(temp_ts)
    return filtered_TS_list
    #filteredTS_list = []
    #for i in range(len(TS)):
    #    ch1 = TS[i]
    #    temp_TS = ""
    #    if ch1.isnumeric():
    #        d_TS = TS[i:]
    #        other_num = False
    #        for j in range(len(d_TS)):
    #            num_text = ""
    #            ch2 = d_TS[j]
    #            if not other_num:
    #                if ch2.isnumeric():
    #                    num_text += ch2
    #                else:
    #                    temp_TS += ch2
    #                    other_num  = True
    #            else:
    #                break
    #    if len(temp_TS) > 0:
    #        filteredTS_list.append(temp_TS)
    #return filteredTS_list

## Save the Test scenarios types to JSON
def feedbackEntry(TStypes):
    log_entry = {
        "TS_types":TStypes
    }
    
    if not os.path.exists('data/feedback.json'):
        data = [log_entry]
        with open("data/feedback.json","w") as f:
            json.dump(data,f,indent=4)
        f.close()
    else:
        # load the data already in the file.
        with open("data/feedback.json","r") as f:
            data = json.load(f)
        f.close()

        # Rewrite the the existing data with new data 
        #data.append(log_entry)

        types_list = data[0]["TS_types"]
        for ty in TStypes:
            types_list.append(ty)
        
        # Removing any duplicates    
        types_set = set(types_list)
        types_list = list(types_set)
    
        data[0]["TS_types"] = types_list
        with open("data/feedback.json","w") as f:
            json.dump(data,f,indent=4)
        f.close()

## Get the Test scenarios types from JSON
def getJsonData():
    types_list = []
    if os.path.exists('data/feedback.json'):
        with open('data/feedback.json','r') as f:
            data = json.load(f)
            types_list = data[0]['TS_types']
    return types_list

## Convert normal text to vectors to help find similarity in vector DB            
def embedding_function():
    model_name = "nomic-ai/modernbert-embed-base"
    em = Embedding(model_name)
    embedding = em.embedding_init()
    return embedding

## Intialize the model with configurations
def get_model():
    llm_model = LLM_Model()
    return llm_model.model_init()

## Store the data to DB
v_db = VectorDB()
#v_db.generate_data_store()
#storeData()

## LLM model initiate
llm_model = get_model()

## Query to DB
user_input = input("Please enter your query: ")
#user_input = "python test scenarios"

## Rephrase the user input to get accurate result from DB and invoke to the LLM.
print("Getting rephrased text from LLM..",end='\r')
prompt = Make_prompt.rephraseUserinput(user_input)
llm_userInput = llm_model.invoke(prompt)
print(f"Rephrased user input: {llm_userInput.content}.   ")

## Make DB request, rephrase the text and invoke to LLM.
print("Trying the get data from vector DB..",end='\r')
db_results = v_db.query_text(llm_userInput.content)
print("Received data from vector DB.          ")
#useJson = True
#useCSV = True
useDB = True
if useDB:
    # Using CSV data
    #positive_type_list, negative_type_list = getPosNegTypes()

    # Using MySQL DB
    positive_type_list, negative_type_list = getPosNegTypesDB()
    print("Asking LLM on the basis of feedback and DB content...",end='\r')
    prompt = Make_prompt.basedOnFBTS(db_results, positive_type_list, negative_type_list)
    llm_TS = llm_model.invoke(prompt)
    print("Data received from LLM on the basis of feedback and DB content.      ")
    writeToFile(llm_TS.content, comments="\n--- Test scenarios generated by LLM ---\n", mode='w')
else:
    prompt = Make_prompt.rephraseDBresults(db_results)
    print("Asking LLM on the basis of DB content...",end='\r')
    llm_TS = llm_model.invoke(prompt)
    print("Data received from LLM on the basis of DB content.      ")
    writeToFile(llm_TS.content, comments="\n--- Test scenarios generated by LLM New ---\n", mode='w')


## Test scenarios to list
filteredTS_list = testscenariostoList(llm_TS.content)
#print(f"\n --- Test scenarios from LLM --- \n{llm_TS.content}\n\n")

####
# [Note] Since we are making many list so look out for the copying it and not taking references.
####

correction_list = copy.deepcopy(filteredTS_list)
valid_TS_list = copy.deepcopy(filteredTS_list)
invalid_TS_list = []

## Show all the test scenarios one by one with an index so that we can make correction to TS in the feedback.
print("\n--- Test Scenarios from LLM ---\n")
for index in range(len(filteredTS_list)):
    print(f"{index + 1}. {filteredTS_list[index]}")
print("\n--------------------------------\n")

#for _ in range(2):
## Get feedback from the user.
# Based on the each test scenarios get feedback for each one
## feedback will be a list so that we can capture multiple feedbacks at once.
print("\n --- Feedback --- \n")
f_val_inval = input("Do you wish to valid/invalid: ").strip().lower()
print(f"Length filtered_TS: {len(filteredTS_list)}")
print(f"Length liked_TS: {len(valid_TS_list)}")
print(f"Length disliked_TS: {len(invalid_TS_list)}")
#if f_val_inval == "invalid":
    #c_input = input("Test scenarios you which to modify. If there is multiples keep space in between: ")
    #feedback_sugg = input("Please enter some suggestions on the test scenarios you felt is invalid: ")
    #print("[Modify] as per suggestion asking LLM...",end='\r')
    #prompt = Make_prompt.makeCorrection(correction_list, feedback_sugg)
    #feedback_llm_resp = llm_model.invoke(prompt)
    #print("[Modify] received the answers from LLM.    ")
    #writeToFile(feedback_llm_resp.content, comments="\n--- Test scenarios generated by LLM Correction ---\n", mode='a')
    #corrected_TS_list = testscenariostoList(feedback_llm_resp.content)
    #print("\n--- Corrected Test Scenarios from LLM ---\n")
    #for index in range(len(corrected_TS_list)):
    #    print(f"{index + 1}. {corrected_TS_list[index]}")
    #    liked_TS_list.append(corrected_TS_list[index])
    #print("\n-----------------------------------------\n")


if f_val_inval == "invalid":
    f_input = input("Test scenarios that you feel is invalid, enter the index of it. If its mutiple give space between them: ").strip()
    if len(f_input) > 0:
        f_input = f_input.split(" ")
        feedback_index_list = list(map(int, f_input))
        # Test scenarios not liked.
        for num in feedback_index_list:
            temp_ts = valid_TS_list[num-1]
            valid_TS_list[num - 1] = None
            invalid_TS_list.append(temp_ts)
        
        # Remove None from the liked list
        index = 0
        temp_liked_list = []
        for t in valid_TS_list:
            if t != None:
                temp_liked_list.append(t)
        valid_TS_list = copy.deepcopy(temp_liked_list)
                
        
print("\n---- Valid list ----\n")
for index in range(len(valid_TS_list)):
    print(f"{index+1}. {valid_TS_list[index]}")
print("\n---------------------------------\n")
print("\n---- Invalid list ----\n")
for index in range(len(invalid_TS_list)):
    print(f"{index+1}. {invalid_TS_list[index]}")
print("\n---------------------------------\n")

#feedback_sugg = input("Please enter some suggestions on the test scenarios you did not liked: ")
    
    ## Make another call to LLM to make corrections as per the feedback. Ask LLM on the basis of suggestion Delete/Modify.
    # If "delete" remove it from the list or the array. if Modify as LLM to modify. Then add it to the original list.
    # prompt must contain [TS not liked, feedback if any from the user, Previous response from LLM]. Accordingly make changes in 
    # the Make_prompt file.
    ## Get from LLM to modify/delete the unliked Test scenario.
    #prompt = Make_prompt.modORDel(feedback_sugg)
    #mod_del_llm_resp = llm_model.invoke(prompt)
    #mod_del_resp = mod_del_llm_resp.content.strip().lower()
    #print("\n---- LLM response on Mod/Del ----\n")
    #print(f"Response: {mod_del_resp}")
    #print("\n---------------------------------\n")    


# From LLM get the scenario's type
prompt = Make_prompt.typeofTS(filteredTS_list)
print("Getting scenario types from LLM...",end='\r')
TS_type_resp = llm_model.invoke(prompt)
TS_LLM_types = TS_type_resp.content
print("Scenario types received.           ")
print(f'--- Test scenario types from LLM --- \n{TS_LLM_types}')
print("------------------------------------------------")
types_LLM_fb = getTypesText(TS_LLM_types, toSearch="Types: ")
print(f"---- TS types -------\n{types_LLM_fb}")
print("----------------------------")

db_0_1_list = []
for i in range(len(filteredTS_list)):
    if filteredTS_list[i] in valid_TS_list:
        db_0_1_list.append('1')
    else:
        db_0_1_list.append('0')

# Save the liked disliked feedback
#saveFeedbackToCSV([' ' for _ in range(len(filteredTS_list))], db_0_1_list, types_LLM_fb)

## Save to MySQL DB
insertToDB([' ' for _ in range(len(filteredTS_list))], db_0_1_list, types_LLM_fb)

print("\n --- Final feedback --- \n")
final_feedback = input("Did you like the Test scenarios over all yes/no: ").strip().lower()
if final_feedback == 'yes':
    print("\n Thank you for using this tool.")
elif final_feedback == 'no':
    print("\n I am very sorry I am not able to generate the Test scenarios as per expectation.")
print("\n ----------------------- \n")




