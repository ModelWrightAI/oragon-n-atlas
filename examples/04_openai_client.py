"""Talk to N-ATLaS through the OpenAI client library.

N-ATLaS must be on this machine first. Import it once (see docs/setup.md):

    poetry run oragon import NCAIR1/N-ATLaS

Then start the server in one terminal:

    poetry run oragon serve N-ATLaS

then, in another:

    poetry run python examples/04_openai_client.py

`oragon serve` speaks the OpenAI API, so code written for that API — in any
language — works against N-ATLaS by changing the address. The same server
also has a browser playground at http://127.0.0.1:8080/.
"""

from openai import OpenAI

SYSTEM = (
    "you are a large language model trained by Awarri AI technologies. "
    "You are a friendly assistant and you are here to help."
)

# On this machine only, the server needs no key; the client library still
# wants one, so any text will do. With `oragon serve --expose` or `--tunnel`,
# use the access token the server prints.
client = OpenAI(base_url="http://127.0.0.1:8080/v1", api_key="not-needed-locally")

stream = client.chat.completions.create(
    model="N-ATLaS",
    messages=[
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": "menene ake nufi da gwagwarmaya"},
    ],
    temperature=0.1,
    max_tokens=400,
    stream=True,
)
for event in stream:
    if event.choices and event.choices[0].delta.content:
        print(event.choices[0].delta.content, end="", flush=True)
print()
