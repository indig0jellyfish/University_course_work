import os
import itertools
import math
import random
import string
import subprocess
import sys
import time
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from collections import Counter

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # folderul in care se afla programul python
DOC_DIR = os.path.join(BASE_DIR, 'docs')
DEFAULT_ALPHABET = string.ascii_lowercase
ADFGVX_SYMBOLS = 'ADFGVX'
ADFGVX_ALPHABET = string.ascii_lowercase + string.digits

ENGLISH_FREQ = {
    'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702,
    'f': 2.228, 'g': 2.015, 'h': 6.094, 'i': 6.966, 'j': 0.153,
    'k': 0.772, 'l': 4.025, 'm': 2.406, 'n': 6.749, 'o': 7.507,
    'p': 1.929, 'q': 0.095, 'r': 5.987, 's': 6.327, 't': 9.056,
    'u': 2.758, 'v': 0.978, 'w': 2.360, 'x': 0.150, 'y': 1.974,
    'z': 0.074
}


# Functii de normalizare (implementarea explicita a functiei N(M))
def clean_text(text, alphabet=DEFAULT_ALPHABET):
    allowed = set(alphabet.lower()) # transf alfabetul intr-un set
    return ''.join(c.lower() for c in text if c.lower() in allowed) # transf char in lit mica, pastreaza char daca se afla  in alfabet, uneste toate char ramase intr-un text

def letter_frequency_table(text):
    text = clean_text(text)
    n = len(text)
    if n == 0:
        return 'Text vid - nu se poate calcula distributia literelor.\n'
    counts = Counter(text) # numara dee cate ori apare fiecare litera
    lines = ['  Litera | Observat(%) | Englez(%)\n']
    for ch in DEFAULT_ALPHABET:
        obs = counts.get(ch, 0) / n * 100 # calc procent observat al char vs frecventa char in engleza
        exp = ENGLISH_FREQ.get(ch, 0)
        if obs > 0.01 or exp >= 4.0:
            lines.append(f'    {ch}   |    {obs:5.2f}    |   {exp:5.2f}\n')
    return ''.join(lines)


# Cifrul Afin
def mod_inverse(a, m): # gasim a^-1
    a %= m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f'Nu exista invers modular pentru a={a}, m={m}.')

def affine_encrypt(text, a, b, alphabet=DEFAULT_ALPHABET):
    alpha = alphabet.lower()
    m = len(alpha)
    if math.gcd(a, m) != 1: # verif daca a e relativ prim cu m
        raise ValueError(f'a trebuie sa fie relativ prim cu m={m} (chei valide: doar a coprim cu m).')
    text = clean_text(text, alpha)
    idx = {ch: i for i, ch in enumerate(alpha)} # asociere intre char si nr ei: a -> 0, b-> 1, etc
    return ''.join(alpha[(a * idx[ch] + b) % m] for ch in text) #formula de cript, se gaseste nr ei, aplica formula, transforma rez in litera

def affine_decrypt(text, a, b, alphabet=DEFAULT_ALPHABET):
    alpha = alphabet.lower()
    m = len(alpha)
    inv = mod_inverse(a, m)
    text = clean_text(text, alpha)
    idx = {ch: i for i, ch in enumerate(alpha)}
    return ''.join(alpha[(inv * (idx[ch] - b)) % m] for ch in text) # formula de decriptare

def affine_keyspace(alphabet=DEFAULT_ALPHABET): # cream lista cu val lui a care sunt valide
    m = len(alphabet)
    valid_a = [a for a in range(1, m) if math.gcd(a, m) == 1]
    return valid_a, m

def affine_bruteforce(ciphertext, alphabet=DEFAULT_ALPHABET, limit=10):
    alpha = alphabet.lower()
    valid_a, m = affine_keyspace(alpha)
    results = []
    for a in valid_a:
        for b in range(m):
            plain = affine_decrypt(ciphertext, a, b, alpha)
            results.append((chi_square_score(plain), a, b, plain)) # incearca sa se descripteze textul, chi calc cat de mult eamana distrubutia literelor din txt cu distrib normala a limbii engleze
    results.sort(key=lambda x: x[0])
    total_tried = len(valid_a) * m
    return results[:limit], total_tried # primele limit rezultate, nr total de chei incercare


# Cifrul Vigenere
def vigenere_encrypt(text, key, alphabet=DEFAULT_ALPHABET):
    alpha = alphabet.lower()
    key = clean_text(key, alpha)
    if not key:
        raise ValueError('Cheia Vigenere nu poate fi vida (dupa normalizare)')
    text = clean_text(text, alpha)
    m = len(alpha)
    idx = {ch: i for i, ch in enumerate(alpha)} # corespondenta litere si numere
    return ''.join(
        alpha[(idx[ch] + idx[key[i % len(key)]]) % m] # C = (P + K) mod 26, i % len(key) repeta cheia
        for i, ch in enumerate(text)
    )

def vigenere_decrypt(text, key, alphabet=DEFAULT_ALPHABET):
    alpha = alphabet.lower()
    key = clean_text(key, alpha)
    if not key:
        raise ValueError('Cheia Vigenere nu poate fi vida (dupa normalizare).')
    text = clean_text(text, alpha)
    m = len(alpha)
    idx = {ch: i for i, ch in enumerate(alpha)}
    return ''.join(
        alpha[(idx[ch] - idx[key[i % len(key)]]) % m] # P = (C - K) mod 26
        for i, ch in enumerate(text)
    )


# Transpozitia dubla pe coloane
DEFAULT_FILLER = 'x'

def columnar_pad(text, cols, filler=DEFAULT_FILLER): # adauga char de umplutura
    if cols <= 0:
        raise ValueError('Numarul de coloane trebuie sa fie cel putin 1.')
    remainder = len(text) % cols # cate char raman dupa impartirea text in randuri de cols char
    if remainder == 0:
        return text
    return text + filler * (cols - remainder) # se adauga char x suficiente

def columnar_padded_length(original_length, key):
    cols = len(''.join(key.lower().split())) # calc nr de col in baza cheii
    if cols == 0 or original_length <= 0:
        return original_length
    remainder = original_length % cols
    return original_length if remainder == 0 else original_length + (cols - remainder) # if txt este multiplu al nr de col, nu se modif, altfel, adauga nr necesar de col

def columnar_encrypt(text, key, filler=DEFAULT_FILLER):
    key_clean = ''.join(key.lower().split())
    if not key_clean:
        raise ValueError('Cheia de transpozitie nu poate fi vida.')
    text = ''.join(text.split())
    cols = len(key_clean) # nr de col = lung cheii
    original_length = len(text) 
    padded = columnar_pad(text, cols, filler) # complet txt pana lung este diivz la nr de col
    rows = len(padded) // cols
    matrix = [[''] * cols for _ in range(rows)] # creeaza tabelul gol
    p = 0
    for r in range(rows):
        for c in range(cols):
            matrix[r][c] = padded[p]
            p += 1
    order = sorted(range(cols), key=lambda i: (key_clean[i], i)) # stabil ordinii col dupa literele cheii, (key_clean[i], i) i este folosit pentru a păstra o ordine deterministă între literele identice
    ciphertext = ''.join(matrix[r][c] for c in order for r in range(rows)) # txt e citit pe col
    return ciphertext, original_length

def columnar_decrypt_with_order(text, cols, order, original_length=None): # decript per se transpoz
    n = len(text)
    if n == 0:
        return ''
    if n % cols != 0:
        raise ValueError(
            f'Lungimea textului criptat ({n}) nu este un multiplu al numarului de coloane ({cols}).' # dreptunghi perfect (cu x-uri)
        )
    rows = n // cols
    columns = [''] * cols
    pos = 0
    for c in order: # parcurg col in ord citirii la criptare, ia din ciphertext caracterele care aparțin coloanei respective, imparte in bucati
        columns[c] = text[pos:pos + rows]
        pos += rows
    out = []
    for r in range(rows): # parc rand, col, adauga in rezult coloana c, rand r
        for c in range(cols):
            out.append(columns[c][r])
    full = ''.join(out)
    if original_length is None or original_length < 0 or original_length > len(full): # eliminam x
        return full
    return full[:original_length]

def columnar_decrypt(text, key, original_length=None): # curata cheia si txt, stabileste ordinea coloanelor in baza cheii, folos ordinea si o transm functiei columnar_decrypt_with_order
    key_clean = ''.join(key.lower().split())
    if not key_clean:
        raise ValueError('Cheia de transpozitie nu poate fi vida.')
    text = ''.join(text.split())
    cols = len(key_clean)
    if len(text) == 0:
        return ''
    order = sorted(range(cols), key=lambda i: (key_clean[i], i))
    return columnar_decrypt_with_order(text, cols, order, original_length)

def columnar_shape_description(key, original_length, filler=DEFAULT_FILLER): # descrie cum este construit tabelul folosit pentru transpozitia pe coloane.
    key_clean = ''.join(key.lower().split())
    cols = len(key_clean)
    padded_length = columnar_padded_length(original_length, key_clean) if cols else 0
    rows = padded_length // cols if cols else 0
    pad_added = padded_length - original_length
    order = sorted(range(cols), key=lambda i: (key_clean[i], i))
    return (
        f'Coloane: {cols}, Randuri: {rows} (dreptunghi COMPLET, fara celule goale).\n'
        f'Lungime text original: {original_length}. Caractere de umplutura ("{filler}") adaugate: {pad_added}.\n'
        f'Ordinea de citire a coloanelor (index original, dupa litera cheii "{key_clean}"): {order}\n'
    )

def double_transposition_encrypt(text, key1, key2, filler=DEFAULT_FILLER): # criptare dubla transpozitie
    clean = ''.join(ch.lower() for ch in text if ch.isalpha())
    first, original_length = columnar_encrypt(clean, key1, filler)
    second, _ = columnar_encrypt(first, key2, filler)
    return first, second, original_length

def double_transposition_decrypt(text, key1, key2, original_length): # decriptare dubla transpozitie
    clean_cipher = ''.join(ch.lower() for ch in text if ch.isalpha())
    first_length = columnar_padded_length(original_length, key1)
    after_second = columnar_decrypt(clean_cipher, key2, first_length)
    original = columnar_decrypt(after_second, key1, original_length)
    return after_second, original


# Cifrul mixt ADFGVX
def keyed_alphabet(key, alphabet=ADFGVX_ALPHABET): # alfab pt patratul adfgvx
    seen = set()
    result = []
    for ch in clean_text(key, alphabet): # pune char din cheie unice, apoi char ramase din alfabet
        if ch not in seen:
            result.append(ch)
            seen.add(ch)
    for ch in alphabet:
        if ch not in seen:
            result.append(ch)
            seen.add(ch)
    return ''.join(result)

def build_adfgvx_square(key=''): # creeaza patrat adfgvx, pentru cript, si descrip
    alpha = keyed_alphabet(key, ADFGVX_ALPHABET)
    square = {ADFGVX_SYMBOLS[r] + ADFGVX_SYMBOLS[c]: alpha[r * 6 + c] for r in range(6) for c in range(6)}
    reverse = {v: k for k, v in square.items()} # dict invers: ex, avem: square["AA"] = "s", atunci invers e reverse["s"] = "AA"
    return square, reverse, alpha

def adfgvx_substitute(text, key): # prima etapa a cript adfgvx
    square, reverse, alpha = build_adfgvx_square(key)
    del reverse # nu avem nevoie in cript
    clean = clean_text(text, ADFGVX_ALPHABET)
    return ''.join(
        ADFGVX_SYMBOLS[i // 6] + ADFGVX_SYMBOLS[i % 6] # i // 6 determina randul, [i % 6] determina col -> ex: D + F -> DF
        for ch in clean
        for i in [alpha.index(ch)] # poz char in alfabet
    ), alpha

def adfgvx_unsubstitute(text, key):
    square, reverse, alpha = build_adfgvx_square(key)
    del reverse, alpha
    clean = ''.join(ch for ch in text.upper() if ch in ADFGVX_SYMBOLS)
    if len(clean) % 2:
        raise ValueError('Textul ADFGVX trebuie sa aiba un numar par de simboluri.')
    return ''.join(square[clean[i:i + 2]] for i in range(0, len(clean), 2)) # ia txt cate 2 char, si obt char originale

def adfgvx_encrypt(text, square_key, transposition_key, filler='A'): # criptarea adfgvx in 2 etape
    substituted, alpha = adfgvx_substitute(text, square_key)
    transposed, original_length = columnar_encrypt(substituted, transposition_key, filler)
    return substituted, transposed, alpha, original_length

def adfgvx_decrypt(text, square_key, transposition_key, original_length):
    only_symbols = ''.join(ch for ch in text.upper() if ch in ADFGVX_SYMBOLS)
    after_transposition = columnar_decrypt(only_symbols, transposition_key, original_length)
    plain = adfgvx_unsubstitute(after_transposition, square_key)
    _, _, alpha = build_adfgvx_square(square_key)
    return after_transposition, plain, alpha

def adfgvx_bruteforce_transposition(ciphertext, square_key, key_length, original_length, limit_candidates=8, max_permutations=20000):
    """
    Cheia patratului ADFGVX este considerata cunoscuta, iar programul
    incearca toate sau o parte dintre permutarile posibile ale coloanelor.
    Pentru fiecare ordine, decripteaza transpozitia, inverseaza substitutia
    si calculeaza un scor chi-patrat pentru a estima cat de apropiat este
    rezultatul de un text normal.

    Returneaza cele mai bune rezultate, numarul de permutari testate,
    numarul total de permutari posibile si indica daca atacul a fost complet.
    """
    only_symbols = ''.join(ch for ch in ciphertext.upper() if ch in ADFGVX_SYMBOLS)
    total_permutations = math.factorial(key_length)
    exhaustive = total_permutations <= max_permutations # daca nr total de permutari e suf sa testam pe toate

    if exhaustive:
        candidate_orders = itertools.permutations(range(key_length)) # se genereaza toate permutarile
    else:
        def sampled_orders(): # funct ce genereaza ordine aleatorii
            seen = set() # permut deja incercate
            attempts = 0
            while len(seen) < max_permutations and attempts < max_permutations * 3: # atata timp cat nu am ajuns nr max de permut si nu am facut pre multe incercari de a gasi var unice
                attempts += 1
                candidate = tuple(random.sample(range(key_length), key_length)) # gener permut aleatorie
                if candidate not in seen:
                    seen.add(candidate)
                    yield candidate # return temp aceastapermut, yield permite funct sa gen variante una cate una, fara sa le pastreze in mem
        candidate_orders = sampled_orders()

    results = []
    tried = 0
    for order in candidate_orders:
        tried += 1
        try:
            substituted = columnar_decrypt_with_order(only_symbols, key_length, list(order), original_length) # invers transpozitiei
            plain = adfgvx_unsubstitute(substituted, square_key) # invers substit
        except ValueError:
            continue
        score = chi_square_score(plain)
        results.append((score, order, plain)) # distrib norm a literelor
    results.sort(key=lambda x: x[0])
    return results[:limit_candidates], tried, total_permutations, exhaustive


# Criptanaliza: scor chi-patrat, indice de coincidenta, atacuri
def chi_square_score(text):
    text = clean_text(text)
    n = len(text)
    if not n:
        return float('inf') # txt gol nu e considerat candid bun in analiza
    counts = Counter(text) # de cate ori apare fiecare char
    score = 0.0
    for ch, pct in ENGLISH_FREQ.items():
        expected = n * pct / 100.0 # cate aparitii a literei ne-am astepta sa avem intr-un txt de lung n, conform frecv norm e limb engleze
        observed = counts.get(ch, 0)
        score += (observed - expected) ** 2 / expected if expected else 0 # formula de calc a scorului
    return score


# lucrul cu fisierele
def export_text_to_file(path, text):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)

def open_pdf(path):
    if not os.path.exists(path):
        return False
    try:
        if sys.platform.startswith('win'):
            os.startfile(path)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', path])
        else:
            subprocess.Popen(['xdg-open', path])
        return True
    except Exception:
        return False


# Interfata grafica
class CipherWindow(tk.Toplevel):
    """
    Clasa de baza pentru ferestrele cifrurilor.
    Creeaza structura comuna a ferestrei: titlul, dimensiunea,
    butonul pentru deschiderea documentatiei si functiile generale
    folosite de celelalte ferestre.
    """
    def __init__(self, master, title, pdf_name):
        super().__init__(master)
        self.title(title)
        self.geometry('1060x800')
        self.minsize(920, 680)
        self.pdf_name = pdf_name
        self.configure(bg='#f3f3f3')
        self.protocol('WM_DELETE_WINDOW', self.destroy)
        self._build_header(title)

    def _build_header(self, title):
        header = tk.Frame(self, bg='#e7e7e7', height=50)
        header.pack(fill='x', padx=12, pady=(12, 6))
        tk.Label(header, text=title, font=('Segoe UI', 17, 'bold'), bg='#e7e7e7').pack(side='left', padx=14, pady=10)
        ttk.Button(header, text='Deschideti prezentarea PDF', command=self.open_docs).pack(side='right', padx=14, pady=8)

    def open_docs(self):
        path = os.path.join(DOC_DIR, self.pdf_name)
        if not open_pdf(path):
            messagebox.showwarning('PDF', f'Nu am putut deschide {path}. Verificati ca fisierul exista in folderul docs.')

    def text_widget(self, parent, height=6):
        w = tk.Text(parent, height=height, wrap='word', font=('Consolas', 10), relief='solid', bd=1)
        return w

    def show_roundtrip_result(self, normalized, recovered):
        """
        Verifica daca textul obtinut dupa criptare si decriptare este
        identic cu textul normalizat initial.
        Afiseaza rezultatul verificarii intr-o fereastra de informare.
        """
        ok = (normalized == recovered)
        status = 'OK - D(E(N(M))) = N(M)' if ok else 'EROARE - textul recuperat difera de N(M)'
        messagebox.showinfo(
            'Verificare round-trip (criptare -> decriptare)',
            f'N(M)          : {normalized[:80]}{"..." if len(normalized) > 80 else ""}\n'
            f'D(E(N(M)))    : {recovered[:80]}{"..." if len(recovered) > 80 else ""}\n\n'
            f'Rezultat: {status}\n\n'
            'Nota: politica de normalizare N(M) elimina spatiile, punctuatia\n'
            'si diferenta majuscule/minuscule, deci acestea nu se recupereaza.'
        )

class AffineWindow(CipherWindow):
    """
    Fereastra grafica dedicata cifrului Afin.
    Permite introducerea textului si a cheilor, criptarea,
    decriptarea, verificarea round-trip si testarea atacului
    prin forta bruta.
    """
    def __init__(self, master):
        super().__init__(master, 'Cifrul Afin (Caesar - caz particular)', 'cifrul_afin.pdf')
        self._build()

    def _build(self):
        """
        Construieste toate elementele interfetei pentru cifrul Afin:
        campurile pentru alfabet si cheile a si b, optiunile de criptare
        sau decriptare, zona pentru text si zona pentru rezultate,
        precum si sectiunea pentru atacul prin forta bruta.
        """
        top = ttk.Frame(self, padding=10)
        top.pack(fill='x')
        ttk.Label(top, text='Alfabet:').grid(row=0, column=0, sticky='w')
        self.alphabet = ttk.Entry(top, width=35)
        self.alphabet.insert(0, DEFAULT_ALPHABET)
        self.alphabet.grid(row=0, column=1, padx=5)
        ttk.Label(top, text='a:').grid(row=0, column=2)
        self.a = ttk.Spinbox(top, from_=1, to=25, width=6)
        self.a.set('5')
        self.a.grid(row=0, column=3, padx=5)
        ttk.Label(top, text='b:').grid(row=0, column=4)
        self.b = ttk.Spinbox(top, from_=0, to=25, width=6)
        self.b.set('8')
        self.b.grid(row=0, column=5, padx=5)
        self.direction = tk.StringVar(value='encrypt')
        ttk.Radiobutton(top, text='Criptare', variable=self.direction, value='encrypt').grid(row=1, column=0, pady=8)
        ttk.Radiobutton(top, text='Decriptare', variable=self.direction, value='decrypt').grid(row=1, column=1, sticky='w')
        ttk.Button(top, text='Transforma', command=self.transform).grid(row=1, column=3)
        ttk.Button(top, text='Verifica round-trip', command=self.verify_roundtrip).grid(row=1, column=4, columnspan=2, sticky='w')

        body = ttk.Frame(self, padding=(10, 0, 10, 10))
        body.pack(fill='both', expand=True)
        left = ttk.LabelFrame(body, text='Textul clar / criptat', padding=8)
        left.pack(side='left', fill='both', expand=True, padx=(0, 5))
        self.input = self.text_widget(left, 12); self.input.pack(fill='both', expand=True)
        ttk.Button(left, text='Curata', command=lambda: self.input.delete('1.0', 'end')).pack(anchor='w', pady=5)
        right = ttk.LabelFrame(body, text='Rezultatul (si N(M) = forma normalizata)', padding=8)
        right.pack(side='left', fill='both', expand=True, padx=(5, 0))
        self.output = self.text_widget(right, 6); self.output.pack(fill='both', expand=True)
        self.normalized_box = self.text_widget(right, 4); self.normalized_box.pack(fill='both', expand=True, pady=6)
        ttk.Button(right, text='Export rezultat .txt', command=self.export).pack(anchor='w', pady=5)

        attack = ttk.LabelFrame(self, text='Rezistenta criptografica - forta bruta pe spatiul de chei (a, b)', padding=8)
        attack.pack(fill='x', padx=10, pady=(0, 10))
        ttk.Button(attack, text='Testeaza forta bruta', command=self.bruteforce).pack(side='left')
        self.attack_out = tk.Text(attack, height=12, wrap='word', font=('Consolas', 9))
        self.attack_out.pack(side='left', fill='x', expand=True, padx=8)

    def transform(self):
        try:
            alpha = self.alphabet.get().lower()
            a = int(self.a.get()); b = int(self.b.get())
            text = self.input.get('1.0', 'end')
            if self.direction.get() == 'encrypt':
                out = affine_encrypt(text, a, b, alpha)
            else:
                out = affine_decrypt(text, a, b, alpha)
            self.output.delete('1.0', 'end'); self.output.insert('1.0', out)
            self.normalized_box.delete('1.0', 'end')
            self.normalized_box.insert('1.0', 'N(M) = ' + clean_text(text, alpha))
        except Exception as e:
            messagebox.showerror('Eroare', str(e))

    def verify_roundtrip(self):
        try:
            alpha = self.alphabet.get().lower()
            a = int(self.a.get()); b = int(self.b.get())
            text = self.input.get('1.0', 'end')
            normalized = clean_text(text, alpha)
            c = affine_encrypt(text, a, b, alpha)
            recovered = affine_decrypt(c, a, b, alpha)
            self.show_roundtrip_result(normalized, recovered)
        except Exception as e:
            messagebox.showerror('Eroare verificare', str(e))

    def bruteforce(self):
        try:
            text = self.input.get('1.0', 'end')
            alpha = self.alphabet.get().lower()
            self.attack_out.delete('1.0', 'end')
            if alpha != DEFAULT_ALPHABET:
                self.attack_out.insert('1.0', 'Atacul statistic este calibrat pentru alfabetul englezesc a-z.\n')
                return
            valid_a, m = affine_keyspace(alpha)
            total_keys = len(valid_a) * m
            start = time.perf_counter()
            rows, total_tried = affine_bruteforce(text, alpha, 8)
            elapsed_ms = (time.perf_counter() - start) * 1000
            self.attack_out.insert(
                '1.0',
                f'Spatiu de chei (ipoteze): a coprim cu {m} => {len(valid_a)} valori; b in [0,{m - 1}] => {m} valori.\n'
                f'Total chei testate: {total_tried} (= {total_keys}).\n'
                f'Timp de executie: {elapsed_ms:.3f} ms.\n'
                f'Criteriu de selectie: scor chi-patrat minim intre frecventa literelor din textul decriptat '
                f'si frecventele limbii engleze (text mai mic = mai probabil corect).\n\n'
                f'Top 8 candidati:\n'
            )
            for score, a, b, plain in rows:
                self.attack_out.insert('end', f'a={a:2d}, b={b:2d}, scor={score:8.2f} -> {plain[:90]}\n')
            if rows:
                self.attack_out.insert('end', '\nCompararea frecventelor pentru candidatul cel mai probabil:\n')
                self.attack_out.insert('end', letter_frequency_table(rows[0][3]))
                self.attack_out.insert(
                    'end',
                    '\nInterpretare: cifrul afin este vulnerabil la forta bruta pentru ca spatiul de chei '
                    'este foarte mic (doar 312 combinatii posibile pentru a-z), iar scorul chi-patrat exploateaza '
                    'faptul ca substitutia monoalfabetica pastreaza distributia de frecvente a literelor limbii '
                    'sursa, doar permutata.\n'
                )
        except Exception as e:
            messagebox.showerror('Eroare atac', str(e))

    def export(self):
        path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text', '*.txt')])
        if path:
            export_text_to_file(path, self.output.get('1.0', 'end-1c'))

class VigenereWindow(CipherWindow):
    """
    Fereastra grafica pentru cifrul Vigenere.
    Permite introducerea alfabetului, cheii si textului si permite
    criptarea, decriptarea si verificarea round-trip.
    Afiseaza si forma normalizata a textului, cheia normalizata
    si calculele efectuate pentru fiecare pozitie.
    """
    def __init__(self, master):
        super().__init__(master, 'Cifrul Vigenere', 'cifrul_vigenere.pdf')
        self._build()

    def _build(self):
        """
        Construieste interfata grafica pentru cifrul Vigenere.
        Creeaza campurile pentru alfabet si cheie, butoanele pentru
        criptare/decriptare si zonele pentru textul de intrare,
        rezultat si calculele intermediare.
        """
        top = ttk.Frame(self, padding=10); top.pack(fill='x')
        ttk.Label(top, text='Alfabet:').grid(row=0, column=0, sticky='w')
        self.alphabet = ttk.Entry(top, width=35); self.alphabet.insert(0, DEFAULT_ALPHABET); self.alphabet.grid(row=0, column=1, padx=5)
        ttk.Label(top, text='Cheie:').grid(row=0, column=2)
        self.key = ttk.Entry(top, width=20); self.key.insert(0, 'lemon'); self.key.grid(row=0, column=3, padx=5)
        self.direction = tk.StringVar(value='encrypt')
        ttk.Radiobutton(top, text='Criptare', variable=self.direction, value='encrypt').grid(row=1, column=0, pady=8)
        ttk.Radiobutton(top, text='Decriptare', variable=self.direction, value='decrypt').grid(row=1, column=1, sticky='w')
        ttk.Button(top, text='Transforma', command=self.transform).grid(row=1, column=3)
        ttk.Button(top, text='Verifica round-trip', command=self.verify_roundtrip).grid(row=1, column=4, sticky='w')

        body = ttk.Frame(self, padding=10); body.pack(fill='both', expand=True)
        left = ttk.LabelFrame(body, text='Text de intrare', padding=8); left.pack(side='left', fill='both', expand=True, padx=(0, 5))
        self.input = self.text_widget(left, 10); self.input.pack(fill='both', expand=True)
        right = ttk.LabelFrame(body, text='Rezultat + date intermediare', padding=8); right.pack(side='left', fill='both', expand=True, padx=(5, 0))
        self.output = self.text_widget(right, 5); self.output.pack(fill='both', expand=True)
        self.intermediate = self.text_widget(right, 8); self.intermediate.pack(fill='both', expand=True, pady=6)

    def transform(self):
        try:
            alpha = self.alphabet.get().lower(); key = self.key.get(); text = self.input.get('1.0', 'end')
            if self.direction.get() == 'encrypt':
                out = vigenere_encrypt(text, key, alpha)
            else:
                out = vigenere_decrypt(text, key, alpha)
            self.output.delete('1.0', 'end'); self.output.insert('1.0', out)
            clean = clean_text(text, alpha); k = clean_text(key, alpha)
            self.intermediate.delete('1.0', 'end')
            self.intermediate.insert('1.0', f'N(M) = {clean}\nCheie normalizata = {k}\n\n')
            self.intermediate.insert('end', 'Pozitie | Text | Cheie | Formula\n')
            for i, ch in enumerate(clean[:250]):
                kc = k[i % len(k)]
                self.intermediate.insert('end', f'{i + 1:7d} | {ch} | {kc} | (P {alpha.index(ch)} +/- K {alpha.index(kc)}) mod {len(alpha)}\n')
        except Exception as e:
            messagebox.showerror('Eroare', str(e))

    def verify_roundtrip(self):
        try:
            alpha = self.alphabet.get().lower(); key = self.key.get()
            text = self.input.get('1.0', 'end')
            normalized = clean_text(text, alpha)
            c = vigenere_encrypt(text, key, alpha)
            recovered = vigenere_decrypt(c, key, alpha)
            self.show_roundtrip_result(normalized, recovered)
        except Exception as e:
            messagebox.showerror('Eroare verificare', str(e))

class DoubleTranspositionWindow(CipherWindow):
    """
    Fereastra grafica pentru cifrul cu transpozitie dubla.
    Permite folosirea a doua chei de transpozitie si afiseaza
    fiecare etapa a criptarii sau decriptarii, inclusiv forma
    tablourilor de transpozitie.
    """
    def __init__(self, master):
        super().__init__(master, 'Cifru cu transpozitie dubla pe verticala', 'transpozitie_dubla.pdf')
        self._build()

    def _build(self):
        """
        Construieste interfata grafica pentru transpozitia dubla.
        Creeaza campurile pentru cele doua chei, optiunile de
        criptare/decriptare, campul pentru lungimea originala si
        zonele pentru text, rezultat si etapele intermediare.
        """
        top = ttk.Frame(self, padding=10); top.pack(fill='x')
        ttk.Label(top, text='Cheia 1:').grid(row=0, column=0); self.k1 = ttk.Entry(top, width=18); self.k1.insert(0, 'cript'); self.k1.grid(row=0, column=1, padx=5)
        ttk.Label(top, text='Cheia 2:').grid(row=0, column=2); self.k2 = ttk.Entry(top, width=18); self.k2.insert(0, 'laborator'); self.k2.grid(row=0, column=3, padx=5)
        self.direction = tk.StringVar(value='encrypt')
        ttk.Radiobutton(top, text='Criptare', variable=self.direction, value='encrypt').grid(row=1, column=0, pady=8)
        ttk.Radiobutton(top, text='Decriptare', variable=self.direction, value='decrypt').grid(row=1, column=1, sticky='w')
        ttk.Button(top, text='Transforma', command=self.transform).grid(row=1, column=3)
        ttk.Button(top, text='Verifica round-trip', command=self.verify_roundtrip).grid(row=1, column=4, sticky='w')
        len_row = ttk.Frame(self, padding=(10, 0)); len_row.pack(fill='x')
        ttk.Label(len_row, text='Lungime text original (metadata publica, necesara la decriptare):').pack(side='left')
        self.original_length = ttk.Entry(len_row, width=8)
        self.original_length.pack(side='left', padx=6)
        body = ttk.Frame(self, padding=10); body.pack(fill='both', expand=True)
        left = ttk.LabelFrame(body, text='Text de intrare', padding=8); left.pack(side='left', fill='both', expand=True, padx=(0, 5))
        self.input = self.text_widget(left, 10); self.input.pack(fill='both', expand=True)
        right = ttk.LabelFrame(body, text='Rezultat + etape (inclusiv forma tabloului)', padding=8); right.pack(side='left', fill='both', expand=True, padx=(5, 0))
        self.output = self.text_widget(right, 5); self.output.pack(fill='both', expand=True)
        self.steps = self.text_widget(right, 14); self.steps.pack(fill='both', expand=True, pady=6)
        note = tk.Label(
            self,
            text='Normalizare: spatiile/semnele sunt eliminate, literele devin minuscule (N(M)). '
                 'Tabloul este COMPLETAT cu caractere de umplutura ("x") pana devine un dreptunghi perfect '
                 '- fara celule goale. Lungimea originala este metadata publica, nu secreta.',
            bg='#f3f3f3', fg='#555', wraplength=1000, justify='left'
        )
        note.pack(anchor='w', padx=14, pady=(0, 10))

    def transform(self):
        try:
            text = self.input.get('1.0', 'end'); k1 = self.k1.get(); k2 = self.k2.get()
            self.steps.delete('1.0', 'end')
            if self.direction.get() == 'encrypt':
                normalized = ''.join(ch.lower() for ch in text if ch.isalpha())
                first, second, original_length = double_transposition_encrypt(text, k1, k2)
                out = second
                self.original_length.delete(0, 'end'); self.original_length.insert(0, str(original_length))
                self.steps.insert('1.0', f'N(M): {normalized}  (lungime originala: {original_length})\n\n')
                self.steps.insert('end', f'Forma tabloului pentru transpozitia 1 (cheie={k1}):\n{columnar_shape_description(k1, original_length)}\n')
                self.steps.insert('end', f'Dupa transpozitia 1 (tablou completat):\n{first}\n\n')
                self.steps.insert('end', f'Forma tabloului pentru transpozitia 2 (cheie={k2}):\n{columnar_shape_description(k2, len(first))}\n')
                self.steps.insert('end', f'Dupa transpozitia 2 (rezultat final):\n{second}\n\n')
                self.steps.insert('end', f'IMPORTANT: pentru decriptare, retineti lungimea originala = {original_length} '
                                          f'(afisata mai sus si completata automat in campul dedicat).')
            else:
                clean_input = ''.join(ch.lower() for ch in text if ch.isalpha())
                try:
                    original_length = int(self.original_length.get())
                except ValueError:
                    raise ValueError('Introduceti lungimea originala a textului (numar intreg), afisata la criptare.')
                after, original = double_transposition_decrypt(text, k1, k2, original_length); out = original
                first_length = columnar_padded_length(original_length, k1)
                self.steps.insert('1.0', f'Text criptat (curatat): {clean_input}\n\n')
                self.steps.insert('end', f'Forma tabloului pentru anularea transpozitiei 2 (cheie={k2}):\n{columnar_shape_description(k2, first_length)}\n')
                self.steps.insert('end', f'Dupa anularea transpozitiei 2 (inca are umplutura):\n{after}\n\n')
                self.steps.insert('end', f'Forma tabloului pentru anularea transpozitiei 1 (cheie={k1}):\n{columnar_shape_description(k1, original_length)}\n')
                self.steps.insert('end', f'Dupa anularea transpozitiei 1 si eliminarea umpluturii (text recuperat):\n{original}\n')
            self.output.delete('1.0', 'end'); self.output.insert('1.0', out)
        except Exception as e:
            messagebox.showerror('Eroare', str(e))

    def verify_roundtrip(self):
        try:
            text = self.input.get('1.0', 'end')
            k1 = self.k1.get(); k2 = self.k2.get()
            normalized = ''.join(ch.lower() for ch in text if ch.isalpha())
            _, c, original_length = double_transposition_encrypt(text, k1, k2)
            _, recovered = double_transposition_decrypt(c, k1, k2, original_length)
            self.show_roundtrip_result(normalized, recovered)
        except Exception as e:
            messagebox.showerror('Eroare verificare', str(e))

class ADFGVXWindow(CipherWindow):
    def __init__(self, master):
        super().__init__(master, 'Cifrul mixt ADFGVX', 'cifrul_adfgvx.pdf')
        self._build()

    def _build(self):
        """Construieste interfata grafica: chei, text, rezultate si optiuni de atac."""
        top = ttk.Frame(self, padding=10); top.pack(fill='x')
        ttk.Label(top, text='Cheia patratului:').grid(row=0, column=0); self.sk = ttk.Entry(top, width=18); self.sk.insert(0, 'secret'); self.sk.grid(row=0, column=1, padx=5)
        ttk.Label(top, text='Cheia transpozitiei:').grid(row=0, column=2); self.transposition_key = ttk.Entry(top, width=18); self.transposition_key.insert(0, 'cipher'); self.transposition_key.grid(row=0, column=3, padx=5)
        self.direction = tk.StringVar(value='encrypt')
        ttk.Radiobutton(top, text='Criptare', variable=self.direction, value='encrypt').grid(row=1, column=0, pady=8)
        ttk.Radiobutton(top, text='Decriptare', variable=self.direction, value='decrypt').grid(row=1, column=1, sticky='w')
        ttk.Button(top, text='Transforma', command=self.transform).grid(row=1, column=3)
        ttk.Button(top, text='Verifica round-trip', command=self.verify_roundtrip).grid(row=1, column=4, sticky='w')
        len_row = ttk.Frame(self, padding=(10, 0)); len_row.pack(fill='x')
        ttk.Label(len_row, text='Lungime (simboluri ADFGVX) original, inainte de umplutura - metadata publica:').pack(side='left')
        self.original_length = ttk.Entry(len_row, width=8)
        self.original_length.pack(side='left', padx=6)
        body = ttk.Frame(self, padding=10); body.pack(fill='both', expand=True)
        left = ttk.LabelFrame(body, text='Text de intrare', padding=8); left.pack(side='left', fill='both', expand=True, padx=(0, 5))
        self.input = self.text_widget(left, 9); self.input.pack(fill='both', expand=True)
        right = ttk.LabelFrame(body, text='Rezultat + date intermediare', padding=8); right.pack(side='left', fill='both', expand=True, padx=(5, 0))
        self.output = self.text_widget(right, 5); self.output.pack(fill='both', expand=True)
        self.steps = self.text_widget(right, 12); self.steps.pack(fill='both', expand=True, pady=6)
        ttk.Button(self, text='Afiseaza patratul ADFGVX', command=self.show_square).pack(anchor='w', padx=14, pady=(0, 10))

        attack = ttk.LabelFrame(
            self,
            text='Rezistenta criptografica - forta bruta pe transpozitie (cheia patratului presupusa cunoscuta)',
            padding=8
        )
        attack.pack(fill='x', padx=10, pady=(0, 10))
        attack_top = ttk.Frame(attack); attack_top.pack(fill='x')
        ttk.Label(attack_top, text='Lungime cheie transpozitie presupusa:').pack(side='left')
        self.assumed_length = ttk.Spinbox(attack_top, from_=1, to=12, width=5)
        self.assumed_length.set(str(len(self.transposition_key.get()) or 6))
        self.assumed_length.pack(side='left', padx=6)
        ttk.Button(attack_top, text='Testeaza forta bruta', command=self.bruteforce_transposition).pack(side='left', padx=6)
        self.attack_out = tk.Text(attack, height=13, wrap='word', font=('Consolas', 9))
        self.attack_out.pack(fill='both', expand=True, pady=6)

    def show_square(self):
        _, _, alpha = build_adfgvx_square(self.sk.get())
        win = tk.Toplevel(self); win.title('Patrat ADFGVX')
        tk.Label(win, text='    ' + '   '.join(ADFGVX_SYMBOLS), font=('Consolas', 12, 'bold')).pack(pady=(10, 2))
        for r in range(6):
            line = ' '.join(f'{alpha[r * 6 + c]:>2}' for c in range(6))
            tk.Label(win, text=f'{ADFGVX_SYMBOLS[r]} {line}', font=('Consolas', 12)).pack(anchor='w', padx=20)

    def transform(self):
        try:
            text = self.input.get('1.0', 'end'); sk = self.sk.get(); tk_key = self.transposition_key.get(); self.steps.delete('1.0', 'end')
            if self.direction.get() == 'encrypt':
                sub, out, alpha, original_length = adfgvx_encrypt(text, sk, tk_key)
                self.output.delete('1.0', 'end'); self.output.insert('1.0', out)
                self.original_length.delete(0, 'end'); self.original_length.insert(0, str(original_length))
                self.steps.insert('1.0', f'N(M) (alfabet ADFGVX): {clean_text(text, ADFGVX_ALPHABET)}\n\n')
                self.steps.insert('end', f'Alfabetul cheiat (6x6): {alpha}\n\n')
                self.steps.insert('end', f'Dupa substitutie ADFGVX (lungime originala: {original_length} simboluri): {sub}\n\n')
                self.steps.insert('end', f'Forma tabloului pentru transpozitie (cheie={tk_key}):\n{columnar_shape_description(tk_key, original_length)}\n')
                self.steps.insert('end', f'Dupa transpozitie pe coloane (tablou completat, rezultat final):\n{out}\n\n')
                self.steps.insert('end', f'IMPORTANT: pentru decriptare, retineti lungimea originala = {original_length} '
                                          f'(completata automat in campul dedicat).')
            else:
                try:
                    original_length = int(self.original_length.get())
                except ValueError:
                    raise ValueError('Introduceti lungimea originala (in simboluri ADFGVX), afisata la criptare.')
                after, plain, alpha = adfgvx_decrypt(text, sk, tk_key, original_length)
                only_symbols = ''.join(ch for ch in text.upper() if ch in ADFGVX_SYMBOLS)
                self.output.delete('1.0', 'end'); self.output.insert('1.0', plain)
                self.steps.insert('1.0', f'Alfabetul cheiat (6x6): {alpha}\n\n')
                self.steps.insert('end', f'Forma tabloului pentru anularea transpozitiei (cheie={tk_key}):\n{columnar_shape_description(tk_key, original_length)}\n')
                self.steps.insert('end', f'Text criptat (doar simboluri ADFGVX, lungime={len(only_symbols)}): {only_symbols}\n\n')
                self.steps.insert('end', f'Dupa inversarea transpozitiei si eliminarea umpluturii: {after}\n\n')
                self.steps.insert('end', f'Dupa substitutie inversa (text recuperat): {plain}')
        except Exception as e:
            messagebox.showerror('Eroare', str(e))

    def verify_roundtrip(self):
        try:
            text = self.input.get('1.0', 'end')
            sk = self.sk.get(); tk_key = self.transposition_key.get()
            normalized = clean_text(text, ADFGVX_ALPHABET)
            _, c, _, original_length = adfgvx_encrypt(text, sk, tk_key)
            _, recovered, _ = adfgvx_decrypt(c, sk, tk_key, original_length)
            self.show_roundtrip_result(normalized, recovered)
        except Exception as e:
            messagebox.showerror('Eroare verificare', str(e))

    def bruteforce_transposition(self):
        try:
            text = self.input.get('1.0', 'end')
            sk = self.sk.get()
            try:
                key_length = int(self.assumed_length.get())
            except ValueError:
                raise ValueError('Introduceti o lungime intreaga pentru cheia de transpozitie presupusa.')
            if key_length < 1:
                raise ValueError('Lungimea cheii trebuie sa fie cel putin 1.')
            try:
                original_length = int(self.original_length.get())
            except ValueError:
                raise ValueError(
                    'Introduceti lungimea originala (in simboluri ADFGVX) in campul dedicat - '
                    'este afisata automat dupa o criptare.'
                )

            self.attack_out.delete('1.0', 'end')
            start = time.perf_counter()
            results, tried, total_permutations, exhaustive = adfgvx_bruteforce_transposition(
                text, sk, key_length, original_length, limit_candidates=8
            )
            elapsed_ms = (time.perf_counter() - start) * 1000
            mode_text = (
                'exhaustiva (s-au incercat TOATE permutarile posibile)' if exhaustive else
                f'esantion aleator de {tried} permutari distincte (spatiul complet are '
                f'{total_permutations} permutari - mult prea mare pentru o cautare exhaustiva)'
            )
            self.attack_out.insert(
                '1.0',
                'Ipoteza atacului:\n'
                f'  - cheia patratului 6x6 este presupusa CUNOSCUTA (= "{sk}"); se ataca DOAR ordinea '
                f'coloanelor din transpozitie.\n'
                f'  - lungimea cheii de transpozitie este presupusa = {key_length} (numar de coloane).\n'
                f'  - lungimea originala (inainte de umplutura) = {original_length} simboluri ADFGVX '
                f'este presupusa cunoscuta (metadata publica).\n\n'
                'De ce nu se ataca si cheia patratului: alfabetul keyed_alphabet are pana la 36! posibile '
                'ordonari - un spatiu complet intractabil pentru forta bruta. De aceea demonstratia se '
                'limiteaza la partea tractabila a problemei: permutarea coloanelor.\n\n'
                f'Spatiul de chei (ipoteze) pentru transpozitie: {key_length}! = {total_permutations} permutari.\n'
                f'Mod de cautare: {mode_text}.\n'
                f'Permutari efectiv testate: {tried}.\n'
                f'Timp de executie: {elapsed_ms:.3f} ms.\n'
                'Criteriu de selectie: scor chi-patrat minim intre frecventa literelor textului decriptat '
                'si frecventele limbii engleze.\n\n'
                f'Top {len(results)} candidati:\n'
            )
            for score, order, plain in results:
                self.attack_out.insert('end', f'ordine coloane={order}, scor={score:8.2f} -> {plain[:80]}\n')
            if results:
                self.attack_out.insert('end', '\nCompararea frecventelor pentru candidatul cel mai probabil:\n')
                self.attack_out.insert('end', letter_frequency_table(results[0][2]))
            self.attack_out.insert(
                'end',
                '\nLimita demonstratiei: daca lungimea de cheie presupusa e gresita, sau daca cheia '
                'patratului nu e de fapt cunoscuta, atacul NU va gasi textul corect. Pentru lungimi mari '
                'de cheie, cautarea exhaustiva devine intractabila (n! creste extrem de rapid), iar '
                'esantionarea aleatoare nu garanteaza gasirea permutarii corecte - doar creste '
                'probabilitatea de a gasi un candidat plauzibil.\n'
            )
        except Exception as e:
            messagebox.showerror('Eroare atac', str(e))

class MainInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Sisteme de criptare clasice - Laborator N1')
        self.geometry('820x560')
        self.minsize(760, 520)
        self.configure(bg='#f3f3f3')
        self._style()
        self._build()
        self._check_docs()

    def _style(self):
        style = ttk.Style(self)
        try:
            style.theme_use('clam')
        except Exception:
            pass
        style.configure('TButton', padding=7, font=('Segoe UI', 10))
        style.configure('TLabel', font=('Segoe UI', 10))
        style.configure('TCombobox', font=('Segoe UI', 10))

    def _build(self):
        """Construieste interfata principala cu lista de cifruri, descriere si butoane."""
        title = tk.Label(self, text='Sisteme de criptare clasice',
                          font=('Segoe UI', 18, 'bold'), bg='#dedede')
        title.pack(fill='x', padx=22, pady=(20, 12))

        select_box = ttk.LabelFrame(
            self, text='Precizati cifrul care va fi utilizat', padding=18
        )
        select_box.pack(fill='x', padx=45, pady=8)

        ttk.Label(select_box, text='Cifru:').grid(
            row=0, column=0, sticky='w', padx=(0, 10)
        )

        self.options = [
            ('Cifru cu transpozitie dubla pe verticala', 'Transpozitie dubla'),
            ('Cifru cu substitutie monoalfabetica - Afin', 'Afin'),
            ('Cifru cu substitutie polialfabetica - Vigenere', 'Vigenere'),
            ('Cifru mixt cu permutare si substitutie - ADFGVX', 'ADFGVX')
        ]

        self.cipher_map = {label: value for label, value in self.options}
        labels = [label for label, _ in self.options]

        self.combo = ttk.Combobox(
            select_box, state='readonly', width=58, values=labels
        )
        self.combo.current(1)
        self.combo.grid(row=0, column=1, sticky='ew')
        self.combo.bind('<<ComboboxSelected>>', self.update_info)
        select_box.columnconfigure(1, weight=1)

        info = ttk.LabelFrame(self, text='Prezentarea cifrului', padding=18)
        info.pack(fill='both', expand=True, padx=45, pady=10)

        self.info = tk.Label(
            info, text='', bg='#f3f3f3', justify='left', wraplength=650,
            font=('Segoe UI', 11)
        )
        self.info.pack(anchor='w', fill='x', pady=8)

        btns = ttk.Frame(info)
        btns.pack(pady=18)
        ttk.Button(btns, text='Deschide cifrul', command=self.open_selected).grid(
            row=0, column=0, padx=8
        )
        ttk.Button(btns, text='Descrierea cifrului (PDF)',
                   command=self.open_pdf_selected).grid(row=0, column=1, padx=8)
        ttk.Button(btns, text='Despre laborator', command=self.show_about).grid(
            row=0, column=2, padx=8
        )

        self.update_info()

    def get_selected_cipher(self):
        """Returneaza cifrul selectat din lista sau genereaza o eroare daca nu exista o selectie."""
        selected_label = self.combo.get()
        if selected_label not in self.cipher_map:
            raise ValueError('Selectati un cifru din lista.')
        return self.cipher_map[selected_label]

    def update_info(self, event=None):
        try:
            val = self.get_selected_cipher()
        except ValueError:
            return

        desc = {
            'Transpozitie dubla':
                'Cifru cu permutare in doua etape. Textul este aranjat intr-un tabel si este citit conform ordinii determinate de prima, apoi de a doua cheie. Tabloul este completat cu caractere de umplutura pana devine un dreptunghi complet (fara celule goale); lungimea originala este afisata si folosita la decriptare.',
            'Afin':
                'Cifru cu substitutie monoalfabetica. Formula este E(x) = (a*x + b) mod m. Cifrul Caesar este cazul particular in care a = 1. Spatiul de chei este mic, de aceea este vulnerabil la forta bruta.',
            'Vigenere':
                'Cifru cu substitutie polialfabetica. Fiecare caracter este deplasat folosind caracterul corespunzator din cheia repetata. Este vulnerabil la analiza indicelui de coincidenta pentru chei scurte.',
            'ADFGVX':
                'Cifru mixt care combina substitutia intr-un patrat 6x6 cu o transpozitie pe coloane. Utilizeaza simbolurile A, D, F, G, V si X.'
        }
        self.info.config(text=desc[val])

    def open_selected(self):
        try:
            val = self.get_selected_cipher()
        except ValueError as e:
            messagebox.showwarning('Selectie', str(e))
            return

        windows = {
            'Afin': AffineWindow,
            'Vigenere': VigenereWindow,
            'Transpozitie dubla': DoubleTranspositionWindow,
            'ADFGVX': ADFGVXWindow
        }
        windows[val](self)

    def open_pdf_selected(self):
        try:
            val = self.get_selected_cipher()
        except ValueError as e:
            messagebox.showwarning('Selectie', str(e))
            return

        names = {
            'Afin': 'cifrul_afin.pdf',
            'Vigenere': 'cifrul_vigenere.pdf',
            'Transpozitie dubla': 'transpozitie_dubla.pdf',
            'ADFGVX': 'cifrul_adfgvx.pdf'
        }
        if not open_pdf(os.path.join(DOC_DIR, names[val])):
            messagebox.showwarning(
                'PDF', 'PDF-ul nu poate fi deschis. Il gasiti in folderul docs.'
            )

    def show_about(self):
        messagebox.showinfo(
            'Laborator N1',
            'Aplicatie Python + Tkinter pentru cifrurile clasice cerute:\n'
            '- Transpozitie dubla pe verticala\n'
            '- Cifru Afin (Caesar - caz particular)\n'
            '- Cifrul Vigenere\n'
            '- Cifrul ADFGVX\n\n'
            'Politica de normalizare: mod clasic (litere mici, doar alfabetul '
            'de lucru), cu verificare explicita a relatiei D(E(N(M))) = N(M) '
            'in fiecare fereastra (buton "Verifica round-trip").\n\n'
            'Aplicatia include criptare, decriptare, date intermediare, '
            'documentatie PDF (deja generata, in folderul docs) si teste de '
            'rezistenta criptografica cu masurarea spatiului de chei si a '
            'timpului de executie.'
        )

    def _check_docs(self):
        """PDF-urile sunt deja create - aici doar verificam existenta lor,
        NU le mai generam automat."""
        expected = ['cifrul_afin.pdf', 'cifrul_vigenere.pdf', 'transpozitie_dubla.pdf', 'cifrul_adfgvx.pdf']
        missing = [name for name in expected if not os.path.exists(os.path.join(DOC_DIR, name))]
        if missing:
            print('Atentie: nu s-au gasit in folderul docs urmatoarele fisiere PDF:', ', '.join(missing))


if __name__ == '__main__':
    app = MainInterface()
    app.mainloop()
