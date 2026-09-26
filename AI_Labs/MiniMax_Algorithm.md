# Lucrarea de laborator nr. 2

## Implementarea algoritmului Mini-Max cu tăiere alfa-beta

**Disciplina:** Inteligență artificială
**Varianta:** 6
**Student:** Șevcenco Irina
**Grupa:** DU-IA2501
**Profesor:** E.Tretiacova
**Anul:** 2026

## 1. Scopul lucrării

Scopul lucrării este însușirea principiilor de implementare a algoritmului Mini-Max și a variantei optimizate prin tăiere alfa-beta, utilizate pentru luarea deciziilor în arborii de joc.

În cadrul lucrării se urmărește:

* construirea unui arbore de joc cu adâncime și lățime prestabilite;
* implementarea algoritmului Mini-Max obișnuit;
* implementarea algoritmului Mini-Max cu tăiere alfa-beta;
* compararea celor două metode în funcție de numărul de noduri verificate și timpul de execuție;
* analiza influenței ordinii de parcurgere a urmașilor asupra eficienței tăierii alfa-beta.

## 2. Formularea problemei

Se cere elaborarea unui program care să implementeze algoritmul Mini-Max și algoritmul Mini-Max cu tăiere alfa-beta pentru un arbore de joc.

Conform variantei individuale, se vor utiliza următorii parametri:

* **Adâncimea arborelui:** 7 niveluri;
* **Lățimea arborelui:** 3 urmași pentru fiecare nod;
* **Valorile frunzelor:** numere întregi generate aleatoriu în intervalul `[-100, 100]`;
* **Jucători:** MAX și MIN;
* **Strategii de parcurgere:** ordine naturală și ordine inversă.

Programul trebuie să determine valoarea Mini-Max a arborelui și să compare eficiența celor două metode prin numărarea nodurilor verificate și măsurarea timpului de execuție.

## 3. Analiza variantei

### 3.1. Parametrii arborelui

Pentru Varianta 6 au fost stabilite următoarele valori:

| Parametru                      |             Valoare |
| ------------------------------ | ------------------: |
| Adâncimea arborelui            |                   7 |
| Lățimea arborelui              |                   3 |
| Intervalul valorilor frunzelor |       `[-100, 100]` |
| Jucătorul de la rădăcină       |                 MAX |
| Ordinea de parcurgere          | Naturală și inversă |

Arborele este generat recursiv. Fiecare nod intern are exact 3 copii, iar la atingerea adâncimii 0 se generează o valoare aleatoare între -100 și 100.

Pentru generarea acelorași valori la fiecare rulare a programului este utilizată instrucțiunea:

```python
random.seed(4)
```

Astfel, comparația dintre Mini-Max și Mini-Max cu tăiere alfa-beta se realizează pe același arbore.

### 3.2. Structura arborelui

Arborele are adâncimea 7 și lățimea 3. Prin urmare, de la rădăcină până la fiecare frunză există 7 muchii.

Structura generală poate fi reprezentată astfel:

![Structura arborelui](https://drive.google.com/file/d/1nkveFF7uRZC6ZO6FKKV-wEbWrG2p2N25/view?usp=sharing)

Nivelurile alternează între jucătorii **MAX** și **MIN**.

La un nod MAX se selectează valoarea maximă dintre copiii săi, iar la un nod MIN se selectează valoarea minimă dintre copiii săi.

## 4. Algoritmul Mini-Max

### 4.1. Principiul de funcționare

Algoritmul Mini-Max este utilizat pentru arbori de joc în care doi jucători au obiective opuse:

* **MAX** încearcă să obțină cea mai mare valoare posibilă;
* **MIN** încearcă să obțină cea mai mică valoare posibilă.

Procesul începe de la frunze, iar valorile sunt propagate spre rădăcină.

În cazul programului realizat, rădăcina este un nod MAX.


### 4.2. Exemplu simplificat

Dacă un nod MAX are următorii trei copii:

```text
        MAX
      /  |  \
     20  50  10
```

atunci:

$$
MAX(20,50,10)=50
$$

Dacă un nod MIN are aceleași valori:

```text
        MIN
      /  |  \
     20  50  10
```

atunci:

$$
MIN(20,50,10)=10
$$

Prin aplicarea succesivă a acestor operații de la frunze spre rădăcină se obține valoarea finală a arborelui.


## 5. Algoritmul Mini-Max cu tăiere alfa-beta

### 5.1. Principiul tăierii alfa-beta

Tăierea alfa-beta este o optimizare a algoritmului Mini-Max. Aceasta permite evitarea analizării unor ramuri care nu mai pot influența rezultatul final.

Se utilizează două valori:

* **α (alpha)** – cea mai bună valoare cunoscută până în acel moment pentru MAX;
* **β (beta)** – cea mai bună valoare cunoscută până în acel moment pentru MIN.

La fiecare nod se verifică condiția:

$$
\beta \leq \alpha
$$

Dacă această condiție este adevărată, restul urmașilor nodului respectiv pot fi ignorați, deoarece nu mai pot modifica rezultatul final.

Important este că **tăierea alfa-beta nu modifică rezultatul Mini-Max**, ci doar reduce numărul de noduri care trebuie analizate.


### 5.2. Influența ordinii de parcurgere

În cadrul Variantei 6 trebuie comparate două moduri de parcurgere:

1. **Ordine naturală** – copiii sunt analizați de la primul la ultimul.
2. **Ordine inversă** – copiii sunt analizați de la ultimul la primul.

Pentru Mini-Max obișnuit, ordinea nu modifică rezultatul și nici numărul de noduri analizate, deoarece algoritmul verifică toate ramurile.

Pentru algoritmul alfa-beta, însă, ordinea poate influența numărul de noduri analizate și numărul de tăieri efectuate.


## 6. Descrierea formală a algoritmilor

### 6.1. Mini-Max

Funcția Mini-Max primește:

* nodul curent;
* tipul jucătorului – MAX sau MIN;
* ordinea de parcurgere;
* contorul nodurilor verificate.

Dacă nodul este o frunză, funcția returnează valoarea numerică a acesteia.

Dacă nodul este MAX, se calculează maximul valorilor copiilor.

Dacă nodul este MIN, se calculează minimul valorilor copiilor.


### 6.2. Mini-Max cu alfa-beta

Funcția alfa-beta primește suplimentar valorile:

$$
\alpha = -\infty
$$

și

$$
\beta = +\infty
$$

La nodurile MAX, valoarea alfa este actualizată:

$$
\alpha = \max(\alpha, value)
$$

La nodurile MIN, valoarea beta este actualizată:

$$
\beta = \min(\beta, value)
$$

Atunci când:

$$
\beta \leq \alpha
$$

se realizează tăierea ramurilor rămase.


## 7. Codul sursă al programului

**Limbaj de programare:** Python 3

```python
import random
import time

def creeaza_arbore(adancime, latime):
    
    if adancime == 0: # daca am ajuns la frunza, generam val aleatoare
        return random.randint(-100, 100)

    # cream lista unde punem copiii nodului
    copii = []

    for i in range(latime):
        copil = creeaza_arbore(adancime - 1, latime)
        copii.append(copil)

    return copii


# minimax: nodul (lista-nod intern, int-frunza), min/max, normala/inversa, nr nod verificate
def minimax(nod, maximizing, ordine, contor):
    contor[0] += 1

    # nodul = frunza ?
    if isinstance(nod, int):
        return nod

    copii = nod # if not frunza, nod e lista cu copiii sai 

    # ordine inversa
    if ordine == "inversa":
        copii = copii[::-1]

    # daca suntem la nod max, val max defavorabila
    if maximizing:
        valoare_maxima = -float("inf")

        for copil in copii:
            valoare = minimax(copil, False, ordine, contor) # dupa max urmeaza min, hence val2 = False (min)
            valoare_maxima = max(valoare_maxima, valoare)

        return valoare_maxima

    else: # min
        valoare_minima = float("inf")

        for copil in copii:
            valoare = minimax(copil, True, ordine, contor)
            valoare_minima = min(valoare_minima, valoare)

        return valoare_minima


# minimax & pruning (alpha, beta)
def alpha_beta(nod, maximizing, alpha, beta, ordine, contor):
    contor[0] += 1

    if isinstance(nod, int):
        return nod

    copii = nod

    if ordine == "inversa":
        copii = copii[::-1]

    # max
    if maximizing:
        valoare = -float("inf")

        for copil in copii: # alpha/beta best max/min val till now
            valoare = max(valoare, alpha_beta(copil, False, alpha, beta, ordine, contor)) # best max val till now

            alpha = max(alpha, valoare) # actualizam alpha

            if beta <= alpha: # pruning / taiere
                break

        return valoare

    # min
    else:
        valoare = float("inf")

        for copil in copii:
            valoare = min(valoare, alpha_beta(copil, True, alpha, beta, ordine, contor))

            beta = min(beta, valoare)

            if beta <= alpha:
                break

        return valoare


def testeaza(arbore, ordine):
    print("\nOrdine:", ordine)

    # minimax normal
    contor_minimax = [0]

    start = time.perf_counter()
    rezultat_minimax = minimax(arbore, True, ordine, contor_minimax)
    timp_minimax = time.perf_counter() - start

    print("\nMiniMax normal")

    print("Rezultat:", rezultat_minimax)
    print("Noduri verificate:", contor_minimax[0])
    print("Timp:", timp_minimax, "secunde")


    # alpha beta
    contor_alpha_beta = [0]

    start = time.perf_counter()
    rezultat_alpha_beta = alpha_beta(arbore, True, -float("inf"), float("inf"), ordine, contor_alpha_beta)
    timp_alpha_beta = time.perf_counter() - start

    print("\nnMiniMax cu Alpha-Beta")

    print("Rezultat:", rezultat_alpha_beta)
    print("Noduri verificate:", contor_alpha_beta[0])
    print("Timp:", timp_alpha_beta, "secunde")


# program principal
adancime = 7
latime = 3

random.seed(4)

arbore = creeaza_arbore(adancime, latime)

print("Arborele are adancimea:", adancime, "si latimea:", latime)

testeaza(arbore, "naturala")
testeaza(arbore, "inversa")
```

## 8. Testarea programului

Pentru testare a fost utilizat același arbore pentru toate cele patru rulări. Acest lucru este important pentru ca rezultatele să poată fi comparate corect.

| Nr. | Metoda    | Ordinea  | Rezultat | Noduri verificate | Timp (sec.) |
| --: | --------- | -------- | -------: | ----------------: | ----------: |
|   1 | Mini-Max  | Naturală |       32 |              3280 |   0.0006924 |
|   2 | Alfa-Beta | Naturală |       32 |              1012 |   0.0003146 |
|   3 | Mini-Max  | Inversă  |       32 |              3280 |   0.0011198 |
|   4 | Alfa-Beta | Inversă  |       32 |              1205 |   0.0004329 |


## 9. Rezultatele executării programului

### Testul 1: Ordine naturală

```text
Ordine: naturala

Mini-Max normal
Rezultat: 32
Noduri verificate: 3280
Timp: 0.0006924 secunde

Mini-Max cu Alpha-Beta
Rezultat: 32
Noduri verificate: 1012
Timp: 0.0003146 secunde
```

În cazul ordinii naturale, ambele metode au obținut aceeași valoare finală:

$$
V = 32
$$

Totuși, algoritmul alfa-beta a verificat doar **1012 noduri**, comparativ cu **3280 noduri** în cazul Mini-Max obișnuit.


### Testul 2: Ordine inversă

```text
Ordine: inversa

Mini-Max normal
Rezultat: 32
Noduri verificate: 3280
Timp: 0.0011198 secunde

Mini-Max cu Alpha-Beta
Rezultat: 32
Noduri verificate: 1205
Timp: 0.0004329 secunde
```

Și în cazul ordinii inverse rezultatul final a fost:

$$
V = 32
$$

Mini-Max obișnuit a verificat din nou toate cele **3280 de noduri**, în timp ce alfa-beta a verificat **1205 noduri**.


## 10. Analiza rezultatelor

Rezultatele experimentului demonstrează avantajul utilizării tăierii alfa-beta.

### 10.1. Compararea numărului de noduri

Pentru ordinea naturală:

$$
3280 - 1012 = 2268
$$

Prin urmare, au fost evitate **2268 de noduri**.

Procentul aproximativ de reducere este:

$$
\frac{3280-1012}{3280}\cdot100 \approx 69.15\%
$$

Pentru ordinea inversă:

$$
3280 - 1205 = 2075
$$

adică o reducere de aproximativ:

$$
\frac{3280-1205}{3280}\cdot100 \approx 63.26\%
$$

Astfel, ordinea naturală a fost mai eficientă pentru arborele generat, deoarece a permis realizarea unui număr mai mare de tăieri.


### 10.2. Compararea timpului de execuție

Pentru ordinea naturală, timpul a scăzut de la aproximativ:

$$
0.0006924s
$$

la:

$$
0.0003146s
$$

Pentru ordinea inversă, timpul a scăzut de la aproximativ:

$$
0.0011198s
$$

la:

$$
0.0004329s
$$

Prin urmare, algoritmul alfa-beta a fost mai rapid în ambele situații.


### 10.3. Influența ordinii de parcurgere

Rezultatele arată că ordinea urmașilor are un efect important asupra algoritmului alfa-beta:

| Ordine   | Mini-Max – noduri | Alfa-Beta – noduri |
| -------- | ----------------: | -----------------: |
| Naturală |              3280 |               1012 |
| Inversă  |              3280 |               1205 |

Mini-Max obișnuit nu beneficiază de ordinea de parcurgere, deoarece trebuie să examineze toate nodurile.

În schimb, alfa-beta depinde de ordinea în care sunt analizate ramurile. O ordine mai favorabilă poate determina apariția mai rapidă a condiției:

$$
\beta \leq \alpha
$$

și, implicit, mai multe tăieri.

În experimentul realizat, **ordinea naturală a fost mai eficientă decât ordinea inversă**.


## 11. Verificarea corectitudinii

Un aspect important este faptul că toate cele patru rulări au produs aceeași valoare finală:

$$
\boxed{32}
$$

Acest lucru confirmă că tăierea alfa-beta nu modifică rezultatul algoritmului Mini-Max. Ea doar elimină acele ramuri care nu mai pot influența decizia finală.

Prin urmare:

```text
Mini-Max normal    → 32
Mini-Max alfa-beta → 32
```

atât pentru ordinea naturală, cât și pentru ordinea inversă.

Diferența dintre metode apare în principal la:

* numărul de noduri verificate;
* timpul necesar pentru execuție.


## 12. Concluzie

În cadrul lucrării de laborator a fost implementat algoritmul **Mini-Max** și versiunea sa optimizată prin **tăiere alfa-beta** pentru un arbore de joc cu **adâncimea 7** și **lățimea 3**.

Valorile frunzelor au fost generate aleatoriu în intervalul `[-100, 100]`, iar pentru reproducerea experimentului a fost utilizată valoarea `random.seed(4)`.

În urma testării s-a constatat că ambele variante ale algoritmului produc același rezultat final, **32**, ceea ce demonstrează corectitudinea tăierii alfa-beta.

În același timp, algoritmul alfa-beta a analizat considerabil mai puține noduri: **1012 față de 3280** în ordinea naturală și **1205 față de 3280** în ordinea inversă. De asemenea, timpul de execuție a fost mai mic în ambele cazuri.

Experimentul a demonstrat și importanța ordinii de parcurgere a urmașilor. Pentru arborele utilizat, **ordinea naturală a fost mai eficientă decât ordinea inversă**, deoarece a permis eliminarea unui număr mai mare de ramuri prin tăiere alfa-beta.

Astfel, tăierea alfa-beta reprezintă o optimizare importantă a algoritmului Mini-Max, deoarece permite obținerea aceluiași rezultat cu un număr semnificativ mai mic de noduri evaluate.


**Student:** Șevcenco Irina
**Grupa:** DU-IA2501
**Varianta:** 6
