# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    map_parser.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jreix-ch <jreix-ch@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/09/27 17:16:12 by jreix-ch          #+#    #+#              #
#    Updated: 2023/09/27 17:46:20 by jreix-ch         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def parse_map(map_file):
    with open(map_file, "r") as f:
        header = f.readline().strip()
        square_char = header[-1]
        obstacle_char = header[-2]
        empty_char = header[-3]
        num_lines = int(header[:-3])

        map_data = []
        for _ in range(num_lines):
            line = f.readline().strip()
            map_data.append(list(line))

    return map_data, empty_char, obstacle_char, square_char
