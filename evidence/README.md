# Evidence: how we know N-ATLaS runs correctly on Oragon

Running a model is easy to claim and easy to get subtly wrong. This page
records what we checked, what we found, and how to repeat each check.

Everything here was measured on one machine: an Apple M4 MacBook with 16 GB
of memory, **processor only**, on 10 and 11 October 2026. The model file was
made from NCAIR's official checkpoint with `oragon import NCAIR1/N-ATLaS`.

## 1. It is N-ATLaS, from NCAIR's checkpoint

`oragon import NCAIR1/N-ATLaS` downloads the four weight files NCAIR
publishes and checks each against the SHA-256 that Hugging Face lists for it.
The import log records them:

| File | Size | SHA-256 (first 16 characters) |
|---|---|---|
| `model-00001-of-00004.safetensors` | 4.6 GiB | `59c6c87e4cbe8787` |
| `model-00002-of-00004.safetensors` | 4.7 GiB | `3d087dd3d4db2c54` |
| `model-00003-of-00004.safetensors` | 4.6 GiB | `3384248a6cb07e82` |
| `model-00004-of-00004.safetensors` | 1.1 GiB | `84a0714c20eb0d2b` |

Checkpoint revision: `e294476928aca9030e924ca27bb8e085e8581273`.

No other model is involved. The file the engine loads is that checkpoint,
converted and reduced in precision, with its tokenizer and chat template
carried over unchanged.

## 2. It is given the prompt it was trained on

N-ATLaS's reference code builds its prompt with the template stored in the
model. That template starts with a start-of-text token and writes two date
lines into the system turn:

```text
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Cutting Knowledge Date: December 2023
Today Date: 10 Oct 2026

you are a large language model trained by Awarri AI technologies. ...<|eot_id|>
```

Oragon runs that template, so N-ATLaS receives exactly this prompt. You can
print it yourself and compare it with what NCAIR's code produces:

```sh
poetry run oragon template N-ATLaS
```

The first line of the output says
`template-source: the model's own template (tokenizer.chat_template), executed`.

### The test

One Hausa question, "menene ake nufi da gwagwarmaya" (what is meant by
"gwagwarmaya", struggle), asked ten times with ten different seeds, at
NCAIR's reference settings (temperature 0.1, repetition penalty 1.12, the
Awarri system prompt). We count how many answers define the word, and how
many instead begin by repeating the question's own words back
("Ake nufi da gwagwarmaya na iya bambanta...").

**Oragon 0.1.2 defines the word in 10 of 10 runs.**

A typical answer:

> Gwagwarmaya na nufin kokarin da ake yi don cimma wani buri, shawo kan
> kalubale, ko shawo kan matsaloli. Yana dauke da jajircewa, sadaukarwa, da
> kuma yunƙurin samun nasara duk da wahala ko ƙalubale.

All ten answers are in
[`results/oragon-0.1.2.json`](results/oragon-0.1.2.json). To repeat it:

```sh
poetry install
poetry run python evidence/template_check.py
```

### What this test is and is not

It is a check on the opening words of an answer, chosen because it is simple
and anyone can repeat it. It is one question in one language. It shows that
N-ATLaS on Oragon defined the word in every one of ten seeded runs; it is
not a measure of how good N-ATLaS is at Hausa. That needs
fluent readers and many more questions.

## Does the smaller file cost quality?

The imported file stores about 4 bits per value where the checkpoint stores
16. We built three precision levels from the same checkpoint and ran the same
ten-seed test on each:

| Precision | File size | Defines the word | Tokens per second |
|---|---|---|---|
| **Q4_K_M** (the default) | 4.9 GB | 10 of 10 | **14.6** |
| Q5_K_M | 5.7 GB | 10 of 10 | 11.4 |
| Q8_0 | 8.5 GB | 10 of 10 | 6.5 (see note) |

The answers were nearly word for word the same across the three, so on this
test the smallest file gives up nothing and is the fastest.

Note on Q8_0: the 16 GB test machine ran short of memory during that run, so
6.5 is lower than a machine with more memory would give. It would still be
slower than Q4_K_M, because more data is read for every token.

To build the other levels yourself (each import prints the model name to
use for the file it made):

```sh
poetry run oragon import NCAIR1/N-ATLaS --quant q5_k_m
poetry run oragon import NCAIR1/N-ATLaS --quant q8_0
```

## 3. Speed on a processor

From [`benchmarks/speed.py`](../benchmarks/speed.py); our output is
[`benchmarks/results/apple-m4-16gb-cpu.json`](../benchmarks/results/apple-m4-16gb-cpu.json).

| | |
|---|---|
| Time to load the model | 10 to 17 seconds, once per run |
| Time to the first word | 0.2 to 0.7 seconds |
| Writing speed | 14.2 tokens per second (mean of four questions) |

## 4. Answers in four languages

Six questions asked on 10 October 2026; four of
them are the ones in
[`examples/02_four_languages.py`](../examples/02_four_languages.py). The
readings below are ours and we are not native speakers of Hausa, Yoruba or
Igbo; treat them as a first pass.

| Question | Result |
|---|---|
| Hausa: what does "gwagwarmaya" mean? | A clear definition |
| English: what is jollof rice, in two sentences? | Correct, two sentences |
| Yoruba: explain what "ìfẹ́" (love) means | Coherent and on topic |
| Hausa: what does "zaman lafiya" (peace) mean? | On topic, but describes it as a period in history |
| Igbo: what are Igbo traditions, briefly? | A concise list of customs |
| Translate "Good morning, how did you sleep?" into all three | **Wrong in all three** |

The translation result is a limit of the model, not of how it is run. The
three translations used
general greetings (Yoruba "Ẹ n lẹ́", Hausa "Assalamu alaikum") or the wrong
time of day (Igbo "Ezi ehihie", good afternoon).

## What we have not shown

- Quality across many questions, or judged by native speakers.
- Speed on machines other than the one above. Run the benchmark on yours.
- Anything about N-ATLaS's speech recognition, which this work does not use.
