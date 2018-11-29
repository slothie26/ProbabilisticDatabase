probabilities = {}
def no_existential_quantifier(sub_CQ,quantifier):
	#Check if the none of the variables in the UCQ are existential in quantifier dict.
	print("SUBCQ-no",sub_CQ,quantifier  )
	for vars in sub_CQ["var"]:
		if(quantifier[vars]==1):
			return False
	return True
def update_quantifiers(sub_CQ, quantifiers):
	print("SUBCQ-up")
	for vars in sub_CQ["var"]:
		if(quantifier[vars]==1):
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
	print("getProbability", UCQ)
	print(probabilities)
	for k,v in UCQ.items():
		print(k)
		prob_list = probabilities[k]
		ans = 1.0
		if(v["negation"]==False):
			for i in prob_list:
				ans*=i
			return ans
		else:
			for i in prob_list:
				ans*=(1-i)
			return ans

	return 0.3

def probability(UCQ, quantifiers, tables):
	# Base of recursion
	if len(UCQ)==1:
		if(no_existential_quantifier(UCQ[0][list(UCQ[0].keys())[0]],quantifiers)):
			print("CASE1")
			return getProbability(UCQ[0])
		else:
			print("CASE2")
			quantifiers = update_quantifiers(UCQ[0][list(UCQ[0].keys())[0]],quantifiers)
			UCQ[0][list(UCQ[0].keys())[0]]["negation"] = True
			return 1 - probability(UCQ, quantifiers,tables)
	else:
		print("CASE3")
	 # decomposable disjunction
	 # elif isUCQ(UCQ):
	 #     if check_Independence_UCQ(tables):
	 #         val1 = 1 - probability(UCQ[0], quantifier, tables)
	 #         val2 = 1 - probability(UCQ[1], quantifier, tables)
	 #         return 1 - val1 * val2
	 # # decomposable conjunction
	 # elif check_Independence_CQ(UCQ):
	 #     val1 = probability(UCQ[0], quantifier, tables)
	 #     val2 = probability(UCQ[1], quantifier, tables)
	 #     return val1 * val2
def parse_UCQ(input_query):
	UCQ = []
	quantifier = {}
	UCQ_list = input_query.split("||")  # split into individual conjunctions
	tables = []  # Represent all tables in each CQ
	for cq in UCQ_list:  # iterate through the above list, cq is each conjunction
			cq = cq.strip()  # remove spaces
			list_cq = cq.split("),")  # to get list of relations. splitting by ), instead of , to ensure that it splits two relations and not withing a single relation
			dict_cq = {}  # dictionary representing each conjunctive clause
			temp_tables = set()
			for q in list_cq:  # iterate through the relations within each conjunctive clause
					q = q.strip()  # remove spaces
					q = q.split("(")  # splitting by ( will ensure that the first index in the list is table name and second is variables
					temp_dict = {}
					temp_dict["var"] = q[1].strip("").replace(")", "").split(",")  # remove spaces, remove the ) at the endd, and split by comma to get a list of variables
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
print(UCQ)
print(quantifier)
print(tables)
probabilities={'S':[0.8,0.2,0.1]}
print(probability(UCQ,quantifier,tables))

