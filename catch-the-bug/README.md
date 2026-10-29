# catch-the-bug

A tiny typing-stats module with a few bugs and some genuinely messy code. Your
job is to point your multi-agent review panel at it, add a **Fixer** agent that
acts on what the reviewers find, and get the checks to pass.

## The module

`typing_stats.py` computes stats for a typing test:

- `count_words(text)` how many words were typed
- `wpm(text, seconds)` typing speed in words per minute
- `accuracy(typed, target)` percentage of characters typed correctly
- `summarize(typed, target, seconds)` a one-line summary of all three

## Your goal

1. Review `typing_stats.py` with your performance and readability reviewers.
2. Add a **Fixer** agent that reads the reviewers' findings and the failing
   tests, applies the fixes, and re-runs until everything is green.
3. Run the qualifier:

   ```bash
   pip install -r requirements.txt
   python verify.py
   ```

   `verify.py` has two gates:
   - **Behavior:** the 4 tests in `tests/` must pass (the logic bugs are fixed).
   - **Panel findings:** the perf/readability issues the reviewers flag must
     actually be gone (the Fixer applied their review, not just patched logic).

   When both gates pass, `verify.py` prints a completion code. Show that code,
   plus your panel's review output, to a workshop host to claim your gift.

## Rules

- Do not edit the tests or `verify.py`. Fix the module, not the checks.
- The correct behavior is defined by the tests in `tests/`.
