import getopt, sys

# from models import TxtFileHandler, IPParser, IpListGeoLocation
from models.FileHandler import TxtFileHandler 
from models.Parser import IPParser
from models.IPData import IpListGeoLocation, IPListRDAPLookUp


def get_file_data(file_name):
    txt_handler = TxtFileHandler()
    file_content = txt_handler.read(file_name)
    get_ip_data(file_content, True, True)


def get_ip_data(ip, geo_locator: bool, rdap_lookup: bool):
    parser = IPParser(ip)
    ips = parser.parse()
    data = []
    if geo_locator:
        geo_location = IpListGeoLocation(ips)
        geo_location_data = geo_location.get_data()
        data.append(geo_location_data)
    if rdap_lookup:
        rdap_lookup_ = IPListRDAPLookUp(ips)
        rdap_lookup_data = rdap_lookup_.get_data()
        data.append(rdap_lookup_data)
    print(data) 


def run_with_args():
    short_options = 'i:f:gr'
    long_options = ['ip=','file=', 'geo', 'rdap']
    arguments_list = sys.argv[1:]
    print(arguments_list)
    try:
        arguments, values = getopt.getopt(arguments_list, short_options, long_options)
    except getopt.error as err:
        print(str(err))
        sys.exit(2)
    ip = ''
    get_geo_locator = False
    make_rdap_lookup = False
    run_with_file = False
    file_name = None
    for current_argument, current_value in arguments:
        if current_argument in ('-i', '--ip'):
            ip = current_value
        if current_argument in ['-g', '--geo']:
            get_geo_locator = True
        if current_argument in ['-r','--rdap']:
            make_rdap_lookup = True
        if current_argument in ('-f', "--file"):
            run_with_file = True
            file_name = current_value
    if run_with_file:
        get_file_data(file_name)
    else:
        get_ip_data(ip, get_geo_locator, make_rdap_lookup)

if __name__ == "__main__":
    run_with_args()
