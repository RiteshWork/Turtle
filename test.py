def testScenariosToList(TS):
    filteredTS_list = []
    temp_TS = ""
    len_TS = len(TS)
    i = 0
    while i < len_TS:
        ch1 = TS[i]
        if ch1.isnumeric() and TS[i+1] == '.':
            #d_TS = TS[i:]
            temp_TS = ""
            other_num = False
            j = i
            num_text = ""
            while j < len_TS:
                ch2 = TS[j]
                if not other_num or not ch2.isnumeric():
                    if ch2.isnumeric() and TS[j+1]:
                        num_text += ch2
                    else:
                        temp_TS += ch2
                        other_num  = True
                elif other_num and ch2.isnumeric():
                    break
                j += 1
            i = j-1
        if len(temp_TS) > 0:
            filteredTS_list.append(temp_TS)
        i += 1
    if len(temp_TS) > 0:
        last_index = temp_TS.rfind("\n")
        if last_index > -1:
            temp_TS = temp_TS[:last_index]
            filteredTS_list.append(temp_TS)
        else:
            filteredTS_list.append(temp_TS)
    return filteredTS_list


if __name__ == "__main__":
    TS = """
**Valid Input, Network Connectivity**

1. User input: "google"
Expected output: The program prints a fully qualified domain name (FQDN) like "www.google.com" and attempts to perform a DNS lookup using socket library.
2. User input: "microsoft"
Expected output: Same as scenario 1.

**Invalid Input**

3. User input: "" (empty string)
Expected output: The program prints an error message saying "Input cannot be empty."
4. User input: " invalid" (non-existent domain name)
Expected output: The program attempts to perform a DNS lookup, but since the domain name is invalid, it will print an error message like "❌ Error: Hostname 'www.invalid.com' could not be resolved." and suggest checking the domain name or network connection.

**Network Connectivity Issues**

5. User input: "google" (while running the program on a machine with no internet connectivity)
Expected output: The program attempts to perform a DNS lookup, but since there is no internet connectivity, it will print an error message like "❌ Error: Hostname 'www.google.com' could not be resolved." and suggest checking the domain name or network connection.

Note that I did not include test scenarios for valid input with network issues because the problem description does not specify this scenario explicitly.
"""

    ts_list = testScenariosToList(TS)
    ts_list = [t.replace(". ", "") for t in ts_list]
    for i in range(len(ts_list)):
        print(f"{i}. {ts_list[i]}")

