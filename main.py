from Formatter import Formatter
from ID3Parser import ID3Parser


def main(name_file: str):
    with open(name_file, 'rb') as file:
        info = ID3Parser.parse(file)
        formatter = Formatter(Formatter.Mode.Table)
        formatter.pretty_print(info, 1, name_file)


if __name__ == '__main__':
    filename = input("Enter file name: ")
    main(filename)
