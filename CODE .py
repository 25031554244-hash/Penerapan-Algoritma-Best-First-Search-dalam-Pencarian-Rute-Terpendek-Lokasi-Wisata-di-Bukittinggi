import tkinter as tk
import heapq
from tkinter import ttk, messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import networkx as nx

# =====================================
# DATA RUTE 
# =====================================

rute_data = [
    ["Rumah Kelahiran Bung Hatta", "Ngarai Sianok", 1.2, 6, 120],
    ["Ngarai Sianok", "Jenjang Seribu", 4.9, 14, 45],
    ["Jenjang Seribu", "Balai Kota", 6.0, 18, 60],
    ["Balai Kota", "Sungai Jemih", 13.8, 32, 45],
    ["Rumah Kelahiran Bung Hatta", "Jam Gadang", 2.5, 8, 60],
    ["Jam Gadang", "Taman Margasatwa dan Budaya Kinantan", 1.8, 5, 90],
    ["Taman Margasatwa dan Budaya Kinantan", "Museum Rumah Adat Baanjuang", 1.2, 4, 60],
    ["Museum Rumah Adat Baanjuang", "Jembatan Limpapeh", 0.8, 3, 45],
    ["Jembatan Limpapeh", "Benteng Fort de Kock", 1.5, 5, 75],
    ["Benteng Fort de Kock", "Lubang Jepang", 1.0, 3, 60],
    ["Ngarai Sianok", "Jam Gadang", 2.0, 7, 60],
    ["Ngarai Sianok", "Taman Margasatwa dan Budaya Kinantan", 2.5, 8, 90],
    ["Jenjang Seribu", "Lubang Jepang", 4.0, 12, 60],
    ["Balai Kota", "Benteng Fort de Kock", 2.8, 9, 75],
    ["Jam Gadang", "Balai Kota", 3.2, 10, 45],
    ["Sungai Jemih", "Lubang Jepang", 3.5, 10, 60],
]

def cari_rute_terpendek(start, goal):
    graph = {}
    for asal, tujuan, jarak, waktu, kunjungan in rute_data:
        graph.setdefault(asal, []).append((tujuan, jarak))
        graph.setdefault(tujuan, []).append((asal, jarak))

    pq = [(0, start, [start])]
    visited = set()

    while pq:
        total_jarak, node, path = heapq.heappop(pq)
        if node == goal:
            return total_jarak, path
        if node in visited:
            continue
        visited.add(node)

        for tetangga, jarak in graph.get(node, []):
            if tetangga not in visited:
                heapq.heappush(pq, (total_jarak + jarak, tetangga, path + [tetangga]))
    return None, []

# =====================================
# VARIABEL JALUR
# =====================================
jalur_terpilih = []

# =====================================
# WINDOW
# =====================================
root = tk.Tk()
root.title("Sistem Rute Wisata Bukittinggi")
root.geometry("1400x800")
root.configure(bg="#EAF4FF")

# =====================================
# HEADER
# =====================================
header = tk.Frame(root, bg="#1565C0", height=80)
header.pack(fill="x")

judul = tk.Label(
    header,
    text="SISTEM PENCARIAN RUTE WISATA KOTA BUKITTINGGI",
    font=("Segoe UI", 22, "bold"),
    bg="#1565C0",
    fg="white"
)
judul.pack(pady=18)

# =====================================
# MAIN FRAME
# =====================================
main_frame = tk.Frame(root, bg="#EAF4FF")
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# =====================================
# INPUT FRAME
# =====================================
input_frame = tk.Frame(main_frame, bg="white", bd=2, relief="ridge")
input_frame.pack(side="left", fill="y", padx=(0, 10))

title_input = tk.Label(
    input_frame,
    text="Menu Navigasi Wisata",
    font=("Segoe UI", 14, "bold"),
    bg="white",
    fg="#0D47A1"
)
title_input.pack(pady=15)

def create_label(text):
    tk.Label(input_frame, text=text, font=("Segoe UI", 11, "bold"), bg="white").pack(anchor="w", padx=15, pady=(15, 0))

# Dropdown Input untuk Cari Rute
create_label("Lokasi Awal")
combo_awal = ttk.Combobox(input_frame, width=28, state="readonly")
combo_awal.pack(padx=15, pady=8)

create_label("Lokasi Tujuan")
combo_tujuan = ttk.Combobox(input_frame, width=28, state="readonly")
combo_tujuan.pack(padx=15, pady=8)

# =====================================
# FUNGSI TOMBOL
# =====================================
def clear_pilihan():
    global jalur_terpilih
    combo_awal.set('')
    combo_tujuan.set('')
    jalur_terpilih = []
    update_grafik()

def cari_rute():
    global jalur_terpilih
    asal = combo_awal.get()
    tujuan = combo_tujuan.get()

    if asal == "" or tujuan == "":
        messagebox.showwarning("Peringatan", "Pilih lokasi asal dan tujuan terlebih dahulu!")
        return

    if asal == tujuan:
        messagebox.showwarning("Peringatan", "Lokasi asal dan tujuan tidak boleh sama!")
        return

    total_jarak, jalur_terpilih = cari_rute_terpendek(asal, tujuan)
    update_grafik()

    if jalur_terpilih:
        messagebox.showinfo(
            "Rute Terpendek Ditemukan",
            f"Rute:\n{' → '.join(jalur_terpilih)}\n\nTotal Jarak: {total_jarak} KM"
        )
    else:
        messagebox.showwarning("Peringatan", "Rute tidak ditemukan!")

# Set isi dropdown
lokasi = sorted(list(set([x[0] for x in rute_data] + [x[1] for x in rute_data])))
combo_awal["values"] = lokasi
combo_tujuan["values"] = lokasi

# =====================================
# TOMBOL AKSI (SESUAI REQUEST)
# =====================================
btn_frame = tk.Frame(input_frame, bg="white")
btn_frame.pack(pady=25)

# Hijau untuk Cari Rute
btn_cari = tk.Button(
    btn_frame,
    text="Cari Rute",
    bg="#4CAF50",
    fg="white",
    font=("Segoe UI", 11, "bold"),
    width=11,
    command=cari_rute
)
btn_cari.grid(row=0, column=0, padx=8, pady=5)

# Abu-abu untuk Clear
btn_clear = tk.Button(
    btn_frame,
    text="Clear",
    bg="#9E9E9E",
    fg="white",
    font=("Segoe UI", 11, "bold"),
    width=11,
    command=clear_pilihan
)
btn_clear.grid(row=0, column=1, padx=8, pady=5)


# =====================================
# RIGHT FRAME (KANVAS & GRAFIK)
# =====================================
container = tk.Frame(main_frame, bg="white", bd=2, relief="ridge")
container.pack(side="right", fill="both", expand=True)

canvas_main = tk.Canvas(container, bg="white")
scroll_y = ttk.Scrollbar(container, orient="vertical", command=canvas_main.yview)
scroll_x = ttk.Scrollbar(container, orient="horizontal", command=canvas_main.xview)

scrollable_frame = tk.Frame(canvas_main, bg="white")
scrollable_frame.bind("<Configure>", lambda e: canvas_main.configure(scrollregion=canvas_main.bbox("all")))

canvas_main.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas_main.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

def _on_mousewheel(event):
    canvas_main.yview_scroll(int(-1*(event.delta/120)), "units")
def _on_mousewheel_horizontal(event):
    canvas_main.xview_scroll(int(-1*(event.delta/120)), "units")

canvas_main.bind_all("<MouseWheel>", _on_mousewheel)
canvas_main.bind_all("<Shift-MouseWheel>", _on_mousewheel_horizontal)

canvas_main.pack(side="left", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")
scroll_x.pack(side="bottom", fill="x")

right_frame = scrollable_frame

# FRAME UNTUK CHARTS
graph_frame = tk.Frame(right_frame, bg="white")
graph_frame.pack(fill="both", expand=True, padx=10, pady=10)

fig = Figure(figsize=(10, 12), dpi=90)
ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)

canvas_chart = FigureCanvasTkAgg(fig, master=graph_frame)
canvas_chart.get_tk_widget().pack(fill="both", expand=True)

# Fungsi gambar graf dinamis agar semua sub-graf merespon rute warna merah
def gambar_sub_graf(ax, index_bobot, judul_graf, warna_node_biasa):
    ax.clear()
    G = nx.Graph()

    for data in rute_data:
        G.add_edge(data[0], data[1], weight=data[index_bobot])

    # Menggunakan layout konstan agar posisi node sejajar dari atas ke bawah
    pos = nx.spring_layout(G, seed=10, k=1.6)

    highlight_edges = []
    for i in range(len(jalur_terpilih)-1):
        highlight_edges.append((jalur_terpilih[i], jalur_terpilih[i+1]))

    node_colors = []
    for node in G.nodes():
        if node in jalur_terpilih:
            node_colors.append("red")
        else:
            node_colors.append(warna_node_biasa)

    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=1200, node_color=node_colors)
    nx.draw_networkx_edges(G, pos, ax=ax, width=2, edge_color="gray")
    nx.draw_networkx_edges(G, pos, edgelist=highlight_edges, ax=ax, width=5, edge_color="red")
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=7, font_weight="bold")

    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, font_size=6)

    ax.set_title(judul_graf, fontsize=14, fontweight="bold")
    ax.axis("off")

def update_grafik():
    gambar_sub_graf(ax1, 2, "Graph Jarak Tempuh (Best First Search)", "skyblue")
    gambar_sub_graf(ax2, 3, "Graph Waktu Tempuh (Menit)", "lightgreen")
    gambar_sub_graf(ax3, 4, "Graph Lama Kunjungan (Menit)", "orange")
    fig.tight_layout(pad=3)
    canvas_chart.draw()

# =====================================
# FOOTER
# =====================================
footer = tk.Frame(root, bg="#1565C0", height=35)
footer.pack(fill="x")
tk.Label(footer, text="Admin Panel - Implementasi Sistem Informasi Rute Wisata", bg="#1565C0", fg="white", font=("Segoe UI", 10)).pack(pady=6)

# =====================================
# RUN SYSTEM
# =====================================
update_grafik()
root.mainloop()
