import argparse

from dictionaries.wiktionary import wiktionary2anki


def main():
    parser = argparse.ArgumentParser(
        prog="APKG Generator",
        description="It takes a path to a file with terms in it as argument then search for those terms in a database like Wiktionary or Cambridge, and creates an APKG file with the data.",
    )
    parser.add_argument("input", help="Ex.: path/to/file_input.txt")
    parser.add_argument(
        "output",
        nargs="?",
        default="-",
        help="Ex.: path/to/file_output.apkg. Defaults to the same path and name as input.",
    )
    parser.add_argument(
        "lang",
        nargs="?",
        default="en",
        help="Choose the terms language (en, es, pt, it, de, etc). Defaults to en (English).",
    )
    parser.add_argument(
        "source",
        choices=["cam", "wik"],
        help="Choose the source: Cambridge or Wiktionary.",
    )

    args = parser.parse_args()

    outpath = args.input if args.output == "-" else args.output

    with open(args.input) as input:
        if args.source == "wik":
            wiktionary2anki(input, outpath, args.lang)


if __name__ == "__main__":
    main()
