from collections import defaultdict
import re
import json
from glob import glob


class ReSearcher(object):
    match = None

    def __call__(self, pattern, string):
        self.match = re.search(pattern, string)
        return self.match

    def __getattr__(self, name):
        return getattr(self.match, name)


def splitrange(raw_range):

    """
    ex. splitrange('105-107') will return ['105','106','107']
    """

    result = []

    if  re.search(r'^(\d+)\-(\d+)$', raw_range):
        match = re.search(r'^(\d+)\-(\d+)$', raw_range)
        first = int(format(match.group(1)))
        last = int(format(match.group(2)))
        for i in range(first, last+1):
            result.append(str(i))
        return result


def configreader(configfiles):

    switchinfo = defaultdict(dict) # Dict containing all info
    match = ReSearcher()

    for configfile in configfiles:

        with open(configfile, 'r') as lines:

            portinfo = defaultdict(dict)
            vlaninfo = defaultdict(dict)
            snmpinfo = {}
            
            port_scanitem = False
            
            for line in lines:

                line = line.rstrip()

                if match(r'hostname (.*)', line):
                    hostname = format(match.group(1))

                # start portinfo items
                elif match(r'^interface (.*)', line):
                    portindex = format(match.group(1))
                    vlan_allow_list = []
                    port_scanitem = True
                                   
                elif match(r'^ switchport mode (\w+)', line) and port_scanitem:
                    value = format(match.group(1))
                    portinfo[portindex]['switchport mode'] = value

                elif match(r'^ description (.*)', line) and port_scanitem:
                    value = format(match.group(1))
                    portinfo[portindex]['description'] = value

                elif (match(r'^ switchport access vlan (\d+)', line)
                        and port_scanitem):
                    value = format(match.group(1))
                    portinfo[portindex]['switchport access vlan'] = value

                elif (match(r'^ switchport trunk allow vlan.* ([0-9,-]+)', line)
                        and port_scanitem):
                    value = format(match.group(1))
                    for raw_vlans in value.split(','):
                        if '-' in raw_vlans:
                            for vlan_id in splitrange(raw_vlans):
                                vlan_allow_list.append(vlan_id)
                        else:
                            vlan_allow_list.append(raw_vlans)
                    portinfo[portindex]['vlan_allow_list'] = vlan_allow_list

                # start vlaninfo items
                elif match(r'^vlan (\d)$', line):
                    vlanindex = format(match.group(1))
                    port_scanitem = True
                    vlaninfo[vlanindex]['vlanindex'] = vlanindex

                elif match(r'^vlan ([0-9,-]+)', line):
                    port_scanitem = True
                    value = format(match.group(1))
                    for raw_vlans in value.split(','):
                        if '-' in raw_vlans:
                            for vlan_id in splitrange(raw_vlans):
                                vlan_id = str(vlan_id)
                                vlaninfo[vlan_id]['vlanindex'] = vlan_id
                        else:
                            vlaninfo[raw_vlans]['vlanindex'] = str(raw_vlans)

                elif match(r' name (.*)', line) and port_scanitem:
                    value = format(match.group(1))
                    vlaninfo[vlanindex]['name'] = value

                # start snmpinfo items
                elif match(r'snmp-server location (.*)', line):
                    value = format(match.group(1))
                    snmpinfo['location'] = value

                elif match(r'!', line) and port_scanitem:
                    port_scanitem = False

        switchinfo[hostname]['portinfo'] = portinfo
        switchinfo[hostname]['vlaninfo'] = vlaninfo
        switchinfo[hostname]['snmpinfo'] = snmpinfo

    return switchinfo


def main():

    configfiles = [file for file in glob('*-cfg.txt')]

    switchinfo = configreader(configfiles)

    with open('10 - switchinfo-json.txt', 'w') as js:
        json.dump(switchinfo, js, indent=4)
        print('\n', file=js)


if __name__ == "__main__":
    main()


                
