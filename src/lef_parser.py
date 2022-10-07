"""
Lef Parser class.
"""


from typing import Iterable, Tuple
from winreg import DisableReflectionKey
import re
from xmlrpc.server import list_public_methods


class LefPort:
    """
    Class to describe a lef port.
    """

    def __init__(self, port_name: str, port_file: str) -> None:
        self.port_name = port_name
        self.port_file = port_file

    def get_name(self) -> str:
        """Get the name of the port.

        Returns:
            str: Name of the port.
        """
        return self.port_name

    def get_direction(self) -> str:
        """Get the direction of the pin.

        Returns:
            str: Direction of the pin, can be INPUT, OUTPUT or INOUT.
        """
        
        # Finds all the words that is preceded by "DIRECTION "
        direction = re.search('(?<=DIRECTION )\w+', self.port_file).group()
        
        return direction

    def get_use(self) -> str:
        """Get the use of the pin.

        Returns:
            str: Use of the pin, can be SIGNAL, GROUND or POWER.
        """
        
        use = re.search('(?<=USE )\w+', self.port_file).group()
        
        return use

    def get_layer(self) -> str:
        """Get the layer associated with the pin.

        Returns:
            str: Layer name.
        """
        
        layer = re.search('(?<=LAYER )\w+', self.port_file).group()
        
        return layer

    def get_polygon(self) -> Tuple[Tuple]:
        """Get the polygon of the port.

        Returns:
            Tuple[Tuple]: Tuple of points.
        """

        polygon = re.search('(?<=RECT )(\d+|\s|\.)*', self.port_file).group()
        polygons = polygon.split(" ")
        polygons.pop()
        
        # Respective coordinates along each axis
        x_coords = (polygons[0], polygons[2])
        y_coords = (polygons[1], polygons[3])
        
        # Nested for loop to parse all the coordinates
        polygon = tuple([(float(x), float(y)) for x in x_coords for y in y_coords])
        
        return polygon

class LefCell:
    """
    Class to describe a lef cell.
    """

    def __init__(self, cell_name: str, cell_file: str) -> None:
        self.cell_name = cell_name
        self.cell_file = cell_file

    def get_name(self) -> str:
        """Get the name of the cell.

        Returns:
            str: Name of the cell.
        """
        return self.cell_name

    def get_size(self) -> Tuple[Tuple]:
        """Get the bounding box of the cell.

        Returns:
            Tuple[Tuple]: Tuple of points representing the bounding box.
        """
        
        size = re.findall('(?<=BY )\d+|\d+(?= BY)', self.cell_file)
        
        # Respective coordinates along each axis
        x_coords = 0, size[1]
        y_coords = 0, size[0]
        
        bounding_box = tuple([(float(x), float(y)) for x in x_coords for y in y_coords])
        
        return bounding_box

    def get_ports(self) -> Iterable[LefPort]:
        """Get the ports in the cell.

        Returns:
            Iterable[LefPort]: Iterable of LefPort in the cell.
        """
        
        ports_name = re.findall('(?<=PIN )\w+', self.cell_file)
        list_ports = []
        
        for port_name in ports_name:
            lef_port_code = re.search('(PIN ' + port_name + ')(.|\n)*(END ' + port_name + ')', self.cell_file).group()
            list_ports.append(LefPort(port_name, lef_port_code))
        
        return list_ports


class LefParser:
    """
    Your lef parser to implement.
    """

    def __init__(self, lef_file: str) -> None:
        self.lef_file = lef_file

    def get_cells(self) -> Iterable[LefCell]:
        """Get cells in the lef.

        Returns:
            Iterable[LefCell]: Iterable of LefCell in the lef file.
        """
        
        cells_name = re.findall('(?<=MACRO )\w+', self.lef_file)
        list_cells = []

        for cell_name in cells_name:
            lef_cell_code = re.search('(MACRO ' + cell_name + ')(.|\n)*(END MACRO)', self.cell_file).group()
            list_cells.append(LefPort(cell_name, lef_cell_code))