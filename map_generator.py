# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    map_generator.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jreix-ch <jreix-ch@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/09/26 21:02:44 by jreix-ch          #+#    #+#              #
#    Updated: 2023/09/27 18:02:54 by jreix-ch         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# Internal modules
import sys
import random
import argparse


def generate_map(x, y, density = 0.4, chars = ".ox", seed = random.randint(0, 2**32 - 1)):
    random.seed(seed)
    map_data = [f"{y}{chars[0]}{chars[1]}{chars[2]}"]
    for i in range(y):
        row = []
        for j in range(x):
            if random.random() < density:
                row.append(chars[1])
            else:
                row.append(chars[0])
        map_data.append("".join(row))
    return map_data

def main():
    parser = argparse.ArgumentParser(description="Map generator and solver")
    parser.add_argument("x", type=int, help="Width of the map")
    parser.add_argument("y", type=int, help="Height of the map")
    parser.add_argument("-d", "--density", type=float, default=0.4, help="Density of the map (default: 0.4)")
    parser.add_argument("-s", "--seed", type=int, default=None, help="Random seed")
    parser.add_argument("-o", "--output", type=str, help="Output file name")

    args = parser.parse_args()

    if args.seed is None:
        args.seed = random.randint(0, 2**32 - 1)

    map_data = generate_map(args.x, args.y, density=args.density, seed=args.seed)

    print(f"[Map of {args.x} * {args.y} - Density of {args.density}; Random seed is {args.seed}]")
    for row in map_data:
        print(row)

    if args.output:
        with open(args.output, "w") as f:
            for row in map_data:
                f.write(row + "\n")


if __name__ == "__main__":
    main()

