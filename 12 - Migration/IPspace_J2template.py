from jinja2 import Environment, FileSystemLoader, StrictUndefined

def _j2_parser(template_name, **kwargs):

    file_loader = FileSystemLoader('j2templates')
    env = Environment(loader=file_loader,
                      trim_blocks=True,
                      lstrip_blocks=True,
                      undefined=StrictUndefined)
    template = env.get_template(template_name)
    return template.render(**kwargs)


def create_port_cfg(
        portindex,
        description=None,
        ipv4_address=None,
        ipv4_address_mask=None,
        ip_vrf=None,
        ip_helpers=None,
        hsrp_gateway_ip=None,
        hsrp_grp_id=None,
        hsrp_active_router=True,
        hsrp_preempt=True,
        hsrp_version2=True,
        hsrp_key_chain_name=None):
    
    """
    Returns interface configuration.

    Arguments:
    portindex (str) --> portindex. 

    Keyword arguments:
    description (str) --> interface description. Defaults to None.

    ipv4_address (str) --> IPv4 address. Defaults to None.
    ipv4_address_mask (str) --> IPv4 address mask. Defaults to None.
    ip_vrf (str) --> VRF name. Defaults to None.
    ip_helpers (list) --> list of helper addresses. Defaults to None.
    
    hsrp_gateway_ip (str) --> Defaults to None.
    hsrp_grp_id (str) --> Defaults to None.
    hsrp_active_router (bool) --> Defaults to True. hsrp_grp_id must be not None
    hsrp_preempt --> (bool) Defaults to True. hsrp_grp_id must be not None
    hsrp_version2 --> (bool) Defaults to True. hsrp_grp_id must be not None
    hsrp_key_chain_name (str) --> Defaults to None. hsrp_grp_id must be not None
    """

    kwargs = {'if_index': portindex,
              'if_description': description,
              'ipv4_address': ipv4_address,
              'ipv4_address_mask': ipv4_address_mask,
              'ip_vrf': ip_vrf,
              'hsrp_grp_id': hsrp_grp_id,
              'ip_helpers': ip_helpers,
              'hsrp_active_router': hsrp_active_router,
              'hsrp_gateway_ip': hsrp_gateway_ip,
              'hsrp_preempt': hsrp_preempt,
              'hsrp_version2': hsrp_version2,
              'hsrp_key_chain_name': hsrp_key_chain_name}

    return _j2_parser('IPspace_interface_template.txt', **kwargs)




    
    
