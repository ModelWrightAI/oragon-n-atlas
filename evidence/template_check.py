"""Does N-ATLaS answer the question it was asked? A test anyone can repeat.

    python evidence/template_check.py
    python evidence/template_check.py --save evidence/results/oragon-0.1.2.json

It asks one Hausa question, "menene ake nufi da gwagwarmaya" (what is meant
by "gwagwarmaya" — struggle), ten times with ten different seeds, at the
sampling settings NCAIR's reference code uses.

A good answer defines the word. A poor one repeats the question's own words
back ("Ake nufi da gwagwarmaya na iya bambanta...") without defining it. This
script counts how many of the ten answers define the word. It is a simple
check on the opening words, not a judgement of the whole answer, so the
answers themselves are saved for a Hausa speaker to read.

Our result with Oragon 0.1.2: the word is defined in 10 of 10 runs.

N-ATLaS must be on this machine first: `oragon import NCAIR1/N-ATLaS`
(see docs/setup.md).
"""

import argparse
import json
import platform
import sys

import oragon
from oragon import Engine, Oragon, Settings, system, user

MODEL = "N-ATLaS"
SYSTEM = (
    "you are a large language model trained by Awarri AI technologies. "
    "You are a friendly assistant and you are here to help."
)
QUESTION = "menene ake nufi da gwagwarmaya"
SEEDS = range(10)
NOT_IMPORTED = (
    "N-ATLaS is not on this machine yet. Import it once with:\n\n"
    "    oragon import NCAIR1/N-ATLaS\n\n"
    "That needs a Hugging Face token with access to the model; "
    "docs/setup.md has the steps."
)


def repeats_the_question(answer: str) -> bool:
    return answer.lstrip(" \"'*").lower().startswith("ake nufi")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--save", metavar="FILE", help="also write every answer as JSON")
    args = parser.parse_args()

    try:
        client = Oragon(engine=Engine.EMBEDDED, model=MODEL, cpu=True, warm_prompt=SYSTEM)
    except FileNotFoundError:
        sys.exit(NOT_IMPORTED)
    answers = []
    try:
        for seed in SEEDS:
            reply = client.chat.generate(
                model=MODEL,
                messages=[system(SYSTEM), user(QUESTION)],
                settings=Settings(
                    temperature=0.1,
                    repeat_penalty=1.12,
                    penalty_last_n=-1,
                    max_tokens=120,
                    seed=seed,
                ),
            )
            text = reply.choices[0].message.content
            repeated = repeats_the_question(text)
            answers.append({"seed": seed, "repeats_the_question": repeated, "answer": text})
            print(f"seed {seed}: {'REPEATS' if repeated else 'defines':<8} {text[:90]!r}")
    finally:
        client.close()

    defined = sum(not a["repeats_the_question"] for a in answers)
    print(f"\noragon {oragon.__version__}: defines the word in {defined} of {len(answers)} runs")

    if args.save:
        with open(args.save, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "oragon": oragon.__version__,
                    "model": MODEL,
                    "machine": f"{platform.system()} {platform.machine()}",
                    "question": QUESTION,
                    "defines_the_word": defined,
                    "runs": len(answers),
                    "answers": answers,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )
        print(f"saved to {args.save}")


if __name__ == "__main__":
    main()
