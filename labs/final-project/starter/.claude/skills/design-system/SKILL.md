---
name: design-system
description: The visual design system for this quiz app, color tokens, typography, spacing, animation rules. Use whenever writing or editing HTML, CSS, templates, or any user-facing markup.
user-invocable: false
---

# Design System: Quiz Night Default

> Replace this with your team's chosen theme.

## Color tokens

```css
--color-bg: #0a0a0f;
--color-surface: #16161f;
--color-accent: #ff4d5e;
--color-text: #f5f5f7;
--color-muted: #8a8a99;
```

## Typography

- Display: `"Space Grotesk", sans-serif`, 600 weight, -0.02em tracking
- Body: `"Inter", sans-serif`, 400 weight
- Mono: `"JetBrains Mono", monospace`

## Spacing rhythm

4px base, multiples of 4 only.

## Animation

- Respect `prefers-reduced-motion: reduce`
- Default transition: 180ms cubic-bezier(0.2, 0.8, 0.2, 1)
- No bouncy springs unless the user has explicitly asked

## Do / Never

- **DO:** use CSS variables, semantic HTML, visible focus rings
- **NEVER:** inline styles, generic `text-gray-500` without a token, animations without reduced-motion fallback
