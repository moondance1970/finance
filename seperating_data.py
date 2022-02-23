import getData as gD

amir = gD.main("--companies_file \"companies - short.csv\"")
print(amir)

"""
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--companies_file', type=str,
                        help="the companies you want to download info for", required=True)
    parser.add_argument("--fetchmode", type=str2bool, nargs='?', const=True, default=False,
                        help="fetch data / analyze data")

    return parser.parse_args()



def main():
    args = parse_arguments()


if __name__ == "__main__":
    main()
"""