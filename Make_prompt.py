from langchain_core.prompts import ChatPromptTemplate

def rephraseDBresults(DBresp):
    template = """
        Consider yourself as a QA tester, create Test scenarios in one line for the following context and give the response in serial numbers wise:

        {context}

        ---

    """
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in DBresp])
    prompt_template = ChatPromptTemplate.from_template(template)
    prompt = prompt_template.format(context=context_text)
    return prompt

def rephraseUserinput(user_input):
    template = """
    Consider yourself as an english teacher and make correction for any of the errors in the user input given below. And give only the corrected text and no extra text.
    User input: {userInput}
    """
    prompt_template = ChatPromptTemplate.from_template(template)
    prompt = prompt_template.format(userInput=user_input)
    return prompt

def typeofTS(TS_list):
    template = """
        Give me the what is the type of each test scenarios 1 to {tot_scenarios} given below. Use minimum words separated by ",".
        [Example] 
        Types: x,x,x... and so on. Where x is type of test scenario. Total no. of types must be {tot_scenarios}
        ---
        [Test scenarios]
        {TS_text}

    """
    TS_text = "\n".join([str(i) + ". " + TS_list[i] for i in range(len(TS_list))])
    prompt_template = ChatPromptTemplate.from_template(template)
    prompt = prompt_template.format(TS_text=TS_text,tot_scenarios=len(TS_list))
    return prompt

def makeCorrection(LLM_TS, suggestion="Make the test scenarios for in-depth testing including all the systems."):
    template = """
        Can you make corrections as per the suggestions by the user on the previous test scenarios given by you below.

        {previous_TS}

        ---
        Suggestion by the user: {suggestion}

        ---        

    """
    previous_TS = "\n".join([str(i) + '. ' + LLM_TS[i] for i in range(len(LLM_TS))])
    prompt_template = ChatPromptTemplate.from_template(template)
    prompt = prompt_template.format(previous_TS=previous_TS, suggestion=suggestion)
    return prompt

def basedOnFBTS(DBresp, positive_list, negative_list):
    template = """
        Consider yourself as a QA tester, create Test scenarios in one line for the following context and give the response in serial numbers wise:
        Include these test scenarios on the following types : {pos_fb}
        Do not include test scenario on the following types : {neg_fb}
        ----
        
        {context}

        ---

    """
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in DBresp])
    pos_fb_cont = ",".join([fb for fb in positive_list])
    neg_fb_cont = ",".join([fb for fb in negative_list])
    prompt_template = ChatPromptTemplate.from_template(template)
    prompt = prompt_template.format(pos_fb=pos_fb_cont, neg_fb=neg_fb_cont ,context=context_text)
    return prompt

def onePrompt(DBresp, positive_list, negative_list):
    template = """Consider yourself as a QA tester, give me Test scenarios and its types based on the context below.
    Include Test scenario of the following types : {pos_fb}
    Do not include Test scenarios of the following types: {neg_fb}
    You can provide other test scenarios with its types if you have any test scenanrios types in mind or if I am missing any.
    
    ---
    [Context]

    {context}

    ---
        
    [Important!!] Can you give the "Test scenarios" and "Types" only in JSON format without any comments. As per below is the example.
    
    
    [Example]
    [   
        {{
            "Data":[[<Test Scenario>,<Type>], [<Test Scenario>,<Type>], [<Test Scenario>,<Type>]]
        }}
    ]
   
"""
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in DBresp])
    pos_fb_cont = ",".join([fb for fb in positive_list])
    neg_fb_cont = ",".join([fb for fb in negative_list])
    prompt_template = ChatPromptTemplate.from_template(template)
    prompt = prompt_template.format(pos_fb = pos_fb_cont, neg_fb = neg_fb_cont, context=context_text)

    return prompt



def modORDel(feedback):
    template = """
        As per the below sentence can you tell me if the user is telling to "modify" or "delete". Only either one should be in the answer and nothing apart from these two word.
        Sentence: {feedback}
    """
    prompt_template = ChatPromptTemplate.from_template(template)
    prompt = prompt_template.format(feedback=feedback)
    return prompt




