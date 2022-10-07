"""
Lef Parser class.
"""


from typing import Iterable, Tuple

import re


class LefPort:
    """
    Class to describe a lef port.
    """

    def __init__(self, port_name: str, direction: str, use: str, layer: str, polygon: Tuple[Tuple]) -> None:
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

    def __init__(self, cell_name: str, ports: Iterable[LefPort]) -> None:
        self.cell_name = cell_name
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

    def get_cells(self) -> Iterable[LefCell]:
        """Get cells in the lef.

        Returns:
            Iterable[LefCell]: Iterable of LefCell in the lef file.
        """
        with open(self.lef_file) as lef_file:
            lef_data = lef_file.read()

        lefcells = []
        lefports = []
        end = 0

#search = re.search(r'PIN\s(?P<name>(\w|\_)+)\n\s+DIRECTION\s(?P<direction>\w+)\s;\n\s+USE\s(?P<use>\w+)\s;\n\s+PORT\n\s+LAYER\s(?P<layer>\w+)\s;\n\s+RECT\s(?P<rect>[0-9\.\s]+);', lef_data[end:])
        
        while(1):
            search = re.search(r'MACRO\s(?P<name>(\w|\_)+)', lef_data[end:])
            if (search == None):
                break
            cellname = search.group('name')
            end = search.end()

            endmacro = re.search(r'END MACRO', lef_data[end:]).start() + end

            print(endmacro)
  
            i = 0

            while(1):
                
                search = re.search(r'PIN\s(?P<g>(\w|\_)+)', lef_data[end:])
                name = search.group('g')
                end += search.end()


                search = re.search(r'DIRECTION\s(?P<g>(\w|\_)+)', lef_data[end:])
                direction = search.group('g')
                end += search.end()


                search = re.search(r'USE\s(?P<g>(\w|\_)+)', lef_data[end:])
                use = search.group('g')
                end += search.end()

                
                search = re.search(r'LAYER\s(?P<g>(\w|\_)+)', lef_data[end:])
                layer = search.group('g')
                end += search.end()

                
                search = re.search(r'RECT\s(?P<g>[0-9\.\s]+)', lef_data[end:])
                tmp_polygon = search.group('g').split(' ')
                polygon = ((tmp_polygon[0], tmp_polygon[1]),(tmp_polygon[2], tmp_polygon[3]))
                end += search.end()

                end += re.search(r'END\s(\w|\_)+\n', lef_data[end:]).end()
                end += re.search(r'END\s(\w|\_)+\n', lef_data[end:]).end()

                lefports.append(LefPort(name,direction,use,layer,polygon))

                if (end == endmacro):
                    break

        lefcells.append(LefCell(cellname, lefports))





if __name__ == "__main__":
    lefparser = LefParser("lef_files/1_cells_4_pins.lef")

    lefparser.get_cells()
