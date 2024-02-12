class Device:
    def __init__(self, region, site, location, rack, position, gps_coordinates, tenant, device_type, description, airflow, serial_number, asset_tag, config_template,
                 power=0,
                #  Custom attributes
                compute_units=0,
                 ):

        # From NetBox
        self.region = region
        self.site = site
        self.location = location
        self.rack = rack
        self.position = position
        self.gps_coordinates = gps_coordinates
        self.tenant = tenant
        self.device_type = device_type
        self.description = description
        self.airflow = airflow
        self.serial_number = serial_number
        self.asset_tag = asset_tag
        self.config_template = config_template

        # Custom attributes
        self.power = power
        

# Example usage:
device_info = {
    'region': 'North America / US-East',
    'site': 'ATL02 - Edgeconnex ATL02',
    'location': 'ATL02 - Pod3',
    'rack': 'p03c46 (500.02)',
    'position': 'U34 / Front',
    'gps_coordinates': '',
    'tenant': 'Rakuten',
    'device_type': 'Supermicro SYS-821GE-TNHR (8U)',
    'description': '',
    'airflow': 'Front to rear',
    'serial_number': 'S899197X3928899C',
    'asset_tag': '',
    'config_template': ''
}

device = Device(**device_info)