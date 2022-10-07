"""
Lef Parser class.
"""


from typing import Iterable, Tuple
import re
import os



class LefPort:
    """
    Class to describe a lef port.
    """

    def __init__(self, port_name: str, port_direction: str, port_use: str, port_layer: str, port_polygon: Tuple[Tuple]) -> None:
        self.port_name = port_name

    def __iter__(self):
        return self

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
        
        return self.port_direction

    def get_use(self) -> str:
        """Get the use of the pin.

        Returns:
            str: Use of the pin, can be SIGNAL, GROUND or POWER.
        """
        
        return self.port_use

    def get_layer(self) -> str:
        """Get the layer associated with the pin.

        Returns:
            str: Layer name.
        """
        return self.port_layer

    def get_polygon(self) -> Tuple[Tuple]:
        """Get the polygon of the port.

        Returns:
            Tuple[Tuple]: Tuple of points.
        """
        return self.port_polygon


class LefCell:
    """
    Class to describe a lef cell.
    """

    def __init__(self, cell_name: str, cell_size: Tuple[Tuple], cell_port: Iterable[LefPort]) -> None:
        self.cell_name = cell_name

    def __iter__(self):
        return self

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
        
        return self.cell_size

    def get_ports(self) -> Iterable[LefPort]:
        """Get the ports in the cell.

        Returns:
            Iterable[LefPort]: Iterable of LefPort in the cell.
        """
        
        return self.cell_port


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
        

        fd = os.open(self.lef_file, os.O_RDONLY)
        #lefp = LefPort()

        regexName = re.compile(r"PIN\s(?P<name>.*\w", fd)
        regexName = regexName.groups()

        regexDirection = re.compile(r"DIRECTION\s(?P<dir>.*\w)", fd)
        regexDirection = regexDirection.groups()

        regexUse = re.compile(r"USE\s(?P<use>.*\w", fd)
        regexUse = regexUse.groups()

        regexLayer = re.compile(r"LAYER\s(?P<layer>.*\w", fd).groups()
        #regexLayer = regexLayer.groups()

        regexPoly = re.compile(r"RECT\s(?P<poly>.*\w", fd) # a traiter pour récup les coordonées en tuple
        regexPoly = regexPoly.groups()
        #polytemp = re.split(r"\w+", regexPoly)
        polyTupletemp = [float(x) for x in regexPoly.split(" ")]
        polyTuple = [[polyTupletemp[0], polyTupletemp[1]], [polyTupletemp[2], polyTupletemp[3]]]



        lefport = LefPort(regexName, regexDirection, regexUse, regexLayer, polyTuple)

        #cellRegex = [line for line in re.compile(r".*", fd).split("END MACRO")] # a corriger si necessaire

        regexCellName = re.compile(r"MACRO\s(?P<poly>.*\w", fd)
        regexCellName = regexCellName.groups()

        regexCellSize = re.compile(r"SIZE\s(?P<height>\d+)\sBY\s(?P<width>\d+)")
        regexCellSizeTuple = [regexCellSize.groups(0), regexCellSize.groups(1)]

        nbPortRegex = re.compile


        









        os.close()

        return 


        
        
        
        

        
        
