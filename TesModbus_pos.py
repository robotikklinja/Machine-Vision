"""
This code is going to try and find the position(s) of the UR5 robot through Modebus.

Made by B.Stokke on 09.01.2025
"""
import numpy as np

# This code is written with AI and help, it might not work (Kommer ann på hvem du er)
from pymodbus.client import ModbusTcpClient

def dh_matrix(theta, d, a, alpha):
    """
    Compute the Denavit-Hartenberg Transformation Matrix.
    
    Parameters:
        theta: Joint angle (in radians)
        d: Link offset
        a: Link length
        alpha: Link twist (in radians)
    Returns:
        4x4 transformation matrix
    """
    return np.array([
        [np.cos(theta), -np.sin(theta) * np.cos(alpha), np.sin(theta) * np.sin(alpha), a * np.cos(theta)],
        [np.sin(theta), np.cos(theta) * np.cos(alpha), -np.cos(theta) * np.sin(alpha), a * np.sin(theta)],
        [0, np.sin(alpha), np.cos(alpha), d],
        [0, 0, 0, 1]
    ])

def forward_kinematics(joint_angles):
    """
    Compute the forward kinematics for the UR5 robot.
    
    Parameters:
        joint_angles: List of 6 joint angles in radians
    Returns:
        A numpy array representing the (x, y, z) coordinates of the end effector
    """
    # UR5 DH Parameters: [theta, d, a, alpha]
    dh_params = [
        [joint_angles[0], 0.089159, 0, np.pi / 2],
        [joint_angles[1], 0, -0.425, 0],
        [joint_angles[2], 0, -0.39225, 0],
        [joint_angles[3], 0.10915, 0, np.pi / 2],
        [joint_angles[4], 0.09465, 0, -np.pi / 2],
        [joint_angles[5], 0.0823, 0, 0]
    ]

    # Initialize transformation matrix as identity
    t_matrix = np.eye(4)

    # Compute the transformation matrix for each joint
    for param in dh_params:
        theta, d, a, alpha = param
        t_matrix = np.dot(t_matrix, dh_matrix(theta, d, a, alpha))

    # Extract the end-effector position from the final transformation matrix
    end_effector_pos = t_matrix[:3, 3]

    return end_effector_pos

# Define the IP address and port of the UR5e robot
ROBOT_IP = '192.168.0.102'  # IP address, replace with the actual IP address of your robot
PORT = 502  # Default Modbus port for UR robots

# Connect to the robot
client = ModbusTcpClient(ROBOT_IP, port=PORT)
client.connect()

# The reference place for the joint rotation:
a_reg = 270
b_reg = 271
c_reg = 272
d_reg = 273
e_reg = 274
f_reg = 275

a_val = client.read_holding_registers(a_reg, 1).registers[0]
b_val = client.read_holding_registers(b_reg, 1).registers[0]
c_val = client.read_holding_registers(c_reg, 1).registers[0]
d_val = client.read_holding_registers(d_reg, 1).registers[0]
e_val = client.read_holding_registers(e_reg, 1).registers[0]
f_val = client.read_holding_registers(f_reg, 1).registers[0]

# Replace with the actual joint angles (in radians)
joint_angles = [a_val, b_val, c_val, d_val, e_val, f_val]

# Compute the end-effector position
end_effector_position = forward_kinematics(joint_angles)

print(f"End Effector Position: {end_effector_position}")

print(f"Robot Position:", a_val, c_val, d_val, e_val, f_val)

# Close the connection
client.close()