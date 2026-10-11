"""Measure N-ATLaS on this machine: load time, time to first word, tokens/s.

    poetry run python benchmarks/speed.py                 # processor only
    poetry run python benchmarks/speed.py --gpu           # let the engine use a GPU if present
    poetry run python benchmarks/speed.py --save benchmarks/results/my-machine.json

N-ATLaS must be on this machine first: `poetry run oragon import NCAIR1/N-ATLaS`
(see docs/setup.md).

Run it with nothing else heavy running: another program using the processor
or the memory shows up directly in these numbers.
"""

import argparse
import json
import os
import platform
import statistics
import subprocess
import sys
import time

import oragon
from oragon import Engine, Oragon, Settings, system, user

MODEL = "N-ATLaS"
SYSTEM = (
    "you are a large language model trained by Awarri AI technologies. "
    "You are a friendly assistant and you are here to help."
)
SETTINGS = Settings(temperature=0.1, repeat_penalty=1.12, max_tokens=200, seed=0)

NOT_IMPORTED = (
    "N-ATLaS is not on this machine yet. Import it once with:\n\n"
    "    poetry run oragon import NCAIR1/N-ATLaS\n\n"
    "That needs a Hugging Face token with access to the model; "
    "docs/setup.md has the steps."
)

QUESTIONS = {
    "hausa": "menene ake nufi da gwagwarmaya",
    "yoruba": "Báwo ni o ṣe máa ṣàlàyé ohun tí ọ̀rọ̀ 'ìfẹ́' túmọ̀ sí?",
    "igbo": "Kedu ihe bụ ọdịnala ndị Igbo? Kọwaa nkenke.",
    "english": "In two sentences, what is jollof rice?",
}


def processor_name() -> str:
    """The processor as its maker names it, where the system will say."""
    try:
        if platform.system() == "Darwin":
            return subprocess.check_output(
                ["sysctl", "-n", "machdep.cpu.brand_string"], text=True
            ).strip()
        with open("/proc/cpuinfo", encoding="utf-8") as f:
            for line in f:
                if line.lower().startswith("model name"):
                    return line.split(":", 1)[1].strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return platform.processor() or platform.machine()


def memory_gb() -> int:
    return round(os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 1024**3)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--gpu", action="store_true", help="allow a GPU if one is present")
    parser.add_argument("--save", metavar="FILE", help="also write the results as JSON")
    args = parser.parse_args()

    try:
        client = Oragon(engine=Engine.EMBEDDED, model=MODEL, cpu=not args.gpu, warm_prompt=SYSTEM)
    except FileNotFoundError:
        sys.exit(NOT_IMPORTED)
    rows = []
    try:
        # The engine starts on first use. One tiny request makes the load time
        # its own number instead of part of the first answer's.
        started = time.perf_counter()
        client.chat.generate(
            model=MODEL,
            messages=[system(SYSTEM), user("hi")],
            settings=Settings(max_tokens=1),
        )
        load = time.perf_counter() - started

        for name, question in QUESTIONS.items():
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
                    first_word = first_word or time.perf_counter() - started
                else:
                    reply = chunk
            total = time.perf_counter() - started
            tokens = reply.usage.completion_tokens
            rows.append(
                {
                    "question": name,
                    "first_word_s": round(first_word, 2),
                    "tokens": tokens,
                    "tokens_per_s": round(tokens / (total - first_word), 1),
                }
            )
    finally:
        client.close()

    result = {
        "oragon": oragon.__version__,
        "model": MODEL,
        "processor_only": not args.gpu,
        "machine": f"{platform.system()} {platform.machine()}",
        "processor": processor_name(),
        "memory_gb": memory_gb(),
        "load_s": round(load, 1),
        "mean_tokens_per_s": round(statistics.mean(r["tokens_per_s"] for r in rows), 1),
        "mean_first_word_s": round(statistics.mean(r["first_word_s"] for r in rows), 2),
        "questions": rows,
    }

    print(f"oragon {result['oragon']}  |  {MODEL}  |  {result['machine']}")
    print(f"{result['processor']}, {result['memory_gb']} GB memory")
    print(f"mode: {'processor only' if not args.gpu else 'GPU allowed'}")
    print(f"model loaded in {result['load_s']}s\n")
    print(f"{'question':<10}{'first word':>12}{'tokens':>9}{'tokens/s':>11}")
    for r in rows:
        print(f"{r['question']:<10}{r['first_word_s']:>11.2f}s{r['tokens']:>9}{r['tokens_per_s']:>11.1f}")
    print(f"{'mean':<10}{result['mean_first_word_s']:>11.2f}s{'':>9}{result['mean_tokens_per_s']:>11.1f}")

    if args.save:
        with open(args.save, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\nsaved to {args.save}")


if __name__ == "__main__":
    main()
