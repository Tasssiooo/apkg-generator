import requests

from utils import toAnki

API_URL = "https://apkggen-cambridge-dictionary-api.vercel.app/api/dictionary"


def gen_answer(data):
    answer = ""

    for item in data["definition"]:
        pos = item["pos"].strip()
        definition = item["text"].strip()
        translation = item["translation"].strip()
        examples = ""

        if "example" in item and len(item["example"]) > 0:
            examples = "".join(
                [
                    f'<li><i>"{example["text"].strip()}:"</i></li><li>trans: <i>"{example["translation"].strip()}"</i></li>'
                    for example in item["example"]
                ]
            )

        answer += f"<strong>{pos}</strong> - {definition}; trans: {translation}.\n<ul>{examples}</ul>\n\n"

    if "verbs" in data:
        verbs = [f"<i>{item["type"]} - {item["text"]} </i>" for item in data["verbs"]]

        answer += f'<div style="text-align: center;">{"".join(verbs)}</div>'

    return answer


def cambridge2anki(infile, outpath, lang):

    fields = []

    for line in infile:
        term = line.strip().lower().replace(" ", "-")

        response = requests.get(f"{API_URL}/{lang}/{term}")

        if response.status_code == 200:
            data = response.json()
        else:
            print(
                f'Error: "{term}" not found in {lang.upper()}!\nTrying again with EN...'
            )

            response = requests.get(f"{API_URL}/en/{term}")

            if response.status_code == 200:
                data = response.json()
            else:
                print(f'Error: "{term}" not found in EN')
                continue

        categories = "/".join({pos for pos in data["pos"]})

        fields.append(
            [
                f'<div style="text-align: center;">{term} <i>({categories})</i></div>',
                gen_answer(data),
            ]
        )

    toAnki(fields, outpath)
