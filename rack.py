class Rack:
    def __init__(self, site, location, facility_id, tenant, 
                #  status, role, description, serial_number, asset_tag, space_utilization, power_utilization, 
                 rack_type, width, height, starting_unit, outer_width, outer_depth, total_weight,
                 devices=[], room_location_x=0, room_location_y=0, power_used=0, power_max=0
                 ):

        # From NetBox
        self.site = site
        self.location = location
        self.facility_id = facility_id
        self.tenant = tenant
        # self.status = status
        # self.role = role
        # self.description = description
        # self.serial_number = serial_number
        # self.asset_tag = asset_tag
        # self.space_utilization = space_utilization
        # self.power_utilization = power_utilization
        self.type = rack_type
        self.width = width
        self.height = height
        self.starting_unit = starting_unit
        self.outer_width = outer_width
        self.outer_depth = outer_depth
        self.total_weight = total_weight

        # Custom attributes        
        self.devices = devices
        self.room_location_x = room_location_x
        self.room_location_y = room_location_y
        self.power_used = power_used
        self.power_max = power_max
        
    
    

# Example usage:
rack_info = {
    'site': 'sitenameXYZ',
    'location': 'locationnameXYZ',
    'facility_id': 'facilityidXYZ',
    'tenant': 'tenantXYZ',
    'devices': [],
    # 'status': 'Active',
    # 'role': 'Production Hosts',
    # 'description': '',
    # 'serial_number': '',
    # 'asset_tag': '',
    # 'space_utilization': '0.0%',
    # 'power_utilization': '0.0%',
    'rack_type': '4-post cabinet',
    'width': '19 inches',
    'height': '45U (ascending)',
    'starting_unit': 1,
    'outer_width': '800 Millimeters',
    'outer_depth': '1200 Millimeters',
    'total_weight': '408.2 Kilograms'
}

rack = Rack(**rack_info)
print(rack.site)

