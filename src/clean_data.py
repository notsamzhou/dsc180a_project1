
import os

def clean_vcf(vcf_path, vcf_out_prefix, vcf_out_path, **kwargs):
    
    abs_vcf_path = os.getcwd() + '/' + vcf_path
    
    os.system(f"plink --vcf {abs_vcf_path} --maf 0.05 --biallelic-only --recode vcf --out {vcf_out_prefix}")
    
    os.system(f"mv {vcf_out_prefix + '.vcf'} {os.getcwd() + '/' + vcf_out_path}")