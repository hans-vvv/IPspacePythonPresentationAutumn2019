# IPython log file

from collections import defaultdict
portinfo = defaultdict(dict)

portinfo['FastEthernet 1']['speed'] = '100'
portinfo
portinfo['FastEthernet 1']['switchport mode'] = 'trunk'
portinfo
portinfo['FastEthernet 2']['speed'] = '1000'
portinfo['FastEthernet 2']['switchport mode'] = 'access'

switchinfo = defaultdict(dict)
switchinfo['switch1']['portinfo'] = portinfo 

switchinfo # display switchinfo dict
switchinfo['switch1']['portinfo']['FastEthernet 1'].get('speed')

portinfo = defaultdict(dict)
portinfo

portinfo['FastEthernet 1']['speed'] = 'auto'
portinfo
portinfo['FastEthernet 1']['switchport mode'] = 'access'
portinfo
switchinfo['switch2']['portinfo'] = portinfo
switchinfo

vlaninfo = defaultdict(dict)

vlaninfo['1']['name'] = 'one'
vlaninfo['2']['name'] = 'two'
vlaninfo['1']['ip address'] = 'no ip address'
vlaninfo['1']['shutdown'] = 'shutdown'

switchinfo['switch1']['vlaninfo'] = vlaninfo

vlaninfo = defaultdict(dict)

vlaninfo['1']['name'] = 'one'
vlaninfo['2']['name'] = 'two'
vlaninfo['1']['ip address'] = '1.1.1.1'
vlaninfo['1']['shutdown'] = 'shutdown'

switchinfo['switch2']['vlaninfo'] = vlaninfo

import json
print(json.dumps(switchinfo, indent=4))

for hostname in switchinfo:
    print(hostname)
    
for hostname in switchinfo:
    for port, portitems in switchinfo[hostname]['portinfo'].items():
        for k,v in portitems.items():
            print('Interface "{}" from "{}" has key "{}" and value "{}"'.format(port, hostname, k, v))
