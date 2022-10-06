"""
Generate dummy lef file.
"""
import os
from typing import List
import random
from definition import *

PATH_TO_WRITE_LEF = f"{ROOT_DIR}/lef_files"


class GenerateLef:
    """Generate Dummy Lef File
    Create a lef file with a specified number of cells and ports.
    """

    def __init__(self, number_of_cells: int = 1, number_of_ports: int = 1) -> None:
        """Init method to generate dummy lef file.

        Args:
            number_of_cells (int): Number of cells to add in the lef file.
            number_of_ports (int): Number of ports to add for each cells.
        """
        self._nb_cells = number_of_cells
        self._nb_ports = number_of_ports
        self.lef_content: List = []

    def write_lef(self, lef_name: str = 'dummy.lef') -> None:
        """Generate dummy lef file.
        This method will generate a lef file with a specified amount of cells and ports.
        The amount of cell generate is set during the initialisation of the class.

        Args:
            lef_name (str, optional): Lef filename to generate. Defaults to 'dummy.lef'.
        """
        os.makedirs(PATH_TO_WRITE_LEF, exist_ok=True)
        with open(f"{PATH_TO_WRITE_LEF}/{lef_name}", 'w', encoding='utf-8') as lef_stream:
            lef_stream.write("\n".join(self.lef_content))

    def get_lenght_of_pin(self, number_of_pin_on_one_side: int) -> float:
        """Calculate the length and spacing of pins

        Args:
            number_of_pin_on_one_side (int): Number of pins on each side.

        Returns:
            float, float: pin length and spacing
        """
        pin_length = 1
        pin_spacing = 5
        while pin_length * number_of_pin_on_one_side > (80 - pin_spacing):
            pin_length = pin_length / 2
        pin_spacing = 80 - (pin_length * number_of_pin_on_one_side)
        return pin_length, pin_spacing / (number_of_pin_on_one_side + 1)

    def add_cell(self, cell_name: str) -> None:
        """Add a cell (MACRO) to the lef to be generated.
        Will create a MACRO (lef statement for cell) as a string and
        add it to the class variable `self.lef_content`.
        It will also add the port for the cell using `add_port` method.

        Output will look like so:
        MACRO <cell_name>
            SIZE 100 BY 100
            <PINS...>
        END MACRO

        Args:
            cell_name (str): Cell name to add.
        """
        cell: List = [f"MACRO {cell_name}"]
        cell.append("\tSIZE 100 BY 100 ;")
        for pin_index in range(self._nb_ports):
            cell += self.add_pin(pin_index)
        cell.append("END MACRO")
        self.lef_content += cell

    def _get_pin_placement_info(self):
        """
        This method will setup multiple variable needed for the pin placement:
            - number_of_pin_shapes_to_generate_on_each_side to know how the pin will be dispatched
                on each side if the cell.
                Examples:
                    - 8 ports to dispatch on eash side (4) of the cell. Which mean 2 ports on each side.
                    - 6 ports to dispatch on each side, since we can't have the same amount of port on
                    each side, we will have 3 ports on the left side and 3 port on the right side.
            - pin_length and pin_spacing, calculating the dimension of the pins and the spacing
                between them.
            - first_pols_on_each_side, we will be calculating the first pin polygon to place on each side
                and when adding more pin to the side we will be shifting that first shape depending on
                the side, the pin_length and the pin_spacing.
            - which_side, will be use to determing on which side are we placing the pin and how we should
                shift the first shape depending on x or y axis.
        """
        if not hasattr(self, "number_of_pin_shapes_to_generate_on_each_side"):
            self.number_of_pin_shapes_to_generate_on_each_side = self._nb_ports // 4 + self._nb_ports % 4
        if not hasattr(self, "pin_length") or not hasattr(self, "pin_spacing"):
            self.pin_length, self.pin_spacing = self.get_lenght_of_pin(self.number_of_pin_shapes_to_generate_on_each_side)
        if not hasattr(self, "first_pols_on_each_side"):
            self.first_pols_on_each_side = {
                'bottom': (10 + self.pin_spacing, 0, 10 + self.pin_length + self.pin_spacing, self.pin_length),
                'right': (100 - self.pin_length, 10 + self.pin_spacing, 100, 10 + self.pin_length + self.pin_spacing),
                'top': (90 - self.pin_length - self.pin_spacing, 100 - self.pin_length, 90 - self.pin_spacing, 100),
                'left': (0, 90 - self.pin_length - self.pin_spacing, self.pin_length, 90 - self.pin_spacing)
            }
        if not hasattr(self, "which_side"):
            self.which_side = ['left', 'right', 'top', 'bottom']

    def _get_pin_shape(self, pin_index: int) -> str:
        """Get the pin shape.

        Args:
            pin_index (int): Pin number.

        Returns:
            str: String of the shape created.
        """
        if pin_index % self.number_of_pin_shapes_to_generate_on_each_side == 0 or (not hasattr(self, "pin_shape") and not hasattr(self, "side")):
            self.side = self.which_side.pop(self.which_side.index(self.which_side[0]))  # remove the first element of the list
            self.which_side.append(self.side)  # append it to become the last element, in case we have multiple cell to add to restart the algo
            self.pin_shape = self.first_pols_on_each_side[self.side]
        elif self.side == 'bottom':
            self.pin_shape = (
                self.pin_shape[2] + self.pin_spacing,
                self.pin_shape[1],
                self.pin_shape[2] + self.pin_spacing + self.pin_length,
                self.pin_shape[3]
            )
        elif self.side == 'right':
            self.pin_shape = (
                self.pin_shape[0],
                self.pin_shape[3] + self.pin_spacing,
                self.pin_shape[2],
                self.pin_shape[3] + self.pin_spacing + self.pin_length
            )
        elif self.side == 'top':
            self.pin_shape = (
                self.pin_shape[0] - self.pin_spacing - self.pin_length,
                self.pin_shape[1],
                self.pin_shape[0] - self.pin_spacing,
                self.pin_shape[3]
            )
        elif self.side == 'left':
            self.pin_shape = (
                self.pin_shape[0],
                self.pin_shape[1] - self.pin_spacing - self.pin_length,
                self.pin_shape[2],
                self.pin_shape[1] - self.pin_spacing
            )
        return " ".join([str(point) for point in self.pin_shape])

    def add_pin(self, pin_index: int) -> List:
        """Add a pin (PIN) to a cell.

        Output will look like so:
        PIN <pin_name>
            DIRECTION INPUT | OUTPUT | INOUT ;
            USE SIGNAL | POWER | GROUND ;
            PORT
                LAYER M1 ;
                RECT bot_left_x bot_left_y top_rigth_x top_right_y ;
            END
        END <pin_name>

        Args:
            pin_index (int): Pin index to use for the name `pin_<pin_index>`.
        """
        pin_name = f"pin_{pin_index}"
        port: List = [f"\tPIN {pin_name}"]
        direction = random.choice(["INPUT", "OUTPUT", "INOUT"])
        use = random.choice(["SIGNAL", "POWER", "GROUND"])
        port.append(f"\t\tDIRECTION {direction} ;")
        port.append(f"\t\tUSE {use} ;")
        port.append("\t\tPORT")
        port.append("\t\t\tLAYER M1 ;")
        self._get_pin_placement_info()
        shape_str = self._get_pin_shape(pin_index=pin_index)
        port.append(f"\t\t\tRECT {shape_str} ;")
        port.append("\t\tEND PORT")
        port.append(f"\tEND {pin_name}")
        return port

    def generate_lef(self) -> None:
        """
        Generate lef file.
        """
        for cell_index in range(self._nb_cells):
            self.add_cell(f"cell_{cell_index}")
