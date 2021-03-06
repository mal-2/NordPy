import requests
from bin.logging_util import get_logger

logger = get_logger(__name__)


def exists_conf_for(server_name, protocol):
    """
    Checks if exists a .ovpn file for the specified server and protocol
    :param server_name: the name of the server
    :param protocol: the protocol to be used
    :return: True if exists, False otherwise
    """
    import os.path
    from bin.openvpn import get_path_to_conf

    conf_filename = get_path_to_conf(server_name, protocol)
    logger.debug("Checking if exists "+conf_filename)

    return os.path.exists(conf_filename)


def update_conf_files(sudo_password):
    """
    Downloads from nordvpn.com all the .ovpn files
    :param sudo_password: the root password
    """
    from bin.root import get_root_permissions
    from bin.pathUtil import CURRENT_PATH

    get_root_permissions(sudo_password)

    logger.debug("Missing files, trying to download the .ovpn files")
    ovpn_download_link = 'https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip'
    zip_filename = CURRENT_PATH + 'ovpn.zip'

    # downloading the zipped files
    r = requests.get(ovpn_download_link, allow_redirects=True)
    with open(zip_filename, 'wb') as zip_f:
        zip_f.write(r.content)

    # unzipping files
    import zipfile
    with zipfile.ZipFile(zip_filename, "r") as zip_ref:
        zip_ref.extractall(CURRENT_PATH)

    # removing zip
    from os import remove
    remove(zip_filename)

    logger.debug("Finished preparing ovpn files")


def get_available_servers():
    """
    returns a list of all available server
    :return: a list with all the server names
    """
    import os.path
    from bin.pathUtil import CURRENT_PATH

    servers_entire_name = os.listdir(CURRENT_PATH + "ovpn_tcp/")
    servers = []
    for server in servers_entire_name:
        servers.append(server.split(".")[0])
    servers.sort()
    return servers[:40]


def get_available_servers_dict():
    """
    returns a list of all available server as a dictionary whose keys are the countries
    :return: a dictionary
    """
    import os.path
    from bin.pathUtil import CURRENT_PATH

    def get_server_domain(server):
        numbers = '1234567890'
        domain = ''

        for letter in server:
            if letter not in numbers:
                domain += letter
            else:
                break

        return domain

    servers_entire_names = os.listdir(CURRENT_PATH + "ovpn_tcp/")
    servers = {}

    for server in servers_entire_names:
        domain_name = get_server_domain(server)

        try:
            servers[domain_name].append(server.split(".")[0])
        except KeyError:
            servers[domain_name] = [server.split(".")[0]]

    # sorts all servers
    for server_domain in servers.keys():
        servers[server_domain].sort()

    return servers

