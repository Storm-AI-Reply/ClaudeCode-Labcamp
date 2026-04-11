---
description: Rewrite a template's HTML/CSS to match the visual identity in CLAUDE.md.
argument-hint: <file-path>
---

Restyle the file at: $ARGUMENTS

Steps:

1. Read `CLAUDE.md` and pull out the **Visual identity** section: palette,
   typography, animation rules. This is the source of truth, do not invent
   colors or fonts.
2. Read the target file. Understand its structure before touching it.
3. Rewrite the template so that:
   - All colors come from CSS variables declared in `src/static/style.css`
     (add the variables there if they don't exist yet).
   - Typography matches the display/body fonts from CLAUDE.md.
   - No inline `style="..."` attributes. No `<style>` blocks in the template.
   - Any animation respects `@media (prefers-reduced-motion: reduce)`.
   - Existing Jinja variables, form fields, and element IDs stay intact (the backend must keep working).
4. If you need to touch `src/static/style.css`, add new rules at the bottom
   under a clearly-labelled section for this template.
5. After editing, summarise in 2–3 bullets what you changed and why.

Hard constraints:
- Do **not** change any Python file.
- Do **not** write to `live/`.
- Do **not** change the route or the template path.
