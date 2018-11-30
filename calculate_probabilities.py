probabilities = {}
import sys
def propogation(UCQ, quantifier, sep, list_of_separator_variables):
    common_table,sep_table_list = find_Common_Table(list_of_separator_variables) # tables whose probabilities can be substituted directly
    remove=[]
    for i in range(0,len(UCQ)):  # to track which common table names need to be removed from each conjunctive query
        subremove = []
        for table in UCQ[i]:
            if table in common_table:
                subremove.append(table)
        remove.append(subremove)
    for i in range(0,len(remove)):# remove common table names from each conjunctive query
        for j in remove[i]:
            del UCQ[i][j]
            if (len(UCQ[i]) == 0):
                UCQ.remove(UCQ[i])
                i -= 1
    return UCQ, quantifier, common_table,sep_table_list


def find_Common_Table(list_of_separator_variables):  # find tables whose probabilities can be substituted directly
    intersection=True
    sep_table_list={} #To store those tables' information that are being removed from UCQ
    common_table = tables[0]
    # Check intersection of all CQs
    for i in range(1, len(tables)):
        common_table = common_table.intersection(tables[i])
    if(len(common_table) == 0):
        intersection=False;
    if(intersection==True):
        for t in common_table:
            sep_table_list[t] = UCQ[0].get(t)
    # If intersection is a null set find a table with separator variable
    if(intersection==False):
        for i in range(0, len(UCQ)):
            for table_name in tables[i]:
                append = True
                varlist = UCQ[i].get(table_name).get("var")
                for e in varlist:
                    if e in list_of_separator_variables:
                        continue
                    else:
                        append = False
                if (append and table_name not in common_table and len(common_table)<=0):
                    common_table.add(table_name)
                    sep_table_list[table_name] = UCQ[i].get(table_name)
    return (common_table,sep_table_list)


def find_Separator(UCQ, quantifier):  # find separator for entire UCQ
    clause_count = 0
    for cq in UCQ:  # calculates how many clauses are there in the UCQ
        for clause in cq:
            clause_count += 1
    for q in quantifier:
        if (quantifier[q] == 0):  # if variable was already used as separator, don't check for it
            continue
        quant_count = 0
        for cq in UCQ:
            for clause in cq:
                if q in cq[clause].get("var"):
                    quant_count += 1
        if quant_count == clause_count:  # if variable appears in all clauses, it is the separator
            quantifier[q] = 0
            return q


def check_Independence_CQ(cq):  # check independence within a CQ
    tables = set()
    for clause in cq:
        if (cq[clause].get("name") in tables):
            return False;
        tables.add(cq[clause].get("name"))
    return True


def check_Independence_UCQ(tables):  # Check independence across entire UCQ, i.e. no repeating table names
    temp = set()
    for cq in range(0, len(tables)):
        if not temp.isdisjoint(tables[cq]):
            return False
        temp = temp | tables[cq]
    return True


def no_existential_quantifier(sub_CQ, quantifier):
    # Check if the none of the variables in the UCQ are existential in quantifier dict.
    print("SUBCQ-no", sub_CQ, quantifier)
    for vars in sub_CQ["var"]:
        if (quantifier[vars] == 1):
            return False
    return True


def update_quantifiers(sub_CQ, quantifiers):
    print("SUBCQ-up")
    for vars in sub_CQ["var"]:
        if (quantifier[vars] == 1):
            quantifier[vars] = 0
    return quantifiers


def test(UCQ):
    for value in UCQ:
        try:
            float(value)
        except ValueError:
            return True
    return False


def isUCQ(UCQ):
    if type(UCQ) is list:
        return True
    elif type(UCQ) is dict:
        return False


def getProbability(sep_table_list):
    print("getProbability",sep_table_list)
    print(probabilities)
    length=sys.maxsize
    for k in sep_table_list:
        length=min(length,len(probabilities[k])) #To check the minimum no. of rows across all tables
    ans=1
    # Iterating through each row
    for i in range(length):
        term=1
        #Iterating through each table for a row
        for k in sep_table_list:
            if(sep_table_list[k]["negation"]==False):
                term=term*probabilities[k][i]
            else:
                term=term*(1-probabilities[k][i])
        if(len(sep_table_list)==1):
            ans=ans*term
        else:
            ans=ans*(1-term)
    return ans


def probability(UCQ, quantifiers, tables):
    # Base of recursion
    if len(UCQ) == 1 and len(UCQ[0]) == 1:
        if (no_existential_quantifier(UCQ[0][list(UCQ[0].keys())[0]], quantifiers)):
            print("CASE1")
            return getProbability(UCQ[0])
        else:
            print("CASE2")
            quantifiers = update_quantifiers(UCQ[0][list(UCQ[0].keys())[0]], quantifiers)
            UCQ[0][list(UCQ[0].keys())[0]]["negation"] = True
            return 1 - probability(UCQ, quantifiers, tables)
    else:
        print("CASE3")
        sep = (find_Separator(UCQ, quantifiers))
        list_of_separator_variables = []
        list_of_separator_variables.append(sep)
        print(quantifiers)
        if sep is None:
            print("No separator variable found")
        else:
            UCQ, quantifiers, common_table,sep_table_list = propogation(UCQ, quantifiers, sep, list_of_separator_variables)
            if(len(UCQ)==0):
                return(1-getProbability(sep_table_list))

        # decomposable disjunction
        #if isUCQ(UCQ):
         #   print()
            #if check_Independence_UCQ(tables):
            #         val1 = 1 - probability(UCQ[0], quantifier, tables)
            #         val2 = 1 - probability(UCQ[1], quantifier, tables)
            #         return 1 - val1 * val2
            # # decomposable conjunction
            #elif check_Independence_CQ(UCQ):
                #val1 = probability(UCQ[0], quantifier, tables)
                #val2 = probability(UCQ[0], quantifier, tables)
                #return val1 * val2
        return 0.5
def parse_UCQ(input_query):
    UCQ = []
    quantifier = {}
    UCQ_list = input_query.split("||")  # split into individual conjunctions
    tables = []  # Represent all tables in each CQ
    for cq in UCQ_list:  # iterate through the above list, cq is each conjunction
        cq = cq.strip()  # remove spaces
        list_cq = cq.split(
            "),")  # to get list of relations. splitting by ), instead of , to ensure that it splits two relations and not withing a single relation
        dict_cq = {}  # dictionary representing each conjunctive clause
        temp_tables = set()
        for q in list_cq:  # iterate through the relations within each conjunctive clause
            q = q.strip()  # remove spaces
            q = q.split(
                "(")  # splitting by ( will ensure that the first index in the list is table name and second is variables
            temp_dict = {}
            temp_dict["var"] = q[1].strip("").replace(")", "").split(
                ",")  # remove spaces, remove the ) at the endd, and split by comma to get a list of variables
            temp_dict["negation"] = False
            temp_tables.add(q[0])
            for var in temp_dict["var"]:  # set the quantifier value as existential for all variables
                quantifier[var] = 1
            dict_cq[q[0]] = temp_dict  # append relation dictionary to the conjunctive clause dictionary
        UCQ.append(dict_cq)  # append conjunctive clause dictionary to the list of union of conjunctive clauses
        tables.append(temp_tables)
    return UCQ, quantifier, tables


input_query = "S(x)"
UCQ, quantifier, tables = parse_UCQ(input_query)

probabilities = {'S': [0.8, 0.2, 0.1]}
print(probability(UCQ, quantifier, tables))


