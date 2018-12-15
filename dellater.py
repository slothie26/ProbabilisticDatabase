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
ucq = [[['R', {'var': ['x1', ' y1'], 'negation': True, 'const': True}], ['P', {'var': ['x1'], 'negation': True, 'const': True}]], [['Q', {'var': ['x2'], 'negation': True, 'const': True}], ['R', {'var': ['x2', ' y2'], 'negation': True, 'const': True}]]]
print(change_vars_if_needed(ucq))