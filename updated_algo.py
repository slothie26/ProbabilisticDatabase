probabilities = {}
import sys
import copy
from itertools import combinations
import getopt
import matplotlib.pyplot as plt  
import random 
import numpy as np
import re
import math
from scipy.stats import multivariate_normal
#fixed
sd=1
mean=0
root2pi=math.sqrt(2*math.pi)
dr=2*(sd**2)  
safeQuery = 0
def decision(prob):
	# print("prob",type(prob), random.random())
	if(random.random()<float(prob)):
		return True
	else:
		return False


def generateconcDatabases(database):
	concDatabases={}
	for key in database:
		list=database[key]
		#print(list)
		concDatabase=[]
		for element in list:
			k=next(iter(element))
			val=element[k]
			flip=decision(val)
			if flip:
				concDatabase.append(k)
		concDatabases[key]=concDatabase
	return concDatabases  


def exponentialDistribution(x):
	if x<0:
		return 0
	else:
		return math.exp(-x)
def gaussianDistribution(x):
	nr=-(x-mean)**2
	return (1/(sd*root2pi))*math.exp(nr/dr)


def metropolisHastings(copyDatabase):
	for key in copyDatabase:
		list=copyDatabase[key]
		new_list=[]
		for element in list:    
			k=next(iter(element))
			currentState=element[k]
			#proposedState=abs(currentState+np.random.normal(currentState,1,size=1)[0])%1
			proposedState=np.clip(currentState+np.random.normal(0,1,size=1)[0],0,1)
			acceptanceProbability=min(1,exponentialDistribution(proposedState)/exponentialDistribution(currentState))         
			randomNumber=np.random.uniform(0,1)
			toAdd={}
			if randomNumber<=acceptanceProbability:
				toAdd[k]=proposedState
			else:
				toAdd[k]=currentState
			new_list.append(toAdd)
		copyDatabase[key]=new_list
	return generateconcDatabases(copyDatabase)    

def getProposedState(list,k):
	for element in list:
		prob=1
		key=next(iter(element))
		val=element[key]
		if key==k:
			prob=float(val)
			break
	if prob!=1:    
		return prob/(1-prob)
	else:
		return 0 
	
def gibbsSampling(copyDatabase):
	for key in copyDatabase:
		list=copyDatabase[key]
		new_list=[]
		for element in list:
			k=next(iter(element))
			currentState=element[k]
			proposedState=getProposedState(list,k)
			proposedState=gaussianDistribution(proposedState)
			toAdd={}
			toAdd[k]=proposedState
			new_list.append(toAdd)
		copyDatabase[key]=new_list
	return generateconcDatabases(copyDatabase)        
	
def findTuples(concDatabase, table):
	tuples = set()
	entries = concDatabase[table]
	for var in entries:
		if len(var) == 1:
			tuples.add(var)
		else:
			for i in var:
				tuples.add(i)
	#print("tuples are: ", tuples)
	return tuples    

#Generate all possible assignments for variables
def getAssignments(variables, index, domains, assignment, allAssignments):
	if (index == len(variables)):
		tempAssignment = copy.deepcopy(assignment)
		allAssignments.append(tempAssignment)
	else:
		for i in range(0, len(domains[index])):
			assignment.append(domains[index][i])
			getAssignments(variables, index+1, domains, assignment, allAssignments)
			del assignment[-1]     

def processClause(clause, concDatabase):
	literals = clause.split("^")
	variables = set()
	tables = []
	domains = []
	for l in literals:
		l = l[:-1]
		values = l.split("(")
		vars = values[1].split(",")
		for v in vars:
			variables.add(v)
	variables = list(variables)
	for var in variables:
		table = []
		domain = set()
		for l in literals:
			if l.find(var) != -1:
				table.append(l[0])
				domain = domain.union(findTuples(concDatabase,l[0]))
		tables.append(table)
		domains.append(list(domain))
	return variables, tables, domains
	
def evaluateQuery(inputQuery, concDatabase):
	clauses = inputQuery.split("||")
	#print("Clauses are: ", clauses)  
	for clause in clauses:
		flag = False
		variables, tables, domains = processClause(clause, concDatabase)
		
		#Variables: all vars in the clause e.g. [x, y]
		#tables: which var appears in which table, order same as 'variables' e.g. [[R, S], [S, T]]
		#Domains: Domain of each variable e.g [[A,B,C],[B,C,D]]

		allAssignments = []
		assignment = []
		getAssignments(variables, 0, domains,assignment, allAssignments)
		
		#ClauseSplit: Variables in each Table e.g {'R': ['x'], 'S': ['x', 'y'], 'T': ['y']}
		clauseSplit = {}
		literals = clause.split("^")
		for literal in literals:
			literal = literal[:-1]
			temp = literal.split("(")
			key = temp[0]
			values = temp[1].split(",")
			clauseSplit[key] = values
		
		#Evaluate query for each assignment
		for assn in allAssignments:
			#print("For Assignment ", assn)
			flag = False
			
			#Evaluate for each literal
			for key, value in clauseSplit.items():        
				#Tuple will contain assignment for each var for comparison e.g ['A'] or ['A', 'B']
				tuple = []
				for i in value:
					index = variables.index(i)
					val = assn[index]
					tuple.append(val)
				found = False
				
				#Check if that tuple is present in concDatabase
				for tuples in concDatabase[key]:
					if tuple == list(tuples):
						found = True
						break
						
				#if tuple not present: literal evaluates to false, clause is false for that assignment, break and move to next assignment    
				if found == False:
					#print("Could not find tuple in concDB")
					flag = True
					break
			
			#No literal evaluated to false(No break) -> found an assignment for this clause -> makes entire query true
			if flag == False:
				#print("Found an assignment")
				#print("Clause ", clause, " evaluated to true")
				return True
	return False

def callSampler(sampler, total_no_of_samples, database):
	count = 0
	total_prob = 0
	total_error = 0
	x_axis = []
	y_axis = []
	if safeQuery == 1:
		expectedProb = prob
	else:
		expectedProb = 0
	
	if sampler == 0:
		print ("Monte Carlo Sampler")
		for no_of_samples in range(1, total_no_of_samples + 1):
			count = 0
			for iterate in range(0,no_of_samples):
				concDatabases=generateconcDatabases(database)
				#print ('concDatabases: ', concDatabases)
				result = evaluateQuery(inputQuery, concDatabases)
				#print("Result of evaluation: ", result)
				if result == True:
					count = count + 1
			probability = count/no_of_samples
			#print("Probability of query is: ", probability)
			total_prob = probability+ total_prob
			error = abs(probability - expectedProb)
			total_error = total_error + error
			y_axis.append(error)
			x_axis.append(no_of_samples)
	elif sampler == 1:
		print ("Metropolis-Hastings MCMC")
		copyDatabase={}
		copyDatabase=copy.deepcopy(database)
		for no_of_samples in range(1, total_no_of_samples + 1):
			count = 0
			for iterate in range(0,no_of_samples):
				concDatabases=generateconcDatabases(database)
				#print("concDatabases: ", concDatabases)
				result = evaluateQuery(inputQuery, concDatabases)
				if result == True:
					count = count + 1
			probability = count/no_of_samples
			total_prob = probability+ total_prob
			error = abs(probability - expectedProb)
			total_error = total_error + error
			y_axis.append(error)
			x_axis.append(no_of_samples)
	elif sampler == 2:
		print ("Gibbs MCMC")
		copyDatabase={}
		copyDatabase=copy.deepcopy(database)
		for no_of_samples in range(1, total_no_of_samples + 1):
			count = 0
			for iterate in range(0,no_of_samples):
				concDatabases=gibbsSampling(copyDatabase)
				result = evaluateQuery(inputQuery, concDatabases)
				if result == True:
					count = count + 1
			probability = count/no_of_samples
			total_prob = probability+ total_prob
			error = abs(probability - expectedProb)
			total_error = total_error + error
			y_axis.append(error)
			x_axis.append(no_of_samples)
			'''
	if sampler == 0:
		for no_of_samples in range(1, total_no_of_samples + 1):
			concDatabases=generateconcDatabases(database)
			#print("concDatabases: ", concDatabases)
			result = evaluateQuery(inputQuery, concDatabases)
			if result == True:
				count = count + 1
			probability = count/no_of_samples
			error = abs(probability - expectedProb)
			total_prob = probability+ total_prob
			total_error = total_error + error
			y_axis.append(error)
			x_axis.append(no_of_samples)
			
	elif sampler == 1:
		print ("Metropolis-Hastings MCMC")
		copyDatabase={}
		copyDatabase=copy.deepcopy(database)
		for no_of_samples in range(1, total_no_of_samples + 1):
			concDatabases=metropolisHastings(copyDatabase)
			result = evaluateQuery(inputQuery, concDatabases)
			if result == True:
				count = count + 1
			probability = count/no_of_samples
			error = abs(probability - expectedProb)
			total_prob = probability+ total_prob
			total_error = total_error + error
			y_axis.append(error)
			x_axis.append(no_of_samples)
		
	elif sampler == 2:
		print ("Gibbs MCMC")
		copyDatabase={}
		copyDatabase=copy.deepcopy(database)
		for no_of_samples in range(1, total_no_of_samples + 1):
			concDatabases=gibbsSampling(copyDatabase)
			result = evaluateQuery(inputQuery, concDatabases)
			if result == True:
				count = count + 1
			probability = count/no_of_samples
			error = abs(probability - expectedProb)
			total_prob = probability+ total_prob
			total_error = total_error + error
			y_axis.append(error)
			x_axis.append(no_of_samples)
			'''
	avg_prob = total_prob/total_no_of_samples
	avg_error = total_error/total_no_of_samples
	print("Average probability is: ", avg_prob)
	if safeQuery == 1: 
		print("Average error is: ", avg_error)
		plt.plot(x_axis, y_axis)
		plt.xlabel("Number of Samples")
		plt.ylabel("Error Rate")
		plt.title("Plot of Error Rate vs. Number of Samples")
		plt.show()

def getInitialDatabase(tableFiles):
	database={}
	for tableFile in tableFiles:
		table=[]
		fh=open(tableFile,"r")
		lineCount=1
		for line in fh:
			if lineCount==1:
				lineCount=lineCount+1
				mainKey=line.strip()
				continue
			else:
				lineSplit=re.split(",",line)
				val=lineSplit[-1].strip()
				localDict={}
				localList=[]
				valueCount=0;
				for value in lineSplit:
					if value.strip()!=val:
						localList.append(value)
				if len(localList)>1:    
					localTuple=tuple(localList)
				else:
					localTuple=localList[0]
				localDict[localTuple]=val
				table.append(localDict)
		database[mainKey]=table 
		fh.close()
	return database


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
	# print("convert_to_ucnf", UCQ)
	ucnf = []
	if (len(UCQ) == 1):
		# print("subcase 1")
		ucnf = split_into_connected_components(UCQ[0])
		# print("ucnf", ucnf)
		return ucnf
	q1_ucnf = split_into_connected_components(UCQ[0])
	q2_ucnf = split_into_connected_components(UCQ[1])
	# print("q1", q1_ucnf, "q2", q2_ucnf)
	if (greaterThanTwoConnectedComponents(q1_ucnf)):
		# print("subcase 2")
		q2_ucnf = [x[0] for x in q2_ucnf]
		for tp in q1_ucnf:
			# print("tp", tp)
			toadd = convert_to_ucnf(q2_ucnf)[0]
			# print("toadd",toadd)
			for tadd in toadd:
				# print("tadd",tadd)
				newtp =[]
				newtp.append(copy.deepcopy(tp[0]))

				newtp.append(tadd)
				# print("newtp",newtp)
				ucnf.append(newtp)
				# print("tadd", tadd)
				# print("intermediat UCNF", ucnf)
			# tp.append(toadd)
			# ucnf.append(tp)
		# print("ucnf", ucnf)
		return ucnf
	elif (greaterThanTwoConnectedComponents(q2_ucnf)):
		# print("subcase 3")
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
		# print("subcase 4")
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
	# print("cancellation")
	name = ''
	# print(UCNF)
	# print(UCNF[0])
	for i in range(len(UCNF)):
		if(UCNF[i][0][0][0] == UCNF[i][1][0][0]):
			name = UCNF[i][0][0][0]
			UCNF[i].pop()
			# print("CHECK",UCNF[0][i] )
	
	todel = -1
	# print(name)
	# print(UCNF)
	i = 0
	for i in range(len(UCNF)):
		# print("i",i,UCNF[i])
		if( len(UCNF[i])==2 and (UCNF[i][0][0][0] ==name or UCNF[i][1][0][0] ==name)):
			# print(i, len(UCNF[i]))
			todel = i
	# print("$$",UCNF)
	del UCNF[todel]
	# print("++",UCNF)
	todel = -1
	# print('1')
	i = 0
	for i in range(len(UCNF)):
		cnf = UCNF[i]
		# print("^^",cnf, cnf[0][0], cnf[1][0], name,len(cnf)==2 )
		if( len(cnf)==2 and (cnf[0][0][0] ==name or cnf[1][0][0] ==name)):
			# print("fixing")
			todel = i
			break
	del UCNF[todel]
	# print("NEW UCNF", UCNF)
	return UCNF
def probability(UCQ):
	# print(UCQ)
	# print("probability")
	sep = ""
	# Base of recursion
	# print(len(UCQ), len(UCQ[0]),allConstantParameters(UCQ[0][0]))
	if (len(UCQ) == 1 and len(UCQ[0]) == 1 and allConstantParameters(
			UCQ[0][0])):  # is a ground atom

		if (UCQ[0][0][1]["negation"] == False):
			# print("CASE1**", getProbability(UCQ), UCQ)
			return getProbability(UCQ)  # checks if the given constant values are present in the given tables, if present return probability, else returns 0
		else:
			# print("CASE1", 1 - getProbability(UCQ), UCQ)
			return 1 - getProbability(UCQ)
	if(len(UCQ)==2):
		UCQ = change_vars_if_needed(UCQ)
	# convert to ucnf
	UCNF = convert_to_ucnf(UCQ)
	#UCNF = []
	# print("************************************************", UCNF)
	if(len(UCNF)==4):
		# print("cancellation")
		UCNF = cancellation(UCNF)
		# print("new UCNF", UCNF)
		# ans = 1 - ((1 - probability(UCNF[0])) *(1 - probability(UCNF[1])))
		# print("case cancellation returning")
		# return ans
	#########I think the if condition below should be--if (len(UCNF) == 2 and type(UCNF[0]) is list):
	# print(len(UCQ))
	if ((len(UCNF) == 2 )and check_Independence_UCNF(UCNF) and type(UCNF[0]) is list):  # both cq are independent of each other
		# print("CASE2")
		ans = 1 - ((1 - probability(UCNF[0])) * (
					1 - probability(UCNF[1])))
		# print("CASE2 returning", ans)
		return ans
	#Inclusion Exclusion
	#'''len(UCNF) ==2 and'''
	if ( check_Independence_UCNF(UCNF)==False and type(UCNF[0]) is list):
		# print("CASE 3")
		incexc = True
		for cnf in UCNF:
			if (check_Independence_UCQ(cnf) == False):
				incexc = False
		# print(incexc)
		if (incexc == True):
			sign = -1
			addition = 0
			# Sums all the single terms since combiner function takes arguments for >=2 only.
			for i in range(len(UCNF)):
				temp_pr = probability(UCNF[i])
				# print("T", temp_pr)
				if(temp_pr!=-1):
					addition = addition + temp_pr
			# print("addition1", addition)
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
					temp_pr = probability(term)
					# print("TT",temp_pr)
					if(temp_pr!=-1):
						addition = addition + (sign *  temp_pr)
					# print("addition",(sign * probability(term))," ",addition)
				sign = sign * -1
			# print("CASE 3 returning", addition)
			return addition
	if (len(UCQ) == 2 and check_Independence_UCQ(UCQ)):
		# print("CASE4", UCQ)
		Pr = 1.0
		for val in UCQ:
			# print("in",[{key:value}])
			Pr *= probability([val])
		# print("CASE4 returning", Pr)
		return Pr
	sep = (find_Separator(UCQ))
	# print("seperator",sep)
	if (sep is not None):
		# print("CASE 5")
		Pr = 1.0
		for d in domain:
			UCQ1, UCQ = substitute(d, UCQ, sep)
			# print("in case 5",probability(UCQ1))
			Pr *= probability(UCQ1)
		# print("CASE 5 returning", Pr)
		return Pr

	# print("UNLIFTABLE", UCQ)
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
def get_input():
   l = len(sys.argv)
   queryFile = sys.argv[1]
   try:
	   opts, args = getopt.getopt(sys.argv[1:], "h",["query=", "table="])
   except getopt.GetoptError as err:
	   # print help information and exit:
	   print (str(err))  # will print something like "option -a not recognized"
	   sys.exit(2)
   return opts,args

def parseHardQuery(input_query):
	input_query = input_query.strip()
	input_query = input_query.replace(" ","")
	input_query = input_query.replace("),",")^")
	return input_query

tableFiles = []
opts, args = get_input()
for i in range(1,len(opts)):
	tableFiles.append(opts[i][1])

queryFile = opts[0][1]
# print(queryFile)

# print(read_query("query.txt"))
# print(parse_tables(["table1.txt", "table2.txt", "table3.txt"]))
# probabilities = {'R': [[[0], 0.7], [[1], 0.8], [[2], 0.6]], 'T': [[[0], 0.7], [[1], 0.3], [[2], 0.5]], 'S': [[[0, 0], 0.8], [[0, 1], 0.4], [[0, 2], 0.5], [[1, 2], 0.6], [[2, 2], 0.9]]}
probabilities = parse_tables(tableFiles)
domain = get_domain(probabilities)

# input_query = "R(x1),S(x1,y1) ||S(x2, y2), T(x2)"
input_query = read_query(queryFile)
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
database=getInitialDatabase(tableFiles)
inputQuery=parseHardQuery(input_query)
copyQuery=inputQuery.replace("||","^")
print('inputQuery: ',inputQuery)
inputQuery_split=re.split("\^",copyQuery)

try:
	prob = 1 - probability(UCQ)
	if(prob>=0 and prob<=1):
		print("Probability using Lifted Inference:",prob)
		safeQuery = 1
		callSampler(0,1000,database)
		callSampler(1,1000,database)
		callSampler(2,1000,database)

	else:	
		print("UNLIFTABLE by lifted inference")
		callSampler(0,1000,database)
		callSampler(1,1000,database)
		callSampler(2,1000,database)

except Exception as e:
	print("UNLIFTABLE by lifted inference")
	print(e)
	safeQuery = 0
	callSampler(0,1000,database)
	callSampler(1,1000,database)
	callSampler(2,1000,database)

