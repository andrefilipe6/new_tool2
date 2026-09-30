# Icon canvas (source)

Source of the "Sysadmin Icon Pack" design canvas: https://claude.ai/artifact/2LE4G7SDBiwfV657ei1EA7

| Artboard | Contents |
|---|---|
| `Main.dc.html` | platform-tools sysadmin icons: outline, 24px grid, `currentColor` |
| `Ducks.dc.html` | the same tools as outlined rubber ducks |
| `DucksFlat.dc.html` | the same tools as flat ducks (yellow silhouette on blue) |
| `Game.dc.html` | game icons: medals, trophies, cards, decks, attacks, potions, heal |
| `MiniGame.dc.html` | mini-game: Patavra do Dia, Quackiz do Dia, Reciclagem, Baralho Raro |
| `Talents.dc.html` | talent tree: 3 rows, 10 talents |
| `Abilities.dc.html` | 9 abilities with Valor / Arref. / Nível mín. slots |
| `FrontDuck.dc.html` | front-facing comic mascot + 4 expressions |

Each icon is inline SVG. `{{duck}}` and `{{bg}}` are the canvas tweak colours (defaults `#FFEB1A` and `#1D5FB5`); replace them when extracting an icon for production. The Google Fonts links are for the mockup only; production pages self-host fonts.
