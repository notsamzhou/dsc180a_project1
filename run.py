import pandas as pd
import io
import os
import sys
import gzip
import numpy as np
import json
from sklearn.linear_model import LinearRegression
from scipy.stats import linregress
import swifter
import warnings
warnings.filterwarnings('ignore')

import src.clean_data as clean_data
import src.analysis as analysis
import src.clean as clean



def main(targets):

    data_config = json.load(open('config/data-params.json'))
    
    if not os.path.exists(os.getcwd() + '/data'):                
        os.system("mkdir data")
    
    if not os.path.exists(os.getcwd() + '/data/out'):                
        os.system("mkdir data/out")
    
    if targets[0] == 'all':
        clean_data.clean_vcf(**data_config)
        analysis.compute_eqtls(**data_config)
        
    else:
    
        if 'data' in targets:

            clean_data.clean_vcf(**data_config)

        if 'analysis' in targets:

            analysis.compute_eqtls(**data_config)
            
        if 'clean' in targets:
            
            clean.clean()


        if 'test' in targets:
            if not os.path.exists(os.getcwd() + '/test/out'):                
                os.system("mkdir test/out")

            clean_data.clean_vcf(**{**data_config, 'vcf_path':'test/testdata/test_genotypes.vcf', 'vcf_out_prefix':'test'})

            analysis.compute_eqtls(**{**data_config, 'vcf_path':'test/testdata/test_genotypes.vcf', 'expressions_path':'test/testdata/test_expressions.txt','populations_path': 'test/testdata/test_populations.txt', 'vcf_out_prefix':'test', 'outfile': 'test/out/test.csv'})

if __name__ == '__main__':
    
    targets = sys.argv[1:]
    main(targets)