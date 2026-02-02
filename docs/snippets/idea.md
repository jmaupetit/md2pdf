---
pdf:
    title: md2pdf idea
---

# `md2pdf` idea :bulb:

In [publishing](https://www.wikiwand.com/en/Publishing) and [graphic
design](https://www.wikiwand.com/en/Graphic_design), **lorem ipsum** (derived
from Latin *dolorem ipsum*, translated as "pain itself") is a [filler
text](https://www.wikiwand.com/en/Filler_text) commonly used to demonstrate the
graphic elements of a document or visual presentation. [^1]

## Text

A common form of *lorem ipsum* reads:

> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
> tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
> quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
> consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
> cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
> proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

----

Inline styles support **strong**, *Emphasis*, `code`, <u>underline</u>,
~~strikethrough~~, emojis (*e.g.* `:rocket:` rendered as :rocket:), $`\LaTeX`$,
X^2^, H~2~O, ==highlight==, [Link](typora.io).

## Images

<!--![md2pdf logo](https://github.com/jmaupetit/md2pdf/raw/main/assets/md2pdf-logo.png) --> 


## $`\LaTeX`$ formulas

```math
f(x) = \int_{-\infty}^\infty
    \hat f(\xi)\,e^{2 \pi i \xi x}
    \,d\xi
```

## Tables

| Left-Aligned  | Center Aligned  | Right Aligned |
| :------------ | :-------------: | ------------: |
| col 3 is      | some wordy text |         $1600 |
| col 2 is      |    centered     |           $12 |
| zebra stripes |    are neat     |            $1 |


## Lists

1. ordered list item 1.
2. ordered list item 2.
   + sub-unordered list item 1.
   + sub-unordered list item 2.
     + [x] something is DONE.
     + [ ] something is not TODO.


## Code

```python
def parse_config(config: str) -> dict:
    """Parse configuration input as a JSON string."""
    try:
        parsed = json.loads(config)
    except json.decoder.JSONDecodeError as err:
        raise ValidationError(
            "Invalid input configuration string (should be valid JSON)"
        ) from err
    return parsed
```

## Table of content

[TOC]

[^1]: *Forked* from https://en.wikipedia.org/wiki/Lorem_ipsum
