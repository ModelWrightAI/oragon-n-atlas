# Validation with external beta testers

The challenge asks Developer Infrastructure entries to be tried by at least
two external beta testers. This folder holds the plan, the form each tester
fills in, and their reports.

**Status: testing in progress. No reports are filed here yet.** Reports are
added to [`reports/`](reports/) as testers return them, unedited.

## Who counts as a tester

A developer who is **not** on our team and did not help build this, working
on **their own machine**, following only what is written in this repository.
If they have to ask us how to do something, that is a finding, and it goes in
their report.

## What a tester does

About an hour, most of it waiting for the model to download.

1. Follow [`docs/setup.md`](../docs/setup.md) from the top, on your own
   machine. Note anything unclear, wrong or missing.
2. Run `poetry run python examples/01_chat.py` and confirm you get an answer
   in Hausa.
3. Run `poetry run python examples/02_four_languages.py`.
4. Run `poetry run python benchmarks/speed.py --save my-machine.json`.
5. Run `poetry run python evidence/template_check.py --save my-check.json`.
6. Start `poetry run oragon serve N-ATLaS`, open `http://127.0.0.1:8080/` in a browser,
   and ask the model two or three questions in a Nigerian language you speak.
7. Fill in [`feedback-form.md`](feedback-form.md).

## What a tester sends back

- The completed feedback form.
- `my-machine.json` and `my-check.json` from steps 4 and 5.
- If anything failed: the full error text and the output of
  `poetry run oragon doctor`.

## How reports are filed

One folder per tester under [`reports/`](reports/), named for the tester and
the date, holding their form and their two JSON files exactly as received.
Testers are named with their permission; one who prefers not to be named is
listed by role and location instead ("backend developer, Kano").

A summary table is added here once reports are in:

| Tester | Machine | Setup worked first time | Tokens per second | Defines the word (of 10) | Main problem reported |
|---|---|---|---|---|---|
| *none yet* | | | | | |
