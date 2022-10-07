"""
Lef Parser class.
"""


from typing import Iterable, Tuple
import re

class LefPort:
    """
    Class to describe a lef port.
    """

    def __init__(self, port_data: str) -> None:
        self.port_data = port_data

    def get_name(self) -> str:
        """Get the name of the port.

        Returns:
            str: Name of the port.
        """
        name = re.findall(r"PIN\s+([^\n]+)",self.port_data)
        if len(name)>0 : return name[0]
        else: return ""

    def get_direction(self) -> str:
        """Get the direction of the pin.

        Returns:
            str: Direction of the pin, can be INPUT, OUTPUT or INOUT.
        """
        direction = re.findall(r"DIRECTION\s+(INPUT|OUTPUT|INOUT)",self.port_data)
        if len(direction)>0 : return direction[0]
        else: return ""

    def get_use(self) -> str:
        """Get the use of the pin.

        Returns:
            str: Use of the pin, can be SIGNAL, GROUND or POWER.
        """
        use = re.findall(r"USE\s+(GROUND|POWER|SIGNAL)",self.port_data)
        if len(use)>0 : return use[0]
        else: return ""

    def get_layer(self) -> str:
        """Get the layer associated with the pin.

        Returns:
            str: Layer name.
        """
        layer = re.findall(r"LAYER\s+([^\s;]+)",self.port_data)
        if len(layer)>0 : return layer[0]
        else: return ""


    def get_polygon(self) -> Tuple[Tuple]:
        """Get the polygon of the port.

        Returns:
            Tuple[Tuple]: Tuple of points.
        """
        poly = re.findall(r"RECT\s+(?P<i>[\d.]+)\s+(?P<j>[\d.]+)\s+(?P<k>[\d.]+)\s+(?P<l>[\d.]+)",self.port_data)
        if len(poly)!=4 : return (0,0,0,0)
        else: return (poly["i"],poly["j"],poly["k"],poly["l"])


class LefCell:
    """
    Class to describe a lef cell.
    """

    def __init__(self, cell_inp: str) -> None:
        self.cell_data = re.search(r"MACRO\s+(?P<name>[^\n]+)\n\s*?SIZE\s*?(?P<size1>\d+)\s*?BY\s*?(?P<size2>\d+)[^;];\n(?P<data>(?:.|\n)*?)\nEND\s+MACRO", cell_inp)
        self.cell_name = self.cell_data["name"] if self.cell_data["name"] is not None else ""
        self.cell_size = (int(self.cell_data["size1"]), int(self.cell_data["size2"])) if self.cell_data["size1"] != None and self.cell_data["size2"] != None else (0,0)
        self.pins_names = re.findall(r"PIN\s+([^\n]+)", self.cell_data["data"]) if self.cell_data["data"] != None else []
        self.pins_data = []
        for k in self.pins_names:
            mydata=re.findall(rf"(PIN\s+{k}(?:\s|\n)(?:.|\n)*?END\s+{k})", self.cell_data["data"])
            #if len(mydata) != 1:
            #    print(mydata[:10])
            self.pins_data+=mydata
        self.cell_ports = [LefPort(k) for k in self.pins_data]


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
        return self.cell_ports


class LefParser:
    """
    Your lef parser to implement.
    """

    def __init__(self, lef_file_name: str) -> None:
        with open("lef_files/"+lef_file_name, "r") as monFichier:
            self.lef_file = monFichier.read()

    def get_cells(self) -> Iterable[LefCell]:
        """Get cells in the lef.
        
        Returns:
            Iterable[LefCell]: Iterable of LefCell in the lef file.
        """
        cells = re.findall(r"(MACRO(?:.|\n)*?\nEND\s+MACRO)", self.lef_file)
        return [LefCell(k) for k in cells] if cells is not None else []

