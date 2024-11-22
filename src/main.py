import argparse
from dictionaries.cambridge import cambridge2anki
from dictionaries.wiktionary import wiktionary2anki


def main():
    parser = argparse.ArgumentParser(
        prog="APKG Generator",
        description="It takes a path to a file with terms in it as argument then search for those terms in a database like Wiktionary or Cambridge, and creates an APKG file with the data.",
        usage="apkg-generator [-h] input [-o output] [lang] {cam, wik}",
    )
    parser.add_argument("input", help="Ex.: path/to/file_input.txt")
    parser.add_argument(
        "-o",
        "--output",
        help="Ex.: path/to/file_output.apkg. Defaults to the same path and name as input.",
    )
    parser.add_argument(
        "lang",
        help="Choose the terms language (en, es, pt, en-pt, en-es, etc).",
    )
    parser.add_argument(
        "source",
        choices=["cam", "wik"],
        help="Choose the source: Cambridge or Wiktionary",
    )

    args = parser.parse_args()

    outpath = args.input if not args.output else args.output

    with open(args.input) as input:
        match args.source:
            case "wik":
                wiktionary2anki(input, outpath, args.lang)
            case "cam":
                cambridge2anki(input, outpath, args.lang)
            case _:
                print(f'Unknown source: "{args.source}".')


if __name__ == "__main__":
    main()
