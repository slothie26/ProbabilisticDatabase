def get_probability(UCQ, quantifier):
	
def parse_UCQ(input_query):
	UCQ = []
	quantifier = {}
	UCQ_list = input_query.split("||") #split into individual conjunctions
	for cq in UCQ_list: #iterate through the above list, cq is each conjunction
		cq = cq.strip() #remove spaces
		list_cq = cq.split("),") #to get list of relations. splitting by ), instead of , to ensure that it splits two relations and not withing a single relation
		dict_cq = {} #dictionary representing each conjunctive clause
		clause_count = 0
		for q in list_cq: #iterate through the relations within each conjunctive clause
			q = q.strip() #remove spaces
			q = q.split("(") #splitting by ( will ensure that the first index in the list is table name and second is variables
			temp_dict = {} #dict representing each relation
			temp_dict["name"] = q[0]
			temp_dict["variables"] = q[1].strip("").replace(")","").split(",") #remove spaces, remove the ) at the endd, and split by comma to get a list of variables
			for var in temp_dict["variables"]: #set the quantifier value as existential for all variables 
				quantifier[var] = 1
			dict_cq[clause_count] = temp_dict #append relation dictionary to the conjunctive clause dictionary
			clause_count+=1
		UCQ.append(dict_cq) #append conjunctive clause dictionary to the list of union of conjunctive clauses
	return UCQ, quantifier

input_query="R(x1),S(x1,y1) || S(x2, y2), T(x2)"
UCQ, quantifier = parse_UCQ(input_query)
print(UCQ)
print(quantifier)
final_probability = get_probability(UCQ, quantifier)