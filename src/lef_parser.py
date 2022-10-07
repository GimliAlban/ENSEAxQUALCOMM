"""
Lef Parser class.
"""
import re

from typing import Iterable, Tuple


class LefPort:
    """
    Class to describe a lef port.
    """

    def __init__(self, port_name: str, port_content: str) -> None:
        self.port_name = port_name

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

    def get_use(self) -> str:
        """Get the use of the pin.

        Returns:
            str: Use of the pin, can be SIGNAL, GROUND or POWER.
        """

    def get_layer(self) -> str:
        """Get the layer associated with the pin.

        Returns:
            str: Layer name.
        """

    def get_polygon(self) -> Tuple[Tuple]:
        """Get the polygon of the port.

        Returns:
            Tuple[Tuple]: Tuple of points.
        """


class LefCell:
    """
    Class to describe a lef cell.
    """

    def __init__(self, cell_name: str, cell_content: str) -> None:
        self.cell_name = cell_name
        regex = re.compile(r"SIZE (\d*) BY (\d*)")
        for match in re.finditer(regex, cell_content):
            self.size = (match.group(1), match.group(2))
        self.ports = []
        regex = re.compile(r"PIN (\w*)\n([\w\s;.]*)END \1")
        for match in re.finditer(regex, cell_content):
            self.ports.append(LefCell(match.group(1), match.group(2)))

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
        return self.size

    def get_ports(self) -> Iterable[LefPort]:
        """Get the ports in the cell.

        Returns:
            Iterable[LefPort]: Iterable of LefPort in the cell.
        """
        return self.ports


class LefParser:
    """
    Your lef parser to implement.
    """

    def __init__(self, lef_file: str) -> None:
        lef_file = open(lef_file)
        regex = re.compile(r"MACRO (\w*)\n([\w\s;.]*)END MACRO")
        self.cells = []
        for match in re.finditer(regex, lef_file.read()):
            self.cells.append(LefCell(match.group(1), match.group(2)))

    def get_cells(self) -> Iterable[LefCell]:
        """Get cells in the lef.

        Returns:
            Iterable[LefCell]: Iterable of LefCell in the lef file.
        """
        return self.cells
