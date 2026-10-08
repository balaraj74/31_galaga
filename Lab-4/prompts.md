# PES UNIVERSITY — DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING
## Software Engineering Lab (UE24CS242) — Lab 4: VibeCoding
**Student Name:** Mohith N  
**SRN:** PES1UG24CS580  
**Semester & Branch:** 4th Semester, B.Tech CSE  
**Assigned Repository:** `https://github.com/SETAPESU26/31_galaga`  
**Lab Repository:** `https://github.com/Mohith-1502/SE-LAB-PES1UG24CS580`  
**Date:** October 8, 2026  

---

## Executive Summary & Objectives

The goal of this laboratory assignment is to leverage **Vibe Coding** with AI pair-programming assistants to diagnose, debug, and implement advanced features in a Python/Pygame-based retro arcade game (`Galaga`). The core requirements include:
1. Identifying and fixing mathematical/algorithmic defects under strict prompt-budget limits (under 3–4 prompts).
2. Implementing 3 feature hooks (`enemy_tint`, `on_wave_start`, `shield_charges`) left blank in the starter codebase.
3. Capturing 10+ seconds of video gameplay before and after changes.
4. Structuring individual atomic commits for each task without submitting PRs to the upstream repository.
5. Exporting full chat history and deliverables to the Lab repository under the `Lab-4` directory.

---

## Iterative Vibe Coding Log & Prompts

### Prompt 1: Task 1 — Bug Fix: Cubic Bézier Curve Trajectory Overshoot
- **Objective:** Fix the enemy entry and dive curves noticeably overshooting and bulging mid-flight.
- **Root Cause Analysis:** In the mathematical definition of a cubic Bézier curve, the Bernstein polynomial basis functions are:
  $$B(t) = (1-t)^3 P_0 + 3(1-t)^2 t P_1 + 3(1-t) t^2 P_2 + t^3 P_3$$
  In `game.py`, the third term was written as `3 * u * t * p2[0]` instead of `3 * u * t^2 * p2[0]`. Because the exponent of $t$ was 1 instead of 2, the weights failed to sum to 1 ($u^3 + 3u^2 t + 3ut + t^3 \neq 1$), causing excessive deviation and bulging in the middle of paths.
- **Prompt:**
```text
In game.py, examine the bezier(p0, p1, p2, p3, t) function. Enemy entry and dive paths overshoot and bulge unnaturally mid-flight even though endpoints match. Compare the four weighted terms against the standard cubic Bézier formula:
B(t) = (1-t)^3*P0 + 3*(1-t)^2*t*P1 + 3*(1-t)*t^2*P2 + t^3*P3
Fix the missing exponent on t in the third term for both x and y coordinates.
```
- **Outcome:** Corrected `3 * u * t * p2[0]` to `3 * u * t * t * p2[0]` (and identically for y). Enemies now enter along smooth, graceful curves without clipping or bulging.
- **Git Commit:** `9981dca fix: correct cubic bezier curve calculation in bezier()`

---

### Prompt 2: Task 2 — Feature: Implement `enemy_tint(kind)` for Wave-Based Recoloring
- **Objective:** Implement the `enemy_tint(kind)` hook called in `Game.draw()` to give enemies distinct, vibrant palettes that scale with the wave progression.
- **Design:** Created wave-specific color palettes (`WAVE_PALETTES`) mapping each enemy type (`"boss"`, `"red"`, `"blue"`) to cyber-arcade color sets (Neon Emerald / Golden / Cyber Magenta for bosses; Crimson / Vivid Orange / Amber for reds; Electric Cyan / Indigo / Azure for blues).
- **Prompt:**
```text
Implement enemy_tint(kind) in game.py. The function receives kind ("boss", "red", or "blue") and should return an (r, g, b) color tuple or None. Recolor enemies dynamically based on the current wave number so that subsequent waves look visually distinct and challenging.
```
- **Outcome:** Added `WAVE_PALETTES` and dynamically indexed using `current_wave`. Enemies now switch color themes seamlessly on each new wave.
- **Git Commit:** `43c6005 feat: implement enemy_tint() for dynamic wave-based enemy recoloring`

---

### Prompt 3: Task 3 — Feature: Implement `on_wave_start(wave)` Stage Announcement Banner
- **Objective:** Implement `on_wave_start(wave)` called during `spawn_wave(wave)` to announce wave transitions with arcade flair.
- **Design:** Stored the active wave in `current_wave` and initialized a timed banner `wave_banner = {"text": f"STAGE {wave} - READY", "timer": 2.2}`. Decremented the timer in `Game.update()` and rendered a styled arcade banner with dark blue background and gold border centered on screen.
- **Prompt:**
```text
Implement on_wave_start(wave) in game.py. It is called when a wave spawns. When invoked, track the wave number and show a retro arcade "STAGE <wave> - READY" announcement banner for 2 seconds in the center of the screen with a golden border and timed fadeout.
```
- **Outcome:** Integrated stage banner system in `on_wave_start`, `Game.update`, and `Game.draw`. Displays crisp stage banners whenever a new wave begins or resets.
- **Git Commit:** `26ae4e6 feat: implement on_wave_start() with stage announcement banner`

---

### Prompt 4: Task 4 — Feature: Implement `shield_charges(wave)` & Visual Energy Shield
- **Objective:** Implement `shield_charges(wave)` to grant hit absorption charges each wave, and add visual feedback so the player knows their shield status.
- **Design:** Granted 1 shield charge at wave 1, scaling by +1 charge every 3 waves (`1 + (wave - 1) // 3`). Enhanced `Game.draw()` to display `Shield {self.shield}` on the top HUD and draw a glowing cyan energy bubble around the player ship while charges remain.
- **Prompt:**
```text
Implement shield_charges(wave) in game.py to grant 1 shield charge at wave 1 plus 1 additional charge every 3 waves. In Game.draw(), display the current shield charges on the HUD and draw an active cyan energy shield ring around the player ship when shield charges are greater than zero.
```
- **Outcome:** Returns `1 + (wave - 1) // 3`. When player absorbs enemy lasers or diving enemies, the shield absorbs the hit, grants brief invulnerability, and visibly depletes with accurate HUD and ring indicators.
- **Git Commit:** `cf4085c feat: implement shield_charges() and visual energy shield aura`

---

## Deliverables Summary

| Deliverable | Location in Lab Repository | Description |
|---|---|---|
| **Before Video** | `Lab-4/before.mp4` | 15s recording of gameplay showing cubic Bézier trajectory overshooting bug and unassigned features. |
| **After Video** | `Lab-4/after.mp4` | 15s recording of gameplay showing fixed Bézier curves, stage banner, dynamic enemy recoloring, and active energy shield. |
| **Updated Code** | `Lab-4/code/` & `game.py` | Complete working source code with all 4 tasks implemented. |
| **Chat History Doc** | `Lab-4/PES1UG24CS580_Lab4_VibeCoding_ChatHistory.docx` | Formatted Word document containing complete Vibe Coding prompt interactions. |
| **Chat History PDF** | `Lab-4/PES1UG24CS580_Lab4_VibeCoding_ChatHistory.pdf` | Formatted PDF document export of the prompt engineering and pair programming history. |
