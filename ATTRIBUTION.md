# Attribution and asset notice

## Source material

This repository is an **unofficial, educational Python/pygame port** of the example programs
in:

> **Jazon Yamamoto**, *Black Art of Multiplatform Game Programming*.

It is not affiliated with, endorsed by, or sponsored by the author or the publisher. The
book's text, design and original C++ source code remain the property of their respective
copyright holders. Please buy the book for the full explanations. This port is meant as a
companion to it, not a replacement.

## Media assets

The media files in this repository were reproduced from the book's companion example files
so that the ported programs run exactly like the originals. They include:

| Type | Format | Where |
|------|--------|-------|
| Images, sprite sheets, bitmap fonts | `.bmp` | `ChNN/*/graphics/` |
| Sound effects and piano notes | `.wav` | `Ch05/5_1_sound_effects/notes/`, `ChNN/*/audio/` |
| Music | `.mp3` | `Ch05/5_2_music_files/audio/`, `Ch06/*/audio/`, `Ch07/*/audio/` |
| TrueType fonts | `.ttf` | `Ch03/3_8_outline_fonts/fonts/`, `Ch06/*/graphics/`, `Ch07/*/graphics/`, `Ch08/8_3_fonts/graphics/` |

**These assets are not covered by any licence granted for this repository's own code.**
All rights remain with their original authors and copyright holders:

- **Graphics, sounds and music:** © their original creators, as distributed with
  *Black Art of Multiplatform Game Programming*.
- **Fonts** (`Alfphabet.ttf` / `alfphabet.ttf`, `brick.ttf`, `bbrick.ttf`): third-party
  typefaces distributed with the book's examples. Each remains under its own author's
  licence terms. Check those terms before reusing a font outside this project.

They are included **solely for non-commercial, educational purposes**, so that learners can
run each example as the book presents it. If you redistribute or build on this repository,
replace these assets with your own or with openly licensed ones (for example from
[OpenGameArt.org](https://opengameart.org/) or [Kenney.nl](https://kenney.nl/assets)).

## Python port

The Python source files (`*.py`) are an independent re-implementation of the book's
examples using [pygame](https://www.pygame.org/) (LGPL). pygame itself is not
redistributed here; install it from PyPI (see `requirements.txt`).

## Takedown

If you are a rights holder and would like any material removed or credited differently,
please [open an issue](https://github.com/kpillai2017/black_art_pygame/issues) and it will
be dealt with promptly.
