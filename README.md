<p align="center"><img src="https://raw.githubusercontent.com/YARA-Silly-Silly/yarasilly2/master/docs/_static/yarasilly2.png" /></p>

# YARA Silly Silly

A Semi automatic handy tool to generate YARA rules from sample virus files ( WIP ) for Malware Analyst, inspired by DIFF function of VirusTotal Premium Account.

You can find some sample virus files at [https://github.com/YARA-Silly-Silly/sample-malwares](https://github.com/YARA-Silly-Silly/sample-malwares)

You can find the project repo at [https://github.com/YARA-Silly-Silly/yarasilly2](https://github.com/YARA-Silly-Silly/yarasilly2)

## Installing YARA Silly Silly

**Python3 is required.**

0. Clone the git repository and enter into the folder

```
git clone https://github.com/YARA-Silly-Silly/yarasilly2.git
cd yarasilly2
```

1. Create and activate a virtual environment:

`Linux`

```
python -m venv venv
source venv/bin/activate
```

`Windows`

```
python -m venv venv
.\venv\Scripts\activate.bat
```

2. Install ssdeep according to your **OS** from

[https://python-ssdeep.readthedocs.io/en/latest/installation.html#installation](https://python-ssdeep.readthedocs.io/en/latest/installation.html#installation)

**Example Ubuntu 20.04**

```
sudo apt-get install build-essential libffi-dev python3 python3-dev python3-pip libfuzzy-dev
```

3. Install the package inside the environment:

```
pip3 install -r requirements.txt
```

## QuickStart

To start the application check all the options that can be passed to the application using

```
python yarasilly2.py --help
```

Config for the application is also present in the file **config.ini** in the root folder.

**Example**

```
python yarasilly2.py  -r "Test-Rule" -t "APT" -a "John Doe" -o 2 -f "office"
```

The above command will pass the name of the rule **Test-Rule**, tag **APT**, author **John Doe**, pattern occurance **2** and sample file type **office**.

<img src="https://raw.githubusercontent.com/YARA-Silly-Silly/yarasilly2/master/docs/_static/yarasilly2_example.png" />

Using **fuzzy match** example

```
python yarasilly2.py  -r "Test-Rule" -t "APT" -a "John Doe" -f "office" -fm ./confirm-sample 80 ./probable-sample 60
```

The above command will pass the name of the rule **Test-Rule**, tag **APT**, author **John Doe**, file type **office** and then **fuzzy match** parameters, the first is the confirm malware samples folder, second is the percentage of match between all the files in that folder, third is the probable malware samples folder and fourth one is the percentage of match with the files within the probable folder.

## Command Line Parameters

```
Usage: yarasilly2.py [OPTIONS]

Options:
  -r, --rulename TEXT             Provide a rule name with no spaces and must
                                  start with letter.  [required]

  -f, --filetype [office]         Select sample set file type choices.
                                  [required]

  -m, --matchpatternfile TEXT     Matched pattern will be saved to this file.
                                  Please provide full path eg:
                                  ./output/matched-pattern

  -i, --inputfilepath TEXT        File or files will be read from this
                                  location eg: ./files-folder

  -fd, --folderdepth INTEGER      How much depth within the inputfilepath the
                                  files will be searched. To search all files
                                  with any depth enter 0

  -fm, --fuzzymatch <TEXT INTEGER TEXT INTEGER>...
                                  Match file patterns using fuzzy hashing.
                                  Please provide folder path of confirm virus
                                  samples with match percentage of same type
                                  and probable virus samples with should be
                                  matched percent. For eg: -fm ./confirm-
                                  sample 80 ./probable-sample 60

  -o, --patternoccurance INTEGER  How many match of the pattern within the
                                  files is considered as match.

  -b, --block INTEGER             File buffer size when reading file.
  -l, --loglevel [CRITICAL|ERROR|WARNING|INFO|DEBUG]
                                  Select log level for the application.
                                  [default: ERROR]

  -a, --author TEXT               Type you name to be filled in the author
                                  field in generate YARA rule. Eg. -n "John
                                  Doe"  [default: N/A]

  -d, --description TEXT          Provide a useful description of the YARA
                                  rule.  [default: No Description Provided]

  -t, --tags TEXT                 Apply Tags to Yara Rule For Easy Reference
                                  (AlphaNumeric)  [default: ]

  --help                          Show this message and exit.  [default:
                                  False]
```

## About Us

Yara Silly Silly is maintained by:

<table>
  <tr>
    <td align="center"><a href="https://www.linkedin.com/in/hganguly/"><img src="https://avatars0.githubusercontent.com/u/5839433?s=88&u=6ed858dba3762eb0d929b48649b787ac9db112b7&v=4" width="100px;" alt="himadriganguly"/><br /><sub><b>Himadri Ganguly</b></sub></a><br /><a href="https://github.com/himadriganguly" title="Code">:octocat:</a> <a href="https://twitter.com/himadritech" title="Twitter">:bird:</a></td>
    <td align="center"><a href="https://www.linkedin.com/in/krishpaul/"><img src="https://avatars2.githubusercontent.com/u/3284091?s=400&u=9c3983a826301000f0d6b8191fdda6042b065157&v=4" width="100px;" alt="bidhata"/><br /><sub><b>Krishnendu Paul</b></sub></a><br /><a href="https://github.com/bidhata" title="Code">:octocat:</a> <a href="https://twitter.com/bidhata" title="Twitter">:bird:</a> <a href="https://krishnendu.com/" title="Website">:house:</a></td>
  </tr>
</table>

## Contributing

Please see our [CONTRIBUTING.md](/CONTRIBUTING.md).

## LICENSE

Yara Silly Silly is GNU GPL3 licensed. See the LICENSE file for details.
