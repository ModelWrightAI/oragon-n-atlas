# Oragon for N-ATLaS

**Run N-ATLaS on your own computer, with one `pip install`, no GPU and no
internet connection once the model is on disk.**

[N-ATLaS](https://huggingface.co/NCAIR1/N-ATLaS) is Nigeria's open
multilingual language model: a Llama 3 8B fine-tune for Hausa, Yoruba, Igbo
and Nigerian-accented English, published by NCAIR. Its reference code needs a
GPU and a deep-learning stack. This repository shows how to run the same
model through [Oragon](https://pypi.org/project/oragon/), a Python SDK with
its own built-in engine, so that a developer with an ordinary laptop or a
plain server can build on it.

This is our entry for the National AI Innovation Challenge 2026, *Build with
N-ATLAS*, under **Developer Infrastructure**.

Once the model has been imported (a single command, shown under
[Quick start](#quick-start)), this is all the code it takes:

```python
from oragon import Engine, Oragon, Settings, system, user

client = Oragon(engine=Engine.EMBEDDED, model="N-ATLaS", cpu=True)

reply = client.chat.generate(
    model="N-ATLaS",
    messages=[
        system("you are a large language model trained by Awarri AI technologies. "
               "You are a friendly assistant and you are here to help."),
        user("menene ake nufi da gwagwarmaya"),
    ],
    settings=Settings(temperature=0.1, repeat_penalty=1.12, max_tokens=400),
)
print(reply.choices[0].message.content)
```

```text
Gwagwarmaya na nufin kokarin da ake yi don cimma wani buri, shawo kan
kalubale, ko shawo kan matsaloli. Yana dauke da jajircewa, himma, da kuma
yunƙurin samun nasara ko ci gaba duk da wahala ko ƙalubale. ...
```

## What you get

| | |
|---|---|
| **A Python SDK** | `client.chat.generate(...)`, with streaming, conversations, typed errors and async |
| **An OpenAI-compatible API** | `oragon serve N-ATLaS` — any OpenAI client, in any language, can use the model |
| **A browser playground** | at `http://127.0.0.1:8080/` while the server runs; works with no internet |
| **One-command import** | `oragon import NCAIR1/N-ATLaS` fetches NCAIR's official checkpoint and prepares it |
| **The model's own prompt format** | N-ATLaS is given exactly the prompt its publishers' code gives it — see [the evidence](evidence/README.md) |
| **No GPU required** | 14 tokens per second on a laptop processor; a GPU is used if you have one |
| **Nothing leaves the machine** | no telemetry, and your prompts and answers are never sent anywhere |

## Measured on a laptop

Apple M4 MacBook, 16 GB of memory, **processor only**, Oragon 0.1.2:

| | |
|---|---|
| Model file on disk | 4.9 GB |
| Time to load the model | 12 to 17 seconds, once per run |
| Time to the first word of an answer | 0.2 to 0.7 seconds |
| Writing speed | 14 tokens per second |

Run [`benchmarks/speed.py`](benchmarks/speed.py) to get the same table for
your own machine.

## Quick start

You need Python 3.9 to 3.13 on macOS (Apple silicon) or Linux, about 6 GB of
free memory, and about 36 GB of free disk while the model is being prepared
(5 GB afterwards). Full details are in [docs/setup.md](docs/setup.md).

**1. Install.**

```sh
pip install "oragon>=0.1.2"
```

**2. Get access to N-ATLaS.** The model is gated. Sign in to Hugging Face,
open [NCAIR1/N-ATLaS](https://huggingface.co/NCAIR1/N-ATLaS), accept its
terms, then create a read token under *Settings → Access Tokens*.

**3. Import the model.** This downloads NCAIR's checkpoint (15 GB), prepares
a 4.9 GB file for local use, and deletes the download. It takes about half an
hour on a home connection and is done once.

```sh
export HF_TOKEN=hf_your_token_here
oragon import NCAIR1/N-ATLaS
```

The examples load the model by the name `N-ATLaS`. They do not download it,
so this step has to come before any of them.

**4. Run it.**

```sh
git clone https://github.com/ModelWrightAI/oragon-n-atlas.git && cd oragon-n-atlas
python examples/01_chat.py
```

## Examples

| File | What it shows |
|---|---|
| [`examples/01_chat.py`](examples/01_chat.py) | One question, one answer |
| [`examples/02_four_languages.py`](examples/02_four_languages.py) | Hausa, Yoruba, Igbo and English, streamed, with timings |
| [`examples/03_terminal_chat.py`](examples/03_terminal_chat.py) | A conversation that remembers earlier turns |
| [`examples/04_openai_client.py`](examples/04_openai_client.py) | The OpenAI client library talking to `oragon serve N-ATLaS` |

## The server and the playground

```sh
oragon serve N-ATLaS
```

This starts an OpenAI-compatible API on `http://127.0.0.1:8080/v1` and a
playground page at `http://127.0.0.1:8080/`: a chat pane, and a live view of
tokens per second and requests in progress. Add `--expose` to let other
machines on your network use it, or `--tunnel` for a public HTTPS link; both
create an access token for you.

## What is in this repository

| Folder | Contents |
|---|---|
| [`examples/`](examples/) | Four short programs you can copy from |
| [`benchmarks/`](benchmarks/) | A script that measures N-ATLaS on your machine, and our results |
| [`evidence/`](evidence/) | How we checked that N-ATLaS runs correctly, with a test you can repeat |
| [`docs/`](docs/) | [Architecture](docs/architecture.md), [setup](docs/setup.md) and [usage](docs/usage.md) |
| [`validation/`](validation/) | The beta-test plan, the feedback form, and testers' reports |

## Known limits

We would rather you read these here than discover them.

- **Translation is weak.** Asked to translate "Good morning, how did you
  sleep?" into Yoruba, Hausa and Igbo, N-ATLaS gave general greetings instead
  of the morning ones. This is a limit of the model, not of the way it is run.
- **Facts need checking.** As with any model of this size, a fluent answer is
  not always a correct one.
- **Our quality reading is not a native speaker's.** The checks in
  [`evidence/`](evidence/) are deliberately simple and repeatable. A proper
  judgement of Hausa, Yoruba and Igbo quality needs fluent readers.
- **Platforms.** Oragon runs on macOS (Apple silicon) and recent Linux.
  Windows is not supported yet; Windows users can use WSL.
- **Text only.** N-ATLaS's speech recognition is not part of this work.

## About

Oragon is built by Oragon Labs: AI that runs where people and their data
already are, on their own machines, with no GPU required.

- Oragon on PyPI: <https://pypi.org/project/oragon/>
- Website: <https://www.oragonlabs.com>
- Contact: [hello@oragonlabs.com](mailto:hello@oragonlabs.com)

N-ATLaS is the work of NCAIR and Awarri Technologies. This repository
contains no model weights; you download them from the publishers under their
terms.
