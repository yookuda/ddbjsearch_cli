#!/opt/pkg/python/3.7.2/bin/python3
import sys
import json
import argparse

def main():
    args = parse_args()
    type = args.type
    urls = []
    for line in sys.stdin:
        json_obj = json.loads(line)
        if 'downloadUrl' in json_obj and json_obj['downloadUrl']:
            for i in json_obj['downloadUrl']:
                if i['type'] == type:
                    urls.append(i['url'])
    for url in urls:
        print(url)

def parse_args():
    parser = argparse.ArgumentParser(description='DDBJSearchのAPIサーバから取得したjsonを標準入力から読み（1行1json）、downloadUrl中の指定されたtypeのurlを抽出します。')
    parser.add_argument('-t', '--type', choices=['meta', 'sra', 'fastq'], help='取得するURLのtypeを指定してください。', default='meta')
    args = parser.parse_args()
    return(args)

if __name__ == '__main__':
    main()
