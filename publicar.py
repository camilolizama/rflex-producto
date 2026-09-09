"""Genera la variante PUBLICABLE del mapa a partir de la completa.

La completa (mapa_tickets_v3.5.N.html) lleva incrustada la foto del 4-sep:
25.314 asuntos, 2.977 personas con correo y el MRR de 119 instancias. Sirve
para abrir en el equipo sin red. NO puede ir a GitHub Pages: Pages es publico
aunque el repo sea privado, y la foto se lee con "Ver la foto" o con
ver-codigo-fuente, sin login.

La publicable es el mismo HTML con SNAPSHOT = null: solo dato vivo, con sesion
@rflex.cl, via mapa_payload(). Sin foto no hay nada que leer sin entrar.

Uso (sin shebang a proposito: corre con `py` en Windows):
    py publicar.py <completa.html> <publicable.html>
    py publicar.py mapa_tickets_v3.5.0.html rflex-producto/mapa/index.html
"""
import sys, pathlib, re

if len(sys.argv) != 3:
    sys.exit(__doc__)
src_path, dst_path = map(pathlib.Path, sys.argv[1:3])
html = src_path.read_text(encoding='utf-8')

# 1. la foto: la linea completa `const SNAPSHOT = {...};` pasa a null
i = html.index('const SNAPSHOT = ')
j = html.index('\n', i)
assert html[i:j].rstrip().endswith('};'), 'no encontre el cierre del SNAPSHOT'
quitados = j - i
html = (html[:i]
        + 'const SNAPSHOT = null; // version publicada: sin foto incrustada, solo dato vivo con sesion'
        + html[j:])

# 2. el comentario de arriba deja de ser cierto
html = html.replace(
    '// Foto incrustada: respaldo cuando no hay sesión ni red. Es el dato del v3.4.4.\n',
    '// Sin foto incrustada en esta variante (ver publicar.py).\n', 1)

# 3. el loader: sin foto, el boton se esconde y el camino "foto" avisa en vez de romper
old = "  const usarFoto = motivo => arrancar(SNAPSHOT, 'foto', { motivo });\n  $('gFoto').onclick = () => usarFoto('elegida a mano');\n"
new = ("  const usarFoto = motivo => {\n"
       "    if (!SNAPSHOT){ gateMsg('Esta versi\\u00f3n publicada no lleva foto incrustada: el dato solo se ve con sesi\\u00f3n.'); return }\n"
       "    arrancar(SNAPSHOT, 'foto', { motivo });\n"
       "  };\n"
       "  $('gFoto').onclick = () => usarFoto('elegida a mano');\n"
       "  if (!SNAPSHOT) $('gFoto').style.display = 'none'; // no basta hidden: .gbtn{display:flex} le gana al [hidden] del navegador\n")
assert html.count(old) == 1, 'el loader cambio: revisar el parche 3'
html = html.replace(old, new)

# 4. el texto del caso "sin clave" prometia la foto
html = html.replace(
    "Puedes ver la foto incrustada.');",
    "' + (SNAPSHOT ? 'Puedes ver la foto incrustada.' : 'Esta variante no lleva foto.') + '');", 1)

# 5. documento completo. El HTML nacio como artifact (claude.ai le ponia el
#    esqueleto al publicar) y arranca directo en <title>. Servido por Pages
#    necesita doctype (modo estandar), charset y viewport propios. Y que los
#    buscadores no lo indexen: la pagina es publica, el dato no.
def envolver(h):
    if h.lstrip().lower().startswith('<!doctype'):
        return h
    assert h.startswith('<title>') and h.count('</style>') == 1, 'estructura inesperada'
    cab = ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
           '<meta name="robots" content="noindex,nofollow">\n')
    h = cab + h.replace('</style>', '</style>\n</head>\n<body>', 1)
    return h.rstrip() + '\n</body>\n</html>\n'
html = envolver(html)

# 6. controles: nada de la foto puede quedar
for patron in (r'"personas":\[\[', r'"mrr":\d{5,}', r'"subj":\['):
    assert not re.search(patron, html), f'quedo rastro de la foto: {patron}'
if re.search(r"supabaseAnonKey:\s*''", html):
    print('AVISO: CONFIG.supabaseAnonKey sigue vacia; la publicable no podra leer nada')

dst_path.parent.mkdir(parents=True, exist_ok=True)
dst_path.write_text(html, encoding='utf-8')
print(f'ok {dst_path}  {len(html):,} bytes  (foto quitada: {quitados:,} bytes)')
