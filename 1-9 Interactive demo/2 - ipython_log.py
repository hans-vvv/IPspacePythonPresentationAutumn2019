# IPython log file


portinfo = {}
portinfo['FastEthernet 1']['speed'] = '100' # returns KeyError

from collections import defaultdict

portinfo = defaultdict(dict)

portinfo['FastEthernet 1']['speed'] = '100'
portinfo
portinfo['FastEthernet 1']['switchport mode'] = 'trunk'
portinfo
portinfo['FastEthernet 2']['speed'] = '1000'
portinfo['FastEthernet 2']['switchport mode'] = 'access'
portinfo
portinfo['FastEthernet 1'].get('speed')
portinfo['FastEthernet 2'].get('speed')

for port in portinfo:
    print(port)
    
for port, portitems in portinfo.items():
    for k,v in portitems.items():
        print('Interface {} has key "{}" and value "{}"'.format(port, k, v))
