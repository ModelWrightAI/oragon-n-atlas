# Setup

From an empty machine to N-ATLaS answering a question. Allow about 45
minutes, nearly all of it waiting for the download.

## What you need

| | |
|---|---|
| **Operating system** | macOS 11 or later on Apple silicon, or Linux on x86-64 or arm64 (Ubuntu 24.04+, Debian 13+, Fedora 40+). Windows is not supported yet; use WSL with one of those Linux versions. |
| **Python** | 3.9 to 3.13 |
| **Memory** | About 6 GB free. A 16 GB machine is comfortable; on 8 GB, close other programs first. |
| **Disk** | About 36 GB free while the model is being prepared. Afterwards the model takes 4.9 GB and the rest is given back. |
| **GPU** | Not needed. If one is present it is used, unless you ask for the processor only. |
| **Internet** | Needed once, to install and to download the model. Not needed to run it. |

## 1. Get the code and install

This repository uses [Poetry](https://python-poetry.org/docs/#installation)
to install what it needs. If you do not have Poetry yet, follow that link
first.

```sh
git clone https://github.com/OragonLabs/oragon-n-atlas.git
cd oragon-n-atlas
poetry install
```

`poetry install` creates a separate Python environment for this project and
installs Oragon into it, at the versions recorded in `poetry.lock`. Every
command in this guide starts with `poetry run`, which runs it inside that
environment.

Check the version. Everything in this repository was built and measured with
0.1.2, so it must be 0.1.2 or later.

```sh
poetry run python -c "import oragon; print(oragon.__version__)"
```

If `poetry install` says it cannot find a matching `oragon`, your platform or
Python version is not supported yet (see the table above).

`oragon doctor` reports what the machine has and what it can run:

```sh
poetry run oragon doctor
```

### Without Poetry

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install "oragon>=0.1.2" openai
```

Then leave `poetry run` off every command below.

## 2. Get access to N-ATLaS

NCAIR publishes the model on Hugging Face behind a terms page.

1. Create a Hugging Face account, or sign in.
2. Open <https://huggingface.co/NCAIR1/N-ATLaS> and accept the terms shown
   there.
3. Go to *Settings → Access Tokens* and create a token with **read** access.
4. Put it where Oragon will find it:

```sh
export HF_TOKEN=hf_your_token_here
```

Keep the token out of your code and out of version control.

## 3. Import the model

```sh
poetry run oragon import NCAIR1/N-ATLaS
```

This does three things, and shows progress for each:

1. **Downloads NCAIR's official checkpoint** — four weight files, 15 GB in
   total, each verified against the checksum Hugging Face publishes.
2. **Converts it** into the single-file format the engine reads, carrying
   over the model's own tokenizer and chat template unchanged.
3. **Optimizes it** from full precision to a 4.9 GB file suited to a
   processor, and deletes the 15 GB download.

When it finishes it prints where the file is and the name to use:

```text
imported. Use it as model="N-ATLaS": client.chat.generate(model="N-ATLaS", messages=[...])
```

The model lives in Oragon's model folder (`~/.local/share/oragon/models` on
macOS and Linux), not in your project.

### If the import stops

| What you see | What to do |
|---|---|
| `answered 401` or `403` | The token is missing, or its account has not accepted the model's terms. Repeat step 2. |
| Not enough disk space | The check runs before the download starts. Free the space it asks for and run the command again. |
| The connection drops | Run the same command again. The download starts over, so use the most reliable connection you have. |

## 4. Check that it works

See the exact prompt N-ATLaS will be given. The first line should say the
model's own template is being executed, and the prompt should begin with
`<|begin_of_text|>` and contain the two date lines:

```sh
poetry run oragon template N-ATLaS
```

```text
template-source: the model's own template (tokenizer.chat_template), executed

--- rendered prompt (44 tokens) ---
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Cutting Knowledge Date: December 2023
Today Date: 10 Oct 2026

You are a helpful assistant.<|eot_id|><|start_header_id|>user<|end_header_id|>
...
```

Then ask it something:

```sh
poetry run python examples/01_chat.py
```

Every run spends its first 10 to 17 seconds loading the model before it
answers.

## Running with no internet

Once the model is imported, nothing in this repository needs a connection. To
make sure the SDK never tries to reach one:

```sh
export ORAGON_AUTO_DOWNLOAD=0
```

To set up a machine that has never been online, import the model on a
connected machine and copy the one file,
`~/.local/share/oragon/models/N-ATLaS-q4_k_m.gguf`, to the same folder on the
other machine.
