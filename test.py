import json
def testScenariosToList(TS):
    s_splitter = '['
    e_splitter = ']'
    start_index = TS.find(s_splitter)
    end_index = TS.rfind(e_splitter)
    scenario_types = []
    test_scenarios = []
    if start_index > -1 and end_index > -1:
        str_dump = TS[start_index : end_index + 1]
        js_list = json.loads(str_dump)

        for dic_str in js_list:
            try:
                ts_t_list = dic_str['Data']
            except:
                ts_t_list = dic_str['data']
            for ts, tp in ts_t_list:
                test_scenarios.append(ts)
                scenario_types.append(tp)
    return test_scenarios, scenario_types

    #    while temp_str.find('{')
    #    s_splitter = '{'
    #    e_splitter = '}'
    #    split_text(s_splitter, e_splitter)
    #    dict_str = json.loads(str_dump)
    #    try:
    #        ts_t_list = dict_str['Data']
    #    except:
    #        ts_t_list = dict_str['data']
    #    for d1, d2 in ts_t_list:
    #        test_scenarios.append(d1)
    #        scenario_types.append(d2)
    #return test_scenarios, scenario_types

    


if __name__ == "__main__":
    TS = """
Here are the test scenarios and types in JSON format:

```
[
  {
    "Data": [
      ["Constructing hostname with invalid prefix", "Boundary Testing"],
      ["Validating domain name without www prefix", "Equivalence Partitioning"],
      ["Checking IP address retrieval for valid FQDN", "Error Guessing"]
    ]
  },
  {
    "Data": [
      ["Handling empty input from user", "Boundary Testing"],
      ["Invalid domain name with special characters", "Equivalence Partitioning"],
      ["DNS lookup failure due to network issue", "Error Guessing"]
    ]
  }
]
```

These test scenarios and types are based on the provided context, including:

* Constructing a hostname with an invalid prefix (boundary testing)
* Validating a domain name without the www prefix (equivalence partitioning)
* Checking IP address retrieval for a valid FQDN (error guessing)

Additionally, I've included some more test scenarios that cover various edge cases and potential issues:

* Handling empty input from the user (boundary testing)
* Invalid domain name with special characters (equivalence partitioning)
* DNS lookup failure due to a network issue (error guessing)
"""

    ts_list, ts_types = testScenariosToList(TS)
    ts_list = [t.replace(". ", "") for t in ts_list]
    for i in range(len(ts_list)):
        print(f"{i+1}. {ts_list[i]} -> {ts_types[i]}")

