"""Assemble src/app.html + src/cartes.json en un seul fichier HTML autonome."""
import json, pathlib, sys
root = pathlib.Path(__file__).parent
cartes = json.loads((root / "src/cartes.json").read_text(encoding="utf-8"))
blob = json.dumps(cartes, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
app = (root / "src/app.html").read_text(encoding="utf-8").replace("/*CARTES*/", blob)
head, body = app.split("</style>", 1)
page = ('<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + head + "</style>\n</head>\n<body>" + body + "</body>\n</html>\n")
(root / "dist").mkdir(exist_ok=True)
(root / "dist/index.html").write_text(page, encoding="utf-8")  # page d'accueil du site en ligne
import shutil
for f in (root / "public").glob("*"):
    shutil.copy(f, root / "dist" / f.name)
if len(sys.argv) > 1:  # version sans squelette, pour une page publiée
    pathlib.Path(sys.argv[1]).write_text(app, encoding="utf-8")
n = sum(len(v) for k in ("verites", "actions") for v in cartes[k].values())
g = sum(len(v) for k in ("verite", "action") for v in cartes["gages"][k].values()) + len(cartes["gages"]["coeur"])
c = sum(len(v) for v in cartes["coeur"].values())
print(f"{n} vérités/actions, {g} gages, {c} cartes cœur ouvert -> dist/index.html")
