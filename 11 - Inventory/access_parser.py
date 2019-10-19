import json
from glob import glob
import re
from collections import defaultdict


class ReSearcher:

    """
    Helper class to enable evaluation
    and regex formatting in a single line
    """

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

        with open(configfile, 'r') as f:

            file = f.read()

        portinfo = defaultdict(dict)
        vlaninfo = defaultdict(dict)
        
        port_scanitem = False
        
        for line in file.splitlines():

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
            elif match(r'^vlan (.*)', line):
                vlanindex = format(match.group(1))
                port_scanitem = True

            elif match(r' name (.*)', line) and port_scanitem:
                value = format(match.group(1))
                vlaninfo[vlanindex]['name'] = value

            elif match(r'!', line) and port_scanitem:
                port_scanitem = False

        switchinfo[hostname]['portinfo'] = portinfo
        switchinfo[hostname]['vlaninfo'] = vlaninfo

    return switchinfo


def calc_inventory(dist_info):

    switch_cand_config_list = []

    for dist in dist_info:
        for port, portitems in dist_info[dist]['portinfo'].items():

            desc = portitems.get('description')
            
            # Find interfaces connected to access switches
            if (desc is None or 'core' in desc):
                continue

            # show regex101.com
            match = re.search(r'^(switch\d+)_(\d\/\d+)', desc)
         
            # Invalid syntax in description
            if match:
                switch = format(match.group(1))
                switch_cand_config_list.append(switch + '-cfg.txt')
            else:
                fmt = '{} of distribution switch {} has invalid format'
                print(fmt.format(port, dist))

 
    # Calculate list of switches present in config directory
    present_access_cfgs = [f for f in glob('switch*')]

    # Calculate list of switches with missing configuration
    switch_missing_cfg = list(set(switch_cand_config_list) -
                              set(present_access_cfgs))
    print('The following candidate switches have no config backup:')
    for switch in switch_missing_cfg:
        print(switch)
    print('\n')
        
    # Calculate list of switches present in descriptions of distribution
    # switches which are present in configuration backup directory
    switch_cfgs = list(set(present_access_cfgs) & set(switch_cand_config_list))
    
    return switch_cfgs



def main():
  
    with open('distr-json.txt', 'r') as js:
        dist_info = json.load(js)

    switch_cfgs = calc_inventory(dist_info)

    switchinfo = configreader(switch_cfgs)

    with open('switchinfo-json.txt', 'w') as js:
        json.dump(switchinfo, js, indent=4, sort_keys=True)
    
main()


        
    
