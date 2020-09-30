# ACECA-simple-classification

This repository is for preprint paper *Asynchronous communicating cellular automata: formalization, robustness and equivalence*

## Requirements for using this library 
Python 3.5.3, numpy 1.14.0, and matplotlib 2.0.2, pandas 1.0.3.

## The file list
generate_Fig_5x5_time_space_diagram.py : generate Fig. 5 in paper

generate_Fig_sampling_surface.py : generate Fig. 6 in paper

generate_Fig_ph_time_space_diagram.py : generate Fig. 7 in paper

generate_Fig_phase_transition.py : generate Fig. 8 in paper

acca/ECA.py: ECA model. generate Fig.9 (a) in paper.

acca/ACECA.py: ACECA model. generate Fig.9 (b) in paper.

acca/m3.py: ($m^3$ )ACCA model which can simulate ECA. 

acca/m2_2m.py: ($m^2+2m$ )ACCA model which can simulate ECA. 

acca/plot_ACCA.py: generate Fig.10(a, b, c) 、Fig.11(a, b, c)、Fig.12 in paper.

## Dir

util: some helper functions and class.

data/aceca_surface : the data for draw ACECA sampling surface and there are 88 rules for ECA. The data format is that m*n matrix. Rows represent the d_ini and columns represent the alpha.

data/ECAsurface_new : the data for draw AECA sampling surface and there are 88 rules for ECA.

data/ph : the data for draw phase transition plots. ACECA_dic.npy is for before modified algorithm 1, and ACECAph_dic_dpAll.npy is for after modified algorithm 1. The detail of usage can find in file generate_Fig_phase_transition.py. The data in it contains at least the SPT class.

acca/result: the images of CA.



