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
  title: manipulation simple sur une adresse IP
---

# analyse adresse IP

+++

## le problème

+++

Une adresse IP v4 se présente sous la forme d'une chaine contenant 4 octets (de 0 a 255 donc) en décimal séparés par des `.`

```{code-cell} ipython3
# exemples

IP_1 = "192.168.0.9"
IP_2 = "138.96.19.1"
```

## v0

+++

On vous demande d'écrire une fonction qui transforme cette donnée (une chaine donc) en une liste de 4 entiers

```
# remarquez bien l'absence de quotes (') dans le résultat
>>> ip_v0(IP_1)
[192, 168, 0, 9]
```

```{code-cell} ipython3
# à vous
def ip_v0():
    pass
```

```{code-cell} ipython3
# devrait retourner True
ip_v0(IP_1) == [192, 168, 0, 9]
```

```{code-cell} ipython3
# devrait retourner True
ip_v0(IP_2) == [138, 96, 19, 1]
```

## v1

+++

Même analyse, mais le retour est un entier dans l'espace $[0..2^{32}-1]$

So j'appelle $b_0$, $b_1$, $b_2$, $b_3$ les 4 valeurs retournées par `ip_v0`, le résultat ici sera obtenu avec la formule

$I = b_0.2^{24} + b_1*2^{16} + b_2*2^8 + b_3$

```{code-cell} ipython3
# à vous
def ip_v1():
    pass
```

```{code-cell} ipython3
# devrait retourner True
ip_v1(IP_1) == 0xc0a80009
```

```{code-cell} ipython3
# devrait retourner True
ip_v1(IP_2) == 0x8a601301
```

## astuce

+++

Comment faire ces calculs facilement de manière interactive ?

```{code-cell} ipython3
# les différents morceaux de ip_v0 valent ceci
hex(192), hex(168), hex(0), hex(9)
```

```{code-cell} ipython3
# ça veut dire que le résultat final doit être ceci
0xc0a80009
```

---

```{code-cell} ipython3
# prune-begin
```

# solutions

+++

## v0

```{code-cell} ipython3
def ip_v0(ip_str):
    return [int(x) for x in ip_str.split('.')]
```

```{code-cell} ipython3
ip_v0(IP_1)
```

## v1

+++

### solution naive

```{code-cell} ipython3
def ip_v1(ip_str):
    v0 = ip_v0(ip_str)
    b0 = v0[0]
    b1 = v0[1]
    b2 = v0[2]
    b3 = v0[3]
    return b0*2**24 + b1*2**16 + b2*2**8 + b3
```

### pareil mais un peu mieux

```{code-cell} ipython3
def ip_v1(ip_str):
    b0, b1, b2, b3 = ip_v0(ip_str)
    return b0*2**24 + b1*2**16 + b2*2**8 + b3
```

## solution poussive

```{code-cell} ipython3
# un peu poussif, mais qui fonctionne
def ip_v1(ip_str):
    result = 0
    # the first byte needs to be shifted by 2**24
    # the second one will be shifted by only 2**16, ...
    rank = 24
    for byte in ip_v0(ip_str):
        result += byte * 2**rank
        rank -= 8
    return result
```

## solution 2

```{code-cell} ipython3
# la version one-liner
# élégant si on veut, mais plus ou moins illisible
def ip_v1(ip_str):
    return sum(byte<<(8*i) for (i, byte) in enumerate(ip_v0(ip_str)[::-1]))
```
