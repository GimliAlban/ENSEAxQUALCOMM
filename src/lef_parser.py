"""
Lef Parser class.
"""


from typing import Iterable, Tuple
import re


class LefPort:
    """
    Class to describe a lef port.
    """

    def __init__(self, port_name: str, direction: str, use: str, layer: str, polygon: Tuple) -> None:
        self.port_name = port_name
        self.direction = direction
        self.use = use
        self.layer = layer
        self.polygon = polygon

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
        return self.direction

    def get_use(self) -> str:
        """Get the use of the pin.

        Returns:
            str: Use of the pin, can be SIGNAL, GROUND or POWER.
        """
        return self.use

    def get_layer(self) -> str:
        """Get the layer associated with the pin.

        Returns:
            str: Layer name.
        """
        return self.layer

    def get_polygon(self) -> Tuple[Tuple]:
        """Get the polygon of the port.

        Returns:
            Tuple[Tuple]: Tuple of points.
        """
        return self.polygon

class LefCell:
    """
    Class to describe a lef cell.
    """

    def __init__(self, cell_name: str, size: Tuple, ports: Iterable) -> None:
        self.cell_name = cell_name
        self.size = size
        self.ports = ports

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
        self.lef_file = f'./lef_files/{lef_file}'
        self.cells = self.parse()


    def parse(self):

        with open(self.lef_file) as file:
            lef = file.read()

        # Regex to get file infos 
        cells = re.findall(r"(?<=\bMACRO ).*", lef)
        sizes = re.findall(r'(?<=\bSIZE )(.*?)\s.*(?<=\bBY )(.*?)\s', lef)

        pins = re.findall(r'(?<=\bPIN ).*', lef)
        directions = re.findall(r'(?<=\bDIRECTION ).+?(?= ;)', lef)
        uses = re.findall(r'(?<=\bUSE ).+?(?= ;)', lef)
        layers = re.findall(r'(?<=\bLAYER ).+?(?= ;)', lef)
        polygons = re.findall(r'(?<=\bRECT ).+?(?= ;)', lef)

        # Build squares with length and height
        sizes = [((0.0, 0.0), (0.0, float(a[0])), (float(a[0]), float(a[1])), (float(a[1]), 0.0)) for a in sizes]

        # Check for cell divisions
        portsDiv = [i for i, x in enumerate(pins) if x == pins[0]]
        portsDiv = portsDiv[1:]
        portsDiv.append(len(pins))

        j = 0
        cellPorts = []
        ports = []

        # Create list of ports for each cell
        for i, pin in enumerate(pins):
            polygon = tuple([float(y) for y in polygons[i].split(" ")])
            ports.append(LefPort(pin, directions[i], uses[i], layers[i], polygon))

            if(i == portsDiv[j] - 1):
                cellPorts.append(ports)
                ports = []
                j += 1
        

        ret = []

        # Instantiate each cell
        for i, cellName in enumerate(cells):
            ret.append(LefCell(cellName.strip(), sizes[i], cellPorts[i]))

        return ret


    def get_cells(self) -> Iterable[LefCell]:
        """Get cells in the lef.

        Returns:
            Iterable[LefCell]: Iterable of LefCell in the lef file.
        """
        return self.cells