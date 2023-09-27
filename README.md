# BSQ Test Unit

This is a simple automated BSQ test unit for 42 piscine. This test suite contains three main files: `map_generator.py`, `map_solver.py`, and `test_bsq.py`. You can run each of these files separately, excluding the `map_parser.py` file, which is a helper module.

## Disclaimer

Please note that the tests provided in this test suite may not be entirely accurate, as the author cannot guarantee that they align with the expectations of the moulinette. The tests are based on the author's understanding and are intended to help others. The author takes no responsibility for any discrepancies or issues that may arise from using these tests.

You are encouraged to contribute and add your own tests to improve the test suite. If you have any ideas or suggestions, feel free to reach out to the author on Discord: julesreixcharat.

## Overview and Usage

### map\_generator.py

`map_generator.py` is a script that generates a random map based on the given parameters. It can be used to create test cases for the BSQ solver.

To run the `map_generator.py` file, use the following command:

```
python3 map_generator.py <x> <y> [-d <density>] [-s <seed>] [-o <output>]
```

Arguments:

- `<x>`: Width of the map
- `<y>`: Height of the map
- `<density>`: Density of the map (default: 0.4)
- `<seed>`: Random seed
- `<output>`: Output file name

### map\_solver.py

`map_solver.py` is a script that solves the generated map and finds the biggest square. It can be used to test the efficiency and correctness of the BSQ solver.

To run the `map_solver.py` file, use the following command:

```
python3 map_solver.py <x> <y> [-d <density>] [-s <seed>] [-p <process>]
```

Arguments:

- `<x>`: Width of the map
- `<y>`: Height of the map
- `<density>`: Density of the map (default: 0.4)
- `<seed>`: Random seed
- `<process>`: Solved map file name

### test\_bsq.py

`test_bsq.py` is a test suite that runs various test cases on the BSQ solver. It uses the `map_generator.py` and `map_solver.py` scripts to create test cases and compare the results with the expected output.

Before running `test_bsq.py`, make sure to set the relative or absolute path to the `./bsq` binary in the `BSQ_PATH` variable at the beginning of the file.

To run the `test_bsq.py` file, use the following command:

```
python3 test_bsq.py
```

This will run the test suite and display the results.

