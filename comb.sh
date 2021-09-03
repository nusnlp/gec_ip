#!/bin/sh

set -x
set -e

if [ $# -ne 2 ]; then
	echo "Usage: `basename $0` <project-dir> <lingo-sol-file>"
fi

PROJ_DIR=$1
SOL_FILE=$2


echo "[`date`] ***Merge and apply edits following the NIP optimized selection variables***" >&2

python ${PROJ_DIR}/merge_edits.py -dir $PROJ_DIR -sol $SOL_FILE

mkdir -p ${PROJ_DIR}/submissions
OUT_DIR=${PROJ_DIR}/submissions

filename=$(basename -- "$SOL_FILE")
filename="${filename%.*}"
combname="$(cut -d "_" -f2- <<< "$filename")"

python ${PROJ_DIR}/m2_to_parallel_with_spacy_tok_rules.py -m2 ${PROJ_DIR}/merged_m2/merged_NIP_blind_test_${combname}.m2 -out ${OUT_DIR}/merged_NIP_blind_test_${combname} --copy-unchanged-source