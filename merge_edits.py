"""
Merge edits 
Usage: python merge_edits.py -dir . -sol sol_uedinms_kakao.txt
""" 

import argparse
import json
import os
import re
import utils


# Error types
ERROR_TYPES = ['M:ADJ', 'M:ADV', 'M:CONJ', 'M:CONTR', 'M:DET', 'M:NOUN', 'M:NOUN:POSS', 'M:OTHER', 'M:PART', 'M:PREP', 'M:PRON', 'M:PUNCT', 'M:VERB', 'M:VERB:FORM', 'M:VERB:TENSE', 'R:ADJ', 'R:ADJ:FORM', 'R:ADV', 'R:CONJ', 'R:CONTR', 'R:DET', 'R:MORPH', 'R:NOUN', 'R:NOUN:INFL', 'R:NOUN:NUM', 'R:NOUN:POSS', 'R:ORTH', 'R:OTHER', 'R:PART', 'R:PREP', 'R:PRON', 'R:PUNCT', 'R:SPELL', 'R:VERB', 'R:VERB:FORM', 'R:VERB:INFL', 'R:VERB:SVA', 'R:VERB:TENSE', 'R:WO', 'U:ADJ', 'U:ADV', 'U:CONJ', 'U:CONTR', 'U:DET', 'U:NOUN', 'U:NOUN:POSS', 'U:OTHER', 'U:PART', 'U:PREP', 'U:PRON', 'U:PUNCT', 'U:VERB', 'U:VERB:FORM', 'U:VERB:TENSE']


def clean_lingo_output_txt(lingoOut, lingoOutNew):
	# Retains those of x(sys, err_type) = 1
	a = utils.get_edits_by_groups(lingoOut, '-')
	pairs = a['---------------------\n']
	print(len(pairs))
	with open(lingoOutNew, 'w') as f:
		for x in pairs:
			y=x.split()
			if float(y[-1])==1.0: # find pairs that has a solution of 1
				sys_and_type = 'X('+y[0]+','+y[1]+')=1\n'
				f.write(sys_and_type)

def add_sys_id(sys, sys_id):
	sys = open(sys).read().strip().split("\n\n")
	sys = [x.split('\n') for x in sys]
	for i in range(len(sys)):
		for j in range(1, len(sys[i])):
			sys[i][j] = sys[i][j] +'|||'+'%s'%(sys_id)
	return sys

def merge_m2_sys_list(list_of_sys):
	# The order has to be according to step 1
	sys1_path = list_of_sys[0]
	sys1 = add_sys_id(sys1_path, 'sys1')
	rest = {}
	for i in range(1, len(list_of_sys)):
		sys = add_sys_id(list_of_sys[i], 'sys'+str(i+1))
		rest['sys'+str(i+1)] = sys
	ori_sentences = [x[0] for x in sys1]
	merged = sys1
	for i in range(len(ori_sentences)):
		for k in rest:
			merged[i].extend(rest[k][i][1:])
	return merged

def convert_to_corr_dict(raw_weights):
	# Convert Lingo solutions to dict; key: err_type, val: a list of system ids
	corr_dict = {}
	for i in range(len(ERROR_TYPES)):
		corr_dict[i] = []
	raw = open(raw_weights).readlines()
	for s in raw:
		m = re.search(r"\((.+)\)", s)
		weight_group = m.group()[1:-1].split(',')
		err_type = int(weight_group[1])-1 # minus 1 to be in range 0-53
		sys_id = weight_group[0]
		corr_dict[err_type].append('sys'+sys_id)
	return corr_dict

def correct_single_entry(key, annotations, corr_dict):
	# corr_dict contains the systems used for each error type; key: err_type, val: a list of system ids
	new_annotations = []
	for a in annotations:
		err_type = a.split('|||')[1]
		sys_id = a.strip().split('|||')[-1]
		if err_type == 'noop':
			new_annotations.append(a[:int(-(len(a.split('|||')[-1])+3))])
		else:
			err_type_id = str(ERROR_TYPES.index(err_type))
			if sys_id in corr_dict[err_type_id]:
				new_annotations.append(a[:int(-(len(a.split('|||')[-1])+3))])
	new_annotations = list(set(new_annotations))
	return new_annotations


def correct_all(merged_m2, corr_dict):
	merged = open(merged_m2).read().strip().split("\n\n")
	merged = [x.split('\n') for x in merged]
	corrected = []
	for group in merged:
		key = group[0]
		annotations = group[1:]
		a = [key]
		a.extend(correct_single_entry(key, annotations, corr_dict))
		corrected.append(a)
	# print('corrected len: ', len(corrected))
	return corrected

def remove_redundant_noop(ori_m2):
	# Remove redundant A -1 -1
	data = open(ori_m2).read().strip().split("\n\n")
	res = []
	noop = 'A -1 -1|||noop|||-NONE-|||REQUIRED|||-NONE-|||0'
	c1 = 0
	c2 = 0
	for i in range(len(data)):
		s = data[i].split('\n')[0]
		a = data[i].split('\n')[1:]
		a_cleaned = []
		if a == []:
			c1+=1
			sa = s+'\n'+noop
			res.append(sa)
		elif len(a) > 1:
			for x in a:
				if x != noop:
					a_cleaned.append(x)
				else:
					c2+=1
			sa = [s] + a_cleaned
			sa = '\n'.join(sa)
			res.append(sa)
		else:
			res.append(data[i])
	out_m2 = ori_m2
	with open(out_m2, 'w') as f:
		for x in res:
			f.write(x+'\n\n')

# Optional: check if .m2 contains conflicating annotations at the same location
def check_dups(M2):
	dummy = open(M2).read().strip().split('\n\n')
	dummy = [x.split('\n') for x in dummy]
	ori_sents = [x[0] for x in dummy]
	print('len ori_sents ', len(ori_sents))
	a = [[y.split('|||')[0] for y in x[1:]] for x in dummy]
	c = 0
	for i in range(len(a)):
		if len(a[i]) != len(set(a[i])):
			print(ori_sents[i], ' ', a[i])
			c+=1 
	print('Total number of sentences that contains duplicated annotations ', c)

def main(proj_dir, lingo_sol):

	print('Start converting lingo solutions to dict...')
	lingoOut = os.path.join(proj_dir, 'lingo/outputs/%s'%(lingo_sol))
	list_of_sys = lingo_sol.split('.')[0].split('_')[1:]
	# print('list_of_sys ', list_of_sys)

	# Load raw lingo output
	lingoOutNew = os.path.join(proj_dir, 'lingo/outputs/'+lingo_sol.split('.')[0]+'_raw.txt')
	clean_lingo_output_txt(lingoOut, lingoOutNew)    

	# Save cleaned output
	corr_dict = convert_to_corr_dict(lingoOutNew)
	dictOut = os.path.join(proj_dir, 'lingo/outputs/'+lingo_sol.split('.')[0]+'.json')
	with open(dictOut, 'w') as fp:
		json.dump(corr_dict, fp)
	print('Done!')

	# Merge edits
	print('Start merging edits...')
	with open(dictOut, 'r') as fp:
		corr_dict = json.load(fp)
	
	list_of_sys_paths = [os.path.join(proj_dir, 'data/test/%s-blind-test.m2'%(sys_name)) for sys_name in list_of_sys]
	merged_ori = merge_m2_sys_list(list_of_sys_paths)
	combName = '_'.join([x for x in list_of_sys])
	merged_ori_path = os.path.join(proj_dir, 'merged_m2/merged_ori_blind_test_%s.m2'%(combName))
	utils.write_list_to_m2(merged_ori, merged_ori_path)

	merged_nip = correct_all(merged_ori_path, corr_dict)
	merged_nip_path = os.path.join(proj_dir, 'merged_m2/merged_NIP_blind_test_%s.m2'%(combName))
	utils.write_list_to_m2(merged_nip, merged_nip_path)
	remove_redundant_noop(merged_nip_path)
	# check_dups(merged_nip_path)
	print('Done!')


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-dir", required=True, help='Path to project directory')
	parser.add_argument("-sol", required=True, help='Name of the Lingo solution file to the component systems combined.')
	args = parser.parse_args()
	main(args.dir, args.sol)

