# Oragon for N-ATLaS

**Run N-ATLaS on your own computer, with one install command, no GPU and no
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

for chunk in client.chat.generate(
    model="N-ATLaS",
    messages=[
        system("you are a large language model trained by Awarri AI technologies. "
               "You are a friendly assistant and you are here to help."),
        user("menene ake nufi da gwagwarmaya"),
    ],
    settings=Settings(temperature=0.1, repeat_penalty=1.12, max_tokens=400),
    stream=True,  # show each word as it is written
):
    if isinstance(chunk, str):
        print(chunk, end="", flush=True)

client.close()  # when you have no more requests: stops the engine
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
| **The model's own prompt format** | N-ATLaS is given exactly the prompt its publishers' code gives it — see [the prompt](#the-prompt-n-atlas-is-given) and [the evidence](evidence/README.md) |
| **No GPU required** | 14 tokens per second on a laptop processor; a GPU is used if you have one |
| **Nothing leaves the machine** | no telemetry, and your prompts and answers are never sent anywhere |

## Measured on a laptop

Apple M4 MacBook, 16 GB of memory, **processor only**, Oragon 0.1.2 installed
from PyPI:

| | |
|---|---|
| Model file on disk | 4.9 GB |
| Time to load the model | 10 to 17 seconds, once per run |
| Time to the first word of an answer | 0.2 to 0.7 seconds |
| Writing speed | 14 tokens per second |

Run [`benchmarks/speed.py`](benchmarks/speed.py) to get the same table for
your own machine.

## Quick start

You need Python 3.9 to 3.13 on macOS (Apple silicon) or Linux, about 6 GB of
free memory, and about 36 GB of free disk while the model is being prepared
(5 GB afterwards). Full details are in [docs/setup.md](docs/setup.md).

**1. Get the code and install.** This repository uses
[Poetry](https://python-poetry.org/docs/#installation). `poetry install`
creates an environment with Oragon in it, and `poetry run` runs a command
inside that environment.

```sh
git clone https://github.com/OragonLabs/oragon-n-atlas.git && cd oragon-n-atlas
poetry install
```

**2. Get access to N-ATLaS.** The model is gated. Sign in to Hugging Face,
open [NCAIR1/N-ATLaS](https://huggingface.co/NCAIR1/N-ATLaS), accept its
terms, then create a read token under *Settings → Access Tokens*.

**3. Import the model.** This downloads NCAIR's checkpoint (15 GB), prepares
a 4.9 GB file for local use, and deletes the download. It takes about half an
hour on a home connection and is done once.

```sh
export HF_TOKEN=hf_your_token_here
poetry run oragon import NCAIR1/N-ATLaS
```

The examples load the model by the name `N-ATLaS`. They do not download it,
so this step has to come before any of them.

**4. Run it.**

```sh
poetry run python examples/01_chat.py
```

Not using Poetry? `pip install "oragon>=0.1.2" openai` gives you the same
packages; then leave `poetry run` off every command.

## Examples

| File | What it shows |
|---|---|
| [`examples/01_chat.py`](examples/01_chat.py) | One question, answered word by word as it is written |
| [`examples/02_four_languages.py`](examples/02_four_languages.py) | Hausa, Yoruba, Igbo and English, streamed, with timings |
| [`examples/03_terminal_chat.py`](examples/03_terminal_chat.py) | A conversation that remembers earlier turns |
| [`examples/04_openai_client.py`](examples/04_openai_client.py) | The OpenAI client library talking to `oragon serve N-ATLaS` |

## The server and the playground

```sh
poetry run oragon serve N-ATLaS
```

This starts an OpenAI-compatible API on `http://127.0.0.1:8080/v1` and a
playground page at `http://127.0.0.1:8080/`: a chat pane, and a live view of
tokens per second and requests in progress. Add `--expose` to let other
machines on your network use it, or `--tunnel` for a public HTTPS link; both
create an access token for you.

## The prompt N-ATLaS is given

You do not write the prompt format. Oragon runs the chat template stored in
the model, the same one NCAIR's reference code uses.

### A simple example

You send two messages:

```text
system: You are a helpful assistant.
user: Say hello.
```

The template turns them into one piece of text. This is what N-ATLaS reads:

```text
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Cutting Knowledge Date: December 2023
Today Date: 12 Oct 2026

You are a helpful assistant.<|eot_id|><|start_header_id|>user<|end_header_id|>

Say hello.<|eot_id|><|start_header_id|>assistant<|end_header_id|>
```

Reading it piece by piece:

- `<|begin_of_text|>` marks the start of the prompt.
- `<|start_header_id|>system<|end_header_id|>` says who speaks next:
  `system`, `user` or `assistant`.
- `<|eot_id|>` ends that speaker's turn.
- The two date lines come from the template. You did not send them.
  `Today Date` is the day the prompt is built, so yours will differ.
- The prompt ends with an open `assistant` header and a blank line, so the
  next thing written is the model's answer.

To print this on your own machine:

```sh
poetry run oragon template N-ATLaS
```

It prints the example above and then the template below. The second line of
its output should read
`template-source: the model's own template (tokenizer.chat_template), executed`,
which confirms that the model's own template was run, not a copy of it.

### The raw chat template

This is the template exactly as it is stored in the model. It is a small
program in the Jinja language. It is shown here in five parts, in order, with
a note above each. Nothing has been changed: where one part ends and the next
begins, the model's file has a single blank line.

**Part 1. Start of text, and defaults.** The first line writes
`<|begin_of_text|>`. The rest fills in values the caller left out: no tools,
and a fallback date that is used only when no date is supplied. Oragon
supplies today's date.

```jinja
{{- bos_token }}
{%- if custom_tools is defined %}
    {%- set tools = custom_tools %}
{%- endif %}
{%- if not tools_in_user_message is defined %}
    {%- set tools_in_user_message = true %}
{%- endif %}
{%- if not date_string is defined %}
    {%- set date_string = "26 Jul 2024" %}
{%- endif %}
{%- if not tools is defined %}
    {%- set tools = none %}
{%- endif %}
```

**Part 2. Find the system message.** If the first message is a system
message, it is taken off the list and kept for part 3.

```jinja
{#- This block extracts the system message, so we can slot it into the right place. #}
{%- if messages[0]['role'] == 'system' %}
    {%- set system_message = messages[0]['content']|trim %}
    {%- set messages = messages[1:] %}
{%- else %}
    {%- set system_message = "" %}
{%- endif %}
```

**Part 3. Write the system turn.** Writes the `system` header, the two date
lines and your system message, then ends the turn. The lines that mention
tools run only when tools are passed.

```jinja
{#- System message + builtin tools #}
{{- "<|start_header_id|>system<|end_header_id|>\n\n" }}
{%- if builtin_tools is defined or tools is not none %}
    {{- "Environment: ipython\n" }}
{%- endif %}
{%- if builtin_tools is defined %}
    {{- "Tools: " + builtin_tools | reject('equalto', 'code_interpreter') | join(", ") + "\n\n"}}
{%- endif %}
{{- "Cutting Knowledge Date: December 2023\n" }}
{{- "Today Date: " + date_string + "\n\n" }}
{%- if tools is not none and not tools_in_user_message %}
    {{- "You have access to the following functions. To call a function, please respond with JSON for a function call." }}
    {{- 'Respond in the format {"name": function name, "parameters": dictionary of argument name and its value}.' }}
    {{- "Do not use variables.\n\n" }}
    {%- for t in tools %}
        {{- t | tojson(indent=4) }}
        {{- "\n\n" }}
    {%- endfor %}
{%- endif %}
{{- system_message }}
{{- "<|eot_id|>" }}
```

**Part 4. Tools, if any.** Runs only when tools are passed: their
descriptions are written into the first user message. With no tools, this
part writes nothing.

```jinja
{#- Custom tools are passed in a user message with some extra guidance #}
{%- if tools_in_user_message and not tools is none %}
    {#- Extract the first user message so we can plug it in here #}
    {%- if messages | length != 0 %}
        {%- set first_user_message = messages[0]['content']|trim %}
        {%- set messages = messages[1:] %}
    {%- else %}
        {{- raise_exception("Cannot put tools in the first user message when there's no first user message!") }}
{%- endif %}
    {{- '<|start_header_id|>user<|end_header_id|>\n\n' -}}
    {{- "Given the following functions, please respond with a JSON for a function call " }}
    {{- "with its proper arguments that best answers the given prompt.\n\n" }}
    {{- 'Respond in the format {"name": function name, "parameters": dictionary of argument name and its value}.' }}
    {{- "Do not use variables.\n\n" }}
    {%- for t in tools %}
        {{- t | tojson(indent=4) }}
        {{- "\n\n" }}
    {%- endfor %}
    {{- first_user_message + "<|eot_id|>"}}
{%- endif %}
```

**Part 5. Every other message, then the assistant's turn.** Each remaining
message is written as a header, its text and `<|eot_id|>`. The longer
branches handle tool calls and tool results. The last three lines open the
assistant's turn, where the answer goes.

```jinja
{%- for message in messages %}
    {%- if not (message.role == 'ipython' or message.role == 'tool' or 'tool_calls' in message) %}
        {{- '<|start_header_id|>' + message['role'] + '<|end_header_id|>\n\n'+ message['content'] | trim + '<|eot_id|>' }}
    {%- elif 'tool_calls' in message %}
        {%- if not message.tool_calls|length == 1 %}
            {{- raise_exception("This model only supports single tool-calls at once!") }}
        {%- endif %}
        {%- set tool_call = message.tool_calls[0].function %}
        {%- if builtin_tools is defined and tool_call.name in builtin_tools %}
            {{- '<|start_header_id|>assistant<|end_header_id|>\n\n' -}}
            {{- "<|python_tag|>" + tool_call.name + ".call(" }}
            {%- for arg_name, arg_val in tool_call.arguments | items %}
                {{- arg_name + '="' + arg_val + '"' }}
                {%- if not loop.last %}
                    {{- ", " }}
                {%- endif %}
                {%- endfor %}
            {{- ")" }}
        {%- else  %}
            {{- '<|start_header_id|>assistant<|end_header_id|>\n\n' -}}
            {{- '{"name": "' + tool_call.name + '", ' }}
            {{- '"parameters": ' }}
            {{- tool_call.arguments | tojson }}
            {{- "}" }}
        {%- endif %}
        {%- if builtin_tools is defined %}
            {#- This means we're in ipython mode #}
            {{- "<|eom_id|>" }}
        {%- else %}
            {{- "<|eot_id|>" }}
        {%- endif %}
    {%- elif message.role == "tool" or message.role == "ipython" %}
        {{- "<|start_header_id|>ipython<|end_header_id|>\n\n" }}
        {%- if message.content is mapping or message.content is iterable %}
            {{- message.content | tojson }}
        {%- else %}
            {{- message.content }}
        {%- endif %}
        {{- "<|eot_id|>" }}
    {%- endif %}
{%- endfor %}
{%- if add_generation_prompt %}
    {{- '<|start_header_id|>assistant<|end_header_id|>\n\n' }}
{%- endif %}
```

How we tested that this gives correct answers is in
[the evidence](evidence/README.md).

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

## Licence and contributing

The code, examples and documentation here are released under the
[MIT licence](LICENSE). The Oragon SDK and engine are installed from PyPI
under their own licence. To report a problem or suggest a change, see
[CONTRIBUTING.md](CONTRIBUTING.md).
