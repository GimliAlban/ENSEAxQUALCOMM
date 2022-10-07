"""
Test file for LefParser.
"""
import pytest
import os
import re
from src.lef_parser import LefParser
from definition import ROOT_DIR

LEF_FILES = list(map(lambda file: f"{ROOT_DIR}/lef_files/{file}", os.listdir("./lef_files")))


@pytest.mark.parametrize("lef_file", LEF_FILES)
def test_instantiation_is_ok(lef_file: str) -> None:
    """
    Test if the initialisation of the LefParser is ok.

    Args:
        lef_file (str): Path to the lef file.
    """
    lef_parser = LefParser(lef_file)
    assert lef_parser


@pytest.mark.parametrize("lef_file", LEF_FILES)
def test_lef_get_cells(lef_file: str) -> None:
    """
    Verify that all cell are found.
    We get the number of cells in a file from the file name.

    Args:
        lef_file (str): Path of the lef file.
    """
    re_nb_of_cells = re.compile(r"(?P<nb_cells>\d+)_cell(s)*")
    match = re_nb_of_cells.search(lef_file)
    nb_of_cells = match.group("nb_cells") if match else 0
    lef_parser = LefParser(lef_file)
    lef_cells = lef_parser.get_cells()  # this is flag as an error because get_cells is not implemented
    assert len(lef_cells) == nb_of_cells
    assert {cell.get_name() for cell in lef_cells} == {f"cell_{i}" for i in range(nb_of_cells)}
    for cell in lef_cells:
        assert cell.get_name()
        assert cell.get_size() == ((0.0, 0.0), (0.0, 100.0), (100.0, 100.0), (100.0, 0.0))


@pytest.mark.parametrize("lef_file", LEF_FILES)
def test_lef_get_ports(lef_file: str) -> None:
    """
    Verify that all ports are correctly find in the cells.

    Args:
        lef_file (str): Path of the lef file.
    """
    re_nb_of_pins = re.compile(r"(?P<nb_pins>\d+)_(port|pin)(s)*")
    match = re_nb_of_pins.search(lef_file)
    nb_of_ports = match.group("nb_pins") if match else 0
    lef_parser = LefParser(lef_file)
    lef_cells = lef_parser.get_cells() or []
    assert len(lef_cells) > 0
    for cell in lef_cells:
        lef_ports = cell.get_ports()
        assert len(lef_ports) == nb_of_ports
        assert {port.get_name() for port in lef_ports} == {f"pin_{i}" for i in range(nb_of_ports)}
        for port in lef_ports:
            assert port.get_name()
            assert port.get_use() in ("SIGNAL", "POWER", "GROUND")
            assert port.get_direction() in ("INPUT", "OUTPUT", "INOUT")
            assert port.get_layer() == 'M1'
            assert len(port.get_polygon()) == 4
