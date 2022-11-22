
import os

def clean_vcf(data_path, vcf_name, vcf_out_prefix, **kwargs):
    
    vcf_path = os.getcwd() + '/' + data_path + '/raw/vcf/' + vcf_name
    
    os.system(f"plink --vcf {vcf_path} --maf 0.05 --biallelic-only --recode vcf --out {vcf_out_prefix}")
    
    os.system(f"mv {vcf_name + '.vcf'} {os.getcwd() + '/' + data_path + '/temp/'}")