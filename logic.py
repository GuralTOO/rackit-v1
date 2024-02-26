import math
from rack import Rack
from device import Device
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Cluster:
    def __init__(self, name):
        self.name = name
        self.racks = []
        self.devices = []
        self.site = ''
        self.location = ''
        self.facility_id = ''
        self.tenant = ''
        self.compute_devices = []
        self.region = 'North America / US-East'

        self.su_count = 0


    # a scalable unit is a set of 8 compute and 1 network racks + storage racks if needed, it is composed of 256 gpus
    def create_scalable_unit(self, storage_racks=False, cage_location_x=0, cage_location_y=0):

        # where do we place the first rack? - x, y offset
        self.su_count += 1

        # add 9 racks to the cluster, no storage racks
        for i in range(0, 9):
            rack = Rack(
                
                # if su_count is < 10, the rack id is c01, c02, c03, etc. if su_count is > 10, the rack id is c10, c11, c12, etc.        
                id='p' + str(self.su_count).zfill(2) + 'c' + str(i+1).zfill(2),                
                
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
            
            # iterate over the last 9 racks in the cluster
        cnt = 0
        for rack in self.racks[-9:]:
            # add the network rack in the middle
            # 8 leaf switches and 4 spine switches
            rack_key = self.racks.index(rack)
            print(rack_key)
            cnt+=1
            
            if cnt == 5:
                
                rack.rack_type = 'Network Rack'
                # predifined positions for the leaf and spine switches (U position in the rack)
                leaf_switch_positions = [9, 11, 13, 15, 17, 19, 21, 23]
                spine_switch_positions = [27, 29, 31, 33]

                for i in range(0, 8):
                    leaf_switch = Device(
                        site=self.site, 
                        location=self.location,
                        # facility_id=self.facility_id,
                        region=self.region,
                        tenant=self.tenant,
                        rack_id=self.racks[4].id,
                        position='U' + str(leaf_switch_positions[i]) + ' / Front',
                        gps_coordinates='',
                        device_type='Nvidia QM9790-NS2F',
                        description='',
                        airflow='Front to rear',
                        serial_number='...',
                        asset_tag='',
                        config_template='',
                        power=0,
                        height=1,
                        compute_units=0,
                    )
                    self.racks[rack_key].devices.append(leaf_switch)
                    self.devices.append(leaf_switch)
                
                for i in range(0, 4):
                    spine_switch = Device(
                        site=self.site, 
                        location=self.location,
                        # facility_id=self.facility_id,
                        region=self.region,                    
                        tenant=self.tenant,
                        rack_id=self.racks[4].id,
                        position='U' + str(spine_switch_positions[i]) + ' / Front',
                        gps_coordinates='',
                        device_type='Juniper QFX5120-32C',
                        description='',
                        airflow='Front to rear',
                        serial_number='...',
                        asset_tag='',
                        config_template='',
                        power=0,
                        height=1,
                        compute_units=0,
                    )
                    self.racks[rack_key].devices.append(spine_switch)
                    self.devices.append(spine_switch)
                
                # move onto the next rack
                continue
            
            
            
            # for each compute rack, add 4 servers with 8 GPUs each
            for server_key in range(0, 4):
                
                rack.rack_type = 'Compute Rack'
                # server position is the height of the slot in the rack
                server_position = [3, 12, 25, 34]
                server = Device(
                    site=self.site, 
                    location=self.location,
                    # facility_id=self.facility_id,
                    region=self.region,
                    tenant=self.tenant,
                    rack_id=self.racks[4].id,
                    position='U' + str(server_position[server_key]) + ' / Front',
                    gps_coordinates='',
                    
                    device_type='Supermicro SYS-821GE-TNHR (8U)',
                    description='',
                    airflow='Front to rear',
                    serial_number='...',
                    asset_tag='',
                    config_template='',
                    # TODO: add the power consumption of the server based on the device type
                    power=0,
                    height=8,
                    compute_units=8,
                )
                rack.devices.append(server)
                self.devices.append(server)
                
        print('Created scalable unit')
        print('Racks:', len(self.racks))
        for rack in self.racks:
            print("Rack:", rack.id, "Devices:", len(rack.devices))
            for device in rack.devices:
                print("Device:", device.device_type, "Position:", device.position)

        
    # The network topology is a work in progress, not yet integrated into the cluster
    # Idea: use network topology to work out the connections between the devices
    def create_network_topology(self):
        ports_per_switch = 64
        
        gpu_count = 0
        for device in self.devices:
            if device.compute_units:
                gpu_count += device.compute_units

        # Does not support Core Switches so far, gpu count < 2k
        if gpu_count > ports_per_switch * (ports_per_switch // 2):
            raise ValueError("Too many GPUs for this topology")

        if gpu_count <= ports_per_switch:
            leaf_count = 1
        else:
            leaf_count = math.ceil(gpu_count / (ports_per_switch / 2))

        spine_count = math.ceil(gpu_count / ports_per_switch)
        if leaf_count < 2:
            spine_count = 0

        # Init connection cables
        leaf_south_bound = [[] for _ in range(leaf_count + 1)]
        leaf_north_bound = [[] for _ in range(leaf_count + 1)]
        gpu_connections = [[] for _ in range(gpu_count + 1)]
        spine_connections = [[] for _ in range(spine_count + 1)]

        gpus_per_leaf = math.ceil(gpu_count / leaf_count)

        # Calculate compute connections
        for i in range(1, leaf_count + 1):
            
            # Connect each GPU to the leaf switch (south bound)
            # Connections are stored both ways, from the GPU to the leaf switch and from the leaf switch to the GPU
            for j in range(gpus_per_leaf * (i - 1) + 1, min(gpus_per_leaf * i, gpu_count) + 1):
                leaf_index = j - gpus_per_leaf * (i - 1)
                leaf_south_bound[i].append({
                    'gpu': j,
                    'cable_count': 1,
                    'gpu_port': j,
                    'leaf_ports': [leaf_index],
                })
                gpu_connections[j] = {'leaf': i}

            # Connect the leaf switch to the spine switch (north bound) and store the connections both ways
            for j in range(1, spine_count + 1):
                leaf_ports = list(range((i - 1) * (ports_per_switch // 2) + 1, i * (ports_per_switch // 2) + 1))
                leaf_north_bound[i].append({
                    'spine': j,
                    'cable_count': gpus_per_leaf / spine_count,
                    'leaf_ports': leaf_ports,
                    'spine_port': i,
                })
                spine_connections[j].append({
                    'leaf': i,
                    'cable_count': gpus_per_leaf / spine_count,
                    'spine_port': i,
                    'leaf_ports': leaf_ports,
                })

        # TODO:  Create a Cable class to store the connections
        # Map the connections to the compute devices
        
        
        return {
            'leaf_south_bound': leaf_south_bound,
            'leaf_north_bound': leaf_north_bound,
            'gpu_connections': gpu_connections,
            'spine_connections': spine_connections,
        }
            
    def visualize(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        for i, rack in enumerate(self.racks):
            # Assuming outer_width and outer_depth are in millimeters and converting to a unified scale for visualization
            outer_width_mm = int(rack.outer_width.split()[0])  # Extracting numerical value
            outer_depth_mm = int(rack.outer_depth.split()[0])  # Extracting numerical value
            rect = patches.Rectangle((rack.room_location_x, rack.room_location_y), outer_width_mm, outer_depth_mm, linewidth=1, 
                                        # edge color is red if the rack is a compute rack, blue if it is a network rack, black otherwise
                                        edgecolor='red' if rack.rack_type == 'Compute Rack' else 'blue' if rack.rack_type == 'Network Rack' else 'black',
                                     
                                     facecolor='none')
            ax.add_patch(rect)
            ax.text(rack.room_location_x + outer_width_mm / 2, rack.room_location_y + outer_depth_mm / 2, str(rack.id), horizontalalignment='center', verticalalignment='center')

        ax.set_xlim(0, max([rack.room_location_x + int(rack.outer_width.split()[0]) for rack in self.racks]) + 1000)
        ax.set_ylim(0, max([rack.room_location_y + int(rack.outer_depth.split()[0]) for rack in self.racks]) + 1000)
        ax.set_aspect('equal')
        plt.show()
        
            
# create a cluster
cluster = Cluster('Cluster1')
# set the cluster attributes
cluster.site = 'sitenameXYZ'
cluster.location = 'locationnameXYZ'
cluster.facility_id = 'facilityidXYZ'
cluster.tenant = 'tenantXYZ'
# create a scalable unit
for i in range(0, 4):
    cluster.create_scalable_unit(cage_location_y=i * 2200)
    
print(len(cluster.racks))
cluster.visualize()

