---
name: polish-page
description: Run a structured UI polish pass on an HTML file. Checks contrast, focus states, keyboard navigation, reduced-motion, touch targets.
argument-hint: <file-path>
disable-model-invocation: true
---

# Polish Page

Audit $ARGUMENTS against these rules:

1. **Contrast**, WCAG AA (4.5:1 body, 3:1 large text)
2. **Focus states**, every interactive element must have a visible focus ring
3. **Keyboard navigation**, no mouse-only flows; tab order is logical
4. **Reduced motion**, animations wrapped in `@media (prefers-reduced-motion: no-preference)`
5. **Touch targets**, interactive elements >= 44x44px on mobile viewports
6. **Typography hierarchy**, consistent with the design-system skill

Output format:
- Structured list: file:line · severity (critical/high/medium) · one-line finding · one-line fix
- Auto-fix the safe ones (missing focus rings, reduced-motion wrappers)
- Report the rest for the team to decide

End with a summary: total findings by severity and an overall score (1-10).
