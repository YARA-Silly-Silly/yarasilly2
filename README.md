# YARA Silly Silly

Automatic generation of YARA rules from sample files.

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
python -m virtualenv venv
source venv/bin/activate
```

`Windows`

```
python -m virtualenv venv
.\venv\Scripts\activate.bat
```

2. Install the package inside the environment:

```
pip install -r requirements
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

The above command will pass the name of the rule **Test-Rule**, tag **APT**, author **John Doe**, pattern occurance **2** and sample file type **office**

<img src="docs/\_static/yarasilly2_example.png" />

## LICENSE

Yara Silly Silly is GNU GPL3 licensed. See the LICENSE file for details.
