from rack import Rack
from device import Device

class Cluster:
    def __init__(self, name, nodes):
        self.name = name
        self.nodes = nodes
        self.racks = []
        self.devices = []
        self.site = ''
        self.location = ''
        self.facility_id = ''
        self.tenant = ''
        

    def create_scalable_unit(self):

        # where do we place the first rack? - x, y offset
        cage_location_x = 0
        cage_location_y = 0

        # add 8 racks to the cluster
        for i in range(0, 9):
            rack = Rack(

                # cluster attributes
                site=self.site, 
                location=self.location,
                facility_id=self.facility_id,
                tenant=self.tenant,

                # need to dynamically add devices to the rack
                devices=[],

                # assuming the standard dimensions for a 4-post cabinet
                rack_type='4-post cabinet',
                width='19 inches',
                height='45U (ascending)',
                starting_unit=1,
                outer_width='800 Millimeters',
                outer_depth='1200 Millimeters',
                total_weight='408.2 Kilograms',
                
                # assuming that the racks are placed next to each other moving from left to right
                room_location_x=cage_location_x + (i * 800),
                room_location_y=cage_location_y,                  
            )
            self.racks.append(rack)
        for rack, key in zip(self.racks, range(0, 9)):
            # skip the network rack
            if key == 4:
                continue
            
            # for each compute rack, add 4 servers with 8 GPUs each
            for i in range(0, 4):
                server_position = 3
                if i == 1:
                    server_position = 12
                elif i == 2:
                    server_position = 25
                elif i == 3:
                    server_position = 34
                    
                server = Device(
                    site=self.site, 
                    location=self.location,
                    facility_id=self.facility_id,
                    tenant=self.tenant,
                    rack=rack,
                    position='U' + str(server_position) + ' / Front',
                    gps_coordinates='',
                    device_type='Supermicro SYS-821GE-TNHR (8U)',
                    description='',
                    airflow='Front to rear',
                    serial_number='...',
                    asset_tag='',
                    config_template='',
                    # TODO: add the power consumption of the server
                    power=0,
                    compute_units=8,
                )
                rack.devices.append(server)
                self.devices.append(server)
