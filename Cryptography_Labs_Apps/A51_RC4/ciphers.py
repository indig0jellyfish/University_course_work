from typing import List, Tuple
ENCODING = "utf-8"


def text_to_bytes(text: str) -> bytes: # primeste text si transf in octeti (bytes)
    return text.encode(ENCODING)


def bytes_to_text(data: bytes) -> str: # incearca sa transforme octetii in text
    try:
        return data.decode(ENCODING)
    except UnicodeDecodeError:
        return "[nu se poate decoda UTF-8] " + data.hex()


def bytes_to_bits(data: bytes) -> List[int]:
    bits = []
    for byte in data:
        for k in range(7, -1, -1): # se parcurg cei 8 biti a octet, de la cel mai semnificatic la mai putin semnif
            bits.append((byte >> k) & 1) # extrage bitul, e pus in lista
    return bits


def bits_to_bytes(bits: List[int]) -> bytes:
    pad = (-len(bits)) % 8
    bits = bits + [0] * pad
    out = bytearray()
    for i in range(0, len(bits), 8): # cate 8 biti, se reconstr octetul
        byte = 0
        for b in bits[i:i + 8]:
            byte = (byte << 1) | b # completeaza cu 0 daca nu e multiplu de 8 (nu ar trebui sa se intample in fluxul normal al aplicatiei, dar ramane o protectie)
        out.append(byte)
    return bytes(out)


def xor_bits(a: List[int], b: List[int]) -> List[int]:# a5/1
    n = min(len(a), len(b))
    return [a[i] ^ b[i] for i in range(n)]


def xor_bytes(a: bytes, b: bytes) -> bytes: # rc4
    n = min(len(a), len(b))
    return bytes(a[i] ^ b[i] for i in range(n))


def hex_of_bits(bits: List[int]) -> str: # biti -> bytes -> hex
    return bits_to_bytes(bits).hex()


def char_breakdown(text: str, max_chars: int = 8): # demonstatie educationala
    rows = []
    data = text_to_bytes(text)
    shown = 0
    idx = 0
    for ch in text:
        ch_bytes = ch.encode(ENCODING)
        for b in ch_bytes:
            rows.append((ch, b, format(b, "08b")))
            shown += 1
        if shown >= max_chars:
            break
    return rows



# A5/1

A51_R1_LEN, A51_R2_LEN, A51_R3_LEN = 19, 22, 23 # registre de deplasare, lungimea lor (total 64 bit)
A51_R1_CLOCK, A51_R2_CLOCK, A51_R3_CLOCK = 8, 10, 10 # poz folos pt clocking (decid care registre se deplaseaza)
A51_R1_TAPS: Tuple[int, ...] = (13, 16, 17, 18) # poz din registre folos pt calc bitului de feedback
A51_R2_TAPS: Tuple[int, ...] = (20, 21)
A51_R3_TAPS: Tuple[int, ...] = (7, 20, 21, 22)
A51_KEY_BITS = 64 # cheia
A51_COUNT_BITS = 22
A51_WARMUP_CLOCKS = 100


def a51_new_state() -> dict: # creeaza stare noua ((registre goale, loguri goale))
    return {
        "r1": [0] * A51_R1_LEN,
        "r2": [0] * A51_R2_LEN,
        "r3": [0] * A51_R3_LEN,
        "init_log": [], # pt interfata
        "clock_log": [],
        "initialized": False,
    }


def _a51_feedback(reg: List[int], taps: Tuple[int, ...]) -> int: # calc xor -> f = R1[13] ^ R1[16] ^ R1[17] ^ R1[18]
    f = 0
    for t in taps:
        f ^= reg[t]
    return f


def _a51_shift(reg: List[int], taps: Tuple[int, ...], inbit: int = None): # calc feedback, deplas registru
    f = _a51_feedback(reg, taps)
    if inbit is not None: # inbit e un bit suplimentar, primit din exterior
        f ^= inbit
    new_reg = [f] + reg[:-1] # feedback + toate elem registrului cu except ultimului
    return new_reg, f


def _a51_majority_bits(state: dict): # care registre se deplas la urmatorul pas
    c1 = state["r1"][A51_R1_CLOCK] # clock bits!!
    c2 = state["r2"][A51_R2_CLOCK]
    c3 = state["r3"][A51_R3_CLOCK]
    maj = 1 if (c1 + c2 + c3) >= 2 else 0 # se deplas reg ale caror bit de ceas e egal cu majorit
    return c1, c2, c3, maj


def a51_clock_once(state: dict, record: bool = True) -> int:
    c1, c2, c3, maj = _a51_majority_bits(state)
    moved = [] # care reg au fost depl
    if c1 == maj:
        state["r1"], _ = _a51_shift(state["r1"], A51_R1_TAPS)
        moved.append("R1")
    if c2 == maj:
        state["r2"], _ = _a51_shift(state["r2"], A51_R2_TAPS)
        moved.append("R2")
    if c3 == maj:
        state["r3"], _ = _a51_shift(state["r3"], A51_R3_TAPS)
        moved.append("R3")
    z = state["r1"][18] ^ state["r2"][21] ^ state["r3"][22] # calc bit de iesire (xor a ultim bit fiecare reg)- bit al keystream
    if record:
        state["clock_log"].append({
            "u1": c1, "u2": c2, "u3": c3, "F": maj,
            "deplasate": ",".join(moved) if moved else "-",
            "z": z,
            "R1": "".join(map(str, state["r1"])),
            "R2": "".join(map(str, state["r2"])),
            "R3": "".join(map(str, state["r3"])),
        })
    return z


def a51_load_key_and_count(state: dict, key_bits: List[int], count_bits: List[int]) -> dict: # key si count bits sunt din app.py
    if len(key_bits) != A51_KEY_BITS:
        raise ValueError(f"Cheia A5/1 trebuie sa aiba exact {A51_KEY_BITS} biti (64 = 16 cifre hex).")
    if len(count_bits) != A51_COUNT_BITS:
        raise ValueError(f"Count trebuie sa aiba exact {A51_COUNT_BITS} biti (valoare 0..4194303).")

    state["r1"] = [0] * A51_R1_LEN
    state["r2"] = [0] * A51_R2_LEN
    state["r3"] = [0] * A51_R3_LEN
    state["init_log"] = []
    state["clock_log"] = []

    # Faza 1: incarcarea cheii, enumerate(key_bits) parcurge fiecare bit al cheii și furnizează indexul step și valoarea bitului kb
    for step, kb in enumerate(key_bits):
        state["r1"], _ = _a51_shift(state["r1"], A51_R1_TAPS, kb) # calc feedback pt r1 si se comb cu bit cheii, r1 se depl
        state["r2"], _ = _a51_shift(state["r2"], A51_R2_TAPS, kb)
        state["r3"], _ = _a51_shift(state["r3"], A51_R3_TAPS, kb)
        state["init_log"].append({
            "faza": "Key", "pas": step, "bit_intrare": kb,
            "R1": "".join(map(str, state["r1"])),
            "R2": "".join(map(str, state["r2"])),
            "R3": "".join(map(str, state["r3"])),
        })

    # Faza 2: incarcarea Count (22 cicluri, clocking regulat)
    for step, cb in enumerate(count_bits):
        state["r1"], _ = _a51_shift(state["r1"], A51_R1_TAPS, cb)
        state["r2"], _ = _a51_shift(state["r2"], A51_R2_TAPS, cb)
        state["r3"], _ = _a51_shift(state["r3"], A51_R3_TAPS, cb)
        state["init_log"].append({
            "faza": "Count", "pas": step, "bit_intrare": cb,
            "R1": "".join(map(str, state["r1"])),
            "R2": "".join(map(str, state["r2"])),
            "R3": "".join(map(str, state["r3"])),
        })

    # Faza 3: 100 de cicluri de "incalzire" cu ceas majoritar, iesirea se arunca (se calc major, deplas registr coresp, calc bit de iesire z, nu e pastrat pt flux final)
    for _ in range(A51_WARMUP_CLOCKS): 
        a51_clock_once(state, record=False)

    state["initialized"] = True
    return state


def a51_generate_bits(state: dict, n: int, record: bool = True) -> List[int]: # genereaza n biti
    if not state.get("initialized"):
        raise RuntimeError("A5/1 nu a fost initializat (lipseste incarcarea cheii/Count).")
    return [a51_clock_once(state, record=record) for _ in range(n)]


def a51_step(state: dict) -> dict: # Avanseaza generatorul cu UN singur ceas (mod Step / Next iteration)
    a51_clock_once(state, record=True)
    return state["clock_log"][-1]


def hex_key_to_bits64(hex_key: str) -> List[int]:
    hex_key = hex_key.strip().replace(" ", "")
    if len(hex_key) != 16:
        raise ValueError("Cheia A5/1 trebuie introdusa ca 16 cifre hexazecimale (64 biti).")
    try:
        value = int(hex_key, 16)
    except ValueError:
        raise ValueError("Cheia A5/1 contine caractere ne-hexazecimale.")
    return [(value >> (63 - i)) & 1 for i in range(64)]


def int_count_to_bits22(count_val: int) -> List[int]:
    if not (0 <= count_val < (1 << 22)):
        raise ValueError("Count trebuie sa fie intre 0 si 4194303 (22 biti).")
    return [(count_val >> (21 - i)) & 1 for i in range(22)]




# RC4
RC4_MIN_KEY_BYTES = 1
RC4_MAX_KEY_BYTES = 256


def rc4_init(key: bytes) -> dict:
    if not (RC4_MIN_KEY_BYTES <= len(key) <= RC4_MAX_KEY_BYTES):
        raise ValueError("Cheia RC4 trebuie sa aiba intre 1 si 256 octeti.")

    S = list(range(256)) # KEYSTREAM, vect de 256 valori posib a unui octet
    ksa_log = []
    j = 0 # KEY SCHEDULING
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256 # key[i % len(key)]) cheia se repeta
        S[i], S[j] = S[j], S[i]
        if i < 10:
            ksa_log.append({"i": i, "j": j, "S[i]_dupa_swap": S[i], "S[j]_dupa_swap": S[j]}) # primele 10 etape ksa pentru explicari

    return {
        "key": key,
        "S": S,
        "S_dupa_ksa": S.copy(),   # copie, ca sa o pastram neschimbata de PRGA
        "i": 0,
        "j": 0,
        "ksa_log": ksa_log,
        "prga_log": [],
    }


def rc4_prga_next(state: dict, record: bool = False) -> int: # state pastreaza return al rc4
    S = state["S"]
    state["i"] = (state["i"] + 1) % 256 # calc i, j, swap, generarea oct z (nr de la 0 l 255)
    state["j"] = (state["j"] + S[state["i"]]) % 256
    S[state["i"]], S[state["j"]] = S[state["j"]], S[state["i"]]
    t = (S[state["i"]] + S[state["j"]]) % 256
    z = S[t] # KEY STREAM KS
    if record:
        state["prga_log"].append({"i": state["i"], "j": state["j"], "t": t, "z": z})
    return z


def rc4_keystream(state: dict, n: int, record_first: int = 10) -> bytes: # gener n octeti de keystream (10 octeti sunt inregistr pe demonstr)
    out = bytearray()
    for k in range(n):
        out.append(rc4_prga_next(state, record=(k < record_first)))
    return bytes(out)


def rc4_step(state: dict) -> dict: # interf educationala unde utiliz poate apasa (urmatorul pas) si sa vada cum se modif
    rc4_prga_next(state, record=True)
    return state["prga_log"][-1]


def parse_rc4_key(raw: str, as_hex: bool) -> bytes: # transf cheia introdusa in o forma pt rc4
    raw = raw.strip()
    if not raw:
        raise ValueError("Cheia RC4 nu poate fi goala.")
    if as_hex: # daca am ales ca este pusa cheia deodata in hex
        raw = raw.replace(" ", "")
        if len(raw) % 2 != 0:
            raise ValueError("Cheia hex trebuie sa aiba un numar par de cifre.")
        try:
            return bytes.fromhex(raw)
        except ValueError:
            raise ValueError("Cheia hex contine caractere invalide.")
    else:
        return raw.encode(ENCODING)




# Experiment: reutilizarea cheii fluide
def reuse_experiment(m1: bytes, m2: bytes, keystream: bytes) -> dict:
    """
    C1 = M1 xor Z ; C2 = M2 xor Z
    Verifica: C1 xor C2 == M1 xor M2
    Recuperare: M2' = C1 xor C2 xor M1  (presupunand M1 cunoscut)
    Mesajele sunt trunchiate la lungimea minima comuna (si a keystream-ului).
    """
    n = min(len(m1), len(m2), len(keystream))
    m1, m2, keystream = m1[:n], m2[:n], keystream[:n]

    c1 = xor_bytes(m1, keystream)
    c2 = xor_bytes(m2, keystream)
    c1_xor_c2 = xor_bytes(c1, c2)
    m1_xor_m2 = xor_bytes(m1, m2)
    m2_recovered = xor_bytes(xor_bytes(c1, c2), m1)

    return {
        "n": n,
        "c1": c1, "c2": c2,
        "c1_xor_c2": c1_xor_c2,
        "m1_xor_m2": m1_xor_m2,
        "relatia_verificata": c1_xor_c2 == m1_xor_m2,
        "m2_recovered": m2_recovered,
        "recuperare_corecta": m2_recovered == m2,
    }
