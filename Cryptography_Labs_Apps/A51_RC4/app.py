import tkinter as tk
from tkinter import ttk, messagebox

from ciphers import (
    text_to_bytes, bytes_to_text, bytes_to_bits, bits_to_bytes,
    xor_bits, xor_bytes, hex_of_bits, char_breakdown, ENCODING,
    a51_new_state, a51_load_key_and_count, a51_generate_bits, a51_step,
    hex_key_to_bits64, int_count_to_bits22,
    rc4_init, rc4_keystream, rc4_step, parse_rc4_key,
    reuse_experiment,
)

FONT_MONO = ("Consolas", 9)



# Utilitare de interfata (functii simple, reutilizate de toate tab-urile)

def make_table(parent, columns, height=8):
    """Creeaza un Treeview (tabel) cu coloanele date si intoarce (tree, scrollbar)."""
    tree = ttk.Treeview(parent, columns=columns, show="headings", height=height)
    for c in columns:
        tree.heading(c, text=c)
        tree.column(c, width=max(70, 620 // len(columns)), anchor="center")
    vsb = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    return tree, vsb


def fill_table(tree, rows, columns):
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", "end", values=[row.get(c, "") for c in columns])


def fill_char_breakdown(table, text, max_chars=8):
    rows = [{"Caracter": ch, "Cod (dec)": code, "Binar (8 biti)": b}
            for ch, code, b in char_breakdown(text, max_chars)]
    fill_table(table, rows, ("Caracter", "Cod (dec)", "Binar (8 biti)"))


def log_line(text_widget, msg):
    text_widget.insert("end", msg + "\n")
    text_widget.see("end")


def log_s_grid(text_widget, S, title="S dupa KSA"):
    log_line(text_widget, f"{title} (256 valori, 16 pe rand):")
    for r in range(16):
        log_line(text_widget, " ".join(f"{v:3d}" for v in S[r * 16:(r + 1) * 16]))


# TAB 1: A5/1
def build_a51_tab(notebook):
    frame = ttk.Frame(notebook, padding=10)

    # starea mutabila a acestui tab, intr-un singur dictionar
    data = {
        "a5": None, # starea A5/1 curenta (dict din ciphers.py)
        "last_msg_bytes": None,
        "last_cipher_bytes": None,
    }

    top = ttk.LabelFrame(frame, text="Cheie si parametri (A5/1)")
    top.pack(fill="x", pady=(0, 8))

    ttk.Label(top, text="Cheie Kc (16 cifre hex = 64 biti):").grid(row=0, column=0, sticky="w", padx=4, pady=3)
    key_entry = ttk.Entry(top, width=24, font=FONT_MONO)
    key_entry.insert(0, "0123456789ABCDEF")
    key_entry.grid(row=0, column=1, sticky="w", padx=4)

    ttk.Label(top, text="Count (0..4194303, 22 biti):").grid(row=0, column=2, sticky="w", padx=4)
    count_entry = ttk.Entry(top, width=12, font=FONT_MONO)
    count_entry.insert(0, "12345")
    count_entry.grid(row=0, column=3, sticky="w", padx=4)

    ttk.Label(top, text="Mesaj (UTF-8):").grid(row=1, column=0, sticky="w", padx=4, pady=3)
    msg_entry = ttk.Entry(top, width=50, font=FONT_MONO)
    msg_entry.insert(0, "Atac in zori")
    msg_entry.grid(row=1, column=1, columnspan=3, sticky="we", padx=4)

    btns = ttk.Frame(top)
    btns.grid(row=2, column=0, columnspan=4, sticky="w", pady=6)

    rep = ttk.LabelFrame(frame, text="Caracter -> cod numeric -> binar (primele caractere)")
    rep.pack(fill="x", pady=4)
    rep_table, rep_vsb = make_table(rep, ("Caracter", "Cod (dec)", "Binar (8 biti)"), height=4)
    rep_table.pack(side="left", fill="x", expand=True)
    rep_vsb.pack(side="left", fill="y")

    mid = ttk.Frame(frame)
    mid.pack(fill="both", expand=True, pady=4)

    init_frame = ttk.LabelFrame(mid, text="Incarcarea cheii/Count (ultimii pasi afisati)")
    init_frame.pack(side="left", fill="both", expand=True, padx=(0, 4))
    init_table, init_vsb = make_table(init_frame, ("faza", "pas", "bit_intrare", "R1", "R2", "R3"), height=8)
    init_table.pack(side="left", fill="both", expand=True)
    init_vsb.pack(side="left", fill="y")

    clock_frame = ttk.LabelFrame(mid, text="Ceas majoritar (u1,u2,u3,F, registre deplasate, z)")
    clock_frame.pack(side="left", fill="both", expand=True, padx=(4, 0))
    clock_table, clock_vsb = make_table(
        clock_frame, ("u1", "u2", "u3", "F", "deplasate", "z", "R1", "R2", "R3"), height=8)
    clock_table.pack(side="left", fill="both", expand=True)
    clock_vsb.pack(side="left", fill="y")

    out = ttk.LabelFrame(frame, text="Rezultate")
    out.pack(fill="both", expand=True, pady=4)
    out_text = tk.Text(out, height=8, font=FONT_MONO, wrap="word")
    out_text.pack(fill="both", expand=True)

    def read_params():
        key_bits = hex_key_to_bits64(key_entry.get())
        count_val = int(count_entry.get().strip())
        count_bits = int_count_to_bits22(count_val)
        return key_bits, count_bits

    def on_init():
        try:
            key_bits, count_bits = read_params()
        except ValueError as e:
            messagebox.showerror("Parametri invalizi", str(e))
            return
        except Exception:
            messagebox.showerror("Parametri invalizi", "Count trebuie sa fie un numar intreg.")
            return

        data["a5"] = a51_new_state()
        a51_load_key_and_count(data["a5"], key_bits, count_bits)

        fill_char_breakdown(rep_table, msg_entry.get(), 8)
        fill_table(init_table, data["a5"]["init_log"][-12:], ("faza", "pas", "bit_intrare", "R1", "R2", "R3"))

        out_text.delete("1.0", "end")
        log_line(out_text, f"Registre initializate cu Kc si Count={count_entry.get()}.")
        log_line(out_text, f"S-au facut {len(data['a5']['init_log'])} cicluri de incarcare "
                            f"+ 100 cicluri de incalzire (aruncate).")
        log_line(out_text, "Apasa 'Pas cu pas' ca sa vezi ceasul majoritar bit cu bit, "
                            "sau 'Cripteaza' pentru tot mesajul.")

    def on_step():
        if data["a5"] is None:
            messagebox.showwarning("Atentie", "Mai intai apasa 'Initializeaza registrele'.")
            return
        info = a51_step(data["a5"])
        fill_table(clock_table, data["a5"]["clock_log"][-10:],
                   ("u1", "u2", "u3", "F", "deplasate", "z", "R1", "R2", "R3"))
        log_line(out_text, f"[Step] u1={info['u1']} u2={info['u2']} u3={info['u3']} F={info['F']} "
                            f"deplasate={info['deplasate']} -> z={info['z']}")

    def on_encrypt():
        try:
            key_bits, count_bits = read_params()
        except ValueError as e:
            messagebox.showerror("Parametri invalizi", str(e))
            return
        except Exception:
            messagebox.showerror("Parametri invalizi", "Count trebuie sa fie un numar intreg.")
            return

        msg = msg_entry.get()
        msg_bytes = text_to_bytes(msg)
        bits = bytes_to_bits(msg_bytes)

        # reinitializam ca sa generam exact de la inceputul fluxului (dupa warmup)
        data["a5"] = a51_new_state()
        a51_load_key_and_count(data["a5"], key_bits, count_bits)
        z = a51_generate_bits(data["a5"], len(bits)) # generează exact atâția biți de keystream cât are mesajul
        cbits = xor_bits(bits, z)
        ct = bits_to_bytes(cbits)

        data["last_msg_bytes"] = msg_bytes
        data["last_cipher_bytes"] = ct

        fill_table(clock_table, data["a5"]["clock_log"][-10:], ("u1", "u2", "u3", "F", "deplasate", "z", "R1", "R2", "R3"))

        out_text.delete("1.0", "end")
        log_line(out_text, f"Mesaj (UTF-8, {len(msg_bytes)} octeti): {msg!r}")
        log_line(out_text, f"Cheie fluida (primii 32 biti): {''.join(map(str, z[:32]))}...")
        log_line(out_text, f"Cheie fluida (hex, {len(z)} biti): {hex_of_bits(z)}")
        log_line(out_text, f"Text criptat C = M xor Z (hex): {ct.hex()}")

    def on_decrypt():
        if data["last_cipher_bytes"] is None:
            messagebox.showwarning("Atentie", "Mai intai cripteaza un mesaj.")
            return
        try:
            key_bits, count_bits = read_params()
        except Exception as e:
            messagebox.showerror("Parametri invalizi", str(e))
            return

        a5b = a51_new_state()
        a51_load_key_and_count(a5b, key_bits, count_bits)
        cbits = bytes_to_bits(data["last_cipher_bytes"])
        z2 = a51_generate_bits(a5b, len(cbits))
        pbits = xor_bits(cbits, z2)
        recovered_bytes = bits_to_bytes(pbits)
        recovered_text = bytes_to_text(recovered_bytes)

        ok = recovered_bytes == data["last_msg_bytes"]
        log_line(out_text, f"Text decriptat: {recovered_text!r}")
        log_line(out_text, f"Verificare D(E(M)) = M : {'OK' if ok else 'ESUAT'}")
        if not ok:
            messagebox.showerror("Verificare esuata", "D(E(M)) != M -- verifica cheia/Count.")

    ttk.Button(btns, text="1) Initializeaza registrele", command=on_init).pack(side="left", padx=3)
    ttk.Button(btns, text="2) Cripteaza", command=on_encrypt).pack(side="left", padx=3)
    ttk.Button(btns, text="3) Decripteaza", command=on_decrypt).pack(side="left", padx=3)
    ttk.Button(btns, text="Pas cu pas (Step)", command=on_step).pack(side="left", padx=3)

    return frame




# TAB 2: RC4

def build_rc4_tab(notebook):
    frame = ttk.Frame(notebook, padding=10)

    data = {
        "rc4": None,
        "last_msg_bytes": None,
        "last_cipher_bytes": None,
    }

    top = ttk.LabelFrame(frame, text="Cheie (RC4)")
    top.pack(fill="x", pady=(0, 8))

    ttk.Label(top, text="Cheie:").grid(row=0, column=0, sticky="w", padx=4, pady=3)
    key_entry = ttk.Entry(top, width=30, font=FONT_MONO)
    key_entry.insert(0, "TheMatrixIsReal")
    key_entry.grid(row=0, column=1, sticky="w", padx=4)

    hex_key_var = tk.BooleanVar(value=False)
    ttk.Checkbutton(top, text="cheia e in hex", variable=hex_key_var).grid(row=0, column=2, padx=8)

    ttk.Label(top, text="Mesaj (UTF-8):").grid(row=1, column=0, sticky="w", padx=4, pady=3)
    msg_entry = ttk.Entry(top, width=55, font=FONT_MONO)
    msg_entry.insert(0, "Wake up, Neo")
    msg_entry.grid(row=1, column=1, columnspan=2, sticky="we", padx=4)

    btns = ttk.Frame(top)
    btns.grid(row=2, column=0, columnspan=3, sticky="w", pady=6)

    rep = ttk.LabelFrame(frame, text="Caracter -> cod numeric -> binar (primele caractere)")
    rep.pack(fill="x", pady=4)
    rep_table, rep_vsb = make_table(rep, ("Caracter", "Cod (dec)", "Binar (8 biti)"), height=4)
    rep_table.pack(side="left", fill="x", expand=True)
    rep_vsb.pack(side="left", fill="y")

    mid = ttk.Frame(frame)
    mid.pack(fill="both", expand=True, pady=4)

    ksa_frame = ttk.LabelFrame(mid, text="KSA - primii 10 pasi (i, j, interschimb in S)")
    ksa_frame.pack(side="left", fill="both", expand=True, padx=(0, 4))
    ksa_table, ksa_vsb = make_table(ksa_frame, ("i", "j", "S[i]_dupa_swap", "S[j]_dupa_swap"), height=8)
    ksa_table.pack(side="left", fill="both", expand=True)
    ksa_vsb.pack(side="left", fill="y")

    prga_frame = ttk.LabelFrame(mid, text="PRGA - pasi (i, j, t, z)")
    prga_frame.pack(side="left", fill="both", expand=True, padx=(4, 0))
    prga_table, prga_vsb = make_table(prga_frame, ("i", "j", "t", "z"), height=8)
    prga_table.pack(side="left", fill="both", expand=True)
    prga_vsb.pack(side="left", fill="y")

    out = ttk.LabelFrame(frame, text="Rezultate")
    out.pack(fill="both", expand=True, pady=4)
    out_text = tk.Text(out, height=8, font=FONT_MONO, wrap="word")
    out_text.pack(fill="both", expand=True)

    def read_key():
        return parse_rc4_key(key_entry.get(), hex_key_var.get())

    def on_ksa():
        try:
            key = read_key()
        except ValueError as e:
            messagebox.showerror("Cheie invalida", str(e))
            return
        data["rc4"] = rc4_init(key)
        fill_table(ksa_table, data["rc4"]["ksa_log"], ("i", "j", "S[i]_dupa_swap", "S[j]_dupa_swap"))
        fill_char_breakdown(rep_table, msg_entry.get(), 8)

        out_text.delete("1.0", "end")
        log_line(out_text, f"KSA rulat cu cheia {key.decode(ENCODING)!r} "
                   f"({len(key)} octeti): {list(key)}")
        log_line(out_text, "Permutarea S initiala (0..255) a fost amestecata folosind cheia. Vezi tabelul KSA.")
        log_s_grid(out_text, data["rc4"]["S_dupa_ksa"])

    def on_step():
        if data["rc4"] is None:
            messagebox.showwarning("Atentie", "Mai intai apasa 'Ruleaza KSA'.")
            return
        info = rc4_step(data["rc4"])
        fill_table(prga_table, data["rc4"]["prga_log"][-10:], ("i", "j", "t", "z"))
        log_line(out_text, f"[Step PRGA] i={info['i']} j={info['j']} t={info['t']} -> "
                            f"z={info['z']} (0x{info['z']:02x})")

    def on_encrypt():
        try:
            key = read_key()
        except ValueError as e:
            messagebox.showerror("Cheie invalida", str(e))
            return

        msg = msg_entry.get()
        msg_bytes = text_to_bytes(msg)

        data["rc4"] = rc4_init(key)
        ks = rc4_keystream(data["rc4"], len(msg_bytes))
        ct = xor_bytes(msg_bytes, ks)

        data["last_msg_bytes"] = msg_bytes
        data["last_cipher_bytes"] = ct

        fill_table(ksa_table, data["rc4"]["ksa_log"], ("i", "j", "S[i]_dupa_swap", "S[j]_dupa_swap"))
        fill_table(prga_table, data["rc4"]["prga_log"], ("i", "j", "t", "z"))

        out_text.delete("1.0", "end")
        log_line(out_text, f"Mesaj (UTF-8, {len(msg_bytes)} octeti): {msg!r}")
        log_line(out_text, f"Cheie fluida Z (hex, {len(ks)} octeti): {ks.hex()}")
        log_line(out_text, f"Text criptat C = M xor Z (hex): {ct.hex()}")

    def on_decrypt():
        if data["last_cipher_bytes"] is None:
            messagebox.showwarning("Atentie", "Mai intai cripteaza un mesaj.")
            return
        try:
            key = read_key()
        except ValueError as e:
            messagebox.showerror("Cheie invalida", str(e))
            return

        rc4b = rc4_init(key)
        ks2 = rc4_keystream(rc4b, len(data["last_cipher_bytes"]))
        pt = xor_bytes(data["last_cipher_bytes"], ks2)
        recovered_text = bytes_to_text(pt)
        ok = pt == data["last_msg_bytes"]

        log_line(out_text, f"Text decriptat: {recovered_text!r}")
        log_line(out_text, f"Verificare D(E(M)) = M : {'OK' if ok else 'ESUAT'}")
        if not ok:
            messagebox.showerror("Verificare esuata", "D(E(M)) != M -- verifica cheia.")

    ttk.Button(btns, text="1) Ruleaza KSA", command=on_ksa).pack(side="left", padx=3)
    ttk.Button(btns, text="2) Cripteaza (PRGA + XOR)", command=on_encrypt).pack(side="left", padx=3)
    ttk.Button(btns, text="3) Decripteaza", command=on_decrypt).pack(side="left", padx=3)
    ttk.Button(btns, text="Pas PRGA (Step)", command=on_step).pack(side="left", padx=3)

    return frame



# TAB 3: Experiment - reutilizarea cheii fluide

def build_reuse_tab(notebook):
    frame = ttk.Frame(notebook, padding=10)

    info = ttk.Label(
        frame, wraplength=760, justify="left",
        text=("Doua mesaje M1 si M2 sunt criptate cu ACEEASI cheie fluida Z:\n"
              "   C1 = M1 xor Z ,  C2 = M2 xor Z\n"
              "Se calculeaza C1 xor C2, care este egal cu M1 xor M2 (cheia fluida dispare prin XOR).\n"
              "Daca M1 este cunoscut, M2 poate fi recuperat: M2 = C1 xor C2 xor M1."))
    info.pack(fill="x", pady=(0, 8))

    top = ttk.LabelFrame(frame, text="Parametri")
    top.pack(fill="x", pady=4)

    alg_var = tk.StringVar(value="RC4")
    ttk.Label(top, text="Algoritm:").grid(row=0, column=0, sticky="w", padx=4, pady=3)
    ttk.Combobox(top, textvariable=alg_var, values=["A5/1", "RC4"], width=8,
                 state="readonly").grid(row=0, column=1, sticky="w", padx=4)

    ttk.Label(top, text="Cheie (hex pt. A5/1 = 16 cifre; text pt. RC4):").grid(row=0, column=2, sticky="w", padx=4)
    key_entry = ttk.Entry(top, width=22, font=FONT_MONO)
    key_entry.insert(0, "secretkey")
    key_entry.grid(row=0, column=3, sticky="w", padx=4)

    ttk.Label(top, text="Count (doar A5/1):").grid(row=1, column=2, sticky="w", padx=4)
    count_entry = ttk.Entry(top, width=10, font=FONT_MONO)
    count_entry.insert(0, "100")
    count_entry.grid(row=1, column=3, sticky="w", padx=4)

    ttk.Label(top, text="M1:").grid(row=1, column=0, sticky="w", padx=4, pady=3)
    m1_entry = ttk.Entry(top, width=30, font=FONT_MONO)
    m1_entry.insert(0, "ATTACKATDAWN12")
    m1_entry.grid(row=1, column=1, sticky="w", padx=4)

    ttk.Label(top, text="M2:").grid(row=2, column=0, sticky="w", padx=4, pady=3)
    m2_entry = ttk.Entry(top, width=30, font=FONT_MONO)
    m2_entry.insert(0, "RETREATNOW1234")
    m2_entry.grid(row=2, column=1, sticky="w", padx=4)

    out = ttk.LabelFrame(frame, text="Rezultate")
    out.pack(fill="both", expand=True, pady=4)
    out_text = tk.Text(out, height=16, font=FONT_MONO, wrap="word")
    out_text.pack(fill="both", expand=True)

    def keystream_for(alg, n_bytes, key_text, count_text):
        if alg == "A5/1":
            key_bits = hex_key_to_bits64(key_text)
            count_bits = int_count_to_bits22(int(count_text.strip()))
            a5 = a51_new_state()
            a51_load_key_and_count(a5, key_bits, count_bits)
            zbits = a51_generate_bits(a5, n_bytes * 8)
            return bits_to_bytes(zbits)
        else:
            key = parse_rc4_key(key_text, as_hex=False)
            rc4 = rc4_init(key)
            return rc4_keystream(rc4, n_bytes)

    def on_run():
        out_text.delete("1.0", "end")
        try:
            m1 = text_to_bytes(m1_entry.get())
            m2 = text_to_bytes(m2_entry.get())
            n = max(len(m1), len(m2))
            z = keystream_for(alg_var.get(), n, key_entry.get(), count_entry.get())
        except ValueError as e:
            messagebox.showerror("Parametri invalizi", str(e))
            return
        except Exception as e:
            messagebox.showerror("Eroare", str(e))
            return

        if len(m1) != len(m2):
            log_line(out_text, f"Nota: M1 ({len(m1)} octeti) si M2 ({len(m2)} octeti) au lungimi diferite; "
                                f"se compara doar pe lungimea minima ({min(len(m1), len(m2))} octeti).")

        res = reuse_experiment(m1, m2, z)

        log_line(out_text, f"Algoritm folosit pentru Z: {alg_var.get()}")
        log_line(out_text, f"M1 = {m1_entry.get()!r} -> {m1.hex()}")
        log_line(out_text, f"M2 = {m2_entry.get()!r} -> {m2.hex()}")
        log_line(out_text, f"Z  (primii {res['n']} octeti, hex) = {z[:res['n']].hex()}")
        log_line(out_text, "")
        log_line(out_text, f"C1 = M1 xor Z = {res['c1'].hex()}")
        log_line(out_text, f"C2 = M2 xor Z = {res['c2'].hex()}")
        log_line(out_text, "")
        log_line(out_text, f"C1 xor C2       = {res['c1_xor_c2'].hex()}")
        log_line(out_text, f"M1 xor M2       = {res['m1_xor_m2'].hex()}")
        log_line(out_text, f"Relatia C1^C2 = M1^M2 verificata: {'DA' if res['relatia_verificata'] else 'NU'}")
        log_line(out_text, "")
        log_line(out_text, "Presupunand M1 cunoscut, recuperam M2 = C1 xor C2 xor M1:")
        log_line(out_text, f"M2 recuperat (hex)  = {res['m2_recovered'].hex()}")
        log_line(out_text, f"M2 recuperat (text) = {bytes_to_text(res['m2_recovered'])!r}")
        log_line(out_text, f"Recuperare identica cu M2 original: {'DA' if res['recuperare_corecta'] else 'NU'}")

        if res["relatia_verificata"] and res["recuperare_corecta"]:
            log_line(out_text, "\n=> Concluzie: refolosirea aceleiasi chei fluide Z pentru doua mesaje "
                                "diferite permite unui atacator care cunoaste (sau ghiceste) un mesaj sa "
                                "recupereze complet celalalt mesaj, fara sa cunoasca deloc cheia secreta K.")

    ttk.Button(top, text="Ruleaza experimentul", command=on_run).grid(row=2, column=3, sticky="e", padx=4, pady=4)

    return frame





# TAB 4: Schimbarea parametrilor (sectiunea 7)

def build_param_change_tab(notebook):
    frame = ttk.Frame(notebook, padding=10)

    info = ttk.Label(
        frame, wraplength=760, justify="left",
        text=("Se genereaza doua fluxuri cu ACEEASI cheie secreta K, dar cu un parametru "
              "de initializare diferit (Count pentru A5/1, respectiv o cheie diferita pentru RC4 "
              "conform cerintei). Se compara primii octeti si se arata ca fluxurile NU mai coincid."))
    info.pack(fill="x", pady=(0, 8))

    top = ttk.LabelFrame(frame, text="Parametri")
    top.pack(fill="x", pady=4)

    alg_var = tk.StringVar(value="A5/1")
    ttk.Label(top, text="Algoritm:").grid(row=0, column=0, sticky="w", padx=4, pady=3)
    ttk.Combobox(top, textvariable=alg_var, values=["A5/1", "RC4"], width=8,
                 state="readonly").grid(row=0, column=1, sticky="w", padx=4)

    ttk.Label(top, text="Cheie K (A5/1: 16 cifre hex):").grid(row=1, column=0, sticky="w", padx=4)
    key_entry = ttk.Entry(top, width=22, font=FONT_MONO)
    key_entry.insert(0, "0123456789ABCDEF")
    key_entry.grid(row=1, column=1, sticky="w", padx=4)

    ttk.Label(top, text="Count 1 (A5/1) / Cheie 2 (RC4):").grid(row=1, column=2, sticky="w", padx=4)
    param1_entry = ttk.Entry(top, width=18, font=FONT_MONO)
    param1_entry.insert(0, "100")
    param1_entry.grid(row=1, column=3, sticky="w", padx=4)

    ttk.Label(top, text="Count 2 (A5/1, diferit):").grid(row=2, column=2, sticky="w", padx=4)
    param2_entry = ttk.Entry(top, width=18, font=FONT_MONO)
    param2_entry.insert(0, "101")
    param2_entry.grid(row=2, column=3, sticky="w", padx=4)

    ttk.Label(top, text="Nr. octeti de comparat:").grid(row=3, column=0, sticky="w", padx=4)
    n_entry = ttk.Entry(top, width=8, font=FONT_MONO)
    n_entry.insert(0, "16")
    n_entry.grid(row=3, column=1, sticky="w", padx=4)

    out = ttk.LabelFrame(frame, text="Rezultate")
    out.pack(fill="both", expand=True, pady=4)
    out_text = tk.Text(out, height=16, font=FONT_MONO, wrap="word")
    out_text.pack(fill="both", expand=True)

    def on_run():
        out_text.delete("1.0", "end")
        alg = alg_var.get()
        try:
            n = int(n_entry.get().strip())
            if alg == "A5/1":
                key_bits = hex_key_to_bits64(key_entry.get())
                c1 = int_count_to_bits22(int(param1_entry.get().strip()))
                c2 = int_count_to_bits22(int(param2_entry.get().strip()))

                a5a = a51_new_state()
                a51_load_key_and_count(a5a, key_bits, c1)
                za = bits_to_bytes(a51_generate_bits(a5a, n * 8))

                a5b = a51_new_state()
                a51_load_key_and_count(a5b, key_bits, c2)
                zb = bits_to_bytes(a51_generate_bits(a5b, n * 8))

                label1, label2 = f"Count={param1_entry.get()}", f"Count={param2_entry.get()}"
            else:
                key1 = parse_rc4_key(key_entry.get(), as_hex=False)
                key2 = parse_rc4_key(param1_entry.get(), as_hex=False)

                za = rc4_keystream(rc4_init(key1), n)
                zb = rc4_keystream(rc4_init(key2), n)

                label1, label2 = f"cheia1={key_entry.get()!r}", f"cheia2={param1_entry.get()!r}"
        except ValueError as e:
            messagebox.showerror("Parametri invalizi", str(e))
            return
        except Exception as e:
            messagebox.showerror("Eroare", str(e))
            return

        log_line(out_text, f"Algoritm: {alg}")
        log_line(out_text, f"Flux 1 ({label1}): {za.hex()}")
        log_line(out_text, f"Flux 2 ({label2}): {zb.hex()}")

        diff_positions = [i for i in range(len(za)) if za[i] != zb[i]]
        same = len(diff_positions) == 0
        log_line(out_text, "")
        log_line(out_text, f"Octeti diferiti: {len(diff_positions)} din {len(za)}")
        log_line(out_text, f"Fluxurile coincid: {'DA (neasteptat!)' if same else 'NU'}")
        if not same:
            log_line(out_text, "=> Confirma ca schimbarea parametrului de initializare (Count/cheie), "
                                "chiar pastrand aceeasi cheie secreta K, produce o cheie fluida complet "
                                "diferita -- exact motivul pentru care Count/IV/nonce nu trebuie repetat "
                                "niciodata cu aceeasi cheie.")

    ttk.Button(top, text="Compara fluxurile", command=on_run).grid(row=3, column=3, sticky="e", padx=4, pady=4)

    return frame


# Fereastra principala

def main():
    root = tk.Tk()
    root.title("Laborator 2 - Criptografie - Varianta I: A5/1 + RC4")
    root.geometry("1000x720")

    header = ttk.Label(
        root, text="Sisteme de criptare fluida - A5/1 si RC4  |  Codificare text: " + ENCODING.upper(),
        font=("Segoe UI", 11, "bold"), padding=8)
    header.pack(fill="x")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=6, pady=6)

    notebook.add(build_a51_tab(notebook), text="A5/1")
    notebook.add(build_rc4_tab(notebook), text="RC4")
    notebook.add(build_reuse_tab(notebook), text="Experiment: reutilizare cheie fluida")
    notebook.add(build_param_change_tab(notebook), text="Schimbare parametri (sectiunea 7)")

    root.mainloop()


if __name__ == "__main__":
    main()
