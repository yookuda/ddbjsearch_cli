#!/opt/pkg/python/3.7.2/bin/python3
import argparse
import subprocess
import json
import sys
import re

def main():
    args = parse_args()
    index = 'jga-*,sra-*,bioproject,biosample'
    host_ip = '172.19.7.150'
    port = '9200'
    json_flag = args.json
    QUERY_STRING = args.query
    TYPE = args.type
    ORGANISM_NAME = args.organism
    START_DATE = args.start
    END_DATE = args.end
    COUNT = args.count
    SIZE = 100

    AGGS = ',"aggs":{"type.keyword":{"terms":{"field":"type.keyword","size":100,"order":{"_count":"desc"}}}}'

    SEARCHES = []
    search_flag = 0
    query = ''

    if QUERY_STRING:
        QUERY_STRING_SEARCH = '{"bool":{"should":[{"multi_match":{"query":"' + QUERY_STRING + '","fields":["search^1","identifier^3","title^3","description^3","name^3","type^3","url^3","sameAs.*","isPartOf","organism.*","status","visibility"],"type":"cross_fields","operator":"and"}},{"multi_match":{"query":"' + QUERY_STRING + '","fields":["search^1","identifier^3","title^3","description^3","name^3","type^3","url^3","sameAs.*","isPartOf","organism.*","status","visibility"],"type":"phrase","operator":"and"}}],"minimum_should_match":"1"}}'
        SEARCHES.append(QUERY_STRING_SEARCH)
        search_flag = 1
    if TYPE:
        TYPE_SEARCH = '{"term":{"type.keyword":"' + TYPE + '"}}'
        SEARCHES.append(TYPE_SEARCH)
        search_flag = 1
    if ORGANISM_NAME:
        ORGANISM_SEARCH = '{"term":{"organism.name.keyword":"' + ORGANISM_NAME + '"}}'
        SEARCHES.append(ORGANISM_SEARCH)
        search_flag = 1
    if START_DATE and END_DATE:
        RANGE_SEARCH = '{"range":{"datePublished":{"gte":"' + START_DATE + 'T00:00:00+09:00","lte":"' + END_DATE + 'T00:00:00+09:00"}}}'
        SEARCHES.append(RANGE_SEARCH)
        search_flag = 1

    if search_flag:
        SEARCH_STR = ','.join(SEARCHES)
        query = '{"preference":"list"}' + "\n" + '{"query":{"bool":{"must":[{"bool":{"must":[' + SEARCH_STR + ']}}]}},"size":' + str(SIZE) + AGGS + ',"_source":{"includes":["identifier"]},"from":' + str(COUNT) + '}' + "\n"
    else:
        query = '{"preference":"list"}' + "\n" + '{"query":{"match_all":{}},"size":10' + AGGS + ',"_source":{"includes":["identifier"]},"from":0}' + "\n"

    command = 'curl -X POST -H "Content-type: application/x-ndjson" -d \'' + query + '\' ' + host_ip + ':' + port + '/' + index + '/_msearch'
#    print(command)
    stdout, stderr = exec_subprocess(command)
    if json_flag:
        json_obj = json.loads(stdout)
        json_text = json.dumps(json_obj, indent=4)
        print(json_text)
    else:
        if search_flag:
            get_accessions(stdout)
    count_keys(stdout)
    
#    print('stdout:' + stdout)
#    print('stderr:' + stderr)


def parse_args():
    parser = argparse.ArgumentParser(description='ddbjsearchのコマンドライン検索ツールです。検索でヒットしたaccession番号を出力します。')
    parser.add_argument('-q', '--query', help='検索ワードを入力してください。')
    parser.add_argument('-t', '--type', choices=['biosample', 'bioproject', 'sra-run', 'sra-experiment', 'sra-sample', 'sra-submission', 'sra-study', 'sra-analysis', 'jga-dataset', 'jga-study', 'jga-policy', 'jga-dac'], help='検索するタイプを指定してください。')
    parser.add_argument('-o', '--organism', help='検索する生物種名を学名で指定してください。')
    parser.add_argument('-s', '--start', help='検索するpublication dateの範囲の開始日を指定してください。')
    parser.add_argument('-e', '--end', help='検索するpublication dateの範囲の終了日を指定してください。')
    parser.add_argument('-j', '--json', help='accession番号のリストではなく検索結果のjsonで出力する場合に指定してください。', action='store_true')
    parser.add_argument('-c', '--count', help='検索結果を出力する開始番号を指定してください。デフォルトでは0が指定されており、0件目から99件目を出力します。', default=0)

    args = parser.parse_args()
    if args.start:
        check_date(args.start)
    if args.end:
        check_date(args.end)
    if args.start and not args.end:
        print('specify both start and end.')
        sys.exit()
    if args.end and not args.start:
        print('specify both start and end.')
        sys.exit()

    return(args)

def check_date(date):
    p_date = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    if not p_date.match(date):
        print('date format is yyyy-mm-dd.')
        sys.exit()

def exec_subprocess(command):
    proc = subprocess.run(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    return(proc.stdout.decode("utf8"), proc.stderr.decode("utf8"))

def count_keys(stdout):
    keys = ['biosample', 'bioproject', 'sra-run', 'sra-experiment', 'sra-sample', 'sra-submission', 'sra-study', 'sra-analysis', 'jga-dataset', 'jga-study', 'jga-policy', 'jga-dac']
    doc_count = {}
    for key in keys:
        doc_count[key] = 0
    json_obj = json.loads(stdout)
    counts = json_obj['responses'][0]['aggregations']['type.keyword']['buckets']
    for count in counts:
        for key in keys:
            if count['key'] == key:
                doc_count[key] = count['doc_count']
    print("", file=sys.stderr)
    for key in keys:
        print(key + ': ' + str(doc_count[key]), file=sys.stderr)

def get_accessions(stdout):
    accessions = []
    json_obj = json.loads(stdout)
    hits = json_obj['responses'][0]['hits']['hits']
    for hit in hits:
        accessions.append(hit['_source']['identifier'])
    for accession in accessions:
        print(accession)

if __name__ == '__main__':
    main()
