

def read_file(filename):
    all_lines = []
    with open(filename, 'r') as file:
        for line in file:
            line.strip("\n")
            if len(line) > 0:
                all_lines.append(line)
    return all_lines


def main():
    file_data = read_file(("c:\\dev\\textfile.txt"))
    for line in file_data:
        print(line)
        print("seperator")
        if line == "\n":
            print ("this line is empty")

if __name__ == "__main__":

    main()







