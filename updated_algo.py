probabilities = {}
import sys
import copy

def propogation(UCQ, quantifier, sep, list_of_separator_variables):
    common_table, sep_table_list = find_Common_Table(list_of_separator_variables)  # tables whose probabilities can be substituted directly
    #remove=[]
    #for i in range(0,len(UCQ)):  # to track which common table names need to be removed from each conjunctive query
    subremove = []
    #for table in UCQ[i]:
    #if table in common_table:
    #subremove.append(table)
    #remove.append(subremove)
    # for i in range(0,len(remove)):
    # remove common table names from each conjunctive query
    # for j in remove[i]:
    # del UCQ[i][j]
    # if (len(UCQ[i]) == 0):
    # UCQ.remove(UCQ[i])
    # i -= 1
    return UCQ, quantifier, common_table, sep_table_list

def find_Common_Table(list_of_separator_variables):  # find tables whose probabilities can be substituted directly
    intersection = True
    common_table = set()
    sep_table_list = {}  # To store those tables' information that are being removed from UCQ
    # Check intersection of all CQs only if number of CQs is > 1
    if (len(tables) > 1):
        common_table = tables[0]
        for i in range(1, len(tables)):
            common_table = common_table.intersection(tables[i])
        if (len(common_table) == 0):
            intersection = False;
        if (intersection == True):
            for t in common_table:
                sep_table_list[t] = UCQ[0].get(t)
    # If intersection is a null set or number of CQs is 1 then find a table with separator variable
    if (intersection == False or len(tables) == 1):
        for i in range(0, len(UCQ)):
            for table_name in tables[i]:
                append = True
                varlist = UCQ[i].get(table_name).get("var")
                for e in varlist:
                    if e in list_of_separator_variables:
                        continue
                    else:
                        append = False
                if (append == True and table_name not in common_table):
                    common_table.add(table_name)
                    sep_table_list[table_name] = UCQ[i].get(table_name)
    return (common_table, sep_table_list)

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
        
def substitute(fp,UCQ,sep):
    UCQ1 = copy.deepcopy(UCQ)
    for cq in UCQ1:
        for t in cq.keys():
            temp = cq[t]["var"]
            for s in temp:
                if (sep == s):
                    temp[temp.index(s)] = str(fp)
    return UCQ1

def check_Independence_CQ(cq):  # check independence within a CQ
    tables = set()
    for clause in cq:
        temp=cq[clause].get("var")
        for v in temp:
            if v in tables:
                return False;
        if v.isdigit()==False:
            tables.add(clause)
    return True

def check_Independence_UCQ(UCQ):  # Check independence across entire UCQ, i.e. no repeating table names
    temp = set()
    for cq in range(len(UCQ)):
        for k in UCQ[cq].keys():
            if k in temp:
                return False
            else:
                return True
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

def getProbability(UCQ):
    given_table_name =list(UCQ[0].keys())[0]
    constant_values = set(UCQ[0][list(UCQ[0].keys())[0]]["var"])
    flag = True
    for table_name,tuples in probabilities.items():
        if(table_name == given_table_name):
            for my_tuple in tuples:
                flag = True
                for my_input in constant_values:
                    if(my_input not in my_tuple[0]):
                        flag = False
                if(flag == True):
                    return my_tuple[1]
                    


def allConstantParameters(subUCQ):  # checks if all variables are numbers and not characters
    for x in subUCQ["var"]:
        if (x.isdigit() == False):
            return False
    return True

def probability(UCQ, quantifiers, tables):
    print(UCQ)
    sep=""
    # Base of recursion
    if (len(UCQ) == 1 and len(UCQ[0]) ==1 and allConstantParameters(UCQ[0][list(UCQ[0].keys())[0]])):  # is a ground atom
        print("CASE1")
        return getProbability(UCQ)# checks if the given constant values are present in the given tables, if present return probability, else returns 0
    # convert to ucnf
    if (len(UCQ) == 2 and check_Independence_UCQ(UCQ)):  # both cq are independent of each other
        print("CASE2")
        return 1 - ((1 - probability(UCQ[0])) * (1 - probability(UCQ[1])))
    if (len(UCQ)>2):
        if(check_Independence_UCQ(UCQ)):  # check if all cq are independent
            print("CASE3")
            sum = 0
            return -2
        # not sure how to translate this formula. what is m? why have they sued subset and not belongs
    if (len(UCQ) == 0 and check_Independence_CQ(UCQ[0])):
        print("CASE4")
        return probability(UCQ[0][UCQ[0][list(UCQ[0].keys())[0]]]) * probability(UCQ[0][UCQ[0][list(UCQ[0].keys())[1]]])
    sep = (find_Separator(UCQ, quantifiers))
    if (sep is not None):
        Pr = 0.0
        for d in domain:
            Pr*= probability(substitute(d,UCQ,sep))
        return Pr
    return -1
def get_domain(probabilities):
    domain = set()
    for table_name,tuples in probabilities.items():
        for my_tuple in tuples:
            for my_input in my_tuple[0]:
                if(my_input not in domain):
                    domain.add(my_input)
    return domain
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
            temp_dict["const"] = False
            temp_tables.add(q[0])
            for var in temp_dict["var"]:  # set the quantifier value as existential for all variables
                quantifier[var] = 1
            dict_cq[q[0]] = temp_dict  # append relation dictionary to the conjunctive clause dictionary
        UCQ.append(dict_cq)  # append conjunctive clause dictionary to the list of union of conjunctive clauses
        tables.append(temp_tables)
    return UCQ, quantifier, tables
input_query = "S(x),R(x,y)"
UCQ,quantifier,tables = parse_UCQ(input_query)
#probabilities = {'S': [0.8, 0.2, 0.3], 'R': [0.3, 0.4, 0.9]}
probabilities = {'P': [[[0],0.7],[[1],0.8], [[2],0.6]], 'Q': [[[0],0.7],[[1],0.3], [[2],0.5]], 'R':[[[0,0],0.8],[[0,1],0.4],[[0,2],0.5],[[1,2],0.6],[[2,2],0.9]]}
domain = get_domain(probabilities)
print("domain",domain)
temp = [{'R': {'var': [0,1], 'negation': False, 'const': False}}]
print("geprob", getProbability(temp)) #testing
print(probability(UCQ, quantifier, tables))


# 1 - 0.09 = 0.91
# 1 - 0.08 = 0.92
# 1 - 0.24 = 0.76
# 0.636
# 1- 0.636 = 0.364
#Inclusion Exclusion- Split into Q1,Q2 -Vaishnavi / Apply formula
#Case 4-Changes
#S(x) and S(x) --> S(x) -Vidhu
#substitute(Update Constant) - vaishnavi
#initially convert all existential to Universal -Vidhu
#conversion to ucnf -Hold

