# Authors

[Raphael Pichon](https://ie.linkedin.com/in/raphael-pichon-raphael) and [Alban Pieprzyk](https://ie.linkedin.com/in/alban-pieprzyk)

# Goal of the project

1. Generate and parse multiple lef files.
   The generation of the lef files is already handle.
   You will need to create your own `LefParser` class in the file `./src/lef_parser.py`.
   Read the docstrings in `./src/lef_parser.py` to understand what each methods are for.
   We ask you to use regular expression (since a lesson will be given on it). You are
   free to use whatever you want if you don't want to go with regular expression but
   no help will be given in that case.
2. Connect multiple cells between each of them.
   #TODO: Raph to fill this part with directive.

# Setup Project

1. Run `git clone <github_repository>`.
2. Download and Install python v3.10.7 `https://www.python.org/downloads/` if it's not already done.
3. Run `python3 -m venv ensea_venv`. It will create a virtual environment for the project.
   - If on Windows, run `.\ensea_venv\Scripts\activate` & `pip3 install -r requirements.txt`.
   - If on Linux, run `source ./ensea_venv/bin/activate.csh` & `pip3 install -r requirements.txt`.
4. Run `pytest ./tests/test_generate_lef.py` (you should be in the terminal of your virtual environment, ie you should see `(ensea_venv)` at the begining of your line in the terminal), this will generate the lef files you need and run the tests for it, to make sure everything is ok.
5. Run `pytest` in the terminal and it should run all the test available in the project. You should have 14 test failing and 20 test passing.
6. Create a branch for your work: `git checkout -b <your_group_names>`.
7. At this points you can start to complete the `lef_parser.py` file.
   - Your goal is to have the tests that fail passing by completing the `lef_parser.py` file.
   - !! Do not modify the tests. !!

# LEF file

LEF (Library Exchange Format) files describe an abstract view of a design.
The LEF files generated in this project are very basic one.
The first statement use is `MACRO cell_name`, it's a block where we are
defining our top design. It is usualy a square and inside that square
we will define our pins. The size of this sqaure is define by `SIZE 100 BY 100`,
which mean that our cell is a 100 by 100 square, we don't care about unit here.
Then we define a pin like so `PIN pin_name`. Note that, this statement is a block
statement at it as to be close by `END pin_name`. Same for `MACRO`, it has to
be close by `END cell_name`. In the pin block, we are defining multiple statement,
the direction (`DIRECTION INPUT|OUTPUT|INOUT`), the use (`USE SIGNAL|POWER|GROUND`)
and his position which is define by a small square (in comparison of the cell size)
which is placed on the sides of the cell.
Imagine a microprocessor, it is a square, with pins all around it. The pins are
small in comparison with the microprocessor. This is exactly what we have here.
