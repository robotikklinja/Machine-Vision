# This code i written with AI and help, it might not work (Kommer ann på hvem du er)
from pymodbus.client import ModbusTcpClient

# Define the IP address and port of the UR5e robot
ROBOT_IP = '192.168.0.102'  # Example IP address, replace with the actual IP address of your robot
PORT = 502  # Default Modbus port for UR robots

# Connect to the robot
client = ModbusTcpClient(ROBOT_IP, port=PORT)
client.connect()

# # Read from 16-bit registers
# register_address = 139  # Starting address of the general-purpose 16-bit registers
# num_registers_to_read = 1  # Number of 16-bit registers to read (addresses 128 to 255)
# registers = client.read_holding_registers(register_address, num_registers_to_read)

# print("16-bit Registers:", registers.registers)

# Write to 16-bit registers
register_to_write = 139  # Address of the register to write
value_to_write = 0  # Value to write
client.write_register(register_to_write, value_to_write)
print("Wrote value", value_to_write, "to register", register_to_write)

# Close the connection 
client.close()
