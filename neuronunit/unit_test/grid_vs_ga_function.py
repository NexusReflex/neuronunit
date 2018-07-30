import timeit
import numpy as np
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import math as math
from pylab import rcParams
from neuronunit.optimization.optimization_management import run_ga
from neuronunit.optimization.exhaustive_search import run_grid, reduce_params, create_grid
from neuronunit.optimization.model_parameters import model_params


import os
import pickle
from neuronunit.optimization.results_analysis import min_max, error_domination, param_distance


from neuronunit.optimization.results_analysis import make_report
from neuronunit.optimization import get_neab
import time

import nbformat
import os
from nbconvert.preprocessors import ExecutePreprocessor

import copy
reports = {}




electro_path = str(os.getcwd())+'/pipe_tests.p'
print(os.getcwd())
assert os.path.isfile(electro_path) == True
with open(electro_path,'rb') as f:
    electro_tests = pickle.load(f)

electro_tests = get_neab.replace_zero_std(electro_tests)
electro_tests = get_neab.substitute_parallel_for_serial(electro_tests)
test, observation = electro_tests[0]

npoints = 6
tests = copy.copy(electro_tests[0][0][0:2])
#tests+= electro_tests[0][0][4:-1]
#tests = copy.copy(electro_tests[0][0])




with open('pre_ga_reports.p','rb') as f:
    package = pickle.load(f)




#opt_keys = list(copy.copy(grid_results)[0].dtc.attrs.keys())
#ga_out = run_ga(model_params,nparams,npoints,tests,provided_keys = opt_keys)
#ga_out = run_ga(model_params,10,npoints,tests)#,provided_keys = opt_keys)


start_time = timeit.default_timer()
#sel = [str('selNSGA2'),str('selIBEA'),str('')]
flat_iter = [ (test, observation) for test, observation in electro_tests ] #for s in sel ]
print(flat_iter)



import shutil

def run_and_save(opt_keys,tests):
    nparams = len(opt_keys)

    it = timeit.default_timer()
    grid_results = run_grid(nparams,npoints,tests,provided_keys = opt_keys)
    ft = timeit.default_timer()
    elapsed_grid = ft - it
    with open('dim_{0}_errs{1}_grid.p','wb') as f:#
        pickle.dump([grid_results,opt_keys,tests,elapsed_grid],f)

    it = timeit.default_timer()
    ga_out = run_ga(model_params,nparams,npoints,tests,provided_keys = opt_keys, use_cache = True, cache_name='simple')
    ft = timeit.default_timer()
    elapsed_ga = ft - it

    shutil.chown('dim_{0}_errs{1}_ga.p', user='jovyan', group='user')

    with open('dim_{0}_errs{1}_ga.p'.format(len(opt_keys),len(tests)),'wb') as f:
       pickle.dump([ga_out,opt_keys,tests,elapsed_ga],f)
    file_name ='dim_{0}_errs{1}_ga.ipynb'.format(len(opt_keys),len(tests))

    shutil.chown(file_name, user='jovyan', group='user')

    #os.system("cp agreement_df.ipynb "+file_name)
    #os.system("ipython nbconvert --to html --execute "+file_name)


    with open('agreement_df.ipynb') as f:
        nb = nbformat.read(f, as_version=4)
    #ep = ExecutePreprocessor()
    ep = ExecutePreprocessor(timeout=5600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': os.getcwd()}})
    with open(file_name, 'wt') as f:
        nbformat(nb, f)
    return ga_out


for (s,test, observation) in flat_iter:
    opt_keys = [str('a'),str('vr'),str('b')]
    ga_out = run_and_save(opt_keys,test)
    pipe_results[dic_key] = ga_out


_ = run_and_save(opt_keys,tests)
import grid_vs_ga_h_constant