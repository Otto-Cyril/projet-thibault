"""Assemble src/app.html + src/cartes.json en un seul fichier HTML autonome."""
import json, pathlib, sys
root = pathlib.Path(__file__).parent
cartes = json.loads((root / "src/cartes.json").read_text(encoding="utf-8"))
blob = json.dumps(cartes, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
app = (root / "src/app.html").read_text(encoding="utf-8").replace("/*CARTES*/", blob)
# Clés publiques Supabase pour le mode deux téléphones (src/config.json, facultatif).
cfg_file = root / "src/config.json"
cfg = json.loads(cfg_file.read_text(encoding="utf-8")) if cfg_file.exists() else {}
app = app.replace("/*SUPABASE_URL*/", cfg.get("supabase_url", "")).replace("/*SUPABASE_KEY*/", cfg.get("supabase_anon_key", ""))
head, body = app.split("</style>", 1)
page = ('<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + head + "</style>\n</head>\n<body>" + body + "</body>\n</html>\n")
# Le site publié par Netlify : dist/ (page + manifest + icônes).
import shutil
dist = root / "dist"
dist.mkdir(exist_ok=True)
# Empreinte de la page : l'appli la compare à dist/version.json pour se mettre à jour toute seule.
import hashlib
version = hashlib.sha256(page.encode("utf-8")).hexdigest()[:12]
page = page.replace("/*VERSION*/", version)
(dist / "index.html").write_text(page, encoding="utf-8")
(dist / "version.json").write_text(json.dumps({"v": version}) + "\n", encoding="utf-8")
for name in ("manifest.webmanifest", "icon.svg", "icon-180.png", "icon-512.png"):
    shutil.copy(root / "assets" / name, dist / name)
shutil.copytree(root / "assets/vendor", dist / "vendor", dirs_exist_ok=True)  # supabase-js, chargé seulement en mode deux téléphones
if len(sys.argv) > 1:  # version sans squelette, pour une page publiée
    pathlib.Path(sys.argv[1]).write_text(app, encoding="utf-8")
n = sum(len(v) for k in ("verites", "actions") for v in cartes[k].values())
g = sum(len(v) for k in ("verite", "action") for v in cartes["gages"][k].values()) + len(cartes["gages"]["coeur"])
c = sum(len(v) for v in cartes["coeur"].values())
print(f"{n} vérités/actions, {g} gages, {c} cartes cœur ouvert -> dist/index.html")
