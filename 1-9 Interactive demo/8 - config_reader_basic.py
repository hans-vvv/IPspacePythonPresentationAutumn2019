from collections import defaultdict
import re
import json


class ReSearcher(object):
    match = None

    def __call__(self, pattern, string):
        self.match = re.search(pattern, string)
        return self.match

    def __getattr__(self, name):
        return getattr(self.match, name)


def configreader(configfiles):

    switchinfo = defaultdict(dict) # Dict containing all info
    match = ReSearcher()

    for configfile in configfiles:

        with open(configfile, 'r') as f:

            file = f.read()


        portinfo = defaultdict(dict)
        
        for line in file.splitlines():

            if match(r'^interface (.*)', line):
                portindex = format(match.group(1))

            elif match(r'hostname (.*)', line):
                hostname = format(match.group(1))

            elif match(r'^ switchport mode (\w+)', line):
                value = format(match.group(1))
                portinfo[portindex]['switchport mode'] = value

            elif match(r'^ description (.*)', line):
                value = format(match.group(1))
                portinfo[portindex]['description'] = value

            elif match(r'^ switchport access vlan (\d+)', line):
                value = format(match.group(1))
                portinfo[portindex]['switchport access vlan'] = value

            elif match(r'^ switchport trunk allow vlan (\d+)', line):
                value = format(match.group(1))
                portinfo[portindex]['switchport trunk allow vlan'] = value

        switchinfo[hostname]['portinfo'] = portinfo

    return switchinfo


def main():

    configfiles = ['8 - Switch1.txt']

    switchinfo = configreader(configfiles)

    with open('8 - switchinfo-json.txt', 'w') as js:
        json.dump(switchinfo, js, indent=4, sort_keys=True)
        print('\n', file=js)


if __name__ == "__main__":
    main()


                
