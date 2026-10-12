# Contributing

Thank you for helping improve Oragon for N-ATLaS.

## What this licence covers

The code, examples and documentation in this repository are released under
the [MIT licence](LICENSE). This repository contains no N-ATLaS weights;
those are published by NCAIR on Hugging Face under their own terms. The
Oragon SDK and engine are installed from PyPI under their own licence.

## Reporting a problem

Open an issue and include:

- what you ran, and what you expected to happen;
- what actually happened, with the full error text;
- the output of `poetry run oragon doctor`.

Problems with the docs count too. If a step was unclear or you had to guess,
please tell us.

## Suggesting a change

1. Fork the repository and create a branch from `main`.
2. Keep each change small and focused. If behaviour changes, update the
   matching file in `docs/` in the same pull request.
3. Before opening a pull request, run the examples you touched and
   `poetry run python evidence/template_check.py` to confirm N-ATLaS still
   receives its own prompt format.
4. Open a pull request that says what changed and why.

## Adding examples

New examples are welcome, especially ones in Hausa, Yoruba or Igbo, or ones
that show N-ATLaS inside a real application. Keep them short, use the
settings in `docs/usage.md`, and close the client in a `finally` block as the
existing examples do.

## Beta testing

To test the toolkit as an external developer, follow
[`validation/README.md`](validation/README.md) and send back the feedback
form with your results.

## Conduct

Be respectful and constructive. We want this to be a welcoming place for
developers across Nigeria and beyond.

## Contact

hello@oragonlabs.com
