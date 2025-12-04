from VectorDB import VectorDB
from LLM_Model import LLM_Model
from Embedding import Embedding
import Make_prompt
import os, json
from datetime import datetime

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

def getJsonData():
    types_list = []
    if os.path.exists('data/feedback.json'):
        with open('data/feedback.json','r') as f:
            data = json.load(f)
            types_list = data[0]['TS_types']
    return types_list
            

def embedding_function():
    model_name = "nomic-ai/modernbert-embed-base"
    em = Embedding(model_name)
    embedding = em.embedding_init()
    return embedding

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

## Rephrase the user input to get accurate result from DB and invoke to the LLM.
prompt = Make_prompt.rephraseUserinput(user_input)
llm_userInput = llm_model.invoke(prompt)
print(f"Rephrased user input: {llm_userInput.content}")

## Make DB request, rephrase the text and invoke to LLM.
db_results = v_db.query_text(llm_userInput)
useJson = True
if useJson:
    # Using JSON data
    TS_types_list = getJsonData()
    prompt = Make_prompt.userLikeTS(db_results, TS_types_list)
    llm_TS = llm_model.invoke(prompt)
else:
    prompt = Make_prompt.rephraseDBresults(db_results)
    llm_TS = llm_model.invoke(prompt)

print(f"\n --- Test scenarios from LLM --- \n{llm_TS.content}\n\n")

for _ in range(2):
## Get feedback from the user.
    feedback = input("Enter your feedback yes/no: ").strip().lower()

## As per feedback perform the action.
    if feedback == 'yes':
        # From LLM get the scenario's type
        prompt = Make_prompt.typeofTS(llm_TS.content)
        TS_type = llm_model.invoke(prompt)
        print(f' Test scenario types: {TS_type.content}')
        break
    elif feedback == 'no':
        # Make another call to LLM for the correction.
        suggestion = input("Please enter some suggestions: ").strip()
        prompt = Make_prompt.makeCorrection(llm_TS.content,suggestion)
        sugg_resp = llm_model.invoke(prompt)
        print(f"\n --- Test scenarios from LLM --- \n{sugg_resp.content}\n\n")

if feedback == 'no':
    feedback = input("Enter your feedback yes/no: ").strip().lower()

if feedback == 'yes':
    # Add to the learning JSON
    TStypes_list = TS_type.content.strip().split(',')
    TStypes_list = [ty.strip() for ty in TStypes_list]
    feedbackEntry(TStypes_list)
    print(" Types saved to JSON.")

elif feedback == 'no':
    print("\n I am very sorry I am not able to generate the Test scenarios as per expectation.")
##
