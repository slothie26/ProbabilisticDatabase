probabilities = {}
import sys
import copy
from itertools import combinations

#fixed
def find_Separator(UCQ):  # find separator for entire UCQ
    # print("In find_Separator")

    for q in quantifier:
        for cq in UCQ:
            quant_count = 0
            for clause in range(len(cq)):
                # print(q,"&&",cq[clause])
                if q in cq[clause][1]["var"]:
                    # print("updated")
                    quant_count += 1
            if quant_count == len(cq) and q.isdigit() == False :  # if variable appears in all clauses, it is the separator
                quantifier[q] = 0
                return q

#fixed
def substitute(fp, UCQ, sep):
    UCQ1 = copy.deepcopy(UCQ)
    for cq in range(len(UCQ1)):
        for t in range(len(UCQ1[cq])):
            constant = True
            temp = UCQ1[cq][t][1]["var"]
            for i in range(0, len(temp)):
                if (sep == temp[i]):
                    temp[i] = str(fp)
                if (temp[i].isalpha()):
                    constant = False
            if (constant == True):
                UCQ1[cq][t][1]["const"] = True
                UCQ[cq][t][1]["const"] = True
    return UCQ1, UCQ

#fixed
def check_Independence_UCQ(UCQ):  # Check independence across entire UCQ, i.e. no repeating table names
    # print("check_Independence_UCQ")
    temp = set()
    for cq in range(len(UCQ)):
        for k in UCQ[cq]:
            # print("k",k)
            if k[0] in temp:
                return False
            else:
                temp.add(k[0])
    return True
#fixed
def getProbability(UCQ):
    # print("in getProbability")
    given_table_name = UCQ[0][0][0]
    constant_values = UCQ[0][0][1]["var"]
    # print(given_table_name,constant_values)
    flag = True
    for table_name, tuples in probabilities.items():
        if (table_name == given_table_name):
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
                # print("###",flag)
                if (flag == True):
                    # print(my_tuple[1])
                    return my_tuple[1]
    # print("0")
    return 0

#fixed
def allConstantParameters(subUCQ):  # checks if all variables are numbers and not characters
    for x in subUCQ[1]["var"]:
        if (x.isdigit() == False):
            return False
    return True


def split_into_connected_components(sub_UCQ):
    # print("split_into_connected_components", sub_UCQ)
    ucnf = []
    list_of_component_variables = []
    # print("UCNF",ucnf)
    for sub in sub_UCQ:
        # print("sub",sub, list_of_component_variables)
        flag = False
        for i in range(len(list_of_component_variables)):
            for j in sub[1]["var"]:
                if j in list_of_component_variables[i]:
                    if (j.isdigit() == False):
                        flag = True
                        ucnf[i][0].append(sub)
                        break
        if (flag == False):
            # print("False")
            list_of_component_variables.append(set(sub[1]["var"]))

            ucnf.append([[sub]])
    # print("ucnf",ucnf)
    return ucnf


def greaterThanTwoConnectedComponents(q_ucnf):
    # for q in q_ucnf:
    #     print("q",q)
    #     if (len(q[0]) > 1):
    #         return True
    # print(len(q_ucnf))
    if(len(q_ucnf)>1):
        return True
    return False


def convert_to_ucnf(UCQ):
    print("convert_to_ucnf", UCQ)
    ucnf = []
    if (len(UCQ) == 1):
        print("subcase 1")
        ucnf = split_into_connected_components(UCQ[0])
        # print("ucnf", ucnf)
        return ucnf
    q1_ucnf = split_into_connected_components(UCQ[0])
    q2_ucnf = split_into_connected_components(UCQ[1])
    print("q1", q1_ucnf, "q2", q2_ucnf)
    if (greaterThanTwoConnectedComponents(q1_ucnf)):
        print("subcase 2")
        q2_ucnf = [x[0] for x in q2_ucnf]
        for tp in q1_ucnf:
            print("tp", tp)
            toadd = convert_to_ucnf(q2_ucnf)[0]
            # print("toadd",toadd)
            for tadd in toadd:
                print("tadd",tadd)
                newtp =[]
                newtp.append(copy.deepcopy(tp[0]))

                newtp.append(tadd)
                # print("newtp",newtp)
                ucnf.append(newtp)
                # print("tadd", tadd)
                print("intermediat UCNF", ucnf)
            # tp.append(toadd)
            # ucnf.append(tp)
        # print("ucnf", ucnf)
        return ucnf
    elif (greaterThanTwoConnectedComponents(q2_ucnf)):
        print("subcase 3")
        q1_ucnf = [x[0] for x in q1_ucnf]
        for tp in q2_ucnf:
            # print("tp", tp)
            toadd = convert_to_ucnf(q1_ucnf)[0]
            for tadd in toadd:
                newtp =[]
                newtp.append(copy.deepcopy(tp))

                newtp.append(tadd[0])
                ucnf.append(newtp)
                # print("tadd", tadd)
                # print("intermediat UCNF", ucnf)
        # print("ucnf", ucnf)
        return [ucnf]
    else:
        print("subcase 4")
        return [UCQ]
def check_Independence_UCNF(ucnf):
    cnf_set = set()
    for cnf in ucnf:
        for q in cnf[0]:
            # print("q",q)
            if(q[0] in cnf_set):
                return False
            else:
                cnf_set.add(q[0])
    return True
def change_vars_if_needed(UCQ):
    cq1 = UCQ[0]
    cq2 = UCQ[1]
    table_name_1 = set()
    table_name_2 = set()
    for t in cq1:
        table_name_1.add(t[0])
    for t in cq2:
        table_name_2.add(t[0])
    common_table = ''
    for tname in table_name_1:
        if tname in table_name_2:
            common_table = tname
    common_table_vars = []
    equiv_vars = []
    for tables in cq1:
        if tables[0] == common_table:
            common_table_vars = tables[1]['var']
    for tables in cq2:
        if tables[0] == common_table:
            equiv_vars = tables[1]['var']
    equiv_vars_dict = {}
    for eq_ind in range(len(equiv_vars)):
        equiv_vars_dict[equiv_vars[eq_ind]] = eq_ind 
    for i in range(len(cq2)):
        for j in range(len(cq2[i][1]['var'])):
            if cq2[i][1]['var'][j] in equiv_vars_dict.keys():
                cq2[i][1]['var'][j] = common_table_vars[equiv_vars_dict[cq2[i][1]['var'][j]]] 
    del UCQ[1]
    UCQ.append(cq2)
    return UCQ
def cancellation(UCNF):
    print("cancellation")
    name = ''
    # print(UCNF)
    # print(UCNF[0])
    for i in range(len(UCNF)):
        if(UCNF[i][0][0][0] == UCNF[i][1][0][0]):
            name = UCNF[i][0][0][0]
            UCNF[i].pop()
            # print("CHECK",UCNF[0][i] )
    
    todel = -1
    print(name)
    print(UCNF)
    for i in range(len(UCNF)):
        # print("i",i,UCNF[0][i])
        if( len(UCNF[i])==2 and (UCNF[i][0][0][0] ==name or UCNF[i][1][0][0] ==name)):
            todel = i
    # print("$$",UCNF)
    del UCNF[i]
    print("++",UCNF)
    todel = -1
    # print('1')
    for i in range(len(UCNF)):
        cnf = UCNF[i]
        # print("^^",cnf, cnf[0][0], cnf[1][0], name,len(cnf)==2 )
        if( len(cnf)==2 and (cnf[0][0][0] ==name or cnf[1][0][0] ==name)):
            # print("fixing")
            todel = i
            break
    del UCNF[i]
    print("NEW UCNF", UCNF)
    return UCNF
def probability(UCQ):
    print(UCQ)
    # print("probability")
    sep = ""
    # Base of recursion
    # print(len(UCQ), len(UCQ[0]),allConstantParameters(UCQ[0][0]))
    if (len(UCQ) == 1 and len(UCQ[0]) == 1 and allConstantParameters(
            UCQ[0][0])):  # is a ground atom

        if (UCQ[0][0][1]["negation"] == False):
            print("CASE1**", getProbability(UCQ), UCQ)
            return getProbability(UCQ)  # checks if the given constant values are present in the given tables, if present return probability, else returns 0
        else:
            print("CASE1", 1 - getProbability(UCQ), UCQ)
            return 1 - getProbability(UCQ)
    if(len(UCQ)==2):
        UCQ = change_vars_if_needed(UCQ)
    # convert to ucnf
    UCNF = convert_to_ucnf(UCQ)
    #UCNF = []
    print("************************************************", UCNF)
    if(len(UCNF)==4):
        print("cancellation")
        UCNF = cancellation(UCNF)
        print("new UCNF", UCNF)
        # ans = 1 - ((1 - probability(UCNF[0])) *(1 - probability(UCNF[1])))
        print("case cancellation returning")
        # return ans
    #########I think the if condition below should be--if (len(UCNF) == 2 and type(UCNF[0]) is list):
    print(len(UCQ))
    if ((len(UCNF) == 2 )and check_Independence_UCNF(UCNF) and type(UCNF[0]) is list):  # both cq are independent of each other
        print("CASE2")
        ans = 1 - ((1 - probability(UCNF[0])) * (
                    1 - probability(UCNF[1])))
        print("CASE2 returning", ans)
        return ans
    #Inclusion Exclusion
    if (len(UCNF) ==2 and check_Independence_UCNF(UCNF)==False and type(UCNF[0]) is list):
        print("CASE 3")
        incexc = True
        for cnf in UCNF:
            if (check_Independence_UCQ(cnf) == False):
                incexc = False
        if (incexc == True):
            sign = -1
            addition = 0
            # Sums all the single terms since combiner function takes arguments for >=2 only.
            for i in range(len(UCNF)):
                addition = addition + probability(UCNF[i])
            print("addition1", addition)
            # Adds up all the combinations of 2,3...n terms in UCNF
            for i in range(2, len(UCNF) + 1):
                # Combination is an inbuilt function accepting array and number of terms in combination
                ans = list(combinations(UCNF, i))
                final = []
                for t in ans:
                    y = copy.deepcopy(t[0])
                    for i in range(1, len(t)):
                        for p in t[i]:
                            y.append(p)
                    final.append(y)
                for term in final:
                    addition = addition + (sign * probability(term))
                    print("addition",(sign * probability(term))," ",addition)
                sign = sign * -1
            print("CASE 3 returning", addition)
            return addition
    if (len(UCQ) == 2 and check_Independence_UCQ(UCQ)):
        print("CASE4", UCQ)
        Pr = 1.0
        for val in UCQ:
            # print("in",[{key:value}])
            Pr *= probability([val])
        print("CASE4 returning", Pr)
        return Pr
    sep = (find_Separator(UCQ))
    print("seperator",sep)
    if (sep is not None):
        print("CASE 5")
        Pr = 1.0
        for d in domain:
            UCQ1, UCQ = substitute(d, UCQ, sep)
            # print("in case 5",probability(UCQ1))
            Pr *= probability(UCQ1)
        print("CASE 5 returning", Pr)
        return Pr

    print("UNLIFTABLE", UCQ)
    return -1

#fixed
def get_domain(probabilities):
    domain = set()
    for table_name, tuples in probabilities.items():
        for my_tuple in tuples:
            for my_input in my_tuple[0]:
                if (my_input not in domain):
                    domain.add(my_input)
    return domain

#fixed
def parse_UCQ(input_query):
    UCQ = []
    quantifier = {}
    UCQ_list = input_query.split("||")  # split into individual conjunctions
    tables = []  # Represent all tables in each CQ
    for cq in UCQ_list:  # iterate through the above list, cq is each conjunction
        cq = cq.strip()  # remove spaces
        list_cq = cq.split(
            "),")  # to get list of relations. splitting by ), instead of , to ensure that it splits two relations and not withing a single relation
        dict_cq = []  # dictionary representing each conjunctive clause
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
            temp_list = [q[0], temp_dict]
            dict_cq.append(temp_list)  # append relation dictionary to the conjunctive clause dictionary
        UCQ.append(dict_cq)  # append conjunctive clause dictionary to the list of union of conjunctive clauses
        tables.append(temp_tables)
    return UCQ, quantifier, tables
def read_query(fname):
    f = open(fname, "r")
    query = f.read().splitlines()
    input_query="".join(query)
    return input_query
def parse_tables(tablefiles):
    probabilities = {}
    for tablefile in tablefiles:
        table_list = []
        tbf = open(tablefile, "r")
        tname = tbf.readline().strip()
        templist = tbf.read().splitlines()
        rows = []
        for t in templist:
            t2 = t.split(",")
            t2 = [tsub2.strip() for tsub2 in t2]
            prob = float(t2[len(t2)-1])
            del t2[len(t2)-1]
            var = [int(v) for v in t2]
            row = [var,prob]
            rows.append(row)
        probabilities[tname] = rows
    return probabilities
# print(read_query("query.txt"))
# print(parse_tables(["table1.txt", "table2.txt", "table3.txt"]))
# probabilities = {'R': [[[0], 0.7], [[1], 0.8], [[2], 0.6]], 'T': [[[0], 0.7], [[1], 0.3], [[2], 0.5]], 'S': [[[0, 0], 0.8], [[0, 1], 0.4], [[0, 2], 0.5], [[1, 2], 0.6], [[2, 2], 0.9]]}
probabilities = parse_tables(["table1.txt", "table2.txt", "table3.txt"])
domain = get_domain(probabilities)

# input_query = "R(x1),S(x1,y1) ||S(x2, y2), T(x2)"
input_query = read_query("query.txt")
UCQ, quantifier, tables = parse_UCQ(input_query)
# print("UCQ",UCQ)
# print("")
# probabilities = {'S': [0.8, 0.2, 0.3], 'R': [0.3, 0.4, 0.9]}
# probabilities = {'P': [[[0],0.7],[[1],0.8], [[2],0.6]], 'Q': [[[0],0.7],[[1],0.3], [[2],0.5]], 'R':[[[0,0],0.8],[[0,1],0.4],[[0,2],0.5],[[1,2],0.6],[[2,2],0.9]]}
# print("domain",domain)
# temp = [{'S': {'var': ['x'], 'negation': True, 'const': False},'R': {'var': ['x','y'], 'negation': True, 'const': False}}]
# print("geprob", getProbability(temp)) #testing
cnf = True
# temp_UCQ = [{'R': {'var': ['x', 'y'], 'negation': False, 'const': False}, 'Q': {'var': ['x'], 'negation': False, 'const': False}}]
print(1 - probability(UCQ))
