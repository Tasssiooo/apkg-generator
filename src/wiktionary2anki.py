import requests
import genanki
import random
import os
import pathlib

API_URL = "https://en.wiktionary.org/api/rest_v1/page/definition"


def gen_id():
    return random.randrange(1 << 30, 1 << 31)


def gen_answer(data):
    answer = ""

    for item in data:
        partOfSpeech = item["partOfSpeech"]
        definition = item["definitions"][0]["definition"]
        examples = ""

        if "examples" in item["definitions"][0]:
            examples = "".join(
                [
                    f'<li><i>"{example}"</i></li>'
                    for example in item["definitions"][0]["examples"]
                ]
            )

        answer += (
            f"<strong>{partOfSpeech}</strong> - {definition}\n<ul>{examples}</ul>\n\n"
        )

    return answer


def wiktionary2anki(infile, outfile):

    outfile = pathlib.Path(outfile)

    if outfile.suffix:
        if not outfile.suffix == ".apkg":
            outfile = outfile.with_suffix(".apkg")
    else:
        outfile = outfile.with_suffix(".apkg")

    model = genanki.Model(
        gen_id(),
        "Term&Definition",
        fields=[
            {"name": "Term"},
            {"name": "Definition"},
        ],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "{{Term}}",
                "afmt": "{{FrontSide}}<hr id=answer>{{Definition}}",
            },
        ],
        css=".card {font-family: arial;font-size: 20px;",
    )

    deck = genanki.Deck(gen_id(), os.path.basename(outfile).replace(".apkg", ""))

    for term in infile:
        response = requests.get(f"{API_URL}/{term.strip().lower()}")
        data = response.json()

        categories = "/".join([item["partOfSpeech"] for item in data["en"]])

        note = genanki.Note(
            model=model,
            fields=[
                f'<div style="text-align: center;">{term} <i>({categories})</i></div>',
                gen_answer(data["en"]),
            ],
        )

        deck.add_note(note)

    genanki.Package(deck).write_to_file(outfile)

    print("Anki package has been created successfully!")
