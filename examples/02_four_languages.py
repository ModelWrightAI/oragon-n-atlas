"""N-ATLaS in Hausa, Yoruba, Igbo and English, streamed as it is written.

    poetry run python examples/02_four_languages.py

Each answer appears word by word, followed by how long the first word took
and how fast the rest came.

N-ATLaS must be on this machine first. Import it once (see docs/setup.md):

    poetry run oragon import NCAIR1/N-ATLaS
"""

import sys
import time

from oragon import Engine, Oragon, Settings, system, user

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

QUESTIONS = {
    "Hausa": "menene ake nufi da gwagwarmaya",
    "Yoruba": "Báwo ni o ṣe máa ṣàlàyé ohun tí ọ̀rọ̀ 'ìfẹ́' túmọ̀ sí?",
    "Igbo": "Kedu ihe bụ ọdịnala ndị Igbo? Kọwaa nkenke.",
    "English": "In two sentences, what is jollof rice?",
}

# warm_prompt reads the system prompt once at startup, so the first question
# does not wait for it.
try:
    client = Oragon(engine=Engine.EMBEDDED, model=MODEL, cpu=True, warm_prompt=SYSTEM)
except FileNotFoundError:
    sys.exit(NOT_IMPORTED)
try:
    # The model loads on the first request. Asking for one token here keeps
    # that wait out of the first question's timing.
    print("loading N-ATLaS...")
    client.chat.generate(
        model=MODEL,
        messages=[system(SYSTEM), user("hi")],
        settings=Settings(max_tokens=1),
    )
    for language, question in QUESTIONS.items():
        print(f"\n[{language}] {question}\n")
        started = time.perf_counter()
        first_word = None
        reply = None
        for chunk in client.chat.generate(
            model=MODEL,
            messages=[system(SYSTEM), user(question)],
            settings=SETTINGS,
            stream=True,
        ):
            if isinstance(chunk, str):
                if first_word is None:
                    first_word = time.perf_counter() - started
                print(chunk, end="", flush=True)
            else:
                reply = chunk  # the last item is the complete response
        total = time.perf_counter() - started
        tokens = reply.usage.completion_tokens
        speed = tokens / (total - first_word)
        print(f"\n\n  first word {first_word:.2f}s, {tokens} tokens, {speed:.1f} tokens/s")
finally:
    client.close()
