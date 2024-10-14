import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="Apkg generator",
        description="It takes a path to a file with terms in it as argument then search for those terms in the Wiktionary database and creates an apkg file with the data.",
    )
    parser.add_argument("input", help="Ex.: path/to/file_input.txt")
    parser.add_argument(
        "output", nargs="?", default="-", help="Ex.: path/to/file_output.apkg"
    )
    args = parser.parse_args()

    out_name = args.input if args.output == "-" else args.output

    with open(args.input) as input:
        with open(out_name) as output:
            # todo
            ...


if __name__ == "__main__":
    main()
