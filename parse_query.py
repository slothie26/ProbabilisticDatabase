#def get_probability(UCQ, quantifier):
	
def check_Independence_CQ(cq): #check independence within a CQ
	tables = set()
	for clause in cq:
		if (cq[clause].get("name") in tables):
			return False;
		tables.add(cq[clause].get("name"))
	return True

def check_Independence_UCQ(tables): #Check independence across entire UCQ, i.e. no repeating table names
	temp = set()
	for cq in range(0, len(tables)):
		if not temp.isdisjoint(tables[cq]):
			return False
		temp = temp | tables[cq]
	return True

def find_Separator(UCQ, quantifier): #find separator for entire UCQ
	clause_count = 0
	for cq in UCQ: #calculates how many clauses are there in the UCQ
			for clause in cq:
				clause_count += 1
	for q in quantifier:
		if (quantifier[q] == 0): #if variable was already used as separator, don't check for it
			continue
		quant_count = 0
		for cq in UCQ:
			for clause in cq:
				if q in cq[clause].get("variables"):
					quant_count += 1
		if quant_count == clause_count: #if variable appears in all clauses, it is the separator
			quantifier[q] = 0
			return q

def parse_UCQ(input_query):
	UCQ = []
	quantifier = {}
	UCQ_list = input_query.split("||") 	#split into individual conjunctions
	tables = [] #Represent all tables in each CQ
	for cq in UCQ_list:  #iterate through the above list, cq is each conjunction
		cq = cq.strip() #remove spaces
		list_cq = cq.split("),") #to get list of relations. splitting by ), instead of , to ensure that it splits two relations and not withing a single relation
		dict_cq = {} #dictionary representing each conjunctive clause
		clause_count = 0
		temp_tables = {}
		temp_tables = set()
		for q in list_cq: #iterate through the relations within each conjunctive clause
			q = q.strip() #remove spaces
			q = q.split("(") #splitting by ( will ensure that the first index in the list is table name and second is variables
			temp_dict = {} #dict representing each relation
			temp_dict["name"] = q[0]
			temp_dict["variables"] = q[1].strip("").replace(")","").split(",") #remove spaces, remove the ) at the endd, and split by comma to get a list of variables
			temp_tables.add(q[0])
			for var in temp_dict["variables"]: #set the quantifier value as existential for all variables 
				quantifier[var] = 1
			dict_cq[clause_count] = temp_dict #append relation dictionary to the conjunctive clause dictionary
			clause_count+=1
		UCQ.append(dict_cq) #append conjunctive clause dictionary to the list of union of conjunctive clauses
		tables.append(temp_tables)
	return UCQ, quantifier, tables

input_query="R(x1),S(x1,y1) || R(x1)"
UCQ, quantifier, tables = parse_UCQ(input_query)
print(UCQ)
print(quantifier)

print(check_Independence_CQ(UCQ[0]))
print(check_Independence_UCQ(tables))
#After checking for independence, we can split the query and recursively apply lifted inference on each part

print(find_Separator(UCQ, quantifier))
print(quantifier)

#final_probability = get_probability(UCQ, quantifier)
