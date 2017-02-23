# Global Variables
INI_PATH = 'conf/python.ini'

### Configuration module

# Init Config Object
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read(INI_PATH)

def ConfigSectionMap(section):
    _dict = {}
    options = Config.options(section)
    for option in options:
        try:
            _dict[option] = Config.get(section, option)
            if _dict[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            _dict[option] = None
    return _dict