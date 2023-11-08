# 遺伝研スパコンでDDBJ Searchを検索するCLIツール
[DDBJ Search](https://ddbj.nig.ac.jp/search) はINSDC BioProject/BioSample/SRA, JGA データをアクセッション番号やキーワードで検索するサービスです。本ツールは遺伝研スパコン内でDDBJ Searchを検索するためのCLIツールです。

本ツールは /lustre7/software/experimental/ddbjsearch_cli/bin/ にインストールされています。
PATH環境変数に /lustre7/software/experimental/ddbjsearch_cli/bin を追加してご利用ください。

## ddbjsearch_cli.py
DDBJSearchのElastic Searchを検索してaccession番号のリストを取得します。

accession番号の出力が標準出力、タイプ別件数の出力が標準エラー出力になっています。ファイルにリダイレクトするとaccession番号のみファイルに出力されます。

最大100件のaccession番号を取得できます。検索結果が100件以上の場合は-cオプションで開始番号を指定することで続きを取得できます。

### help
```
$ ddbjsearch_cli.py --help
usage: ddbjsearch_cli.py [-h] [-q QUERY]
                         [-t {biosample,bioproject,sra-run,sra-experiment,sra-sample,sra-submission,sra-study,sra-analysis,jga-dataset,jga-study,jga-policy,jga-dac}]
                         [-o ORGANISM] [-s START] [-e END] [-j] [-c COUNT]

ddbjsearchのコマンドライン検索ツールです。検索でヒットしたaccession番号を出力します。

optional arguments:
  -h, --help            show this help message and exit
  -q QUERY, --query QUERY
                        検索ワードを入力してください。
  -t {biosample,bioproject,sra-run,sra-experiment,sra-sample,sra-submission,sra-study,sra-analysis,jga-dataset,jga-study,jga-policy,jga-dac}, --type {biosample,bioproject,sra-run,sra-experiment,sra-sample,sra-submission,sra-study,sra-analysis,jga-dataset,jga-study,jga-policy,jga-dac}
                        検索するタイプを指定してください。
  -o ORGANISM, --organism ORGANISM
                        検索する生物種名を学名で指定してください。
  -s START, --start START
                        検索するpublication dateの範囲の開始日を指定してください。
  -e END, --end END     検索するpublication dateの範囲の終了日を指定してください。
  -j, --json            accession番号のリストではなく検索結果のjsonで出力する場合に指定してください。
  -c COUNT, --count COUNT
                        検索結果を出力する開始番号を指定してください。デフォルトでは0が指定されており、0件目から99件目を出力しま
                        す。
```
### 実行例
"metagenomic analysis of human intestinal bacteria"で検索
```
$ ddbjsearch_cli.py -q "metagenomic analysis of human intestinal bacteria"
PRJDB6814
PRJNA515425
PRJNA386500
PRJEB17978
PRJDB8606
PRJNA421331
PRJNA825520
PRJNA738226
PRJNA789273
SRP126261
SRP179725
PRJEB52712
ERP019886
SRP007633
SRP107004
PRJNA188106
PRJNA188943
SRP100462
SRP324298
SRP057027
SRP350910
PRJNA313047
PRJNA485481

biosample: 0
bioproject: 14
sra-run: 0
sra-experiment: 0
sra-sample: 0
sra-submission: 0
sra-study: 9
sra-analysis: 0
jga-dataset: 0
jga-study: 0
jga-policy: 0
jga-dac: 0
```
タイプ sra-studyで絞り込み
```
$ ddbjsearch_cli.py -q "metagenomic analysis of human intestinal bacteria" -t sra-study
SRP126261
SRP179725
ERP019886
SRP007633
SRP107004
SRP100462
SRP324298
SRP057027
SRP350910

biosample: 0
bioproject: 0
sra-run: 0
sra-experiment: 0
sra-sample: 0
sra-submission: 0
sra-study: 9
sra-analysis: 0
jga-dataset: 0
jga-study: 0
jga-policy: 0
jga-dac: 0
```
published dateで絞り込み
```
$ ddbjsearch_cli.py -q "metagenomic analysis of human intestinal bacteria" -t sra-study -s 2020-01-01 -e 2021-01-01
SRP324298
SRP350910

biosample: 0
bioproject: 0
sra-run: 0
sra-experiment: 0
sra-sample: 0
sra-submission: 0
sra-study: 2
sra-analysis: 0
jga-dataset: 0
jga-study: 0
jga-policy: 0
jga-dac: 0
```
検索結果をjsonで出力
```
$ ddbjsearch_cli.py -q "metagenomic analysis of human intestinal bacteria" -t sra-study -s 2020-01-01 -e 2021-01-01 -j
{
    "took": 144,
    "responses": [
        {
            "took": 144,
            "timed_out": false,
            "_shards": {
                "total": 61,
                "successful": 61,
                "skipped": 0,
                "failed": 0
            },
            "hits": {
                "total": {
                    "value": 2,
                    "relation": "eq"
                },
                "max_score": 14.385858,
                "hits": [
                    {
                        "_index": "sra-study",
                        "_type": "_doc",
                        "_id": "SRP324298",
                        "_score": 14.385858,
                        "_ignored": [
                            "search.keyword",
                            "properties.DESCRIPTOR.STUDY_ABSTRACT.keyword"
                        ],
                        "_source": {
                            "identifier": "SRP324298"
                        }
                    },
                    {
                        "_index": "sra-study",
                        "_type": "_doc",
                        "_id": "SRP350910",
                        "_score": 13.040397,
                        "_ignored": [
                            "search.keyword",
                            "properties.DESCRIPTOR.STUDY_ABSTRACT.keyword"
                        ],
                        "_source": {
                            "identifier": "SRP350910"
                        }
                    }
                ]
            },
            "aggregations": {
                "type.keyword": {
                    "doc_count_error_upper_bound": 0,
                    "sum_other_doc_count": 0,
                    "buckets": [
                        {
                            "key": "sra-study",
                            "doc_count": 2
                        }
                    ]
                }
            },
            "status": 200
        }
    ]
}

biosample: 0
bioproject: 0
sra-run: 0
sra-experiment: 0
sra-sample: 0
sra-submission: 0
sra-study: 2
sra-analysis: 0
jga-dataset: 0
jga-study: 0
jga-policy: 0
jga-dac: 0
```
## get_json.py

指定したaccession番号の情報をDDBJSearchのAPIサーバからjson形式で取得します。

### help
```
$ get_json.py --help
usage: get_json.py [-h] [-p] accession

positional arguments:
  accession     accession number

optional arguments:
  -h, --help    show this help message and exit
  -p, --pretty  jsonを整形して出力します。
```
### 実行例
```
$ get_json.py -p SRP324298
{
    "identifier": "SRP324298",
    "title": "Novel Gut Microbiota Modulator, Which Markedly Increases in Akkermansia Muciniphila Occupancy, Ameliorates Experimental Colitis in Rats",
    "description": null,
    "name": "PRJNA738226",
    "type": "sra-study",
    "url": "https://ddbj.nig.ac.jp/resource/sra-study/SRP324298",
    "sameAs": [
        {
            "identifier": "PRJNA738226",
            "type": "bioproject",
            "url": "https://ddbj.nig.ac.jp/resource/bioproject/PRJNA738226"
        }
    ],
    "isPartOf": "sra",
    "organism": null,
    "dbXrefs": [
        {
            "identifier": "PRJNA738226",
            "type": "bioproject",
            "url": "https://ddbj.nig.ac.jp/resource/bioproject/PRJNA738226"
        },
（中略）
        {
            "identifier": "SRS9220853",
            "type": "sra-sample",
            "url": "https://ddbj.nig.ac.jp/resource/sra-sample/SRS9220853"
        }
    ],
    "dbXrefsStatistics": [
        {
            "type": "bioproject",
            "count": 1
        },
        {
            "type": "sra-run",
            "count": 104
        },
        {
            "type": "sra-submission",
            "count": 1
        },
        {
            "type": "biosample",
            "count": 2
        },
        {
            "type": "sra-sample",
            "count": 2
        },
        {
            "type": "sra-experiment",
            "count": 104
        }
    ],
    "properties": {
        "alias": "PRJNA738226",
        "center_name": "BioProject",
        "accession": "SRP324298",
        "IDENTIFIERS": {
            "PRIMARY_ID": {
                "content": "SRP324298"
            },
            "EXTERNAL_ID": [
                {
                    "label": "primary",
                    "namespace": "BioProject",
                    "content": "PRJNA738226"
                }
            ]
        },
        "DESCRIPTOR": {
            "STUDY_TITLE": "Novel Gut Microbiota Modulator, Which Markedly Increases in Akkermansia Muciniphila Occupancy, Ameliorates Experimental Colitis in Rats",
            "STUDY_TYPE": {
                "existing_study_type": "Other"
            },
            "STUDY_ABSTRACT": "Background: Since gut microbiota is involved in the pathogenesis of inflammatory bowel disease (IBD), antibiotics or probiotics may be attractive options for the treatment of IBD. Akkermansia Muniiciphila is expected as a next-generation probiotic for IBD, and OPS-2071 is a novel quinolone with potent antibacterial activity against Clostridioides difficile.Aims: The aim of this study is to assess the potential of OPS-2071 as a gut microbiota modulator for IBD.Methods: Minimum inhibitory concentrations of several bacteria in the human intestinal microbiota were determined. Microbiota changes in the feces were typed using metagenomic analysis after oral administration of OPS-2071 (100 mg/kg) twice a day to normal rats. The amounts of mucin were also determined using the Fecal Mucin Assay kit. The effects of OPS-2071 (1, 3, 10 mg/kg) twice a day on fecal symptoms and fecal microbiota were evaluated in a colitis rat model induced by free access to drinking water containing 3% dextran sulfate sodium for 10 days.Results: OPS-2071 showed notably low antibacterial activity against only A. muciniphila in spite of higher antimicrobial activity against other strains of intestinal bacteria. OPS-2071 rapidly and dramatically increased the occupancy of A. muciniphila as well as the amount of mucin in the feces of normal rats. OPS-2071 (10 mg/kg) significantly suppressed the exacerbation of stool scores, especially the bloody stool score, with the increase in A. muciniphila occupancy.Conclusions: OPS-2071 is expected to be a new therapeutic option for IBD as the gut microbiota modulator by significantly increasing A. muciniphila occupancy."
        }
    },
    "search": "{\n  \"alias\" : \"PRJNA738226\",\n  \"center_name\" : \"BioProject\",\n  \"accession\" : \"SRP324298\",\n  \"IDENTIFIERS\" : {\n    \"PRIMARY_ID\" : {\n      \"content\" : \"SRP324298\"\n    },\n    \"EXTERNAL_ID\" : [ {\n      \"label\" : \"primary\",\n      \"namespace\" : \"BioProject\",\n      \"content\" : \"PRJNA738226\"\n    } ]\n  },\n  \"DESCRIPTOR\" : {\n    \"STUDY_TITLE\" : \"Novel Gut Microbiota Modulator, Which Markedly Increases in Akkermansia Muciniphila Occupancy, Ameliorates Experimental Colitis in Rats\",\n    \"STUDY_TYPE\" : {\n      \"existing_study_type\" : \"Other\"\n    },\n    \"STUDY_ABSTRACT\" : \"Background: Since gut microbiota is involved in the pathogenesis of inflammatory bowel disease (IBD), antibiotics or probiotics may be attractive options for the treatment of IBD. Akkermansia Muniiciphila is expected as a next-generation probiotic for IBD, and OPS-2071 is a novel quinolone with potent antibacterial activity against Clostridioides difficile.Aims: The aim of this study is to assess the potential of OPS-2071 as a gut microbiota modulator for IBD.Methods: Minimum inhibitory concentrations of several bacteria in the human intestinal microbiota were determined. Microbiota changes in the feces were typed using metagenomic analysis after oral administration of OPS-2071 (100 mg/kg) twice a day to normal rats. The amounts of mucin were also determined using the Fecal Mucin Assay kit. The effects of OPS-2071 (1, 3, 10 mg/kg) twice a day on fecal symptoms and fecal microbiota were evaluated in a colitis rat model induced by free access to drinking water containing 3% dextran sulfate sodium for 10 days.Results: OPS-2071 showed notably low antibacterial activity against only A. muciniphila in spite of higher antimicrobial activity against other strains of intestinal bacteria. OPS-2071 rapidly and dramatically increased the occupancy of A. muciniphila as well as the amount of mucin in the feces of normal rats. OPS-2071 (10 mg/kg) significantly suppressed the exacerbation of stool scores, especially the bloody stool score, with the increase in A. muciniphila occupancy.Conclusions: OPS-2071 is expected to be a new therapeutic option for IBD as the gut microbiota modulator by significantly increasing A. muciniphila occupancy.\"\n  }\n}",
    "distribution": [
        {
            "type": "DataDownload",
            "encodingFormat": "JSON",
            "contentUrl": "https://ddbj.nig.ac.jp/resource/sra-study/SRP324298.json"
        },
        {
            "type": "DataDownload",
            "encodingFormat": "JSON-LD",
            "contentUrl": "https://ddbj.nig.ac.jp/resource/sra-study/SRP324298.jsonld"
        }
    ],
    "downloadUrl": [
        {
            "type": "meta",
            "name": "SRA1245460.study.xml",
            "url": "https://ddbj.nig.ac.jp/public/ddbj_database/dra/fastq/SRA124/SRA1245460/SRA1245460.study.xml",
            "ftpUrl": "ftp://ftp.ddbj.nig.ac.jp/ddbj_database/dra/fastq/SRA124/SRA1245460/SRA1245460.study.xml"
        }
    ],
    "status": "public",
    "visibility": "unrestricted-access",
    "dateCreated": "2021-06-16T18:30:11Z",
    "dateModified": "2021-06-16T22:58:30Z",
    "datePublished": "2021-06-16T22:58:30Z"
}
```
accession番号を1個だけ処理する作りのため、ddbjsearch_cli.pyの出力したaccession番号のリストからjsonファイルを個別に取得する場合は以下のようにfor文を使います。
```
$ mkdir test
$ for i in `ddbjsearch_cli.py -q "metagenomic analysis of human intestinal bacteria" -t sra-study`; do get_json.py $i > test/$i.json; done

biosample: 0
bioproject: 0
sra-run: 0
sra-experiment: 0
sra-sample: 0
sra-submission: 0
sra-study: 9
sra-analysis: 0
jga-dataset: 0
jga-study: 0
jga-policy: 0
jga-dac: 0
$ ls -l test
合計 5
-rw-r--r-- 1 y-okuda users  94997 11月  7 14:51 ERP019886.json
-rw-r--r-- 1 y-okuda users  11863 11月  7 14:51 SRP007633.json
-rw-r--r-- 1 y-okuda users 170825 11月  7 14:51 SRP057027.json
-rw-r--r-- 1 y-okuda users   9808 11月  7 14:51 SRP100462.json
-rw-r--r-- 1 y-okuda users  13224 11月  7 14:51 SRP107004.json
-rw-r--r-- 1 y-okuda users  12774 11月  7 14:51 SRP126261.json
-rw-r--r-- 1 y-okuda users   7092 11月  7 14:51 SRP179725.json
-rw-r--r-- 1 y-okuda users  29969 11月  7 14:51 SRP324298.json
-rw-r--r-- 1 y-okuda users  14972 11月  7 14:51 SRP350910.json
```
ddbjsearch_cli.pyの出力をファイルに保存してからget_json.pyに回す場合も同様にfor文を使います。
```
$ ddbjsearch_cli.py -q "metagenomic analysis of human intestinal bacteria" -t sra-study > test_list.txt

biosample: 0
bioproject: 0
sra-run: 0
sra-experiment: 0
sra-sample: 0
sra-submission: 0
sra-study: 9
sra-analysis: 0
jga-dataset: 0
jga-study: 0
jga-policy: 0
jga-dac: 0
$ cat test_list.txt 
SRP126261
SRP179725
ERP019886
SRP007633
SRP107004
SRP100462
SRP324298
SRP057027
SRP350910
$ for i in `cat test_list.txt`; do get_json.py $i > test/$i.json; done
$ ls -l test
合計 5
-rw-r--r-- 1 y-okuda users  94997 11月  7 15:27 ERP019886.json
-rw-r--r-- 1 y-okuda users  11863 11月  7 15:27 SRP007633.json
-rw-r--r-- 1 y-okuda users 170825 11月  7 15:27 SRP057027.json
-rw-r--r-- 1 y-okuda users   9808 11月  7 15:27 SRP100462.json
-rw-r--r-- 1 y-okuda users  13224 11月  7 15:27 SRP107004.json
-rw-r--r-- 1 y-okuda users  12774 11月  7 15:27 SRP126261.json
-rw-r--r-- 1 y-okuda users   7092 11月  7 15:27 SRP179725.json
-rw-r--r-- 1 y-okuda users  29969 11月  7 15:27 SRP324298.json
-rw-r--r-- 1 y-okuda users  14972 11月  7 15:27 SRP350910.json
```
## get_download_url.py

DDBJSearchのAPIサーバから取得したjsonを標準入力から読み、downloadUrl中の指定したtypeのURLを抽出します。

標準入力から読むjsonは1行を1つのjsonとして扱うため、get_json.pyで -p オプションを付けて整形したjsonは使用できません。

### help
```
$ get_download_url.py --help
usage: get_download_url.py [-h] [-t {meta,sra,fastq}]

DDBJSearchのAPIサーバから取得したjsonを標準入力から読み（1行1json）、downloadUrl中の指定されたtypeのurlを抽出します
。

optional arguments:
  -h, --help            show this help message and exit
  -t {meta,sra,fastq}, --type {meta,sra,fastq}
                        取得するURLのtypeを指定してください。
```
### 実行例

typeを指定してmeta, sraまたはfastqのURLを取得します。typeを指定しない場合はmetaのURLを取得します。
```
$ cat test/ERP019886.json | get_download_url.py 
https://ddbj.nig.ac.jp/public/ddbj_database/dra/fastq/ERA903/ERA903431/ERA903431.study.xml
```
get_json.pyの出力をパイプで受けて実行できます。
```
$ get_json.py SRR14830546 | ./get_download_url.py -t meta
https://ddbj.nig.ac.jp/public/ddbj_database/dra/fastq/SRA124/SRA1245460/SRA1245460.run.xml
$ get_json.py SRR14830546 | ./get_download_url.py -t sra
https://ddbj.nig.ac.jp/public/ddbj_database/dra/sralite/ByExp/litesra/SRX/SRX111/SRX11159521/SRR14830546/SRR14830546.sra
$ get_json.py SRR14830546 | ./get_download_url.py -t fastq
https://ddbj.nig.ac.jp/public/ddbj_database/dra/fastq/SRA124/SRA1245460/SRX11159521
```
get_json.pyで-pオプションを付けるとエラーになります。
```
$ get_json.py -p SRR14830546 | ./get_download_url.py -t meta
Traceback (most recent call last):
  File "get_download_url.py", line 26, in <module>
    main()
  File "get_download_url.py", line 11, in main
    json_obj = json.loads(line)
  File "/opt/pkg/python/3.7.2/lib/python3.7/json/__init__.py", line 348, in loads
    return _default_decoder.decode(s)
  File "/opt/pkg/python/3.7.2/lib/python3.7/json/decoder.py", line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File "/opt/pkg/python/3.7.2/lib/python3.7/json/decoder.py", line 353, in raw_decode
    obj, end = self.scan_once(s, idx)
json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 2 column 1 (char 2)
```
## conv_sc_path.py

get_download_url.pyで取得したURLを遺伝研スパコン内のパスに変換します。

遺伝研スパコン内ではFTP公開データが /usr/local/shared_data/ にマウントされているため、HTTP, FTPを使わずcpコマンドで取得可能です。

### 実行例
```
$ get_json.py SRR14830546 | get_download_url.py -t fastq | conv_sc_path.py 
/usr/local/shared_data/dra/fastq/SRA124/SRA1245460/SRX11159521
```
fastqのURLはディレクトリを指していますが、以下の実行結果のようにディレクトリが存在しない場合があります。
```
$ get_json.py SRR14830546 | get_download_url.py -t meta | conv_sc_path.py | xargs -i ls -l {}
-rw-r--r-- 1 tracesys tracesys 47249 10月 23 20:49 /usr/local/shared_data/dra/fastq/SRA124/SRA1245460/SRA1245460.run.xml
$ get_json.py SRR14830546 | get_download_url.py -t sra | conv_sc_path.py | xargs -i ls -l {}
-rw-r--r-- 1 tracesys tracesys 13472673  6月 18  2021 /usr/local/shared_data/dra/sralite/ByExp/litesra/SRX/SRX111/SRX11159521/SRR14830546/SRR14830546.sra
$ get_json.py SRR14830546 | get_download_url.py -t fastq | conv_sc_path.py | xargs -i ls -l {}
ls: /usr/local/shared_data/dra/fastq/SRA124/SRA1245460/SRX11159521 にアクセスできません: そのようなファイルやディレクトリはありません
$ ls /usr/local/shared_data/dra/fastq/SRA124/SRA1245460/
SRA1245460.experiment.xml  SRA1245460.run.xml  SRA1245460.sample.xml  SRA1245460.study.xml  SRA1245460.submission.xml
```
