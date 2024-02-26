import requests

class Rack:
    def __init__(self, id=None, url="", display="", name="", facility_id="", site=None, location=None, tenant=None, 
                 status=None, role=None, serial="", asset_tag="", rack_type=None, width=None, u_height=0, starting_unit=0, 
                 weight=0, max_weight=0, weight_unit=None, desc_units=False, outer_width=0, outer_depth=0, outer_unit=None, 
                 mounting_depth=0, description="", comments="", tags=None, custom_fields=None, created="", last_updated="", 
                 device_count=0, powerfeed_count=0, 
                 
                #  custom attributes
                 devices=[], room_location_x=0, room_location_y=0, power_used=0, power_max=0, height=0, total_weight=0):
        self.id = id
        self.url = url
        self.display = display
        self.name = name
        self.facility_id = facility_id
        self.site = site
        self.location = location
        self.tenant = tenant
        self.status = status
        self.role = role
        self.serial = serial
        self.asset_tag = asset_tag
        self.rack_type = rack_type
        self.width = width
        self.u_height = u_height
        self.starting_unit = starting_unit
        self.weight = weight
        self.max_weight = max_weight
        self.weight_unit = weight_unit
        self.desc_units = desc_units
        self.outer_width = outer_width
        self.outer_depth = outer_depth
        self.outer_unit = outer_unit
        self.mounting_depth = mounting_depth
        self.description = description
        self.comments = comments
        self.tags = tags if tags is not None else []
        self.custom_fields = custom_fields
        self.created = created
        self.last_updated = last_updated
        self.device_count = device_count
        self.powerfeed_count = powerfeed_count
        
        
        # Custom attributes
        self.devices = devices
        self.room_location_x = room_location_x
        self.room_location_y = room_location_y
        self.power_used = power_used
        self.power_max = power_max
        self.height = height
        self.total_weight = total_weight
        

    def save_to_netbox(self, netbox_url, api_token):
        """Placeholder for saving rack to NetBox."""
        headers = {'Authorization': f'Token {api_token}', 'Content-Type': 'application/json'}
        data = self.__dict__
        # response = requests.post(f'{netbox_url}/api/dcim/racks/', json=data, headers=headers)
        # return response.json()

    def retrieve_from_netbox(self, rack_id, netbox_url, api_token):
        """Placeholder for retrieving rack from NetBox."""
        headers = {'Authorization': f'Token {api_token}'}
        # response = requests.get(f'{netbox_url}/api/dcim/racks/{rack_id}/', headers=headers)
        # Populate this object's attributes with response data
        # data = response.json()
        pass





# class Rack:
#     def __init__(self, site, location, facility_id, tenant, 
#                 #  status, role, description, serial_number, asset_tag, space_utilization, power_utilization, 
#                  rack_type, width, height, starting_unit, outer_width, outer_depth, total_weight,
#                  devices=[], room_location_x=0, room_location_y=0, power_used=0, power_max=0
#                  ):

#         # From NetBox
#         self.site = site
#         self.location = location
#         self.facility_id = facility_id
#         self.tenant = tenant
#         # self.status = status
#         # self.role = role
#         # self.description = description
#         # self.serial_number = serial_number
#         # self.asset_tag = asset_tag
#         # self.space_utilization = space_utilization
#         # self.power_utilization = power_utilization
#         self.type = rack_type
#         self.width = width
#         self.height = height
#         self.starting_unit = starting_unit
#         self.outer_width = outer_width
#         self.outer_depth = outer_depth
#         self.total_weight = total_weight

#         # Custom attributes        
#         self.devices = devices
#         self.room_location_x = room_location_x
#         self.room_location_y = room_location_y
#         self.power_used = power_used
#         self.power_max = power_max
        
    
    

# # Example usage:
# rack_info = {
#     'site': 'sitenameXYZ',
#     'location': 'locationnameXYZ',
#     'facility_id': 'facilityidXYZ',
#     'tenant': 'tenantXYZ',
#     'devices': [],
#     # 'status': 'Active',
#     # 'role': 'Production Hosts',
#     # 'description': '',
#     # 'serial_number': '',
#     # 'asset_tag': '',
#     # 'space_utilization': '0.0%',
#     # 'power_utilization': '0.0%',
#     'rack_type': '4-post cabinet',
#     'width': '19 inches',
#     'height': '45U (ascending)',
#     'starting_unit': 1,
#     'outer_width': '800 Millimeters',
#     'outer_depth': '1200 Millimeters',
#     'total_weight': '408.2 Kilograms'
# }

# rack = Rack(**rack_info)
# print(rack.site)

