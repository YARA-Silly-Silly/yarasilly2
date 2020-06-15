<center> <img src="docs/\_static/yarasilly2.png" /> </center>

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

## About Us

Yara Silly Silly is maintained by:

<table>
  <tr>
    <td align="center"><a href="https://www.linkedin.com/in/hganguly/"><img src="https://avatars0.githubusercontent.com/u/5839433?s=88&u=6ed858dba3762eb0d929b48649b787ac9db112b7&v=4" width="100px;" alt="himadriganguly"/><br /><sub><b>Himadri Ganguly</b></sub></a><br /><a href="https://github.com/himadriganguly" title="Code">:octocat:</a> <a href="https://twitter.com/himadritech" title="Twitter">:bird:</a></td>
    <td align="center"><a href="https://www.linkedin.com/in/krishpaul/"><img src="https://avatars2.githubusercontent.com/u/3284091?s=400&u=9c3983a826301000f0d6b8191fdda6042b065157&v=4" width="100px;" alt="bidhata"/><br /><sub><b>Krishnendu Paul</b></sub></a><br /><a href="https://github.com/bidhata" title="Code">:octocat:</a> <a href="https://twitter.com/bidhata" title="Twitter">:bird:</a> <a href="https://krishnendu.com/" title="Website">:house:</a></td>
  </tr>
</table>

## LICENSE

Yara Silly Silly is GNU GPL3 licensed. See the LICENSE file for details.
