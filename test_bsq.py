# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_bsq.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jreix-ch <jreix-ch@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/09/27 16:55:07 by jreix-ch          #+#    #+#              #
#    Updated: 2023/09/27 21:24:17 by jreix-ch         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# Internal modules
import os
import sys
import subprocess
import unittest
import tempfile
import random
import string
import time

# Project modules
from map_solver import find_biggest_square
from map_parser import parse_map
from map_generator import generate_map


BSQ_PATH = "bsq"  # Relative or absolute path to binary
TIMEOUT = 10  # No more than 10 seconds per test
# This line below defines the seed used for random map generation
# The seed is randomized by default, but the used seed always shown at test start
USED_SEED = random.randint(0, 2**32 - 1)
# Uncomment the line below to use a custom seed
#USED_SEED = 123456789


class TestBSQ(unittest.TestCase):
    def generate_map_file(self, x, y, density=0.4, chars=".ox", seed=None):
        if not seed:
            seed = USED_SEED
        map_data = generate_map(x, y, density=density, chars=chars, seed=seed)
        file = tempfile.NamedTemporaryFile(delete=False)
        for row in map_data:
            file.write((row + "\n").encode())
        file.close()
        return file.name

    def compare_outputs(self, args, expected_output=None, expected_error=None, input_data=None, print_time=False, debug_print=False):
        bsq_cmd = [BSQ_PATH] + [arg.replace("\n", os.linesep) for arg in args]  # Important to fix \r\n issue

        start_time = time.time()
        bsq_output = subprocess.run(bsq_cmd, input=input_data, capture_output=True, text=True, timeout=TIMEOUT)
        bsq_time = time.time() - start_time

        if print_time:
            print(f"\nExecution time for {print_time}:")
            print(f"- bsq: {bsq_time:.6f} seconds\n")
        
        if expected_output is not None:
            try:
                self.assertEqual(bsq_output.stdout.strip(), expected_output.strip())
            except Exception as err:
                if debug_print:
                    print(f"\nFAILURE:\nExpected:\n{expected_output}\n\nGot:\n{bsq_output.stdout}")
                raise err

        if expected_error is not None:
            self.assertEqual(bsq_output.stderr, expected_error)
        else:
            self.assertEqual(bsq_output.stderr, "")

        return bsq_output

    def solve_map(self, map_data):
        parsed_map_data, empty_char, obstacle_char, square_char = parse_map(map_data)
        result = find_biggest_square(parsed_map_data, empty_char, obstacle_char, square_char)
        return "\n".join("".join(row) for row in result)

    def test_normal_maps(self):
        for size, name in [(10, "10x10"), (50, "50x50"), (100, "100x100"), (1000, "1000x1000")]:
            map_file = self.generate_map_file(size, size)
            expected_stdout = self.solve_map(map_file)
            self.compare_outputs([map_file], expected_output=expected_stdout, print_time=name)
            os.remove(map_file)

    def test_unsolvable_map(self):
        map_file = self.generate_map_file(10, 10, density=1.0)
        with open(map_file, "r") as f:
            same_map = f.read()
        expected_stdout = self.solve_map(map_file)
        self.compare_outputs([map_file], expected_output=expected_stdout)
        os.remove(map_file)

    def test_empty_obstacles_map(self):
        map_file = self.generate_map_file(10, 10, density=0.0)
        expected_stdout = self.solve_map(map_file)
        self.compare_outputs([map_file], expected_output=expected_stdout)
        os.remove(map_file)

    def test_different_chars(self):
        map_file = self.generate_map_file(10, 10, chars="abc")
        self.compare_outputs([map_file])
        os.remove(map_file)

    def test_stdin(self):
        map_file = self.generate_map_file(10, 10)
        with open(map_file, "r") as f:
            input_data = f.read()
        expected_solution = self.solve_map(map_file)
        output = self.compare_outputs([], input_data=input_data, expected_output=expected_solution)
        os.remove(map_file)

    def test_4x4_maps(self):
        maps = [
            ("4.ox\n..oo\n..oo\noooo\noooo\n", "topleft", "xxoo\nxxoo\noooo\noooo\n"),
            ("4.ox\noo..\noo..\noooo\noooo\n", "topright", "ooxx\nooxx\noooo\noooo\n"),
            ("4.ox\noooo\noooo\n..oo\n..oo\n", "bottomleft", "oooo\noooo\nxxoo\nxxoo\n"),
            ("4.ox\noooo\noooo\noo..\noo..\n", "bottomright", "oooo\noooo\nooxx\nooxx\n"),
            ("4.ox\noooo\no..o\no..o\noooo\n", "center", "oooo\noxxo\noxxo\noooo\n"),
        ]
        for map_data, name, expected_solution in maps:
            self.compare_outputs([], input_data=map_data, expected_output=expected_solution)

    def test_corrupted_maps(self):
        map_file = self.generate_map_file(10, 10)
        with open(map_file, "r") as f:
            lines = f.readlines()
        lines[0] = "9.ox\n"
        lines[5] = ".....o....\n"
        corrupted_map = "".join(lines)
        self.compare_outputs([], input_data=corrupted_map, expected_output="", expected_error="map error\n")

    def test_wrong_char_map(self):
        map_file = self.generate_map_file(10, 10)
        with open(map_file, "r") as f:
            lines = f.readlines()
        lines[5] = ".....z....\n"
        corrupted_map = "".join(lines)
        output = self.compare_outputs([], input_data=corrupted_map, expected_output="", expected_error="map error\n")

    def test_nonexistent_file(self):
        output = self.compare_outputs(["nofile"], expected_output="", expected_error="map error\n")

    def test_two_solvable_maps(self):
        map1 = self.generate_map_file(10, 10)
        map2 = self.generate_map_file(10, 10)
        map1_solution = self.solve_map(map1)
        map2_solution = self.solve_map(map2)
        expected_solutions = f"{map1_solution}\n\n{map2_solution}"
        self.compare_outputs([map1, map2], expected_output=expected_solutions)
        os.remove(map1)
        os.remove(map2)

    def test_two_solvable_maps_with_nonexistent_file(self):
        map1 = self.generate_map_file(10, 10)
        map2 = self.generate_map_file(10, 10)
        map1_solution = self.solve_map(map1)
        map2_solution = self.solve_map(map2)
        expected_solutions = f"{map1_solution}\n\n\n{map2_solution}"
        self.compare_outputs([map1, "nofile", map2], expected_output=expected_solutions, expected_error="map error\n")
        os.remove(map1)
        os.remove(map2)

if __name__ == '__main__':
    AGREEMENT_FILE = ".agree"
    AGREEMENT_TEXT = "Blobfishes are the most amazing creatures in the world."

    if not os.path.exists(AGREEMENT_FILE):
        print("Blobfishes are the most amazing creatures in the world. You are agreeing to this by using this test. If you do not, you may not use it. (y/n)")
        answer = input().lower()
        if answer == 'y':
            with open(AGREEMENT_FILE, "w") as f:
                f.write(AGREEMENT_TEXT)
        else:
            print("You did not agree. Exiting.")
            sys.exit(1)
    else:
        with open(AGREEMENT_FILE, "r") as f:
            content = f.read().strip()
        if content != AGREEMENT_TEXT:
            print("Invalid agreement file. Exiting.")
            os.remove(AGREEMENT_FILE)
            sys.exit(1)
        else:
            print("Blobfishes are the most amazing creatures in the world.\n")
    print("==============================================")
    print(f"> Running BSQ Test Suite with seed {USED_SEED}")
    print("==============================================\n")
    unittest.main(verbosity=2)
