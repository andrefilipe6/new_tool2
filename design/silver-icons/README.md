# Silver Surf Culture — icons (`si-*`)

Canvas: https://claude.ai/artifact/49YMq5rrwaF1MepdsDFpCx

Same system as `design/dancesoul-icons`: 24×24, two-tone through classes (`.fp .fs .fw .sp .ss .sw`, vars `--ip --is --iw`), CSS-only animation (loops by default; `m-hover` / `m-loop` / off, `prefers-reduced-motion`). Brand: navy `#1F4566` + sand `#E9C46A` (header text `#F2D9A0`). Motif: the wave from the active-menu underline, plus round accents.

| Artboard | Contents |
|---|---|
| `Main.dc.html` | 15 navigation / tool icons + a mock of the real backoffice header, Ferramentas menu, greeting buttons and empty state |
| `Surf.dc.html` | 14 surf icons for the public site (lessons, boards, rentals, sea conditions, camp) |
| `Actions.dc.html` | 25 action icons replacing `bi-*`; Dance Soul geometry with circle accents |

`build.py` regenerates the three artboards (reads the Dance Soul actions for the shared geometry). The real logo was not available, so the mock shows a `[logótipo]` placeholder.
