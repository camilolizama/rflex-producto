# rflex.producto

Portal de herramientas de inteligencia de producto de rFlex. HTML estático servido por GitHub Pages; el dato vive en Supabase y solo se lee con sesión de una cuenta **@rflex.cl** (Supabase Auth con Google, restringido al Workspace, y guardia en la base: `mapa_payload()` exige `@rflex.cl` en el JWT).

**Las páginas son públicas, el dato no.** Por eso a este repo no entra nada que lleve dato: ni los `.sql` que siembran dimensiones (MRR por cliente), ni la variante del mapa con la foto incrustada. El `.gitignore` lo hace cumplir; `publicar.py` genera la variante publicable del mapa (sin foto) a partir de la completa.

| Ruta | Qué es |
|---|---|
| `index.html` | El portal: lista de herramientas |
| `mapa/index.html` | Mapa de tickets v3.5.x, variante publicable (solo dato vivo) |
| `publicar.py` | `py publicar.py <completa.html> mapa/index.html` |

Publicar = `git push` a `main`. Settings → Pages → rama `main`, carpeta `/ (root)`.
