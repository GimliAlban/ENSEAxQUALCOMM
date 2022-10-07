"""
Lef Parser class.
"""
import re
from typing import Iterable, Tuple

fileName = input("Quel est le fichier que vous voulez analyser ? ") + ".lef"
f = open(fileName, "r").read()

class LefPort:
    """
    Class to describe a lef port.
    """

    def __init__(self, port_name: str) -> None:
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
        regex = self.name + '\n\s\sDIRECTION\s(.+)\s;'
        return re.findall(regex, f)

    def get_use(self) -> str:
        """Get the use of the pin.

        Returns:
            str: Use of the pin, can be SIGNAL, GROUND or POWER.
        """
        regex = self.name + '\n\s\sDIRECTION\s' + self.get_direction() + '\s;\n\s\sUSE(.+)\s;'
        return re.findall(regex, f)

    def get_layer(self) -> str:
        """Get the layer associated with the pin.

        Returns:
            str: Layer name.
        """
        regex = self.name + '\n\s\sDIRECTION\s(.+)\s' + self.get_direction() + '\n\s\sUSE(.+)\s' + self.get_use() + '\s;\n\s\sPORT\n\s\s\sLAYER\s(.+)\s;'
        return re.findall(regex, f)

    def get_polygon(self) -> Tuple[Tuple]:
        """Get the polygon of the port.

        Returns:
            Tuple[Tuple]: Tuple of points.
        """
        regex = 'RECT\s(.+)\s;\n\s\sEND\sPORT\n\sEND\s' + self.name
        tab = re.findall(regex, f).split(" ")
        return Tuple(tab[0], tab[1], tab[2], tab[3])


class LefCell:
    """
    Class to describe a lef cell.
    """

    def __init__(self, cell_name: str) -> None:
        self.cell_name = cell_name

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
        regex = self.name + '\n\sSIZE\s(.+)\s;'
        tab = re.findall(regex, f).split(" BY ")
        return Tuple(tab[0], tab[1])

    def get_ports(self) -> Iterable[LefPort]:
        """Get the ports in the cell.

        Returns:
            Iterable[LefPort]: Iterable of LefPort in the cell.
        """
        tab = f.split("END MACRO")
        for i in range(len(tab)):
            if re.findall('MACRO\s(.+)', tab[i]) == self.name:
                return Iterable(re.findall('PIN\s(.+)', tab[i]))




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
