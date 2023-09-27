# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    map_solver.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jreix-ch <jreix-ch@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/09/27 17:48:24 by jreix-ch          #+#    #+#              #
#    Updated: 2023/09/27 18:02:18 by jreix-ch         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# Internal modules
import argparse
import random

# Project modules
from map_generator import generate_map
from map_parser import parse_map
from pprint import pprint

def find_biggest_square(map_data, empty_char, obstacle_char, square_char):
    rows = len(map_data)
    cols = len(map_data[0])
    
    # 2D array of biggest square ending for each cell (allowing fast process of the biggest square)
    dp = [[0] * cols for _ in range(rows)]

    # Fill it with zeros
    for i in range(rows):
        dp[i][0] = 1 if map_data[i][0] == empty_char else 0
    for j in range(cols):
        dp[0][j] = 1 if map_data[0][j] == empty_char else 0

    max_size = 0
    max_i = 0
    max_j = 0

    # Basically the same algorithm but in a few lines because it's Python :)
    for i in range(1, rows):
        for j in range(1, cols):
            if map_data[i][j] == empty_char:
                dp[i][j] = min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1]) + 1
                if dp[i][j] > max_size:
                    max_size = dp[i][j]
                    max_i = i
                    max_j = j

    # Fill square characters
    for i in range(max_i, max_i - max_size, -1):
        for j in range(max_j, max_j - max_size, -1):
            map_data[i][j] = square_char

    # Happy blobby now
    return map_data


def main():
    parser = argparse.ArgumentParser(description="Map generator and solver")
    parser.add_argument("x", type=int, help="Width of the map")
    parser.add_argument("y", type=int, help="Height of the map")
    parser.add_argument("-d", "--density", type=float, default=0.4, help="Density of the map (default: 0.4)")
    parser.add_argument("-s", "--seed", type=int, default=None, help="Random seed")
    parser.add_argument("-p", "--process", type=str, help="Solved map file name")

    args = parser.parse_args()

    if args.seed is None:
        args.seed = random.randint(0, 2**32 - 1)

    map_data = generate_map(args.x, args.y, density=args.density, seed=args.seed)

    print(f"[Map of {args.x} * {args.y} - Density of {args.density}; Random seed is {args.seed}]")
    for row in map_data:
        print(row)

    if args.process:
        map_file = args.process + ".map"
        solution_file = args.process + "_solution.map"

        with open(map_file, "w") as f:
            f.write(f"{args.y}{map_data[0][-3]}{map_data[0][-2]}{map_data[0][-1]}\n")
            for row in map_data[1:]:
                f.write("".join(row) + "\n")

        parsed_map_data, empty_char, obstacle_char, square_char = parse_map(map_file)
        result = find_biggest_square(parsed_map_data, empty_char, obstacle_char, square_char)

        with open(solution_file, "w") as f:
            print(f"{args.y}{map_data[0][-3]}{map_data[0][-2]}{map_data[0][-1]}")
            f.write(f"{args.y}{map_data[0][-3]}{map_data[0][-2]}{map_data[0][-1]}\n")
            for row in result:
                print("".join(row))
                f.write("".join(row) + "\n")

        print(f"Map saved to {map_file}")
        print(f"Solution map saved to {solution_file}")


if __name__ == "__main__":
    main()
