# -*- coding: utf-8 -*-
"""
Practica IA - busquedas sobre el grafo (el mismo grafo de la actividad)
Un solo programa con las 5 busquedas: a lo ancho, en profundidad,
escalada simple, escalada maxima pendiente y primero el mejor.

Integrantes 
  1. Arteaga Crescencio Victor Alexis
  2. Tello Aguilera Lilly Michelle

Cada busqueda pide nodo inicial, nodo final y sentido.
El sentido es el orden en que reviso los vecinos de cada nodo:
1 = de menor a mayor numero, 2 = de mayor a menor.
"""
from collections import deque

N = 28
# aristas del grafo (nodo, nodo, costo), van en los dos sentidos
ARISTAS = [
    (11, 7, 696), (11, 5, 705), (7, 8, 662), (7, 27, 475),
    (5, 15, 220), (15, 8, 309), (15, 24, 286), (8, 27, 268),
    (8, 28, 310), (27, 21, 262), (27, 28, 390), (21, 18, 89),
    (21, 28, 380), (21, 22, 449), (18, 14, 328), (18, 3, 291),
    (14, 3, 317), (14, 23, 499), (3, 23, 235), (3, 19, 638),
    (23, 19, 391), (28, 22, 190), (28, 2, 131), (28, 9, 320),
    (22, 2, 171), (22, 23, 401), (2, 12, 137), (2, 9, 245),
    (12, 10, 54), (10, 16, 381), (24, 9, 214), (24, 13, 446),
    (9, 4, 202), (9, 17, 321), (4, 13, 98), (4, 1, 701),
    (13, 1, 699), (17, 26, 259), (26, 16, 66), (16, 19, 95),
    (16, 25, 118), (16, 20, 123), (25, 20, 33), (16, 6, 288),
    (6, 1, 117)
]
# tabla de distancias en linea recta, la fila k tiene la distancia del nodo k a los nodos 1..k-1
TABLA = {
    2: [908],
    3: [117, 515],
    4: [687, 448, 886],
    5: [1651, 970, 1373, 922],
    6: [117, 791, 999, 804, 1540],
    7: [1882, 1013, 117, 1404, 1191, 1765],
    8: [1310, 441, 844, 832, 529, 1193, 662],
    9: [889, 246, 684, 202, 720, 840, 1202, 630],
    10: [760, 181, 559, 479, 997, 643, 1194, 622, 277],
    11: [2348, 1707, 1811, 1619, 697, 2237, 694, 1223, 1417, 1694],
    12: [782, 127, 541, 426, 943, 665, 1140, 568, 223, 54, 1640],
    13: [697, 546, 984, 98, 952, 814, 1502, 930, 300, 577, 1649, 523],
    14: [1370, 928, 317, 1319, 1463, 1253, 1154, 934, 1117, 774, 1848, 756, 1417],
    15: [1431, 750, 1153, 702, 220, 1320, 971, 309, 500, 777, 917, 723, 732, 1250],
    16: [395, 513, 721, 744, 1262, 278, 1407, 915, 542, 365, 1959, 387, 842, 975, 1042],
    17: [697, 316, 739, 504, 1022, 580, 1329, 757, 302, 180, 1719, 202, 602, 954, 802, 302],
    18: [1328, 600, 291, 991, 1148, 1211, 826, 606, 789, 729, 1520, 711, 1089, 328, 928, 933, 913],
    19: [490, 540, 626, 817, 1335, 373, 1553, 981, 615, 392, 2032, 414, 915, 890, 1115, 95, 397, 960],
    20: [481, 636, 813, 867, 1385, 364, 1610, 1038, 665, 480, 2082, 510, 965, 1077, 1165, 123, 425, 1056, 187],
    21: [1244, 511, 300, 902, 1046, 1127, 737, 517, 700, 664, 1431, 646, 1000, 417, 826, 849, 844, 89, 895, 972],
    22: [810, 171, 344, 542, 1029, 693, 1072, 500, 340, 215, 1766, 197, 640, 559, 809, 416, 395, 514, 446, 538, 449],
    23: [881, 572, 235, 943, 1430, 764, 1352, 901, 741, 616, 2046, 598, 1041, 499, 1210, 486, 796, 526, 391, 578, 615, 401],
    24: [1145, 460, 898, 416, 506, 1034, 1257, 595, 214, 491, 1203, 437, 446, 1331, 286, 756, 516, 1003, 829, 879, 914, 554, 955],
    25: [513, 631, 780, 862, 1380, 396, 1605, 1033, 660, 483, 2077, 505, 960, 1044, 1160, 118, 420, 1051, 154, 33, 967, 533, 545, 874],
    26: [461, 497, 704, 678, 1195, 344, 1432, 938, 476, 349, 1893, 371, 776, 1041, 976, 66, 236, 898, 161, 189, 852, 360, 552, 690, 184],
    27: [1407, 538, 642, 929, 784, 1290, 475, 255, 727, 719, 1169, 665, 1027, 679, 564, 1012, 854, 351, 1043, 1135, 262, 597, 877, 850, 1130, 957],
    28: [1000, 131, 534, 522, 839, 883, 882, 310, 320, 312, 1576, 258, 620, 797, 619, 605, 447, 469, 636, 728, 380, 190, 591, 534, 723, 550, 407]
}
# coordenadas de cada nodo, solo sirven para dibujarlo en la ventana
POS = {1: (742, 832), 2: (578, 466), 3: (770, 392), 4: (516, 688), 5: (220, 320), 6: (752, 772), 7: (378, 73),
       8: (431, 385), 9: (519, 586), 10: (697, 510), 11: (31, 38), 12: (629, 518), 13: (449, 716), 14: (867, 262),
       15: (321, 428), 16: (791, 684), 17: (651, 653), 18: (733, 261), 19: (820, 606), 20: (858, 720), 21: (657, 286),
       22: (661, 428), 23: (850, 481), 24: (410, 547), 25: (875, 669), 26: (729, 685), 27: (538, 274), 28: (523, 408)}

# armo la matriz de distancias, la lista de vecinos y los pesos con lo de arriba
DIST = {}
for k, fila in TABLA.items():
    for i, d in enumerate(fila, start=1):
        DIST[(i, k)] = d
        DIST[(k, i)] = d
ADY = {n: [] for n in range(1, N + 1)}
PESO = {}
for a, b, c in ARISTAS:
    ADY[a].append(b); ADY[b].append(a)
    PESO[(a, b)] = c; PESO[(b, a)] = c


def h(n, meta):
    # la heuristica es la distancia en linea recta del nodo a la meta
    return 0 if n == meta else DIST[(n, meta)]


def vecinos(n, sen):
    # regresa los vecinos ordenados segun el sentido que eligio el usuario
    return sorted(ADY[n], reverse=(sen == 2))


def costo(ruta):
    return sum(PESO[(ruta[i], ruta[i + 1])] for i in range(len(ruta) - 1))


class Paso:
    # guarda lo que paso en cada paso: el texto que se muestra y los nodos para pintarlos
    def __init__(self, texto, vis, actual, ruta=None, parcial=False):
        self.texto, self.vis, self.actual = texto, list(vis), actual
        self.ruta, self.parcial = (list(ruta) if ruta else None), parcial


def reconstruir(padre, fin):
    r = [fin]
    while padre[r[-1]] is not None:
        r.append(padre[r[-1]])
    return r[::-1]


# ---------- 5) busqueda a lo ancho (usa una cola) ----------
def ancho(ini, fin, sen):
    # padre sirve para reconstruir la ruta al final y tambien para saber que ya visite
    ps, cola, padre, exp = [], deque([ini]), {ini: None}, []
    k = 0
    while cola:
        a = cola.popleft(); exp.append(a); k += 1   # saco el primero de la cola
        if a == fin:
            ps.append(Paso(f"Paso {k}: se expande {a} (nodo final)", exp, a, reconstruir(padre, fin)))
            return ps
        nuevos = []
        for v in vecinos(a, sen):
            if v not in padre:
                padre[v] = a; cola.append(v); nuevos.append(v)
        ps.append(Paso(f"Paso {k}: se expande {a}\n   Agregados a la cola: {nuevos}\n   Cola: {list(cola)}", exp, a))
    ps.append(Paso("No existe ruta.", exp, -1))
    return ps


# ---------- 6) busqueda en profundidad (usa una pila) ----------
def profundidad(ini, fin, sen):
    ps, pila, padre, vis, exp = [], [(ini, None)], {}, set(), []
    k = 0
    while pila:
        a, p = pila.pop()   # saco el ultimo que meti
        if a in vis:
            continue
        vis.add(a); padre[a] = p; exp.append(a); k += 1
        if a == fin:
            ps.append(Paso(f"Paso {k}: se expande {a} (nodo final)", exp, a, reconstruir(padre, fin)))
            return ps
        hijos = [v for v in vecinos(a, sen) if v not in vis]
        for v in reversed(hijos):          # los meto al reves para que el primero segun el sentido sea el primero en salir
            pila.append((v, a))
        ps.append(Paso(f"Paso {k}: se expande {a}\n   Agregados a la pila: {hijos}\n   Pila (tope al final): {[n for n, _ in pila]}", exp, a))
    ps.append(Paso("No existe ruta.", exp, -1))
    return ps


# ---------- 7) escalada simple y 8) escalada maxima pendiente ----------
# simple: se va al primer vecino que mejore h. maxima pendiente: revisa todos y se va al de menor h
def escalada(ini, fin, sen, max_pendiente):
    ps, ruta, act, k = [], [ini], ini, 0
    while act != fin:
        k += 1
        txt = f"Paso {k}: nodo actual {act}  h={h(act, fin)}\n"
        sig, mejor_h = None, h(act, fin)   # sig = a donde me voy a mover
        for v in vecinos(act, sen):
            hv = h(v, fin)
            mejora = hv < h(act, fin) and v not in ruta
            txt += f"   Vecino {v}: h={hv}  {'(mejora)' if mejora else '(no mejora)'}\n"
            if not max_pendiente:
                if mejora:
                    sig = v; break
            elif mejora and hv < mejor_h:
                sig, mejor_h = v, hv
        if sig is None:   # ningun vecino mejora, me quede atorado -> ruta parcial
            txt += "   Ningun vecino mejora: la busqueda se atoro."
            ps.append(Paso(txt, ruta, act, ruta, True))
            return ps
        txt += f"   Se mueve a {sig}"
        act = sig; ruta.append(act)
        ps.append(Paso(txt, ruta, act))
    ps.append(Paso(f"Se llego al nodo final {fin}.", ruta, act, ruta))
    return ps


# ---------- 9) primero el mejor (siempre expande el de menor h de los que estan abiertos) ----------
def primero_mejor(ini, fin, sen):
    ps, abierta, cerrada, padre = [], [ini], [], {ini: None}
    k = 0
    while abierta:
        a = min(abierta, key=lambda n: h(n, fin))   # si hay empate se queda el que entro primero
        abierta.remove(a); cerrada.append(a); k += 1
        if a == fin:
            ps.append(Paso(f"Paso {k}: se expande {a} (nodo final) h=0", cerrada, a, reconstruir(padre, fin)))
            return ps
        nuevos = []
        for v in vecinos(a, sen):
            if v not in padre:
                padre[v] = a; abierta.append(v); nuevos.append(v)
        ab = ", ".join(f"{n}(h={h(n, fin)})" for n in abierta)
        ps.append(Paso(f"Paso {k}: se expande {a}  h={h(a, fin)}\n   Agregados a abierta: {nuevos}\n   Abierta: {ab}\n   Cerrada: {cerrada}", cerrada, a))
    ps.append(Paso("No existe ruta.", cerrada, -1))
    return ps


ALGOS = ["Busqueda a lo ancho", "Busqueda en profundidad", "Escalada simple",
         "Escalada maxima pendiente", "Primero el mejor"]


def ejecutar(idx_algo, ini, fin, sen):
    if idx_algo == 0: return ancho(ini, fin, sen)
    if idx_algo == 1: return profundidad(ini, fin, sen)
    if idx_algo == 2: return escalada(ini, fin, sen, False)
    if idx_algo == 3: return escalada(ini, fin, sen, True)
    return primero_mejor(ini, fin, sen)


# ================= la ventana ==================
def main():
    import tkinter as tk
    from tkinter import ttk

    root = tk.Tk()
    root.title("Busquedas sobre el grafo - IA61")
    root.geometry("1350x850")
    estado = {"pasos": [], "idx": 0, "paso": None, "ini": None, "fin": None}

    # barra de arriba: aqui se piden los datos (busqueda, nodo inicial, nodo final y sentido)
    top = ttk.Frame(root, padding=8); top.pack(fill="x")
    ttk.Label(top, text="Busqueda:").pack(side="left", padx=(0, 4))
    cb_algo = ttk.Combobox(top, values=ALGOS, state="readonly", width=26); cb_algo.current(0); cb_algo.pack(side="left", padx=6)
    ttk.Label(top, text="Nodo inicial:").pack(side="left")
    cb_ini = ttk.Combobox(top, values=list(range(1, N + 1)), state="readonly", width=4); cb_ini.current(0); cb_ini.pack(side="left", padx=6)
    ttk.Label(top, text="Nodo final:").pack(side="left")
    cb_fin = ttk.Combobox(top, values=list(range(1, N + 1)), state="readonly", width=4); cb_fin.current(10); cb_fin.pack(side="left", padx=6)
    ttk.Label(top, text="Sentido:").pack(side="left")
    cb_sen = ttk.Combobox(top, values=["Ascendente (1)", "Descendente (2)"], state="readonly", width=16); cb_sen.current(0); cb_sen.pack(side="left", padx=6)
    b_ini = ttk.Button(top, text="Iniciar"); b_ini.pack(side="left", padx=4)
    b_sig = ttk.Button(top, text="Siguiente paso", state="disabled"); b_sig.pack(side="left", padx=4)
    b_todo = ttk.Button(top, text="Ejecutar todo", state="disabled"); b_todo.pack(side="left", padx=4)

    # en medio: el grafo a la izquierda y el paso a paso a la derecha
    centro = ttk.Frame(root); centro.pack(fill="both", expand=True)
    canvas = tk.Canvas(centro, bg="white", highlightthickness=0); canvas.pack(side="left", fill="both", expand=True)
    frame_log = ttk.Frame(centro); frame_log.pack(side="right", fill="y")
    log = tk.Text(frame_log, width=58, font=("Menlo", 11), wrap="word", state="disabled")
    sb = ttk.Scrollbar(frame_log, command=log.yview); log.configure(yscrollcommand=sb.set)
    sb.pack(side="right", fill="y"); log.pack(side="left", fill="y")
    lbl = ttk.Label(root, text="Ruta: -", font=("Helvetica", 14, "bold"), padding=8); lbl.pack(fill="x")

    # agrega texto al cuadro de la derecha (el paso a paso)
    def escribir(t):
        log.config(state="normal"); log.insert("end", t); log.see("end"); log.config(state="disabled")

    # dibuja el grafo completo segun el paso en el que vamos
    def dibujar(_e=None):
        canvas.delete("all")
        w, hh = canvas.winfo_width(), canvas.winfo_height()
        X = lambda n: POS[n][0] * (w - 60) / 900 + 30
        Y = lambda n: POS[n][1] * (hh - 60) / 860 + 30
        p = estado["paso"]
        ruta = p.ruta if p and p.ruta else []
        col_ruta = "#E67800" if (p and p.parcial) else "#1EA046"
        en_ruta = {frozenset((ruta[i], ruta[i + 1])) for i in range(len(ruta) - 1)}
        for a, b, c in ARISTAS:
            sel = frozenset((a, b)) in en_ruta
            canvas.create_line(X(a), Y(a), X(b), Y(b), fill=col_ruta if sel else "#AAAAAA", width=4 if sel else 1)
            canvas.create_text((X(a) + X(b)) / 2 + 8, (Y(a) + Y(b)) / 2 - 7, text=str(c), fill="#555555", font=("Helvetica", 9))
        for n in range(1, N + 1):
            c = "white"
            if p and n in p.vis: c = "#AAD2FA"
            if n in ruta: c = col_ruta
            if p and p.actual == n: c = "#FFBE46"
            canvas.create_oval(X(n) - 15, Y(n) - 15, X(n) + 15, Y(n) + 15, fill=c, outline="black", width=1.5)
            canvas.create_text(X(n), Y(n), text=str(n), font=("Helvetica", 12, "bold"))
        if estado["ini"]:
            n = estado["ini"]; canvas.create_oval(X(n) - 19, Y(n) - 19, X(n) + 19, Y(n) + 19, outline="#1E5AE0", width=3)
        if estado["fin"]:
            n = estado["fin"]; canvas.create_oval(X(n) - 19, Y(n) - 19, X(n) + 19, Y(n) + 19, outline="#D22828", width=3)
        canvas.create_text(10, hh - 10, anchor="sw", fill="#444444", font=("Helvetica", 11),
                           text="Azul = inicio | Rojo = final | Naranja = nodo actual | Celeste = visitado | Verde = ruta")

    # lee los datos de arriba, corre la busqueda y guarda todos los pasos
    def iniciar():
        ini, fin = int(cb_ini.get()), int(cb_fin.get())
        sen = cb_sen.current() + 1
        estado.update(pasos=ejecutar(cb_algo.current(), ini, fin, sen), idx=0, paso=None, ini=ini, fin=fin)
        log.config(state="normal"); log.delete("1.0", "end"); log.config(state="disabled")
        escribir(f"{cb_algo.get()} | inicio={ini} | final={fin} | sentido={cb_sen.get()}\n\n")
        lbl.config(text="Ruta: -")
        b_sig.config(state="normal"); b_todo.config(state="normal")
        dibujar()

    # muestra el siguiente paso, y si ya hay ruta la pone abajo con su costo
    def mostrar():
        if estado["idx"] >= len(estado["pasos"]):
            return
        p = estado["pasos"][estado["idx"]]; estado["idx"] += 1
        estado["paso"] = p
        escribir(p.texto + "\n\n")
        if p.ruta:
            s = ("RUTA PARCIAL: " if p.parcial else "RUTA GENERADA: ") + " -> ".join(map(str, p.ruta)) + f"   |   Costo: {costo(p.ruta)}"
            lbl.config(text=s); escribir(s + "\n")
        dibujar()
        if estado["idx"] >= len(estado["pasos"]):
            b_sig.config(state="disabled"); b_todo.config(state="disabled")

    # muestra todos los pasos que faltan de golpe
    def todo():
        while estado["idx"] < len(estado["pasos"]):
            mostrar()

    b_ini.config(command=iniciar); b_sig.config(command=mostrar); b_todo.config(command=todo)
    canvas.bind("<Configure>", dibujar)
    root.mainloop()


if __name__ == "__main__":
    main()
