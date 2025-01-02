import numpy as np
import subprocess

class UnitConverter:
    def __init__(self, dim, E_units, F_units):
        self.dim = dim
        self.E_units = E_units
        self.F_units = F_units
        self.conversion_factor = self.calculate_conversion()

    def calculate_conversion(self):
        conversion_factor = [0, 0, 0]
        # Dimension units
        if self.dim == "Meters":
            conversion_factor[0] = 1
        elif self.dim == "Millimeters":
            conversion_factor[0] = 0.001
        elif self.dim == "Centimeters":
            conversion_factor[0] = 0.01
        elif self.dim == "Inches":
            conversion_factor[0] = 0.0254
        elif self.dim == "Feet":
            conversion_factor[0] = 0.3048
        elif self.dim == "Yards":
            conversion_factor[0] = 0.9144

        # Young's Modulus Units
        if self.E_units == "GPa":
            conversion_factor[1] = 1e9
        elif self.E_units == "MPa":
            conversion_factor[1] = 1e6
        elif self.E_units == "psi":
            conversion_factor[1] = 6894.76
        elif self.E_units == "ksi":
            conversion_factor[1] = 6894.76 * 1e3

        # Force Units
        if self.F_units == "Newtons":
            conversion_factor[2] = 1
        elif self.F_units == "Kilograms-force":
            conversion_factor[2] = 9.80665
        elif self.F_units == "Pounds":
            conversion_factor[2] = 4.44822
        elif self.F_units == "Pounds-force":
            conversion_factor[2] = 4.44822

        return conversion_factor


class Material:
    def __init__(self, E, A):
        self.E = E  # Young's modulus
        self.A = A  # Cross-sectional area


class Node:
    def __init__(self, coordinates):
        self.coordinates = np.array(coordinates)


class Member:
    def __init__(self, start_node, end_node, material):
        self.start_node = start_node
        self.end_node = end_node
        self.material = material
        self.length = self.calculate_length()
        self.direction_cosines = self.calculate_direction_cosines()

    def calculate_length(self):
        dx = self.end_node.coordinates[0] - self.start_node.coordinates[0]
        dy = self.end_node.coordinates[1] - self.start_node.coordinates[1]
        dz = self.end_node.coordinates[2] - self.start_node.coordinates[2]
        return np.sqrt(dx**2 + dy**2 + dz**2)

    def calculate_direction_cosines(self):
        length = self.length
        dx = (self.end_node.coordinates[0] - self.start_node.coordinates[0]) / length
        dy = (self.end_node.coordinates[1] - self.start_node.coordinates[1]) / length
        dz = (self.end_node.coordinates[2] - self.start_node.coordinates[2]) / length
        return np.array([dx, dy, dz])


class Structure:
    def __init__(self):
        self.nodes = []
        self.members = []
        self.global_K = None

    def add_node(self, coordinates):
        node = Node(coordinates)
        self.nodes.append(node)

    def add_member(self, start_node_index, end_node_index, material):
        member = Member(self.nodes[start_node_index], self.nodes[end_node_index], material)
        self.members.append(member)

    def assemble_global_stiffness_matrix(self):
        # Initialize global stiffness matrix
        max_joint = len(self.nodes)
        self.global_K = np.zeros((3 * max_joint, 3 * max_joint))

        for member in self.members:
            K = (member.material.E * member.material.A / member.length)
            c = member.direction_cosines

            # Update global stiffness matrix
            for i in range(3):
                for j in range(3):
                    self.global_K[3 * member.start_node.index + i, 3 * member.start_node.index + j] += K * c[i] * c[j]
                    self.global_K[3 * member.start_node.index + i, 3 * member.end_node.index + j] -= K * c[i] * c[j]
                    self.global_K[3 * member.end_node.index + i, 3 * member.start_node.index + j] -= K * c[i] * c[j]
                    self.global_K[3 * member.end_node.index + i, 3 * member.end_node.index + j] += K * c[i] * c[j]


class Analysis:
    def __init__(self, structure):
        self.structure = structure

    def solve(self, loads, reaction_conditions):
        # Apply boundary conditions and solve for displacements
        global_k_store = self.structure.global_K.copy()
        # Modify global_k_store based on reaction_conditions
        # Solve for displacements
        N_disp = np.linalg.solve(global_k_store, loads)
        return N_disp


# Example of how to use the classes
unit_converter = UnitConverter(dim, E_units, F_units)
material = Material(E=unit_converter.conversion_factor[1], A=some_area_value)

structure = Structure()
# Add nodes and members to the structure
# structure.add_node([x, y, z])
# structure.add_member(start_node_index, end_node_index, material)

analysis = Analysis(structure)
# analysis.solve(loads, reaction_conditions)