import requests
import utils.anki

API_URL = "https://en.wiktionary.org/api/rest_v1/page/definition"


def gen_answer(data):
    answer = []

    for item in data:
        partOfSpeech = item["partOfSpeech"]
        definition = item["definitions"][0]["definition"]
        examples = ""

        if "examples" in item["definitions"][0]:
            examples = "".join(
                [
                    f'<li><i>"{example}";</i></li>'
                    for example in item["definitions"][0]["examples"]
                ]
            )

        if examples:
            answer.append(
                f"<strong>{partOfSpeech}</strong> - {definition}\n<ul>{examples}</ul>\n\n"
            )
        else:
            answer.append(f"<strong>{partOfSpeech}</strong> - {definition}\n\n")

    return "".join(answer)


def wiktionary2anki(infile, outpath, lang):

    fields = []

    for line in infile:
        term = line.strip().lower().replace(" ", "_")

        response = requests.get(f"{API_URL}/{term}")

        if response.status_code == 200:
            data = response.json()

            if not lang in data:
                print(f'Error: term "{term}" not found in {lang.upper()}!\n')
                continue

            print(f'Term "{term}" found!\n')

        else:
            print(f'Error: "{term}" not found!\n')
            continue

        categories = "/".join({item["partOfSpeech"] for item in data[lang]})

        fields.append(
            [
                f'<div style="text-align: center;">{term} <i>({categories})</i></div>',
                gen_answer(data[lang]),
            ]
        )

    utils.anki.to_anki(fields, outpath)
