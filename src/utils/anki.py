import random
import os
import pathlib
import genanki


def gen_id():
    return random.randrange(1 << 30, 1 << 31)


def toAnki(fields, outpath):
    outpath = pathlib.Path(outpath)
    outpath = outpath.with_suffix(".apkg")

    model = genanki.Model(
        gen_id(),
        "Term&Definition",
        fields=[
            {"name": "Term"},
            {"name": "Definition"},
        ],
        templates=[
            {
                "name": "Tasssiooo",
                "qfmt": "{{Term}}",
                "afmt": "{{FrontSide}}<hr id=answer>{{Definition}}",
            },
        ],
        css=".card {font-family: arial; font-size: 20px;}",
    )

    deck = genanki.Deck(gen_id(), os.path.basename(outpath).removesuffix(".apkg"))

    for note_fields in fields:
        deck.add_note(genanki.Note(model=model, fields=note_fields))

    genanki.Package(deck).write_to_file(outpath)

    print("Your Anki package has been created successfully!")
