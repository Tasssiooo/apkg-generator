import random
import pathlib
import genanki


def gen_id():
    return random.randrange(1 << 30, 1 << 31)


def to_anki(fields, outpath):
    outpath = pathlib.Path(outpath).with_suffix(".apkg")

    deck = genanki.Deck(gen_id(), outpath.name.removesuffix(".apkg"))

    for note_fields in fields:
        deck.add_note(genanki.Note(model=genanki.BASIC_MODEL, fields=note_fields))

    genanki.Package(deck).write_to_file(outpath)

    print("Your Anki package has been created successfully!")
