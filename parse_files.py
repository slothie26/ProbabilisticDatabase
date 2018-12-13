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
print(read_query("query.txt"))
print(parse_tables(["table1.txt", "table2.txt", "table3.txt"]))