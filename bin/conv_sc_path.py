#!/opt/pkg/python/3.7.2/bin/python3
import sys
import re

def main():
    p_url = re.compile(r'https://ddbj.nig.ac.jp/public/ddbj_database')
    for line in sys.stdin:
        path = line.replace('https://ddbj.nig.ac.jp/public/ddbj_database', '/usr/local/shared_data')
        print(path, end='')

if __name__ == '__main__':
    main()
