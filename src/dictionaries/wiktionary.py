import requests

from utils.anki import toAnki

API_URL = "https://en.wiktionary.org/api/rest_v1/page/definition"


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


def wiktionary2anki(infile, outpath, lang):

    fields = []

    for line in infile:
        term = line.strip().lower().replace(" ", "_")

        response = requests.get(f"{API_URL}/{term}")

        if response.status_code == 200:
            data = response.json()
        else:
            print(f'Error: "{term}" not found!')
            continue

        if not lang in data:
            print(f"There is no such term in {lang.upper()}: {term}")
            continue

        categories = "/".join({item["partOfSpeech"] for item in data[lang]})

        fields.append(
            [
                f'<div style="text-align: center;">{term} <i>({categories})</i></div>',
                gen_answer(data[lang]),
            ]
        )

    toAnki(fields, outpath)
