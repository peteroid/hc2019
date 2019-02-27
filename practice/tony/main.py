import sys
import math


class PizzaQuestion(object):
    def __init__(self, row, column, min_ingredient, max_cell):
        self.row = int(row)
        self.column = int(column)
        self.min_ingredient = int(min_ingredient)
        self.min_cell = self.min_ingredient*2
        self.max_cell = int(max_cell)
        self.pizza = []
        self.pizza_segment = []
        self.known_segment = []
        self.segment_count = 1

    def init_pizza(self, ingredient_str):
        # Init Pizza
        counter = 0
        for r in range(0, self.row):
            row = []
            for c in range(0, self.column):
                row.append(ingredient_str[counter])
                counter += 1
            self.pizza.append(row)

        # Init Pizza Segment
        for r in range(0, self.row):
            self.pizza_segment.append([0]*self.column)

    def print_pizza(self):
        print('PIZZA:')
        for row in self.pizza:
            print(''.join(row))
        print('')

    def print_pizza_segment(self):
        no_digit = len(str(len(self.known_segment)))
        print('PIZZA SEGMENT:')
        for row in self.pizza_segment:
            row_str = ['[{}]'.format(str(num).zfill(no_digit)) for num in row]
            print(''.join(row_str))
        print('')

    @staticmethod
    def get_possible_dimensions(size):
        possible_dimensions = []
        for i in range(1, int(math.sqrt(size))+1):
            if size % i == 0:
                possible_dimensions.append((i, size/i))
                possible_dimensions.append((size/i, i))
        # print('size {}: {}'.format(size, possible_dimensions))
        return possible_dimensions

    def check_pizza_slice(self, x1, y1, x2, y2):
        existing_segment = None
        pizza_ingredient_counter = {'T': 0, 'M': 0}
        min_x = min(x1, x2)
        max_x = max(x1, x2)
        min_y = min(y1, y2)
        max_y = max(y1, y2)
        if max_x >= self.row or max_y >= self.column:
            return False

        for r in range(min_x, max_x+1):
            for c in range(min_y, max_y+1):
                if self.pizza_segment[r][c] != 0:
                    if existing_segment is None:
                        known_segment = self.known_segment[self.pizza_segment[r][c]-1]
                        if min_x <= known_segment[0][0] and min_y <= known_segment[0][1] and \
                            max_x >= known_segment[1][0] and max_y >= known_segment[1][1]:
                                existing_segment = self.pizza_segment[r][c]
                        else:
                            return False
                    elif existing_segment == self.pizza_segment[r][c]:
                        pass
                    else:
                        return False
                pizza_ingredient_counter[self.pizza[r][c]] += 1
        if pizza_ingredient_counter['T'] >= self.min_ingredient and \
               pizza_ingredient_counter['M'] >= self.min_ingredient:
            return existing_segment if existing_segment else True

    def mark_pizza_segment(self, x1, y1, x2, y2, segment_no=True):
        if segment_no is True:
            segment_no = self.segment_count
            self.segment_count += 1
        min_x = min(x1, x2)
        max_x = max(x1, x2)
        min_y = min(y1, y2)
        max_y = max(y1, y2)
        for r in range(min_x, max_x+1):
            for c in range(min_y, max_y+1):
                self.pizza_segment[r][c] = int(segment_no)
        try:
            self.known_segment[int(segment_no) - 1] = ((min_x, min_y), (max_x, max_y))
        except:
            self.known_segment.append(((min_x, min_y), (max_x, max_y)))

    def find_smallest_slice(self):
        for size in range(self.min_cell, self.max_cell+1):
            dimensions = self.get_possible_dimensions(size)
            for dimension in dimensions:
                for x in range(0, self.row):
                    for y in range(0, self.column):
                        x1 = x
                        y1 = y
                        x2 = x+dimension[0]-1
                        y2 = y+dimension[1]-1
                        # print('size {}: ({},{}) ({},{})'.format(size, x1, y1, x2, y2))
                        result = self.check_pizza_slice(x1, y1, x2, y2)
                        if result:
                            self.mark_pizza_segment(x1, y1, x2, y2, result)
                            # self.print_pizza_segment()


def read_input_file(input_file):
    with open(input_file) as f:
        pizza_info = f.readline()
        row, column, min_ingredient, max_cell = pizza_info.split(' ')
        ingredient_str = ''
        for r in range(0, int(row)):
            ingredient_str += f.readline().replace('\n', '')
        pizza_question = PizzaQuestion(row, column, min_ingredient, max_cell)
        pizza_question.init_pizza(ingredient_str)
        return pizza_question


def write_output_file(output_file, pizza_question):
    with open(output_file, 'w') as f:
        f.write("{}\n".format(len(pizza_question.known_segment)))
        for known_segment in pizza_question.known_segment:
            x1 = known_segment[0][0]
            y1 = known_segment[0][1]
            x2 = known_segment[1][0]
            y2 = known_segment[1][1]
            f.write("{} {} {} {}\n".format(x1, y1, x2, y2))


def main(input_file, output_file):
    pizza_question = read_input_file(input_file)

    pizza_question.print_pizza()
    # pizza_question.print_pizza_segment()

    pizza_question.find_smallest_slice()

    write_output_file(output_file, pizza_question)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: {} <input file> <output file>".format(sys.argv[0]))
        exit(-1)\

    main(sys.argv[1], sys.argv[2])