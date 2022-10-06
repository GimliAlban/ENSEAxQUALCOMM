"""
Lef Parser class.
"""


from typing import Iterable, Tuple


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

    def get_ports(self) -> Iterable[LefPort]:
        """Get the ports in the cell.

        Returns:
            Iterable[LefPort]: Iterable of LefPort in the cell.
        """


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
