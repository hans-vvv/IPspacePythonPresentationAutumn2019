# IPython log file

from collections import defaultdict
vlan_set = defaultdict(set)

vlan_set['switch1'] = {1,2,3}
vlan_set['switch2'] = {2,3,7}
vlan_set['switch3'] = {4,5,6}

result_set = set()
for hostname in vlan_set:
    if hostname == 'switch2':
        continue
    for vlan in vlan_set[hostname]:
        result_set.add(vlan)

print(result_set)
  
##result_set = {item for hostname in vlan_set for item in vlan_set[hostname]
##              if hostname != 'switch2'}



