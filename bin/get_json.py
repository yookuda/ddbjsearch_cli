#!/opt/pkg/python/3.7.2/bin/python3
import sys
import subprocess
import re
import json
import argparse

def main():
    args = parse_args()
    host_ip = '172.19.7.150'
    port = '8090'
    pretty_flag = args.pretty
    accession = args.accession
    
    target = check_target(accession)
    if target == 'ERROR':
        result = error_check(accession)
    elif target == 'BIOPROJECT':
        result = get_bioproject_entry(host_ip, port, accession, pretty_flag)
    elif target == 'BIOSAMPLE':
        result = get_biosample_entry(host_ip, port, accession, pretty_flag)
    elif target == 'SRA-SUBMISSION' or target == 'SRA-STUDY' or target == 'SRA-RUN' or target == 'SRA-EXPERIMENT' or target == 'SRA-SAMPLE' or target == 'SRA-ANALYSIS':
        result = get_dra_entry(host_ip, port, target, accession, pretty_flag)
    elif target == 'JGA-DATASET' or target == 'JGA-STUDY' or target == 'JGA-POLICY' or target == 'JGA-DAC':
        result = get_jga_entry(host_ip, port, target, accession, pretty_flag)
    
    print(result)

def parse_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('accession', help='accession number')
    parser.add_argument('-p', '--pretty', help='jsonを整形して出力します。', action='store_true')
    args = parser.parse_args()
    return(args)

def get_bioproject_entry(host_ip, port, accession, pretty_flag):
    command = "curl -X GET " + host_ip + ":" + port + "/resource/bioproject/" + accession + '.json'
    stdout = exec_command(command)
    if pretty_flag:
        stdout = json.dumps(json.loads(stdout), indent=4)
    return(stdout)

def get_biosample_entry(host_ip, port, accession, pretty_flag):
    command = "curl -X GET " + host_ip + ":" + port + "/resource/biosample/" + accession + '.json'
    stdout = exec_command(command)
    if pretty_flag:
        stdout = json.dumps(json.loads(stdout), indent=4)
    return(stdout)

def get_dra_entry(host_ip, port, target, accession, pretty_flag):
    # targetは小文字に変換する必要あり
    command = "curl -X GET " + host_ip + ":" + port + "/resource/" + target.lower() + "/" + accession + '.json'
    stdout = exec_command(command)
    if pretty_flag:
        stdout = json.dumps(json.loads(stdout), indent=4)
    return(stdout)

def get_jga_entry(host_ip, port, target, accession, pretty_flag):
    command = "curl -X GET " + host_ip + ":" + port + '/resource/' + target.lower() + '/' + accession + '.json'
    stdout = exec_command(command)
    if pretty_flag:
        stdout = json.dumps(json.loads(stdout), indent=4)
    return(stdout)

#------------------------------
# 指定したコマンドをshellで実行
#------------------------------
def exec_command(command):
    result = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return(result.stdout)
    #return(json.dumps(json.loads(result.stdout), indent=4))

def check_target(accession):
    p_bioproject = re.compile(r'PRJ')
    p_biosample = re.compile(r'SAM')
    p_submission = re.compile(r'[DES]RA')
    p_study = re.compile(r'[DES]RP')
    p_run = re.compile(r'[DES]RR')
    p_experiment = re.compile(r'[DES]RX')
    p_sample = re.compile(r'[DES]RS')
    p_analysis = re.compile(r'[DES]RZ')
    p_jgadataset = re.compile(r'JGAD')
    p_jgastudy = re.compile(r'JGAS')
    p_jgapolicy = re.compile(r'JGAP')
    p_jgadac = re.compile(r'JGAC')
    if p_bioproject.match(accession):
        return('BIOPROJECT')
    elif p_biosample.match(accession):
        return('BIOSAMPLE')
    elif p_submission.match(accession):
        return('SRA-SUBMISSION')
    elif p_study.match(accession):
        return('SRA-STUDY')
    elif p_run.match(accession):
        return('SRA-RUN')
    elif p_experiment.match(accession):
        return('SRA-EXPERIMENT')
    elif p_sample.match(accession):
        return('SRA-SAMPLE')
    elif p_analysis.match(accession):
        return('SRA-ANALYSIS')
    elif p_jgadataset.match(accession):
        return('JGA-DATASET')
    elif p_jgastudy.match(accession):
        return('JGA-STUDY')
    elif p_jgapolicy.match(accession):
        return('JGA-POLICY')
    elif p_jgadac.match(accession):
        return('JGA-DAC')
    else:
        return('ERROR')

def error_check(accession):
    return(accession + ' has incorrect prefix.')



if __name__ == '__main__':
    main()
