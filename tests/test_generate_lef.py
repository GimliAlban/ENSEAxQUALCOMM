"""
Test file for GenerateFile.
"""
import os
import sys
import pytest
from src.generate_lef import GenerateLef, PATH_TO_WRITE_LEF


def test_init_generate_lef() -> None:
    """
    Test if the initialisation of GenerateLef works.
    """
    assert GenerateLef()


def test_empty_lef_is_written() -> None:
    """
    Test if the generated lef is created.
    """
    lef = GenerateLef()
    lef.write_lef('empty.lef')
    assert os.path.exists(f"{PATH_TO_WRITE_LEF}/empty.lef")


def test_add_cell() -> None:
    """
    Test that cell is generated correctly.
    """
    lef = GenerateLef()
    lef.add_cell('cell_1')
    assert lef.lef_content[0] == 'MACRO cell_1'
    assert lef.lef_content[1] == '\tSIZE 100 BY 100 ;'
    assert lef.lef_content[-1] == 'END MACRO'


@pytest.mark.parametrize("pin_index", [0, 1])
def test_add_port(pin_index: int) -> None:
    """
    Test that port is generated correctly.
    """
    lef = GenerateLef()
    pin = lef.add_pin(pin_index=pin_index)
    assert pin[0] == f"\tPIN pin_{pin_index}"
    assert pin[1] in ("\t\tDIRECTION INPUT ;", "\t\tDIRECTION OUTPUT ;", "\t\tDIRECTION INOUT ;")
    assert pin[2] in ("\t\tUSE SIGNAL ;", "\t\tUSE POWER ;", "\t\tUSE GROUND ;")
    assert pin[3] == "\t\tPORT"
    assert pin[4] == "\t\t\tLAYER M1 ;"
    assert pin[5] == "\t\t\tRECT 0 49.5 1 50.5 ;"
    assert pin[-2] == "\t\tEND PORT"
    assert pin[-1] == f"\tEND pin_{pin_index}"


def test_generate_one_cell_one_pin_lef() -> None:
    """
    Test if the lef is generated with the correct cells and ports number.
    One cell with one port should be generated.
    """
    lef = GenerateLef()
    lef.generate_lef()
    assert lef.lef_content[0:3] == [
        "MACRO cell_0",
        "\tSIZE 100 BY 100 ;",
        "\tPIN pin_0",
    ]
    assert lef.lef_content[3] in ("\t\tDIRECTION INPUT ;", "\t\tDIRECTION OUTPUT ;", "\t\tDIRECTION INOUT ;")
    assert lef.lef_content[4] in ("\t\tUSE SIGNAL ;", "\t\tUSE POWER ;", "\t\tUSE GROUND ;")
    assert lef.lef_content[5:] == [
        "\t\tPORT",
        "\t\t\tLAYER M1 ;",
        "\t\t\tRECT 0 49.5 1 50.5 ;",
        "\t\tEND PORT",
        "\tEND pin_0",
        "END MACRO"
    ]
    lef.write_lef('1_cell_1_port.lef')
    assert os.path.exists(f"{PATH_TO_WRITE_LEF}/1_cell_1_port.lef")


def test_generate_3_cell_with_1000_pin() -> None:
    """
    Generate a lef with cells and 1000 pin in each cell and
    assure that the generated file as the right expected
    number of lines.
    We can't do an exat comparison since there is some random
    values attributed when running `generate_lef()`.
    """
    lef = GenerateLef(number_of_cells=3, number_of_ports=1000)
    lef.generate_lef()
    lef.write_lef("3_cells_1000_pins.lef")
    assert os.path.exists(f"{PATH_TO_WRITE_LEF}/3_cells_1000_pins.lef")
    with open(f"{PATH_TO_WRITE_LEF}/golden_3_cells_1000_pins.lef", 'r', encoding="utf-8") as lef_stream:
        assert len(lef_stream.readlines()) == len(lef.lef_content)


@pytest.mark.parametrize("number_of_pin", [1, 4, 8])
def test_generate_1_cell_with_x_pins(number_of_pin: int) -> None:
    """
    Generate a lef with cells and 1000 pin in each cell and
    assure that the generated file as the right expected
    number of lines.
    We can't do an exat comparison since there is some random
    values attributed when running `generate_lef()`.
    """
    lef = GenerateLef(number_of_cells=1, number_of_ports=number_of_pin)
    lef.generate_lef()
    lef.write_lef(f"1_cells_{number_of_pin}_pins.lef")
    assert os.path.exists(f"{PATH_TO_WRITE_LEF}/1_cells_{number_of_pin}_pins.lef")
