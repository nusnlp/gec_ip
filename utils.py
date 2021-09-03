# Error types
# ERROR_TYPES = ['M:ADJ', 'M:ADV', 'M:CONJ', 'M:CONTR', 'M:DET', 'M:NOUN', 'M:NOUN:POSS', 'M:OTHER', 'M:PART', 'M:PREP', 'M:PRON', 'M:PUNCT', 'M:VERB', 'M:VERB:FORM', 'M:VERB:TENSE', 'R:ADJ', 'R:ADJ:FORM', 'R:ADV', 'R:CONJ', 'R:CONTR', 'R:DET', 'R:MORPH', 'R:NOUN', 'R:NOUN:INFL', 'R:NOUN:NUM', 'R:NOUN:POSS', 'R:ORTH', 'R:OTHER', 'R:PART', 'R:PREP', 'R:PRON', 'R:PUNCT', 'R:SPELL', 'R:VERB', 'R:VERB:FORM', 'R:VERB:INFL', 'R:VERB:SVA', 'R:VERB:TENSE', 'R:WO', 'U:ADJ', 'U:ADV', 'U:CONJ', 'U:CONTR', 'U:DET', 'U:NOUN', 'U:NOUN:POSS', 'U:OTHER', 'U:PART', 'U:PREP', 'U:PRON', 'U:PUNCT', 'U:VERB', 'U:VERB:FORM', 'U:VERB:TENSE']

def get_groups(seq, group_by):  
	data = []
	for line in seq:
		if line.startswith(group_by):
			if data:
				yield data
				data = []
		data.append(line)
	if data:
		yield data

def get_edits_by_groups(filename, group_by):
	edits = {}
	with open(filename) as f:
		for i, group in enumerate(get_groups(f, group_by), start=1):
			edits[group[0]] = []
			for j in range(1, len(group)):
				if group[j] != '\n':
					edits[group[0]].append(group[j])
	#print('edits ', edits)
	return edits

def write_list_to_m2(l, m2_name):
    with open(m2_name, 'w') as f:
        for group in l:
            for s in group:
                f.write(s+'\n')
            f.write('\n')