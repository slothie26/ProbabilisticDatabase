probabilities = {}
import sys
import copy


def find_Separator(UCQ):  # find separator for entire UCQ
    # print("In find_Separator")
    clause_count = 0
    for cq in UCQ:  # calculates how many clauses are there in the UCQ
        for clause in cq:
            clause_count += 1
    for q in quantifier:
        # if (quantifier[q] == 0):  # if variable was already used as separator, don't check for it
        #     continue
        #print(quantifier[q])
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
    for cq in range (0,len(UCQ1)):
        for t in UCQ1[cq].keys():
            constant = True
            temp = UCQ1[cq][t]["var"]
            for i in range (0,len(temp)):
                if (sep == temp[i]):
                    temp[i] = str(fp)
                if(temp[i].isalpha()):
                    constant=False
            if(constant==True):
                UCQ1[cq][t]["const"]=True
                UCQ[cq][t]["const"]=True
    return UCQ1,UCQ

def check_Independence_CQ(cq):  # check independence within a CQ
    # print("in check independence", cq)
    cq = cq[0]
    tables = set()
    for key,value in cq.items():
        temp=cq[key].get("var")
        for v in temp:
            #print(tables)
            if v in tables:
                # print("False")
                return False;
            #print(v,v.isdigit())
            if v.isdigit()==False:
                tables.add(v)
    # print("True")
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
    #print("SUBCQ-no", sub_CQ, quantifier)
    for vars in sub_CQ["var"]:
        if (quantifier[vars] == 1):
            return False
    return True

def update_quantifiers(sub_CQ, quantifiers):
    #print("SUBCQ-up")
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
    #print("in getProbability")
    given_table_name =list(UCQ[0].keys())[0]
    constant_values = UCQ[0][list(UCQ[0].keys())[0]]["var"]
    #print(given_table_name,constant_values)
    flag = True
    for table_name,tuples in probabilities.items():
        if(table_name == given_table_name):
            for my_tuple in tuples:
                flag = True
                # #print("MYTUPLE", my_tuple, constant_values)
                # for my_input in constant_values:
                #     # print("hi",my_input,my_tuple[0],flag)
                #     if(int(my_input) not in my_tuple[0]):
                #       #  print("false flag")
                #         flag = False
                for i in range(len(constant_values)):
                    if int(constant_values[i]) != my_tuple[0][i]:
                        flag = False
                #print("###",flag)
                if(flag == True):
                    #print(my_tuple[1])
                    return my_tuple[1]
    # print("0")
    return 0

def allConstantParameters(subUCQ):  # checks if all variables are numbers and not characters
    for x in subUCQ["var"]:
        if (x.isdigit() == False):
            return False
    return True
def split_into_connected_components(sub_UCQ):
    # print("split_into_connected_components", sub_UCQ)
    ucnf = []
    list_of_component_variables = []
    for k,v in sub_UCQ.items():
        # print(k,":",v)
        flag = False
        for i in range(len(list_of_component_variables)):
            for j in sub_UCQ[k]["var"]:
                if j in list_of_component_variables[i]:
                    if(j.isdigit() == False):
                        flag = True
                        ucnf[i][0][k] = v
                        break
        if(flag==False):
            list_of_component_variables.append(set(sub_UCQ[k]["var"]))
            ucnf.append([{k:v}])
    return ucnf


def greaterThanTwoConnectedComponents(q_ucnf):
    
    for q in q_ucnf:
        # print("q",q)
        if(len(q[0])>1):
            return True

    return False
def convert_to_ucnf(UCQ):
    print("convert_to_ucnf", UCQ)
    ucnf = []
    if(len(UCQ)==1):
        print("subcase 1")
        ucnf = split_into_connected_components(UCQ[0])
        print("ucnf", ucnf)
        return ucnf
    q1_ucnf = split_into_connected_components(UCQ[0])
    q2_ucnf = split_into_connected_components(UCQ[1])
    print("q1",q1_ucnf, "q2", q2_ucnf)
    if(greaterThanTwoConnectedComponents(q1_ucnf)):
        print("subcase 2")
        for tp in q1_ucnf:
            print("tp", tp)
            toadd = convert_to_ucnf(q2_ucnf[0])[0][0]
            print("to add",toadd)
            tp.append(toadd)
            ucnf.append(tp)
            # print("newtp", newtp)
        print("ucnf", ucnf)
        return ucnf
    elif(greaterThanTwoConnectedComponents(q2_ucnf)):
        print("subcase 3")
        for tp in q1_ucnf:
            tp.append(convert_to_ucnf(q1_ucnf[0])[0][0])
            ucnf.append(tp)
        print("ucnf", ucnf)
        return ucnf
    else:
        print("hhhsubcase 4h")
        return UCQ


def probability(UCQ):
    print(UCQ)
    # print("probability")
    sep=""
    # Base of recursion
    if (len(UCQ) == 1 and len(UCQ[0]) ==1 and allConstantParameters(UCQ[0][list(UCQ[0].keys())[0]])):  # is a ground atom
        
        if(UCQ[0][list(UCQ[0].keys())[0]]["negation"]==False):
            print("CASE1**",getProbability(UCQ), UCQ )
            return getProbability(UCQ)# checks if the given constant values are present in the given tables, if present return probability, else returns 0
        else:
            print("CASE1",1 - getProbability(UCQ), UCQ )
            return 1 - getProbability(UCQ)
    # convert to ucnf
    UCNF = convert_to_ucnf(UCQ)
    print("************************************************",UCNF)
    # print(len(UCQ), len(UCQ[0]))
    if (len(UCNF) == 2):  # both cq are independent of each other
        print("CASE2")
        ans = 1 - ((1 - probability([{list(UCQ[0].keys())[0]:UCQ[0][list(UCQ[0].keys())[0]]}])) * (1 - probability([{list(UCQ[0].keys())[1]:UCQ[0][list(UCQ[0].keys())[1]]}])))
        print("CASE2 returning", ans)
        return ans
    if (len(UCQ)>2):
        if(check_Independence_UCQ(UCQ)):  # check if all cq are independent
            print("CASE3")
            sum = 0
            return -2
        # not sure how to translate this formula. what is m? why have they sued subset and not belongs
    if (len(UCQ) == 2 and check_Independence_UCQ(UCQ)):
        print("CASE4")
        Pr = 1.0
        for key,value in UCQ[0].items():
            # print("in",[{key:value}])
            Pr*= probability([{key:value}])
        print("CASE4 returning", Pr)
        return Pr
    sep = (find_Separator(UCQ))
    # print("seperator",sep)
    if (sep is not None):
        print("CASE 5")
        Pr = 1.0
        for d in domain:
            UCQ1,UCQ=substitute(d,UCQ,sep)
            # print("in case 5",probability(UCQ1))
            Pr*= probability(UCQ1)
        print("CASE5 returning",Pr)
        return Pr
    print("UNLIFTABLE")
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
            temp_dict["negation"] = True
            temp_dict["const"] = False
            temp_tables.add(q[0])
            for var in temp_dict["var"]:  # set the quantifier value as existential for all variables
                quantifier[var] = 1
            dict_cq[q[0]] = temp_dict  # append relation dictionary to the conjunctive clause dictionary
        UCQ.append(dict_cq)  # append conjunctive clause dictionary to the list of union of conjunctive clauses
        tables.append(temp_tables)
    return UCQ, quantifier, tables
input_query = "H(x), E(x,y)"
UCQ,quantifier,tables = parse_UCQ(input_query)
#probabilities = {'S': [0.8, 0.2, 0.3], 'R': [0.3, 0.4, 0.9]}
#probabilities = {'P': [[[0],0.7],[[1],0.8], [[2],0.6]], 'Q': [[[0],0.7],[[1],0.3], [[2],0.5]], 'R':[[[0,0],0.8],[[0,1],0.4],[[0,2],0.5],[[1,2],0.6],[[2,2],0.9]]}
probabilities = {'E':[[[0,0],0.7],[[0,1],0.4],[[1,0],0.3]],'H':[[[0],0.7],[[1],0.4],[[2],0.9]]}
domain = get_domain(probabilities)
#print("domain",domain)
# temp = [{'S': {'var': ['x'], 'negation': True, 'const': False},'R': {'var': ['x','y'], 'negation': True, 'const': False}}]
#print("geprob", getProbability(temp)) #testing
cnf = True
# print(1 - probability(UCQ))
# temp_UCQ = [{'R': {'var': ['x', 'y'], 'negation': False, 'const': False}, 'Q': {'var': ['x'], 'negation': False, 'const': False}}]
# cnf = False
print(1 - probability(UCQ))

# 1 - 0.09 = 0.91
# 1 - 0.08 = 0.92
# 1 - 0.24 = 0.76
# 0.636
# 1- 0.636 = 0.364
#Inclusion Exclusion- Split into Q1,Q2 -Vaishnavi / Apply formula
#Case 4-Changes
#S(x) and S(x) --> S(x) -Vidhu Done
#substitute(Update Constant) - Done
#initially convert all existential to Universal -Vidhu
#conversion to ucnf -Hold
#updated check independence cq