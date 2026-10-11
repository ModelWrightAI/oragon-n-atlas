"""A conversation with N-ATLaS in the terminal.

    poetry run python examples/03_terminal_chat.py

Type in Hausa, Yoruba, Igbo or English. The conversation is remembered from
one turn to the next. Press Ctrl-C, or enter an empty line, to stop.

N-ATLaS must be on this machine first. Import it once (see docs/setup.md):

    poetry run oragon import NCAIR1/N-ATLaS
"""

import sys

from oragon import Engine, Oragon, Settings, assistant, system, user

MODEL = "N-ATLaS"
SYSTEM = (
    "you are a large language model trained by Awarri AI technologies. "
    "You are a friendly assistant and you are here to help."
)
SETTINGS = Settings(temperature=0.1, repeat_penalty=1.12, max_tokens=400)
NOT_IMPORTED = (
    "N-ATLaS is not on this machine yet. Import it once with:\n\n"
    "    poetry run oragon import NCAIR1/N-ATLaS\n\n"
    "That needs a Hugging Face token with access to the model; "
    "docs/setup.md has the steps."
)

try:
    client = Oragon(engine=Engine.EMBEDDED, model=MODEL, cpu=True, warm_prompt=SYSTEM)
except FileNotFoundError:
    sys.exit(NOT_IMPORTED)
history = [system(SYSTEM)]
try:
    while True:
        try:
            said = input("\nyou> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not said:
            break
        history.append(user(said))
        answer = ""
        print("n-atlas> ", end="", flush=True)
        # overflow="slide" drops the oldest turns once the conversation is
        # longer than the model can read; the system prompt is always kept.
        for chunk in client.chat.generate(
            model=MODEL, messages=history, settings=SETTINGS, stream=True, overflow="slide"
        ):
            if isinstance(chunk, str):
                answer += chunk
                print(chunk, end="", flush=True)
        print()
        history.append(assistant(answer))
finally:
    client.close()
