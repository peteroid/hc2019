from collections import defaultdict
import sys


class Question(object):
    def __init__(self):
        self._photo_idx = 0
        self.photo_orientation = []
        self.photo_tag = []
        self.tag_dictionary = defaultdict(set)
        self.orientation_dictionary = defaultdict(set)
        self.used_photo = set()

    def add_photo(self, orientation, tags):
        self.photo_orientation.append(orientation)
        self.photo_tag.append(tags)

        self.orientation_dictionary[orientation].add(self._photo_idx)

        for tag in tags:
            self.tag_dictionary[tag].add(self._photo_idx)

        self._photo_idx += 1

    def debug_print(self):
        print("No. of photos: {}".format(len(self.photo_orientation)))
        print("Photo Orientation: {}".format(self.photo_orientation))
        print("Photo Tags: {}".format(self.photo_tag))
        print("Orientation Dictionary: {}".format(self.orientation_dictionary))
        print("Tag Dictionary: {}".format(self.tag_dictionary))


def read_input_file(input_file):
    question = Question()
    with open(input_file) as f:
        no_of_photos_str = f.readline()
        no_of_photos = int(no_of_photos_str)
        for i in range(0, no_of_photos):
            input_line = f.readline()
            input_line = input_line.replace('\n', '')
            orientation, no_of_tag, tags_str = input_line.split(' ', 2)
            tags = tags_str.split(' ')
            question.add_photo(orientation, tags)
    return question


def write_output_file(output_file, pizza_question):
    with open(output_file, 'w') as f:
        f.write("{}\n".format(len(pizza_question.known_segment)))


def main(input_file, output_file):
    question = read_input_file(input_file)
    question.debug_print()
    # write_output_file(output_file)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: {} <input file> <output file>".format(sys.argv[0]))
        exit(-1)\

    main(sys.argv[1], sys.argv[2])