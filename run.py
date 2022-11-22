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



def main(targets):

    data_config = json.load(open('config/data-params.json'))
    
    if 'data' in targets:

        clean_data.clean_vcf(**data_config)
        
    if 'analysis' in targets:
        
        analysis.compute_eqtls(**data_config)
        
        
    if 'test' in targets:
        pass

if __name__ == '__main__':
    
    targets = sys.argv[1:]
    main(targets)