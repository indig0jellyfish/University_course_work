# Lucrarea de laborator nr. 1

## Implementarea unui automat finit pentru recunoașterea unui limbaj formal

**Disciplina:** Inteligență artificială
**Varianta:** 6
**Student:** Șevcenco Irina
**Grupa:** DU-IA2501
**Profesor:** E.Tretiacova
**Anul:** 2026

## 1. Scopul lucrării

Studierea principiilor de construire și implementare software a unui automat finit determinist (AFD), care recunoaște cuvinte ale unui limbaj formal definit prin varianta individuală.

## 2. Formularea problemei

Să se elaboreze un program care implementează un automat finit pentru recunoașterea cuvintelor de forma:

$$
a^n b^m c^k e, \qquad n,m,k \geq 0.
$$

Programul trebuie să primească un cuvânt de la tastatură, să proceseze fiecare simbol conform tranzițiilor automatului și să determine dacă acesta aparține limbajului dat.

## 3. Analiza variantei

### 3.1. Limbajul formal

Limbajul analizat este:

$$
L = \{a^n b^m c^k e \mid n,m,k \geq 0\}.
$$

Condițiile:

$$
n \geq 0, \qquad m \geq 0, \qquad k \geq 0
$$

înseamnă că simbolurile `a`, `b` și `c` pot apărea de zero sau mai multe ori.

Simbolul `e` este obligatoriu și trebuie să apară la sfârșitul cuvântului.

Prin urmare, structura generală a unui cuvânt este:

```text
aaaa...bbbb...cccc...e
```

unde fiecare dintre grupurile de `a`, `b` și `c` poate fi gol.

### Exemple de cuvinte corecte

- pentru $n = 0$, $m = 0$, $k = 0$: `e`;
- pentru $n = 1$, $m = 0$, $k = 0$: `ae`;
- pentru $n = 2$, $m = 3$, $k = 0$: `aab bbe`, adică `aabbbe`;
- pentru $n = 0$, $m = 2$, $k = 3$: `bbccce`;
- pentru $n = 3$, $m = 2$, $k = 4$: `aaabbcccce`.

Alfabetul limbajului este:

$$
\Sigma = \{a,b,c,e\}.
$$

### 3.2. Logica recunoașterii

Pentru ca un cuvânt să aparțină limbajului, acesta trebuie să respecte următoarea ordine:

1. Pot apărea zero sau mai multe simboluri `a`.
2. După simbolurile `a` pot apărea zero sau mai multe simboluri `b`.
3. După simbolurile `b` pot apărea zero sau mai multe simboluri `c`.
4. La final trebuie să apară obligatoriu simbolul `e`.
5. După simbolul `e` nu mai pot exista alte simboluri.

De exemplu, cuvântul:

```text
aaabbbccce
```

respectă structura:

```text
aaa + bbb + ccc + e
```

și, prin urmare, aparține limbajului.

În schimb, cuvântul:

```text
acbe
```

nu aparține limbajului deoarece simbolul `b` apare după `c`, încălcând ordinea stabilită.

## 4. Descrierea formală a automatului finit

Automatul finit determinist este definit prin cvintuplul:

$$
A = (Q, \Sigma, \delta, q_0, F),
$$

unde:

- $Q = \{q_0, q_1, q_2, q_3\}$ reprezintă mulțimea stărilor;
- $\Sigma = \{a,b,c,e\}$ reprezintă alfabetul de intrare;
- $\delta$ reprezintă funcția de tranziție;
- $q_0$ este starea inițială;
- $F = \{q_3\}$ reprezintă mulțimea stărilor finale.

### 4.1. Rolul stărilor

| Starea | Rolul |
|---|---|
| $q_0$ | Starea inițială; se citesc simbolurile `a` sau se poate trece direct la `b`, `c` sau `e` |
| $q_1$ | Au fost citite simboluri `b`; pot continua simbolurile `b`, pot urma simboluri `c` sau simbolul final `e` |
| $q_2$ | Au fost citite simboluri `c`; pot continua simbolurile `c` sau poate urma simbolul final `e` |
| $q_3$ | A fost citit simbolul final `e`; aceasta este starea finală |

## 5. Diagrama automatului finit

![Diagrama automatului finit](https://drive.google.com/uc?export=view&id=1KX6_Lqpz5vcHDr0HwcTDmR1LgX0WUv9R)

Automatul începe în starea $q_0$.

Starea finală este $q_3$. Prin urmare, un cuvânt este acceptat numai dacă, după procesarea tuturor simbolurilor, automatul ajunge în starea $q_3$.

## 6. Tabelul de tranziții

| Starea curentă | `a` | `b` | `c` | `e` |
|---|---|---|---|---|
| $q_0$ | $q_0$ | $q_1$ | $q_2$ | $q_3$ |
| $q_1$ | — | $q_1$ | $q_2$ | $q_3$ |
| $q_2$ | — | — | $q_2$ | $q_3$ |
| $q_3$ | — | — | — | — |

Simbolul `—` indică faptul că tranziția respectivă nu este permisă.

Dacă automatul întâlnește o tranziție care nu este definită, cuvântul este respins.

## 7. Algoritmul de funcționare al programului

Programul funcționează conform următorilor pași:

1. Se citește cuvântul de la tastatură.
2. Automatului i se atribuie starea inițială $q_0$.
3. Fiecare literă a cuvântului este procesată consecutiv.
4. Se verifică dacă există o tranziție validă pentru starea curentă și simbolul citit.
5. Dacă există tranziția, automatul trece în următoarea stare.
6. Dacă nu există o tranziție validă, cuvântul este respins.
7. După procesarea tuturor simbolurilor, se verifică dacă automatul se află într-o stare finală.
8. Dacă starea curentă este $q_3$, cuvântul este acceptat.

## 8. Codul sursă al programului

**Limbaj de programare:** Python 3

```python
def verifica_cuvant(cuvant):
    tranzitii = {
        "q0": {
            "a": "q0",
            "b": "q1",
            "c": "q2",
            "e": "q3"
        },

        "q1": {
            "b": "q1",
            "c": "q2",
            "e": "q3"
        },

        "q2": {
            "c": "q2",
            "e": "q3"
        }
    }

    stare_curenta = "q0"
    stare_finala = "q3"

    for litera in cuvant:
        # Se verifică dacă există o tranziție validă
        if stare_curenta in tranzitii and litera in tranzitii[stare_curenta]:
            stare_curenta = tranzitii[stare_curenta][litera]
        else:
            return False

    # Se verifică dacă automatul s-a terminat într-o stare finală
    return stare_curenta == stare_finala


cuvant = input("Introduceți cuvântul: ")

if verifica_cuvant(cuvant):
    print("Cuvântul aparține limbajului")
else:
    print("Cuvântul nu aparține limbajului")
```

## 9. Explicația codului

Programul utilizează un dicționar numit `tranzitii` pentru a reprezenta funcția de tranziție a automatului finit.

De exemplu:

```python
"q0": {
    "a": "q0",
    "b": "q1",
    "c": "q2",
    "e": "q3"
}
```

înseamnă că, dacă automatul se află în starea `q0`:

- la citirea simbolului `a`, rămâne în starea `q0`;
- la citirea simbolului `b`, trece în starea `q1`;
- la citirea simbolului `c`, trece în starea `q2`;
- la citirea simbolului `e`, trece în starea finală `q3`.

Funcția `verifica_cuvant()` parcurge fiecare caracter al cuvântului.

Pentru fiecare caracter se verifică dacă există o tranziție validă:

```python
if stare_curenta in tranzitii and litera in tranzitii[stare_curenta]:
```

Dacă tranziția nu există, funcția returnează imediat valoarea `False`.

La final, se verifică dacă automatul a ajuns în starea finală:

```python
return stare_curenta == stare_finala
```

## 10. Testarea programului

| Nr. | Cuvânt de intrare | Explicație | Rezultatul așteptat |
|---:|---|---|---|
| 1 | `e` | $n=0, m=0, k=0$ | Acceptat |
| 2 | `ae` | Un simbol `a`, urmat de `e` | Acceptat |
| 3 | `be` | Zero simboluri `a`, un simbol `b` | Acceptat |
| 4 | `ce` | Zero simboluri `a` și `b`, un simbol `c` | Acceptat |
| 5 | `aaabbbccce` | Respectă structura limbajului | Acceptat |
| 6 | `bbccce` | Zero simboluri `a` | Acceptat |
| 7 | `` (șir gol) | Lipsește simbolul final `e` | Respins |
| 8 | `a` | Lipsește simbolul final `e` | Respins |
| 9 | `abc` | Lipsește simbolul final `e` | Respins |
| 10 | `acbe` | Simbolul `b` apare după `c` | Respins |
| 11 | `eba` | Există simboluri după `e` | Respins |
| 12 | `aaabbbccc` | Lipsește simbolul final `e` | Respins |
| 13 | `aabdc` | Conține simbolul nepermis `d` | Respins |

## 11. Exemple de rulare

### Testul 1: cuvântul minim acceptat

```text
Introduceți cuvântul: e
Cuvântul aparține limbajului
```

### Testul 2: cuvânt format doar din `a` și simbolul final `e`

```text
Introduceți cuvântul: aaaae
Cuvântul aparține limbajului
```

### Testul 3: cuvânt complet

```text
Introduceți cuvântul: aaabbbccce
Cuvântul aparține limbajului
```

### Testul 4: ordine incorectă a simbolurilor

```text
Introduceți cuvântul: acbe
Cuvântul nu aparține limbajului
```

### Testul 5: lipsește simbolul final

```text
Introduceți cuvântul: aaabbbccc
Cuvântul nu aparține limbajului
```

## 12. Analiza rezultatelor

Testarea programului a confirmat funcționarea corectă a automatului finit.

Cuvintele care respectă structura:

$$
a^n b^m c^k e
$$

au fost acceptate de automat.

Automatul permite absența unuia sau mai multor grupuri de simboluri `a`, `b` sau `c`, deoarece valorile $n$, $m$ și $k$ pot fi egale cu zero.

Astfel, cuvinte precum:

```text
e
ae
be
ce
aaabbbccce
```

sunt acceptate.

În schimb, sunt respinse cuvintele care:

- nu se termină cu `e`;
- conțin simboluri care nu aparțin alfabetului;
- nu respectă ordinea `a → b → c → e`;
- conțin simboluri după `e`.

Automatul este determinist deoarece pentru fiecare stare și fiecare simbol există cel mult o singură tranziție posibilă.

## 13. Concluzie

În cadrul acestei lucrări de laborator a fost proiectat și implementat un automat finit determinist pentru recunoașterea limbajului:

$$
L = \{a^n b^m c^k e \mid n,m,k \geq 0\}.
$$

A fost elaborată diagrama automatului, tabelul de tranziții și programul în limbajul Python.

Programul parcurge succesiv fiecare simbol al cuvântului și verifică respectarea structurii impuse de limbaj. Testele efectuate au demonstrat că automatul acceptă corect cuvintele care respectă ordinea simbolurilor `a`, `b`, `c` și se termină cu `e`, respingând cuvintele care conțin simboluri nepermise, au o ordine incorectă sau nu conțin simbolul final obligatoriu.
