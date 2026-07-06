---
name: persistent-drawer-and-appbar
description: Build an application shell — a persistent navigation drawer plus a minimal app bar — in any stack. Use when adding or reworking site-wide navigation, building an app bar or top bar, adding a side drawer or nav rail, making a collapsible mini-rail menu, or when a crowded top nav needs its routing moved into a drawer.
---

An app **shell** is the **chrome** that outlives navigation: it renders once and every route paints inside it. Its spine is a division of labour — the **app bar** carries identity, the **drawer** owns routing, and neither moves under the user as they navigate. Hold that division; the rest is mechanics.

## Build order

1. **Carve the shell.** Render three regions around the app: **app bar** (top), **drawer** (side), and a main region for the page. *Done when* every route paints inside the shell and no page draws its own navigation.
2. **Strip the app bar.** Leave identity (the logo) and one link home; push every other link into the drawer. *Done when* the app bar holds identity and home and nothing else — no route link survives outside the drawer.
3. **Drop the drawer to a rail.** Collapse it to an icons-only **rail** as the floor state; each item is icon + label. *Done when* the rail is usable with labels hidden and every item still carries an accessible name.
4. **Wire rail → peek → pinned.** Hover or focus expands to **peek**; one toggle **pins** it open; both restore labels. *Done when* peek overlays without moving content, the toggle pins and unpins, and `aria-expanded` tracks the pinned state.
5. **Inset by the rail.** Offset the app bar and main region by the **rail** width — never the expanded width. *Done when* peeking never reflows the page and only pinning (on wide viewports) insets content.
6. **Mark the current route.** Receive the active route from the router and highlight its item. *Done when* the matching item reads as **current** on every route and the drawer computes nothing itself.
7. **Exclude the chrome.** Remove the shell and reset the inset on print and full-bleed surfaces. *Done when* those surfaces show no shell and no leftover inset.

## The three states

One model, three rungs — the drawer is always in exactly one:

- **rail** — collapsed, icons only, labels hidden. The resting state on narrow viewports and the floor everywhere.
- **peek** — hover/focus expansion that **overlays** content and forgets itself when the pointer leaves. Transient.
- **pinned** — explicit, sticky expansion from the toggle. On wide viewports it **insets** (pushes) content; on narrow it overlays. Persist it across reloads if the user pinned it.

The cut between **peek** and **pinned** is memory: peek forgets, pinned remembers.

## The inset law

Inset the page by the **rail** width, not the expanded width. **peek** and **pinned**-on-narrow **overlay**; only **pinned**-on-wide **insets**. Break this and the page lurches sideways under the pointer on every hover — the signature shell bug.

## Accessibility

- An icon-only **rail** item is not a nameless one: keep its accessible name when the label is visually hidden.
- The pin toggle owns `aria-expanded` and is the drawer's only control — that restraint is what keeps the **app bar** to identity and home.
- Offer a skip link to the main region; run focus order app bar → drawer → main.
- An overlaying drawer closes on `Esc` and never traps focus it shouldn't.

## Failure modes

- **Reflow-on-hover** — the page is inset by the expanded width, so **peek** shoves it sideways. Inset by the **rail**.
- **Crowded bar** — links or actions creep back into the **app bar**. The drawer owns routing; the bar owns identity. The restraint is load-bearing.
- **Nameless rail** — icon-only items the screen reader can't announce. Keep the label for assistive tech even when it is hidden for sighted users.
- **Orphan chrome** — the shell bleeds into print or a full-bleed page, or its inset is left behind. Exclude and reset on those surfaces.
- **Recomputed current** — the drawer derives the active route itself. Pass **current** down from the router instead.

## Naming

Name components, classes, and states after the words above — `app-bar`, `drawer`, `rail`, `peek`, `pinned`, `inset`, `current`. Shared language across your prompts, code, and this skill makes the agent reach for the same behaviour every time.

Worked example (Django + Tailwind): `django/custom-addons/tinkuy-app/docs/skills/tinkuy-ui-navigation/SKILL.md`.
