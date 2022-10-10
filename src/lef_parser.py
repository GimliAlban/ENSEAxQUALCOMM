"""
Lef Parser class.
"""

import re
import codecs

from typing import Iterable, Tuple


class LefPort:
    """
    Class to describe a lef port.
    """

    def __init__(self, port_name: str, direction: str, use: str, layer: str, polygon: str) -> None:
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

    def __init__(self, cell_name: str, size: Tuple[Tuple], ports: Iterable[LefPort]) -> None:
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
        self.lef_file = lef_file
        self.lef_text = codecs.open(self.lef_file).read()

    def get_cells(self) -> Iterable[LefCell]:
        """Get cells in the lef.

        Returns:
            Iterable[LefCell]: Iterable of LefCell in the lef file.
        """
        listCells = []
        listNameCells = re.compile('MACRO (cell\w*)').findall(self.lef_text)

        for nameCell in listNameCells:
            sizeMatch = re.compile(nameCell+'\n.SIZE (\w*?) BY (\w*?) ;').search(self.lef_text)
            size = ((0.0,0.0),(0.0,float(sizeMatch.group(2))), (float(sizeMatch.group(1)), float(sizeMatch.group(2))), (float(sizeMatch.group(1)),0.0))pytes
            
            cellText = re.compile('(?<='+nameCell+')(.|\n)*?(?=END MACRO)').search(self.lef_text)
            listNamePorts = re.compile('PIN (\w*)').findall(cellText.group(0))
            
            listPorts=[]

            for namePort in listNamePorts:
                direction = re.compile(namePort + '\n.*?DIRECTION (\w*)').search(cellText.group(0)).group(1)
                use = re.compile(namePort+'\n.*?'+direction+'.*?\n.*?USE (\w*)').search(cellText.group(0)).group(1)
                layer = re.compile(namePort+'\n.*?'+direction+'.*?\n.*?'+use+'.*?\n.*\n.*?LAYER (\w*)').search(cellText.group(0)).group(1)
                polygonMatch = re.compile(namePort+'\n.*?'+direction+'.*?\n.*?'+use+'.*?\n.*\n.*?'+layer+'.*?\n.*?RECT ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*)').search(cellText.group(0))
                polygon=(polygonMatch.group(1),polygonMatch.group(2),polygonMatch.group(3),polygonMatch.group(4))
                
                listPorts.append(LefPort(namePort,direction,use,layer,polygon))
            
            listCells.append(LefCell(nameCell,size,listPorts))
        
        return listCells

a = LefParser("lef_files/3_cells_1000_pins.lef")
print(a.get_cells()[0].get_size())
