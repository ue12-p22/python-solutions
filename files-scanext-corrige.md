---
jupytext:
  cell_metadata_filter: all,-hidden,-heading_collapsed,-run_control,-trusted
  notebook_metadata_filter: all, -jupytext.text_representation.jupytext_version, -jupytext.text_representation.format_version,
    -language_info.version, -language_info.codemirror_mode.version, -language_info.codemirror_mode,
    -language_info.file_extension, -language_info.mimetype, -toc
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
language_info:
  name: python
  nbconvert_exporter: python
  pygments_lexer: ipython3
nbhosting:
  title: lister les fichiers *.truc
---

# lister les fichiers *.truc

+++

en 2022 tous les calculs/parcours sur le contenu du disque, dossiers, fichiers, et métadonnées telles que tailles, dates, etc... se font avec le couteau suisse `pathlib`

```{code-cell} ipython3
from pathlib import Path
```

(et non plus avec `os.path` et autres `glob` comme on aurait pu le faire dans le passé)

+++

## exercice v1

* écrire une fonction qui prend en paramètre un nom de dossier (une str)
* et une extension (une str aussi), par exemple `truc`
* parcourt tous les fichiers dans ce dossier (ou ses sous-dossiers) avec cette extension (i.e. de la forme `*.truc`)
* et qui affiche (avec print) pour chacun d'eux
  * le nom complet (à partir de la racine du disque dur), sa taille et la date/heure de dernière modification
  * la première ligne

* **en option**, on peut avoir envie de trier les fichiers par nom

+++

### exemples

+++

```bash
# exemple d'appel
In [11]: scanv1("/Users/Jean Dupont/cours-python/", "py")
File /Users/Jean Dupont/cours-python/notebooks/bidule.py
  2663 B last modified on 2022-05-15 15:06:22
  first line: def bidule(arg1, arg2):
File /Users/Jean Dupont/cours-python/notebooks/machin.py
  2663 B last modified on 2022-08-21 21:09:12
  first line: # la fonction machin doit faire un tri
<etc...>
```

+++

```bash
# un autre exemple: on cherche dans le dossier courant
# qui ici se trouve être le même; on affiche quand même
# les chemins complets
In [12]: scanv1(".", "py")
File /Users/Jean Dupont/cours-python/notebooks/bidule.py
  2663 B last modified on 2022-05-15 15:06:22
  first line: def bidule(arg1, arg2):
File /Users/Jean Dupont/cours-python/notebooks/machin.py
  2663 B last modified on 2022-08-21 21:09:12
  first line: # la fonction machin doit faire un tri
<etc...>
```

+++

### indices

+++

certains traits qu'on peut avoir envie d'utiliser:

```{code-cell} ipython3
# créer une instance de Path
# qui correspond au dossier courant
p = Path(".")
```

```{code-cell} ipython3
# avec resolve() je peux calculer le chemin complet pour arriver
# à un objet Path (en partant de la racine des fichiers)
p.resolve()
```

```{code-cell} ipython3
# les méta données
#        taille
#                      date de dernière modification
p.stat().st_size,   p.stat().st_mtime
```

```{code-cell} ipython3
# st_mtime retourne un 'epoch' 
# c'est-à-dire un nombre de secondes 
# depuis le 1er janvier 1970

# pour traduire ça en date 'lisible'
from datetime import datetime as DateTime

dt = DateTime.fromtimestamp(p.stat().st_mtime)
f"la date est {dt}"
```

vous aurez aussi besoin de voir la documentation du module `pathlib` pour la méthode `Path.glob()`

```{code-cell} ipython3
# à vous de jouer
def scanv1():
    pass
```

```{code-cell} ipython3
# prune-cell

from pathlib import Path
from datetime import datetime as DateTime

# comme toujours c'est juste *une* façon de faire hein...
def scanv1(folder, extension):
    # on convertit la chaine en Path
    # pour pouvoir utiliser la librairie
    path = Path(folder)
    # pour la variante il suffit d'ajouter:
    #              ↓↓↓↓↓↓↓
    # for child in sorted(path.glob(f"**/*.{extension}")):
    for child in path.glob(f"**/*.{extension}"):
        # avec resolve() on obtient le chemin canonique
        print(f"File {child.resolve()}")
        # la taille et l'heure de modification sont accessibles au travers
        # de la méthode stat()
        # on arrondit à la seconde
        modif_timestamp = int(child.stat().st_mtime)
        human_readable = DateTime.fromtimestamp(modif_timestamp)
        print(f"  {child.stat().st_size} B last modified on {human_readable}")
        # pour lire seulement la première ligne
        # on pourrait faire un for + break
        # mais c'est plus élégant comme ceci
        with child.open() as feed:
            print("  first line:", next(feed), end="")
```

## exercice v2

vous insérez le code de la v1 dans un programme python `scan.py` qu'on peut lancer depuis le terminal, par exemple comme ceci

```bash
$ python scan.py /Users/Jean Dupont/cours-python py
File /Users/Jean Dupont/cours-python/notebooks/bidule.py
  2663 B last modified on 2022-05-15 15:06:22
  first line: def bidule(arg1, arg2):
File /Users/Jean Dupont/cours-python/notebooks/machin.py
  2663 B last modified on 2022-08-21 21:09:12
  first line: # la fonction machin doit faire un tri
<etc...>
```

+++

prune-cell

dans le fichier `scan.py`, ajouter les lignes

```python
# le lanceur
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("path")
parser.add_argument("ext")
args = parser.parse_args()

scanv1(args.path, args.ext)
```

+++

## exercice v3

idem mais on a plus de choix pour décrire la ou les extensions qui nous intéressent; le paramètre extension peut maintenant être
  * vide (tous les fichiers)
  * ou une chaine simple
  * ou une liste d'extensions (ou même plus généralement un *itérable* d'extensions)

```{code-cell} ipython3
# à vous de jouer
def scanv3():
    pass
```

```python
# exemple d'appel
scanv3(Path.home() / "flotpython-exos/", 
       ("py", "md"), recursive=True)
```

```{code-cell} ipython3
:tags: [raises-exception]

# prune-begin

def scanv3(folder, extensions=None):
    pattern = "**/*"
    # la gestion des extensions est du coup assez différente
    for child in path.glob(pattern):
        # à ce stade, child est un Path aussi
        ext = child.suffix[1:]
        # on regarde s'il y a lieu d'ignorer ce fichier
        if extensions is not None:
            if isinstance(extensions, str):
                if ext != extensions:
                    continue
            else:
                if ext not in extensions:
                    continue
        # le reste est comme dans la v1
        print(f"File {child.resolve()}")
        print(f"  {child.stat().st_size} B last modified on {child.stat().st_mtime}")
        with child.open() as feed:
            print("  first line:", next(feed), end="")
```

je vous laisse à titre d'exercice corriger quelques défauts résiduels:

* les fichiers de taille nulle posent problème (pour le `next(feed)`)
* les fichiers binaires posent problème (pareil)

pour arranger ça il faut être un peu plus soigneux

+++

***
