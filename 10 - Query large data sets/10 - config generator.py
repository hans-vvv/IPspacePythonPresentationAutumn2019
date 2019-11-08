from random import randint
from collections import defaultdict

switch_vlans = defaultdict(list)
location_id = {}

for index in range(1, 501): # 500 switches

    # 250 VLAN's and 48 access ports per switch and 10 locations
    vlan_list = [str(randint(1, 250)) for p in range(1, 49)] 
    switch_vlans['switch' + str(index)] = vlan_list
    location_id['switch' + str(index)] = 'location' + str(randint(1, 10))

total_vlans = defaultdict(list)
for hostname in switch_vlans:
    total_vlans[hostname] = sorted(list(set(switch_vlans[hostname])), key=int)


for hostname in switch_vlans:

    with open(hostname + '-cfg.txt', 'w') as file:

        print('hostname {}'.format(hostname), file=file)
        print('!', file=file)
        print('snmp-server location {}'.format(location_id[hostname]), file=file)
        print('!', file=file)
        all_vlans_per_switch = ','.join(total_vlans[hostname])
        print('vlan {}'.format(all_vlans_per_switch), file=file)
        print('!', file=file)
        
        for index, vlan in enumerate(switch_vlans[hostname]):

            print('interface FastEthernet {}'.format(index+1), file=file)
            print(' switchport mode access', file=file)
            print(' switchport access vlan {}'.format(vlan), file=file)
            print('!', file=file)

        print('interface Port-channel 1', file=file)
        print(' description uplink to distribution', file=file)
        print(' switchport mode trunk', file=file)
        print(' switchport trunk allow vlan {}'.format(all_vlans_per_switch), file=file)
        print('!', file=file)
           
        

