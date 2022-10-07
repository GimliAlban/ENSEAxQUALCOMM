"""
Lef Parser class.
"""
import re
from typing import Iterable, Tuple

class LefPort:
    """
    Class to describe a lef port.
    """

    def __init__(self, port_name: str, lef_file: str) -> None:
        self.port_name = port_name
        self.lef_file = lef_file

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
        regex = self.port_name + '\n\s\sDIRECTION\s(.+)\s;'
        return re.findall(regex, self.lef_file)[0]

    def get_use(self) -> str:
        """Get the use of the pin.

        Returns:
            str: Use of the pin, can be SIGNAL, GROUND or POWER.
        """
        regex = 'USE\s(.+)\s;'
        return re.findall(regex, self.lef_file)[0]

    def get_layer(self) -> str:
        """Get the layer associated with the pin.

        Returns:
            str: Layer name.
        """
        regex = 'LAYER\s(.+)\s;'
        return re.findall(regex, self.lef_file)[0]

    def get_polygon(self) -> Tuple[Tuple]:
        """Get the polygon of the port.

        Returns:
            Tuple[Tuple]: Tuple of points.
        """
        regex = 'RECT\s(.+)\s;'
        tab = re.findall(regex, self.lef_file)[0].split(' ')
        return (tab[0], tab[1], tab[2], tab[3])


class LefCell:
    """
    Class to describe a lef cell.
    """

    def __init__(self, cell_name: str, lef_file: str) -> None:
        self.cell_name = cell_name
        self.lef_file = lef_file

    def get_name(self) -> str:
        """Get the name of the cell.

        Returns:
            str: Name of the cell.
        """
        return self.cell_name[0]

    def get_size(self) -> Tuple[Tuple]:
        """Get the bounding box of the cell.

        Returns:
            Tuple[Tuple]: Tuple of points representing the bounding box.
        """
        regex = 'SIZE\s(.+)\s;'
        tab = re.findall(regex, self.lef_file)[0].split(" BY ")
        return (int(tab[0]), int(tab[1]))

    def get_ports(self) -> Iterable[LefPort]:
        """Get the ports in the cell.

        Returns:
            Iterable[LefPort]: Iterable of LefPort in the cell.
        """
        tab = self.lef_file.split("PIN")
        tab = tab[1:]
        for i in range(len(tab)):
            tab[i] = "\n\nPIN" + tab[i]
        return [LefPort(re.findall('PIN\s(.+)', x)[0], x + "") for x in tab]




class LefParser:
    """
    Your lef parser to implement.
    """

    def __init__(self, lef_file: str) -> None:
        with open("lef_files/" + lef_file, 'r') as f:
            self.lef_file = f.read()

    def get_cells(self) -> Iterable[LefCell]:
        """Get cells in the lef.

        Returns:
            Iterable[LefCell]: Iterable of LefCell in the lef file.
        """
        tab = self.lef_file.split("END MACRO")
        return [LefCell(re.findall('MACRO\s(.+)\n', x), x + "") for x in tab[:-1]]
         
file = LefParser("1_cells_8_pins.lef")

print(file)

cells = file.get_cells()
print(cells[0:10])

[print(x.get_name()) for x in cells]
print(cells[0].get_size())

port=cells[0].get_ports()
print(port[1:10])

print(port[0].get_name())
print(port[0].get_direction())
print(port[0].get_use())
print(port[0].get_layer())
print(port[0].get_polygon())