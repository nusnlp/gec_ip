# System Combination for Grammatical Error Correction Based on Nonlinear Integer Programming
-------------------------------------------

This repository contains the code and scripts that implement the system combination approach for grammatical error correction in [Lin and Ng (2021)](#reference).

## Reference
Ruixi Lin and Hwee Tou Ng (2021). 
[System Combination for Grammatical Error Correction Based on Nonlinear Integer Programming](https://ranlp.org/ranlp2021/proceedings.pdf). 

Please cite: 
```
@inproceedings{lin2021gecip,
  author    = "Lin, Ruixi and Ng, Hwee Tou",
  title     = "System Combination for Grammatical Error Correction Based on Integer Programming",
  booktitle = "Proceedings of Recent Advances in Natural Language Processing",
  year      = "2021",
  pages     = "829-834"
}

```

**Table of contents**

[Prerequisites](#prerequisites)

[Example](#example)

[License](#license)


## Prerequisites

```
conda create --name comb python=3.6
conda activate comb
pip install spacy
python -m spacy download en
```

For the nonlinear integer programming solver, we use 

```
LINGO10.0
```


## Example

Combine the 3 GEC systems listed in the paper using the IP approach. The three systems are UEdin-MS (https://aclanthology.org/W19-4427), Kakao (https://aclanthology.org/W19-4423), and Tohoku (https://aclanthology.org/D19-1119). The core functions for the IP objective are implemented in model.lg4. You can find model.lg4 under `lingo/inputs`.

1. Run `python prepare_data.py -dir . -list kakao uedinms tohoku` to generate aggregated TP, FP, and FN counts. The counts files are stored under `lingo/inputs`.

2. Load model.lg4 into the LINGO console and specify the input data path with the counts file path, select the INLP model, and run optimizations. Store the solutions to `lingo/outputs/sol_kakao_uedinms_tohoku.txt`.

3. Run `./comb.sh . sol_kakao_uedinms_tohoku.txt` to load LINGO solutions, merge and apply edits. The resulted blind test file can be found under `submissions`. It can be zipped and submitted to the BEA CodeLab website (https://competitions.codalab.org/competitions/20228) for evaluations.


The `data` folder provides individual GEC system output files, and .m2 files generated using ERRANT for the listed systems. For more information, please visit the [ERRANT github page](https://github.com/chrisjbryant/errant).

We include the IP combined .m2 files under `merged_m2`, and the corresponding text files under `submissions`.


## License
The source code and models in this repository are licensed under the GNU General Public License v3.0 (see [LICENSE](LICENSE)). For further research interests and commercial use of the code and models, please contact Ruixi Lin (ruixi@u.nus.edu) and Prof. Hwee Tou Ng (nght@comp.nus.edu.sg).


