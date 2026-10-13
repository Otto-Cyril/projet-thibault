# Juste nous deux

Jeu de cartes pour couple : vérités, actions, gages et « Cœur ouvert ».

## Fichiers

- `dist/` : le site publié par Netlify (`index.html`, manifest, icônes), généré par `python3 build.py`.
- `assets/` : manifest et icônes de l'appli.
- `src/cartes.json` : toutes les cartes. Pour en ajouter, on édite ce fichier puis on relance le build.
- `src/app.html` : l'interface et la logique (HTML, CSS, JavaScript sans framework).
- `build.py` : assemble `src/` et `assets/` dans `dist/`. Lancer `python3 build.py` après chaque modification des cartes.

## Format des cartes

- `@E` au début : seulement quand on est ensemble.
- `@A` au début : seulement en appel vidéo.
- `#20` à la fin : affiche un chrono de 20 secondes.
- `~M` au début : carte musique (love, R&B, chansons à chanter ensemble).

## Fonctionnement

- Tirage sans répétition : chaque paquet (type + intensité + contexte) est vidé avant d'être remélangé, et ce qui a été vu est gardé dans le `localStorage` du téléphone, même après fermeture.
- Le gage suit la carte esquivée : même type, même intensité, même contexte.
- Le joueur désigné est celui qui a eu le moins de cartes, au hasard en cas d'égalité.

## Version 2

- Ambiance qui change selon l'intensité : lueur verte en Soft, ambrée en Medium, violette en Cœur ouvert, et tout l'écran passe en rouge nuit en Hot.
- Animations par catégorie : flammes pour les vérités, étincelles pour les actions, cœurs pour Cœur ouvert, petits diables pour les gages, bisous et roses en plus en Hot.
- Mode Crescendo (remplacé en version 4 par la jauge « 🌡 Auto »).
- Tirage qui s'adapte : 2 esquives sur les 4 dernières cartes proposent de redescendre, 8 cartes sans esquive proposent de monter.
- Glisser la carte : à droite pour une nouvelle carte, à gauche pour passer. Vibration au tirage, écran gardé allumé pendant la partie.

## Version 3 et 4

- Cartes lumineuses (bord animé, halo, reflet), manette Vérité · dé · Action, pastilles de couleur par joueur.
- Jauge de température : « ✓ Fait ! » (ou glisser à droite) fait monter la jauge, plus si la carte est hot ; esquiver la refroidit de 6°. En mode « 🌡 Auto », plus la jauge est haute, plus le tirage a de chances d'être hot (tirage pondéré, donc toujours une part de surprise). À 100° : une carte récompense qui rapproche le couple, puis la jauge repart à zéro.
- Cartes musique love et R&B (Tayc, Dadju, Chris Brown, The Weeknd, SZA, Beyoncé…), avec duos à chanter.
- Public visé : 18-27 ans.

## Jouer sur deux téléphones

« 📱📱 Jouer à deux » : un téléphone crée une partie (code de 5 caractères), l'autre le tape. L'état de la partie (carte, jauge, scores, prénoms, réglages) est envoyé à l'autre téléphone à chaque action via Supabase Realtime Broadcast, sans table ni base de données. Les clés **publiques** sont dans `src/config.json`. Pour tester sans Supabase, ouvrir deux onglets avec `#local` à la fin de l'URL.

« Partager » ouvre la feuille de partage du téléphone par-dessus l'appli et envoie un lien `?partie=CODE` qui fait rejoindre la partie directement. Le système coupe la connexion quand on passe sur une autre appli : au retour au premier plan (ou quand le réseau revient), l'appli rouvre un canal neuf, réessaie seule en cas d'échec, et l'hôte renvoie l'état de la partie dès que l'autre téléphone réapparaît. La partie en cours est mémorisée, même si le téléphone ferme l'onglet.

## Pistes pour la suite

1. Ajouter un service worker pour que l'appli marche hors connexion une fois installée.
2. Sortir les cartes dans une API Symfony (entités `Carte`, `Couple`, `Partie`) avec un front Angular, pour jouer chacun sur son téléphone et partager les cartes perso.

## Mises à jour automatiques

`build.py` écrit l'empreinte de la page dans `dist/version.json`. Quand on revient dans l'appli, elle compare cette empreinte à la sienne et se recharge toute seule si une nouvelle version est en ligne ; la partie, la jauge, la carte en cours et la partie à deux sont gardées. Pendant qu'on joue, un petit message « Mettre à jour » s'affiche au lieu de couper la partie.

## Version 5 : design

- Écran d'accueil (première ouverture) qui sert aussi de réglages via la roue ⚙ : prénoms, avatars emoji (partagés en mode deux téléphones), ensemble ou en appel, deux téléphones, thème.
- Écran de jeu compact : intensité, jauge, carte, « Fait » et « Je passe », manette ; tout tient au-dessus de la barre d'onglets, même sur iPhone SE.
- Thème sombre par défaut, thème clair au choix. Thèmes de Cœur ouvert sur un seul rang qui défile.
