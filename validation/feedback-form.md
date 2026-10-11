# Beta tester feedback form

Copy this file, fill it in, and send it back with your two JSON files. Short
answers are fine. Problems are the most useful part, so please do not leave
them out to be polite.

## About you and your machine

- Name (or "prefer not to be named"):
- What you do (for example: backend developer, student, data scientist):
- City:
- Date of the test:
- Are you part of the team that built this? (must be **no**):
- Computer (make and model, or processor):
- Memory (GB):
- Operating system and version:
- Python version (`poetry run python --version`):
- Oragon version (`poetry run python -c "import oragon; print(oragon.__version__)"`):
- Does the machine have a GPU you used? (yes / no / not sure):

## Setup

- Did `poetry install` work first time? (yes / no; if no, what happened):
- Did `poetry run oragon import NCAIR1/N-ATLaS` finish? (yes / no; if no, where did it stop):
- Roughly how long did the import take:
- Did you have to ask the team for help at any point? (yes / no; if yes, about what):
- Which step in `docs/setup.md` was least clear:

## Running it

- `examples/01_chat.py` gave an answer: (yes / no)
- `examples/02_four_languages.py` ran to the end: (yes / no)
- From `benchmarks/speed.py`: model loaded in ____ s, mean first word ____ s, mean ____ tokens/s
- From `evidence/template_check.py`: defines the word in ____ of 10 runs
- The playground opened in your browser: (yes / no)

## The answers themselves

- Which Nigerian language(s) do you speak well enough to judge:
- Questions you asked in the playground, and whether each answer was good,
  partly right, or wrong:
  1.
  2.
  3.
- Anything in an answer that was clearly incorrect or strange:

## Overall

- Could you build something with this today? (yes / no; why):
- What would you build:
- The one thing that should be fixed first:
- Anything else:
