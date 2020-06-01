import os, sys, logging, configparser, tempfile, shutil, click, re
from pyfiglet import Figlet
from clint.textui import puts, colored
from tqdm import tqdm
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

from pkgs.utils import md5sum, listdir

# sys.path.append('./libs')

from pkgs.utils import splitDirFileName
from pkgs.findfiles import FindFiles
from pkgs.searchpattern import SearchPattern
from pkgs.stringdump import StringDump

@click.command(context_settings=dict(show_default=True))
@click.option('--rulename', '-r', type=click.STRING, help='Provide a rule name with no spaces and must start with letter."', required=True)
@click.option('--filetype', '-f', type=click.Choice(['unknown', 'office', 'email'], case_sensitive=False), help='Select sample set file type choices.', required=True)
@click.option('--matchpatternfile', '-m', type=click.STRING, help='Matched pattern will be saved to this csv file. Please provide full path without extension eg: ./output/matched-pattern.txt', required=False)
@click.option('--inputfilepath', '-i', type=click.STRING, help='File or files will be read from this location eg: ./files-folder', required=False)
@click.option('--folderdepth', '-fd', type=click.INT, help='How much depth within the inputfilepath the files will be searched. To search all files with any depth enter 0', required=False)
@click.option('--patternoccurance', '-o', type=click.INT, help='How many match of the pattern within the files is considered as match.', required=False)
@click.option('--block', '-b', type=click.INT, help='File buffer size when reading file.', required=False)
@click.option('--loglevel', '-l', default='ERROR', type=click.Choice(['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'], case_sensitive=False), help='Select log level for the application.')
@click.option('--author', '-a', type=click.STRING, default='N/A', help='Type you name to be filled in the author field in generate YARA rule. Eg. -n "John Doe"', required=False)
@click.option('--description', '-d', type=click.STRING, default='No Description Provided', help='Provide a useful description of the YARA rule.', required=False)
@click.option('--tags', '-t', type=click.STRING, default='', help="Apply Tags to Yara Rule For Easy Reference (AlphaNumeric)")
def main(rulename=None, filetype=None, matchpatternfile=None, inputfilepath=None, folderdepth=None, patternoccurance=None, block=None, loglevel=None, author=None, description=None, tags=None):
    optionFolderDepth = ''
    logLevelDict = {'CRITICAL': logging.CRITICAL, 'ERROR': logging.ERROR, 'WARNING': logging.WARNING, 'INFO': logging.INFO, 'DEBUG': logging.DEBUG}
    foundPattern = 0

    pattern = re.compile(r"^[A-Za-z]\S*\w*$")
    if not pattern.match(rulename):
        puts(colored.red(("[!] Wrong pattern for rule name.\n")))
        sys.exit(1)

    fileLoader = FileSystemLoader('templates')
    env = Environment(loader=fileLoader)
    yaraTemplate = env.get_template('default.yar')

    try:
        config = configparser.ConfigParser()
        config.read('config.ini')

        if folderdepth:
            optionFolderDepth = None if folderdepth == 0 else folderdepth

        matchPatternDir = splitDirFileName(matchpatternfile)[0] if matchpatternfile else config['DEFAULT']['matchPatternFilePath']
        matchPatternFilePath = matchpatternfile if matchpatternfile else os.path.join(config['DEFAULT']['matchPatternFilePath'], config['DEFAULT']['matchPatternFileName'])
        inputFilesPath = inputfilepath if inputfilepath else config['DEFAULT']['inputFilesPath']
        folderDepth = optionFolderDepth if optionFolderDepth else int(config['DEFAULT']['folderDepth'])
        occurance = patternoccurance if patternoccurance else int(config['DEFAULT']['occurance'])
        blocksize = block if block else int(config['DEFAULT']['blocksize'])

        # Logging config
        if not os.path.exists(config['LOG']['logFilePath']):
            os.makedirs(config['LOG']['logFilePath'])

        if loglevel.upper() != "ERROR" and logLevelDict[loglevel.upper()]:
            logging.basicConfig(filename=os.path.join(config['LOG']['logFilePath'], config['LOG']['logFileName']),format='%(asctime)s - %(levelname)s - %(message)s',level=logLevelDict[loglevel.upper()])
        else:
            logging.basicConfig(filename=os.path.join(config['LOG']['logFilePath'], config['LOG']['logFileName']),format='%(asctime)s - %(levelname)s - %(message)s',level=logging.ERROR)

        if not os.path.exists(matchPatternDir):
            os.makedirs(matchPatternDir)

        findFilesObj = FindFiles(inputFilesPath, folderDepth)

        fileHash = []
        dirPath = os.path.dirname(os.path.abspath(__file__))
        tempFolder = os.path.join(tempfile.gettempdir(), "yara-silly-silly")
        if not os.path.exists(tempFolder):
            os.makedirs(tempFolder)

        stringDumpObj = StringDump(dirPath, 'office', tempFolder, blocksize)
        for file in findFilesObj.searchFiles():
            fileHash.append(md5sum(file))
            stringDumpObj.dumpStringsToTempFile(file)

        del findFilesObj
        del stringDumpObj
        del dirPath

        searchPatternObj = SearchPattern(tempFolder, matchPatternFilePath, occurance)
        for file in listdir(tempFolder):
            foundPattern += searchPatternObj.search(file)

        if(foundPattern):
            puts(colored.green(("[+] Common matched pattern saved to {}.\n".format(os.path.abspath(matchPatternFilePath)))))
        else:
            puts(colored.red(("[!] No matching pattern found within files.\n")))
            os.remove(matchPatternFilePath)

        shutil.rmtree(tempFolder)

        if(foundPattern):
            templateValDict = {
                "ruleName": rulename,
                "ruleTag": tags,
                "authorName": author,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "desc": description,
                "hashArray": fileHash,
                "fileType": "office"
            }

            strPatterns = []
            with open(matchPatternFilePath, 'r') as filePointer:
                while True:
                    buf = filePointer.readline(blocksize).strip('\n')
                    if not buf:
                        break
                    if "\x00" in buf:
                        str = "\"" + buf.split("-",1)[1].replace("\\","\\\\").replace('"','\\"').replace("\x00","") + "\" wide"
                        strPatterns.append(str)
                    else:
                        str = "\"" + buf.split("-",1)[1].replace("\\","\\\\").replace('"','\\"') + "\""
                        strPatterns.append(str)

            templateValDict["patterns"] = strPatterns
            templateValDict["condition"] = "any of them"

            yaraOutput = yaraTemplate.render(templateValDict)

            puts(colored.green("[+] YARA rules generated.\n"))
            puts(colored.blue(yaraOutput+"\n"))

            yaraFilePath = os.path.join(matchPatternDir, rulename.lower()+".yar")
            with open(yaraFilePath, "w") as filePointer:
                filePointer.write(yaraOutput)
            filePointer.close()

            puts(colored.green("[+] YARA rules generated and saved at {}.\n".format(os.path.abspath(yaraFilePath.lower()))))

        puts(colored.yellow("[*] Good BYE. Be Secured.\n"))
    except Exception as error:
        puts(colored.red("[!] Error executing application.\n"))
        logging.exception(error)
        sys.exit(1)
    except OSError as error:
        puts(colored.red("[!] Error executing application.\n"))
        logging.exception(error)
        sys.exit(1)
    except KeyboardInterrupt:
        puts(colored.red("[!] Application Interrupted.\n"))
        sys.exit(1)

if __name__ == '__main__':
    puts(colored.red(r"""
                     ,
                ,.  | \
               |: \ ; :\
               :' ;\| ::\
                \ : | `::\
                _)  |   `:`.
              ,' , `.    ;: ;
            ,' ;:  ;"'  ,:: |_
           /,   ` .    ;::: |:`-.__
        _,' _o\  ,::.`:' ;  ;   . '
    _,-'           `:.          ;""\,
 ,-'                     ,:         `-;,
 \,                       ;:           ;--._
  `.______,-,----._     ,' ;:        ,/ ,  ,`
         / /,-';'  \     ; `:      ,'/,::.:::
       ,',;-'-'_,--;    ;   :.   ,',',;::::::
      ( /___,-'     `.     ;::,,'o/  ,:::::::
       `'             )    ;:,'o /  ;"-   -::
                      \__ _,'o ,'         ,::
                         ) `--'       ,..::::
                         ; `.        ,:::::::
                          ;  ``::.    :::::::
    """))

    f = Figlet(font='slant')
    puts(colored.blue(f.renderText("Yara Silly Silly")))
    puts(colored.green("""
------------------------------------------------------------------------
Yara Silly Silly automatically generates YARA rules for you.
Thank you for using the application
Source code can be found at
https://github.com/YARA-Silly-Silly/yarasilly2
Maintained by:-
Krishnendu Paul and Himadri Ganguly
------------------------------------------------------------------------
    """))

    main()
