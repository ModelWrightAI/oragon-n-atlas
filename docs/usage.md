# Usage

How to use N-ATLaS from Python and over HTTP once it is
[set up](setup.md). The programs in [`examples/`](../examples/) show most of
this running.

## The basics

```python
from oragon import Engine, Oragon, Settings, system, user

client = Oragon(engine=Engine.EMBEDDED, model="N-ATLaS")

reply = client.chat.generate(
    model="N-ATLaS",
    messages=[system("..."), user("menene ake nufi da gwagwarmaya")],
    settings=Settings(temperature=0.1, repeat_penalty=1.12, max_tokens=400),
)
print(reply.choices[0].message.content)
client.close()
```

- `Engine.EMBEDDED` means the model runs in an engine this program starts
  and owns. Nothing else needs to be running.
- The model is loaded on the first request and stays loaded, so only the
  first request pays the 10 to 17 seconds of loading.
- `client.close()` stops the engine. Call it once, after your last request,
  not after each one: closing and reopening would load the model again every
  time. Use `try`/`finally`, as the examples do, so the engine also stops
  when something goes wrong.

## The settings N-ATLaS expects

NCAIR's reference code uses these, and so do all our examples and
measurements:

| Setting | Value | What it does |
|---|---|---|
| System prompt | `you are a large language model trained by Awarri AI technologies. You are a friendly assistant and you are here to help.` | Tells the model who it is, as in training |
| `temperature` | `0.1` | Keeps answers focused and nearly the same from run to run |
| `repeat_penalty` | `1.12` | Discourages the model from repeating itself |
| `max_tokens` | your choice | The longest answer allowed. 300 to 400 suits most questions |

Hausa, Yoruba and Igbo use more tokens per word than English does, so allow
more `max_tokens` than you would for an English answer of the same length.

You do **not** set the prompt format. The engine reads the template stored in
the model and applies it, including today's date, exactly as NCAIR's own code
does.

## Processor or GPU

```python
Oragon(engine=Engine.EMBEDDED, model="N-ATLaS", cpu=True)   # processor only
Oragon(engine=Engine.EMBEDDED, model="N-ATLaS")             # use a GPU if there is one
```

`cpu=True` is the right choice when you want to know what a machine without
a GPU will do. Leave it out to get the most from the machine you have.

## Streaming

Show the answer as it is written, so the user sees the first word in under a
second instead of waiting for the whole reply:

```python
for chunk in client.chat.generate(model="N-ATLaS", messages=[...], stream=True):
    if isinstance(chunk, str):
        print(chunk, end="", flush=True)   # a piece of text
    else:
        reply = chunk                       # the last item: the full response
```

## A faster first answer

If every request starts with the same system prompt, have the engine read it
once at startup:

```python
client = Oragon(engine=Engine.EMBEDDED, model="N-ATLaS", warm_prompt=SYSTEM)
```

## Conversations

Keep the messages in a list and add to it:

```python
from oragon import assistant

history = [system(SYSTEM)]
history.append(user("Sannu"))
reply = client.chat.generate(model="N-ATLaS", messages=history, overflow="slide")
history.append(assistant(reply.choices[0].message.content))

client.close()  # once the conversation is over
```

A conversation too long for the model raises `ContextOverflowError` before
anything is generated. `overflow="slide"` drops the oldest turns instead and
keeps the system prompt.

## Several requests at once

The engine answers up to four requests at the same time for free; more than
four needs a paid plan. Extra requests wait in a queue instead of failing.

```python
import asyncio
from oragon import AsyncOragon

async def main():
    async with AsyncOragon(engine=Engine.EMBEDDED, model="N-ATLaS") as client:
        replies = await asyncio.gather(*(
            client.chat.generate(model="N-ATLaS", messages=[system(SYSTEM), user(q)])
            for q in questions
        ))

asyncio.run(main())
```

## Over HTTP, for any language

```sh
poetry run oragon serve N-ATLaS                 # this machine only
poetry run oragon serve N-ATLaS --expose        # other machines on your network
poetry run oragon serve N-ATLaS --tunnel        # a public HTTPS link
```

| Address | What it is |
|---|---|
| `http://127.0.0.1:8080/` | The browser playground |
| `http://127.0.0.1:8080/v1/chat/completions` | Chat, in the OpenAI format, with streaming |
| `http://127.0.0.1:8080/v1/models` | What is loaded |
| `http://127.0.0.1:8080/health` | Whether the server is up |

`--expose` and `--tunnel` print an access token; send it as the API key.

With the OpenAI Python library:

```python
from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:8080/v1", api_key="not-needed-locally")
reply = client.chat.completions.create(
    model="N-ATLaS",
    messages=[{"role": "system", "content": SYSTEM},
              {"role": "user", "content": "menene ake nufi da gwagwarmaya"}],
    temperature=0.1,
)
print(reply.choices[0].message.content)

client.close()  # closes the connection; the server keeps running
```

With `curl`:

```sh
curl http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "N-ATLaS", "temperature": 0.1,
       "messages": [{"role": "user", "content": "menene ake nufi da gwagwarmaya"}]}'
```

## When something goes wrong

Errors are Python exceptions that say what happened and whether trying again
is safe.

| Error | What it means |
|---|---|
| `InsufficientMemoryError` | The model does not fit in free memory. Raised before loading, not a crash. Close other programs. |
| `ContextOverflowError` | The conversation is too long. Use `overflow="slide"` or shorten it. |
| `EngineBusyError` | Still overloaded after automatic retries. Nothing was started; try again later. |
| `EngineTimeoutError` | The request took longer than your timeout. |

For anything else, `poetry run oragon doctor` prints the machine, the engine and the
installed models in a form you can paste into a bug report, and
`ORAGON_DEBUG=1` turns on detailed logging.
