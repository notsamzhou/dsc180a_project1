import warnings

warnings.filterwarnings('ignore')

import pandas as pd
import io
import os
import gzip
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.stats import linregress
import swifter

def get_vcf_names(vcf_path):
    with open(vcf_path, "rt") as ifile:
        for line in ifile:
            if line.startswith("#CHROM"):
                vcf_names = [x for x in line.split('\t')]
                break
    ifile.close()
    return vcf_names

def get_cis_snps(x, cis_thresh, snps):
    return snps['POS'][(abs(snps['POS'] - x['Coord']) < cis_thresh)].index

def regress(x, snps, total_count, samples):
    exp = x.iloc[4:-1]
    
    valid_keys_exp = exp.index.intersection(samples)
    exp = exp.loc[valid_keys_exp]
    
    sig_alleles = []
    
    for snp in x['local']:

        allele = snps.loc[snp]
        
        valid_keys_allele = allele.index.intersection(samples)
        allele = allele.loc[valid_keys_allele]

        merged = pd.merge(exp, allele, left_index=True, right_index=True)
        merged.columns = ['expression', 'allele']

        slope, intercept, r_value, p_value, std_err = linregress(merged['allele'].values.astype(float), merged['expression'].values.astype(float))
        
        if p_value <= 0.05 / total_count:
            sig_alleles.append(np.array([snp, slope, std_err, p_value]))
            
        
    return sig_alleles
    
    
def compute_n_pairs(expressions_ch, vcf_out_path, vcf_out_prefix, cis_thresh):
    cd = os.getcwd()
    
    names = get_vcf_names(cd + '/' + vcf_out_path + vcf_out_prefix + '.vcf')
    vcf = pd.read_csv(cd + '/' + vcf_out_path + vcf_out_prefix + '.vcf', chunksize=50_000, comment='#',low_memory=False, delim_whitespace=True, header=None, names=names)

    significants = 0
    p_values = []
    total_count = 0

    for i, chunk in enumerate(vcf):

        common = chunk

        expressions_ch.loc[:, 'local'] = expressions_ch.swifter.apply(get_cis_snps, cis_thresh=cis_thresh, snps=common, axis=1)
        alleles = common.iloc[:, 9:].applymap(lambda x: sum(int(i) for i in str(x).split('/')))

        total_count += expressions_ch['local'].apply(len).sum()
        
    return total_count

def compute_eqtls(vcf_out_path, vcf_out_prefix, expressions_path, populations_path, chromosome, target_populations, cis_thresh, outfile, **kwargs):

    cwd = os.getcwd()
    expressions = pd.read_csv(cwd + '/' + expressions_path, sep='\t')
    
    expressions_ch = expressions[expressions['Chr'].astype(str) == chromosome]
    
    pops = pd.read_csv(cwd + '/' + populations_path, sep=' ')
    
    n_pairs = compute_n_pairs(expressions_ch, vcf_out_path, vcf_out_prefix, cis_thresh)

    target_pops = target_populations
    
    samples = pops['sample'][pops['population'].isin(target_pops)]

    names = get_vcf_names(cwd + '/' + vcf_out_path + vcf_out_prefix + '.vcf')
    vcf = pd.read_csv(cwd + '/' + vcf_out_path + vcf_out_prefix + '.vcf', chunksize=50_000, comment='#',low_memory=False, delim_whitespace=True, header=None, names=names)

    significants = pd.DataFrame(columns=['gene', 'snp', 'pos', 'slope', 'SE', 'pvalue'])
    

    for i, chunk in enumerate(vcf):

        expressions_ch.loc[:, 'local'] = expressions_ch.swifter.apply(get_cis_snps, cis_thresh=cis_thresh, snps=chunk, axis=1)
        alleles = chunk.iloc[:, 9:].applymap(lambda x: sum(int(i) for i in str(x).split('/')))
        alleles.columns = alleles.columns.str.split('_').str[0].str.strip()

        expressions_ch.loc[:, 'info'] = expressions_ch.apply(regress, snps=alleles, total_count=n_pairs, samples=samples, axis=1)

        for idx, row in expressions_ch.iterrows():

            for sig in row['info']:
                record = pd.DataFrame.from_dict({
                    'gene': [row['TargetID']],
                    'snp': [chunk.loc[int(sig[0])]['ID']],
                    'pos': [chunk.loc[int(sig[0])]['POS']],
                    'slope': [sig[1]],
                    'SE': [sig[2]],
                    'pvalue': [sig[3]]
                })

                significants = pd.concat([significants, record], ignore_index=True)
                
    significants.to_csv(cwd + '/' + outfile, index=False)
    
    
    
    
    