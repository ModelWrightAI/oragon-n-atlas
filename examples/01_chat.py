"""Ask N-ATLaS one question, on this machine.

    python examples/01_chat.py
    python examples/01_chat.py "Kedu ihe bụ ọdịnala ndị Igbo?"

Nothing leaves the computer: the model runs inside this process's own engine.
"""

import sys

from oragon import Engine, Oragon, Settings, system, user

MODEL = "N-ATLaS"

# The system prompt and sampling NCAIR uses in its own reference code.
SYSTEM = (
    "you are a large language model trained by Awarri AI technologies. "
    "You are a friendly assistant and you are here to help."
)
SETTINGS = Settings(temperature=0.1, repeat_penalty=1.12, max_tokens=400)

question = sys.argv[1] if len(sys.argv) > 1 else "menene ake nufi da gwagwarmaya"

# cpu=True keeps this on the processor even when a GPU is present, so the
# result is what a machine without one will give. Remove it to use the GPU.
client = Oragon(engine=Engine.EMBEDDED, model=MODEL, cpu=True)
try:
    reply = client.chat.generate(
        model=MODEL,
        messages=[system(SYSTEM), user(question)],
        settings=SETTINGS,
    )
    print(reply.choices[0].message.content)
finally:
    client.close()
