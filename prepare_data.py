"""
Aggregate TP, FP, FN counts for component systems
Usage: python prepare_data.py -dir . -list kakao uedinms tohok

""" 

import argparse
import json
import os
import utils


# Error types
ERROR_TYPES = ['M:ADJ', 'M:ADV', 'M:CONJ', 'M:CONTR', 'M:DET', 'M:NOUN', 'M:NOUN:POSS', 'M:OTHER', 'M:PART', 'M:PREP', 'M:PRON', 'M:PUNCT', 'M:VERB', 'M:VERB:FORM', 'M:VERB:TENSE', 'R:ADJ', 'R:ADJ:FORM', 'R:ADV', 'R:CONJ', 'R:CONTR', 'R:DET', 'R:MORPH', 'R:NOUN', 'R:NOUN:INFL', 'R:NOUN:NUM', 'R:NOUN:POSS', 'R:ORTH', 'R:OTHER', 'R:PART', 'R:PREP', 'R:PRON', 'R:PUNCT', 'R:SPELL', 'R:VERB', 'R:VERB:FORM', 'R:VERB:INFL', 'R:VERB:SVA', 'R:VERB:TENSE', 'R:WO', 'U:ADJ', 'U:ADV', 'U:CONJ', 'U:CONTR', 'U:DET', 'U:NOUN', 'U:NOUN:POSS', 'U:OTHER', 'U:PART', 'U:PREP', 'U:PRON', 'U:PUNCT', 'U:VERB', 'U:VERB:FORM', 'U:VERB:TENSE']


def convert_errant_stats_to_lingo_input(errant_stats):
	data = utils.get_edits_by_groups(errant_stats, "=")['===================== Span-Based Correction ======================\n'][1:]
	data_tp={}
	data_fp={}
	data_fn={}
	for x in data:
		xsplit = x.split()
		data_tp[xsplit[0]] = xsplit[1]
		data_fp[xsplit[0]] = xsplit[2]
		data_fn[xsplit[0]] = xsplit[3]
	for t in ERROR_TYPES:
		if t not in data_tp:
			data_tp[t] = '0'
		if t not in data_fp:
			data_fp[t] = '0'
		if t not in data_fn:
			data_fn[t] = '0'
	return data_tp, data_fp, data_fn

def write_to_lingo_input_txt(outfile, stats):
	# write to .txt file
	length = len(stats[0])
	if not os.path.exists(os.path.dirname(outfile)):
		try:
			os.makedirs(os.path.dirname(outfile))
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				raise

	with open(outfile, 'w') as f:
		for i in range(1, length):
			f.write('%d '%(i))
		f.write(str(length)+'\n')
		f.write('~\n')
		f.write('1..54\n')
		f.write('~\n\n')
		for stat in stats:
			for sys in stat:
				for i in range(len(ERROR_TYPES)-1):
					t = ERROR_TYPES[i]
					f.write(sys[t]+'\t')
				f.write(sys[ERROR_TYPES[-1]]+'\n')
			f.write('\n~\n')



def main(proj_dir, list_of_sys):

	# Prepare counts for component systems
	allTP = []
	allFP = []
	allFN = []
	for errant_stats_prefix in list_of_sys:
		errant_stats = os.path.join(proj_dir, 'data/dev/%s-whole-dev.stats'%(errant_stats_prefix))
		data_tp, data_fp, data_fn = convert_errant_stats_to_lingo_input(errant_stats)
		allTP.append(data_tp)
		allFP.append(data_fp)
		allFN.append(data_fn)

	# Write to file
	stats = [allTP, allFP, allFN]
	combname = '_'.join([name for name in list_of_sys])
	lingoIn = os.path.join(proj_dir, 'lingo/inputs/counts_whole_dev_%s.txt'%(combname))
	write_to_lingo_input_txt(lingoIn, stats)
	print('Generated lingo inputs for %s, saved at %s'%(combname, lingoIn))



if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-dir", required=True, help='Path to project directory')
	parser.add_argument("-list", nargs="+", default=['uedinms', 'kakao'], help='A list of component systems, sys1 sys2 sys3...')
	args = parser.parse_args()
	main(args.dir, args.list)

