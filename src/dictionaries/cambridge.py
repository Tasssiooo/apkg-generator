import requests
import utils.anki

API_URL = "https://apkggen-cambridge-dictionary-api.vercel.app/api/dictionary"


def gen_answer(data):
    answer = []

    for item in data["definition"]:
        pos = item["pos"].strip()
        definition = item["text"].strip().strip(":")
        translation = f': {item["translation"].strip()}' if item["translation"] else ""
        examples = []

        if "example" in item and len(item["example"]) > 0:

            for example in item["example"]:
                if example["translation"]:
                    examples.append(
                        f'<li><i>"{example["text"].strip()}";<br/><span style="font-size: 14px">"{example["translation"].strip()}"</span></i></li>'
                    )
                else:
                    examples.append(f'<li><i>"{example["text"].strip()}";</i></li>')

            answer.append(
                f"<strong>{pos}</strong> - {definition}{translation};\n<ul>{"".join(examples)}</ul>\n\n"
            )
        else:
            answer.append(f"<strong>{pos}</strong> - {definition};<br/>")

    if "verbs" in data:
        verbs = [f"<i>{item["type"]} - {item["text"]}</i>" for item in data["verbs"]]

        answer.append(
            f'<div style="text-align: center; font-size: 16px">{"; ".join(verbs)}</div>'
        )

    return "".join(answer)


def cambridge2anki(infile, outpath, lang):

    fields = []

    for line in infile:
        term = line.strip().lower()

        response = requests.get(f"{API_URL}/{lang}/{term.replace(" ", "-")}")

        if response.status_code == 200:
            data = response.json()
            print(f'Term "{term}" found!\n\n')
        else:
            print(
                f'Error: "{term}" not found in {lang.upper()}!\nTrying again with EN...\n'
            )

            response = requests.get(f"{API_URL}/en/{term.replace(" ", "-")}")

            if response.status_code == 200:
                data = response.json()
                print(f'Term "{term}" found in EN!\n\n')
            else:
                print(f'Error: "{term}" not found in EN\n\n')
                continue

        categories = "/".join({pos for pos in data["pos"]})

        fields.append(
            [
                f'<div style="text-align: center;">{term} <i>({categories})</i></div>',
                gen_answer(data),
            ]
        )

    utils.anki.to_anki(fields, outpath)
