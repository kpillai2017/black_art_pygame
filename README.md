# Black Art, Pygame Edition

*Learning game programming from first principles: a Python/pygame port of Jazon Yamamoto's
**Black Art of Multiplatform Game Programming***

> **Who this is for:** you know basic Python (functions, loops, classes) and want to know how
> games actually work underneath: how pixels reach the screen, why every game has a loop,
> how sprites animate, and how a pile of global variables grows into a reusable game engine.
>
> **How to use it:** work through the folders in order. Each one is a small, runnable program
> that adds one idea to the previous one. Read the explanation here, run the program, read the
> code, then try the exercises. Changing working code is how this stuff sticks.

---

## Table of contents

1. [About the book and this port](#1-about-the-book-and-this-port)
2. [Getting set up](#2-getting-set-up)
3. [How to run an example](#3-how-to-run-an-example)
4. [The big picture: what every game does](#4-the-big-picture-what-every-game-does)
5. [The learning path, chapter by chapter](#5-the-learning-path-chapter-by-chapter)
   - [Chapter 2: First pixels and the game loop](#chapter-2--first-pixels-and-the-game-loop)
   - [Chapter 3: Drawing: pixels, shapes, sprites, animation, text, timing](#chapter-3--drawing-pixels-shapes-sprites-animation-text-timing)
   - [Chapter 4: Input: events vs. polling](#chapter-4--input-events-vs-polling)
   - [Chapter 5: Sound effects and music](#chapter-5--sound-effects-and-music)
   - [Chapter 6: Your first complete game (Pong)](#chapter-6--your-first-complete-game-pong)
   - [Chapter 7: Game states (Breakout)](#chapter-7--game-states-breakout)
   - [Chapter 8: Building a reusable game engine](#chapter-8--building-a-reusable-game-engine)
6. [From C++/SDL to Python/pygame: a translation guide](#6-from-csdl-to-pythonpygame-a-translation-guide)
7. [Code-reading challenges: spot the quirks](#7-code-reading-challenges-spot-the-quirks)
8. [Where to go next](#8-where-to-go-next)
9. [Glossary](#9-glossary)

---

## 1. About the book and this port

*Black Art of Multiplatform Game Programming* (Jazon Yamamoto) teaches 2D game programming in
**C++ with SDL** (Simple DirectMedia Layer), a thin, cross-platform layer over the screen,
keyboard, mouse and sound card. The book deliberately avoids big engines. You build everything
yourself, so you understand it.

This repository re-implements the book's examples in **Python using pygame**. pygame is itself
a wrapper around SDL, so almost every SDL concept in the book maps directly onto a pygame call.
That makes this port a good way to:

- learn the **concepts** without fighting C++ memory management and build systems, and
- see **how idioms change** when you move from a low-level language to a high-level one (see
  [section 6](#6-from-csdl-to-pythonpygame-a-translation-guide)).

**Status:** this is a *partial* port covering the book's foundations (Chapters 2–8), from
opening a window up to a small object-oriented engine with a game-state stack. Later chapters
are not ported yet; see [Where to go next](#8-where-to-go-next).

**Folder naming:** `ChNN/N_M_topic/` means *Chapter N, listing M*. For example,
`Ch03/3_5_animation` is the fifth example in Chapter 3.

---

## 2. Getting set up

You need **Python 3** and **pygame 2**. The pinned versions are:

| Tool    | Version | Where it's pinned  |
|---------|---------|--------------------|
| Python  | 3.13.3  | `.envrc`           |
| pygame  | 2.6.1   | `requirements.txt` |

```bash
cd black_art_pygame
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -c "import pygame; print(pygame.version.ver)"   # should print 2.6.1
```

---

## 3. How to run an example

Every example loads its images and sounds with **relative paths** such as
`graphics/background.bmp`. Paths are resolved from your *current working directory*, so
**always `cd` into the example's folder before running it**:

```bash
cd Ch03/3_5_animation
python 3_5_animation.py
```

Chapter 8 examples are split into modules and start from `main.py`:

```bash
cd Ch08/8_7_game_states
python main.py
```

Press **Esc** or close the window to quit (most examples support both).

> **Why not fix the paths?** It's a good exercise. Try building paths from
> `os.path.dirname(os.path.abspath(__file__))` so an example runs from any directory.

---

## 4. The big picture: what every game does

Almost every real-time game, from Pong to a modern 3D title, has this shape:

```text
initialise ──►┌──────────────────────────────┐
              │ 1. handle input (events)     │
              │ 2. update the world (logic)  │◄── the GAME LOOP,
              │ 3. draw the world (render)   │    runs ~30–60×/second
              │ 4. present the frame (flip)  │
              │ 5. wait to keep a steady FPS │
              └──────────────┬───────────────┘
                             ▼ (player quits)
                     free resources & exit
```

Keep this diagram in mind. Each chapter zooms in on one box:

| Box in the loop | Chapter(s) |
|-----------------|-----------|
| Initialise / free | 2, 8 |
| Handle input | 4, 8.4 |
| Update | 3 (movement, animation), 6–7 (game logic, collisions) |
| Draw | 3, 8.1–8.3 |
| Sound | 5, 8.5 |
| Frame timing | 3.9, 8.6 |
| Deciding *which* loop runs (menus, pause…) | 7, 8.7 |

### Two ideas you'll meet everywhere

**The back buffer (double buffering).** You never draw directly onto the visible screen.
You draw onto an off-screen image, the *back buffer*, and when the frame is finished you
**flip** it onto the screen in one go. That stops the player seeing half-drawn frames
(flicker). In pygame, `pygame.display.set_mode(...)` returns the back buffer and
`pygame.display.flip()` presents it.

**The coordinate system.** `(0, 0)` is the **top-left** corner. `x` grows to the right and
`y` grows **downwards**. All examples use an 800 × 600 window.

---

## 5. The learning path, chapter by chapter

Each listing below has:
- **Concept**: the one idea it introduces
- **Look for**: the lines worth reading closely
- **Try it**: exercises, roughly from easy to hard

### Chapter 2: First pixels and the game loop

#### `2_2_image`: Show an image, then exit
**Concept:** the smallest possible pygame program: initialise, open a window, load an image,
**blit** it (copy its pixels) onto the back buffer, flip, wait three seconds, quit.

**Look for:**
- `pygame.image.load(...)` followed by `.convert()`. `convert()` reformats the image to match
  the screen's pixel format so later blits are fast. Forgetting it is a classic performance
  bug.
- `backbuffer.blit(image, (0, 0))`: "copy `image` onto `backbuffer` at x=0, y=0".

**Try it:** draw the image at a different position. Draw it twice. What happens if you
remove `pygame.display.flip()`?

#### `2_3_game_loop`: Your first game loop
**Concept:** replace "wait 3 seconds" with a `while` loop that keeps running until the player
quits. `program_is_running()` drains the **event queue** and returns `False` on `QUIT` or Esc.

**Look for:** the background is drawn **once**, before the loop, but the sprite is drawn
every frame at a random spot. That's why sprites pile up on screen.

**Try it:**
1. Move the background blit *inside* the loop. Why does there now only ever appear to be one
   sprite? (This is the "clear and redraw every frame" model that all later examples use.)
2. Change `pygame.time.delay(100)` to `10` and to `1000`. What are you actually controlling?

> `Ch03/blank_window.py` is an even smaller "Hello World" window. `Ch03/test.py` is an older
> camelCase draft of `2_3_game_loop` and needs that example's `graphics/` folder to run.

### Chapter 3: Drawing: pixels, shapes, sprites, animation, text, timing

#### `3_1_pixel_plot`: Plotting single pixels
**Concept:** everything on screen is ultimately pixels. `draw_pixel()` **locks** the surface
(on some hardware you must lock video memory before touching it directly), bounds-checks,
writes one pixel, and unlocks.

**Try it:** draw a horizontal line using only `draw_pixel` in a loop. Then a diagonal line.
(You've just discovered why line-drawing algorithms such as Bresenham's exist.)

#### `3_2_rectangles`: Outlined and filled rectangles
**Concept:** primitive shapes. `pygame.draw.rect` with a width of `1` draws an outline; with
no width it fills.

**Try it:** the random x position uses `% 600` while the window is 800 wide. Spot it, then
fix it using a constant instead of a magic number.

#### `3_3_moving_image`: Motion
**Concept:** **movement is just changing a position a little every frame.** The sprite's
`x` grows by 5 per frame and wraps back to `-200` when it leaves the screen.

**Look for:** the redraw order: background first (erases the last frame), then the sprite.

**Try it:** make the ship move diagonally. Make it bounce off the edges by flipping the sign
of a velocity variable (`vx = -vx`). You'll reuse this exact trick for the Pong ball.

#### `3_4_color_key`: Transparency with a color key
**Concept:** sprites are rectangles, but ships aren't. A **color key** marks one color as
"don't draw this". The book uses **magenta `(255, 0, 255)`** because it almost never appears
in real art. See `set_colorkey((255, 0, 255))` in `load_image()`.

**Try it:** compare with `3_3`. The ship there has a magenta box around it. Comment out
`set_colorkey` here to watch it come back.

#### `3_5_animation`: Sprite-sheet animation and scrolling
**Concept 1, sprite sheets:** all frames of an animation live in **one image**, laid out in a
grid. `draw_image_frame()` works out which rectangle to copy:

```python
columns = image_width / frame_width
src_x   = (frame %  columns) * frame_width    # column within the grid
src_y   = (frame // columns) * frame_height   # row within the grid
```

**Concept 2, animation speed vs. frame rate:** `frame_counter`/`frame_delay` advance the
animation only every few game frames, so the demon doesn't flap at 50 fps.

**Concept 3, infinite scrolling:** the background is drawn **twice**, at `background_X` and
at `background_X + 800`, and wraps when it has scrolled one full width. That gives a seamless
loop.

**Try it:** open `graphics/demon.bmp` in an image viewer and match it to the arithmetic
above. Make the background scroll the other way. Add a second, slower background layer
(**parallax**).

#### `3_7_raster_fonts`: Text from a bitmap
**Concept:** a **raster font** is just a sprite sheet whose frames are characters in ASCII
order starting at space (code 32). Drawing text means drawing frame `ord(ch) - 32` for each
character. That's the same function as the animation example, reused.

**Try it:** what happens with a character the font image doesn't contain? Add a guard.

#### `3_8_outline_fonts`: TrueType text
**Concept:** **outline (vector) fonts** (`.ttf`) scale to any size and are rendered to a
surface on demand with `font.render(text, antialias, color)`. Flexible but slower than raster
fonts, so games often render static text once and cache it.

**Try it:** the counter text is re-rendered every frame. Cache the two static lines so
they're rendered only once.

#### `3_9_frame_rate`: Fixed frame rate
**Concept:** `3_5` waited a flat 20 ms per frame, so a slow computer ran the game slower.
This version measures how long the frame **took** and only sleeps for the **rest** of the
frame budget:

```python
FRAME_DELAY = 1000 / FPS          # e.g. 33.3 ms at 30 FPS
frame_start = pygame.time.get_ticks()
...update & draw...
frame_time = pygame.time.get_ticks() - frame_start
if frame_time < FRAME_DELAY:
    pygame.time.delay(int(FRAME_DELAY - frame_time))
```

**Try it:** show the measured FPS in the window caption. Then look up `pygame.time.Clock.tick()`,
which does all of this in one line. Also look up **delta time** (multiplying movement by
elapsed time), the other common approach.

### Chapter 4: Input: events vs. polling

There are two ways to ask "what is the player doing?":

| Style | How | Good for |
|-------|-----|----------|
| **Event-driven** | Read `pygame.event.get()` and react to `KEYDOWN`, `MOUSEBUTTONDOWN`… | One-off actions: jump, fire, pause, menu clicks |
| **Polled / buffered** | Ask each frame: `pygame.key.get_pressed()`, `pygame.mouse.get_pressed()` | Continuous actions: holding a key to move |

#### `4_1_event_mouse`: Mouse events
Left-click places one crosshair, right-click the other. `MOUSEMOTION` updates the window
title with the cursor position. **Look for** the `global` statement inside
`program_is_running()`, which is needed because the function assigns module-level variables.

#### `4_2_event_keyboard`: Keyboard events
Arrow keys move the ship, but **only once per key press**. Hold a key down and nothing
repeats. That's the limitation of pure events for movement.

#### `4_3_buffered_mouse`: Polling the mouse
Same crosshairs as `4_1`, but the buttons are **polled** with `pygame.mouse.get_pressed()`
every frame, so holding a button and dragging moves the crosshair continuously.

**Try it:** rewrite `4_2` using `pygame.key.get_pressed()` so holding an arrow key moves the
ship smoothly. Compare how it *feels*.

### Chapter 5: Sound effects and music

pygame splits audio in two:

| | `pygame.mixer.Sound` | `pygame.mixer.music` |
|-|-|-|
| What | Short clips loaded fully into memory | One long track **streamed** from disk |
| How many at once | Many, each on its own **channel** | One |
| Typical use | Explosions, beeps, footsteps | Background music |

#### `5_1_sound_effects`: A playable piano
Keys **A W S E D F T G Y H U J K** play a chromatic octave from C to high C, laid out like a
piano keyboard. Each note gets its own channel so chords work, and releasing a key stops its
channel. **Look for** `pygame.mixer.pre_init(22050, -16, 2, 1024)`: sample rate, 16-bit
signed samples, stereo, and buffer size. A smaller buffer means lower latency (good for a
piano) but more risk of crackling.

**Try it:** the key handling is a long `if/elif` chain. Replace it with a
`dict` mapping keys to note indices. You'll cut dozens of lines.

#### `5_2_music_files`: Streaming music
**Space** toggles play/pause, **Backspace** stops. **Look for** how `get_busy()` decides
whether Space means "start" or "pause/unpause".

### Chapter 6: Your first complete game (Pong)

#### `6_1_paddle_game`
Everything so far, combined into a game: **Up/Down** move your paddle (left), and an AI
paddle (right) chases the ball.

Read the functions in this order. It mirrors the game loop diagram:

1. `init_sdl()` → `load_files()` → `init_game()`: start-up
2. `update_player()`: polled input, clamped to the screen
3. `update_ai()`: the "AI" is a few lines: *move toward the ball's centre, but no faster than
   `ENEMY_SPEED`*. Because `ENEMY_SPEED` (7) is slower than the ball can travel, the AI can
   be beaten. **Tuning that one number is game design.**
4. `update_ball()`: movement, bouncing, scoring, sounds. On every bounce the ball gets a
   new **random** speed of up to `BALL_MAX_SPEED`.
5. `rect_overlap()`: **axis-aligned bounding box (AABB) collision**. Two rectangles overlap
   unless one is entirely left, right, above or below the other.
6. `run_game()` / `draw_game()`: one frame of update, then render everything

**Try it:**
- The random bounce speed feels unfair. Replace it with a ball that keeps its speed and
  speeds up slightly on every paddle hit, capped at `BALL_MAX_SPEED`.
- Make the bounce angle depend on *where* the ball hits the paddle. Edges send it off
  steeply. This one change makes Pong far more fun.
- Replace `rect_overlap()` with pygame's built-in `Rect.colliderect()`.

### Chapter 7: Game states (Breakout)

#### `7_1_paddle_game2`
A Breakout clone: **Left/Right** move the paddle, **Space** launches the ball, **Enter**
starts from the splash screen, **Esc** toggles pause (see `program_is_running()`), and
**Space** on the game-over screen returns to the splash.

**The new concept is the finite state machine.** A real game isn't one loop. It's a title
screen, then gameplay, then pause, then game over. This listing models that with an integer:

```python
GS_SPLASH, GS_RUNNING, GS_GAMEOVER, GS_PAUSED = 0, 1, 2, 3

def run_game():                 # pick the update for the current state
    if   game_state == GS_SPLASH:   update_splash()
    elif game_state == GS_RUNNING:  update_game()
    elif game_state == GS_GAMEOVER: update_game_over()
```

`draw_screen()` uses the same pattern for drawing. **Look for** how `GS_PAUSED` draws the
game *plus* a "paused" overlay, but doesn't update it. That's how freezing works.

Other things to study: the **block grid** built in `set_blocks()` (a 2D layout stored in a
1D list), the `is_locked` ball that sits on the paddle until launch, and `num_blocks_left()`
as a win condition.

**Try it:** draw the state machine on paper (states as circles, key presses as arrows).
Then add a "level cleared" state. Notice how every new state means editing *two* big
`if/elif` chains. Chapter 8.7 fixes that.

### Chapter 8: Building a reusable game engine

Chapters 2–7 copy-paste the same helpers (`load_image`, `draw_image_frame`,
`program_is_running`…) into every file, and keep everything in globals. Chapter 8
**refactors** them into classes, one subsystem at a time. Each folder is a **snapshot**,
which is why files repeat. Diff neighbouring folders to see exactly what each step added:

```bash
diff Ch08/8_3_fonts/graphics.py Ch08/8_4_input/graphics.py
```

| Step | New module(s) | What it wraps |
|------|---------------|---------------|
| `8_1_graphics` | `graphics.py` → `Graphics` | window, back buffer, `clear`, `draw_pixel`, `draw_rect`, `fill_rect`, `flip` |
| `8_2_image` | `image.py` → `Image` | loading, color key, drawing whole images or sprite-sheet frames |
| `8_3_fonts` | `raster_font.py`, `outline_font.py` | the two font techniques from Ch. 3 |
| `8_4_input` | `input.py` → `Input` | events **and** polling, in one place |
| `8_5_audio` | `audio.py`, `sound.py`, `music.py` | mixer start-up, sound clips, music stream |
| `8_6_game_engine` | `game.py` → `Game` | **the game loop itself** |
| `8_7_game_states` | `state.py`, `stack.py`, `splash_state.py`, `run_state.py` | a **stack of game states** |

#### The `Input` class (8.4): "down", "hit" and "up"
This class answers three different questions about a key or mouse button:

| Method | Question | Example use |
|--------|----------|-------------|
| `key_down(k)` | Is it **held** right now? | Move while holding → |
| `key_hit(k)` | Was it **pressed this frame**? | Jump, fire, menu select |
| `key_up(k)` | Was it **released this frame**? | Charge-and-release attacks |

"Hit" and "up" are **edge-triggered**. They're true for exactly one frame. `update()` clears
them at the start of each frame and the event loop refills them. This is the clean solution
to the events-vs-polling tension from Chapter 4.

#### The `Game` class (8.6): Template Method pattern
`Game.run()` owns the loop (input → `update()` → `draw()` → flip → frame delay). You never
rewrite it. You **subclass** `Game` and override the "hooks":

```python
class MyGame(Game):
    def init(self):   return self.init_system("My Game", 800, 600, False)
    def update(self): ...          # game logic
    def draw(self, g): ...         # rendering
    def free(self):   ...          # cleanup
```

`8_6_game_engine/main.py` runs the bare `Game`, a white window, to prove the skeleton works.

#### The state stack (8.7): states as objects
Instead of an integer and `if/elif` chains, each screen is a `GameState` object with its own
`update()` and `draw()`. A `StateManager` keeps them on a **stack** and only runs the top
one:

```text
push RunState      push SplashState         SplashState pops itself      RunState pops itself
┌───────────┐      ┌─────────────┐          ┌───────────┐                (stack empty →
│ RunState  │      │ SplashState │ ◄ active │ RunState  │ ◄ active        game ends)
└───────────┘      │ RunState    │          └───────────┘
                   └─────────────┘
```

In the demo the logo drops in with a sound. Press **Space/Enter/Esc** to pop the splash and
reveal the spinning gear, and **Esc** again to exit. A stack is natural for games: a pause
menu is just *push Pause*, and resuming is *pop*.

**Try it (capstone):** port the Chapter 7 Breakout game onto the 8.7 engine, with a
`SplashState`, a `PlayState`, a `PauseState` pushed on top of `PlayState`, and a
`GameOverState`. Compare the result with the original 500-line single file.

---

## 6. From C++/SDL to Python/pygame: a translation guide

This port preserves the book's structure, so you'll see C++ habits written in Python. That's
useful to recognise:

| In the book (C++/SDL 1.2) | In this port | More idiomatic Python/pygame |
|---------------------------|--------------|------------------------------|
| `SDL_SetVideoMode(800,600,32,SDL_SWSURFACE)` | `set_mode((800,600), SWSURFACE, 32)` | `set_mode((800, 600))`. The flags/depth are legacy and mostly ignored by SDL2. |
| `SDL_BlitSurface(src, &srcRect, dst, &dstRect)` | `dst.blit(src, (x, y), src_rect)` | same |
| `SDL_Flip(screen)` | `pygame.display.flip()` | same |
| `if (image == NULL) return false;` | `if not image: return False` | `pygame.image.load` **raises** an exception on failure; use `try/except`. |
| `SDL_FreeSurface(img)` | `free()` methods that do little | Python frees memory automatically; keep `free()` only for symmetry. |
| `rand() % 255` | `random.randint(0, 32767) % 255` | `random.randint(0, 255)` |
| function overloading | `def draw(self, x, y, *args)` + `len(args)` checks | default/keyword arguments, e.g. `draw(x, y, g, frame=None)` |
| global variables + `extern` | module globals + `global` | pass objects around, or use classes (as Chapter 8 does) |
| `SDL_Delay` frame timing | manual `get_ticks()`/`delay()` | `pygame.time.Clock().tick(FPS)` |
| header/implementation split | one module per class | same |

---

## 7. Code-reading challenges: spot the quirks

Real code has rough edges, and finding them is a valuable skill. Each of these is in the code
right now. Try to explain **why** it's a problem before fixing it.

1. **Colors that can't be white.** `random.randint(0, 32767) % 255` never produces `255`.
   Why? (Ch. 3, 8.1)
2. **A lock that's never released.** In `3_1_pixel_plot/draw_pixel()`, follow the code path
   for an off-screen pixel. Is the surface unlocked?
3. **Type hints that lie.** Several `program_is_running()` functions are annotated
   `-> None` but return a `bool`. Run `mypy` on one file and see what it reports.
4. **Unreachable error handling.** `if not background: return False` after
   `pygame.image.load(...)`: when can that branch run? (See section 6.) Rename an image file
   and see what actually happens.
5. **Running after failure.** In `8_6`/`8_7` `main.py`, what happens when `game.init()`
   returns `False`?
6. **Decorative decorators.** The Chapter 8 classes use `@dataclass` but define their own
   `__init__` and no annotated fields. What does `@dataclass` actually do here?
7. **A frame of lag.** In `Game.run()`, the `QUIT` check happens *before*
   `input.update()` reads new events. When does a close-window click actually take effect?
8. **An ignored asset.** `Ch08/8_4_input/.gitignore` and its siblings contain `*.bmp`. The
   existing images are already tracked, but what happens to the next sprite you add with
   `git add .`, and who will notice?

---

## 8. Where to go next

**Within this repo:**
- Do the **capstone** in 8.7: Breakout on the engine.
- Add `pygame.time.Clock`, delta-time movement and absolute asset paths to the engine.
- Write a tiny `pytest` suite for pure-logic pieces: `rect_overlap`, sprite-sheet frame
  arithmetic, and `Stack`.

**Continuing the book:** later chapters of *Black Art* build on this engine with larger
games and more advanced techniques. Porting them is the natural next step, and the patterns
here (subsystem classes, `Game` subclass, state stack) are the scaffolding they'll need.

**Further reading:**
- pygame docs: <https://www.pygame.org/docs/>
- Robert Nystrom, *Game Programming Patterns* (free online). Read the chapters *Game Loop*,
  *State*, *Update Method* and *Double Buffer* alongside Chapters 3, 7 and 8:
  <https://gameprogrammingpatterns.com/>
- Glenn Fiedler, "Fix Your Timestep!": the next step after `3_9_frame_rate`.

---

## 9. Glossary

| Term | Meaning |
|------|---------|
| **Surface** | pygame's in-memory image; the screen is a surface too |
| **Blit** | "block image transfer": copy pixels from one surface onto another |
| **Back buffer / double buffering** | draw off-screen, then show the whole frame at once to avoid flicker |
| **Flip** | present the back buffer on screen |
| **Game loop** | the repeating input → update → draw cycle |
| **Frame / FPS** | one pass of the loop / passes per second |
| **Sprite** | a movable 2D image (ship, ball, demon) |
| **Sprite sheet** | many animation frames packed into one image grid |
| **Color key** | a color (here magenta) treated as transparent |
| **Raster font** | characters stored as a bitmap sprite sheet |
| **Outline font** | scalable vector font (`.ttf`) rendered on demand |
| **Event** | a message from the OS: key pressed, mouse moved, window closed |
| **Polling** | asking for the current state of a device each frame |
| **Edge-triggered** | true only on the frame something *changes* (hit/up) |
| **Channel** | a mixer slot that plays one sound at a time |
| **AABB** | axis-aligned bounding box: the simplest rectangle collision test |
| **Finite state machine** | a program that is in exactly one of several named states at a time |
| **State stack** | states kept on a stack; only the top one runs |
| **Template Method** | a base class owns an algorithm and subclasses fill in the steps |

---

*Original book and design © Jazon Yamamoto. This port is an educational re-implementation in
Python; refer to the book for the full explanations and C++ source. The images, sounds, music
and fonts belong to their original copyright holders. See [ATTRIBUTION.md](ATTRIBUTION.md).*
