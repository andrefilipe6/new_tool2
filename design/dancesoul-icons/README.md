# Dance Soul Academy — modality icons (`fi-*`)

Canvas: https://claude.ai/artifact/DxeAF7rQGGuWQNEJb9asSi

Two versions: `Main.dc.html` (outline, one colour) and `Filled.dc.html` (filled, brand pink `#E01060` + cyan `#40C0E0`, heads as rounded diamonds like the logo).

10 modality icons for dancesoulacademy.pt: `fi-ballet`, `fi-hiphop`, `fi-jazz`, `fi-contemporaneo`, `fi-salao`, `fi-latinos`, `fi-ginastica`, `fi-pilates`, `fi-fitness`, `fi-infantil`.

- 24×24 grid, single stroke (default 1.5, close to Bootstrap Icons' weight), `stroke="currentColor"`, round caps and joins.
- Animation is CSS only: each icon marks its moving part with an `a-*` class (`a-sway`, `a-pulse`, `a-shake`, `a-wave`, `a-blink`, `a-draw`, `a-lift`, `a-bob`, `a-bounce`). Keyframes are in the `<style>` block of `Main.dc.html`.
- Modes: `.m-loop` (always), `.m-hover` (animate while the card is hovered), off. `prefers-reduced-motion: reduce` switches everything off.
- `{{stroke}}` and `{{accent}}` are canvas tweaks; replace with the real values when extracting to the site's SVG sprite.
- UI, contact and social icons stay on Bootstrap Icons (`bi-*`).
