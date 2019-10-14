from collections import defaultdict, Counter
import json

with open('10 - switchinfo-json.txt', 'r') as myfile:
    switchinfo=json.load(myfile)

# Store SNMP location info
missing_snmp_loc = []
locations = []
for hostname in switchinfo:
    if switchinfo[hostname]['snmpinfo'].get('location') is None:
        missing_snmp_loc.append(hostname)
    if switchinfo[hostname]['snmpinfo'].get('location') is not None:
        location = switchinfo[hostname]['snmpinfo']['location']
        locations.append(location)

# print list of switches without SNMP location information    
print("The following switches have missing SNMP location configuration:")
for hostname in missing_snmp_loc:
    print(hostname)
print('\n')

# Distribution of number of switches per location
print('Distribution of number of switches per location')
dist = Counter(locations)
print(dist)
print('\n')

# VLAN computation example
vlan_db = defaultdict(set)
vlan_access = defaultdict(set)
vlan_allow = defaultdict(set)

# Store VLAN data in dicts
for hostname in switchinfo:
    for port, portitems in switchinfo[hostname]['portinfo'].items():
        if portitems.get('switchport access vlan') is not None:
            vlan = portitems['switchport access vlan']
            vlan_access[hostname].add(vlan)
        if portitems.get('vlan_allow_list') is not None:
            vlan_list = portitems['vlan_allow_list']
            vlan_allow[hostname] = set(vlan_list)

    for vlan, vlanitems in switchinfo[hostname]['vlaninfo'].items():
        vlan_db[hostname].add(vlan)

# Compare dicts to vlan_db
print('VLAN report:')
print('!')
for hostname in vlan_db:
    if vlan_db[hostname] != vlan_access[hostname]:
        fmt = "diff detected between vlan_db and access vlans on host {}"
        print(fmt.format(hostname))
        diff = vlan_db[hostname].symmetric_difference(vlan_access[hostname])
        print("diff is: {}".format(diff))
        print("!")
    if vlan_db[hostname] != vlan_allow[hostname]:
        fmt = "diff detected between vlan_db and vlan_allow_list on host {}"
        print(fmt.format(hostname))
        diff = vlan_db[hostname].symmetric_difference(vlan_allow[hostname])
        print("diff is: {}".format(diff))
        print("!")

# The set of VLAN's present on all access ports
total_vlans = set()
for hostname in vlan_access:
    for vlan in vlan_access[hostname]:
        total_vlans.add(vlan)

fmt = 'The total number of VLANs in use on all access ports is: {}'
print(fmt.format(len(total_vlans)))






