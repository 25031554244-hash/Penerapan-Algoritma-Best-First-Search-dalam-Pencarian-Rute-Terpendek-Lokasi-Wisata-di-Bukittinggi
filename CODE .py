import tkinter as tk
from tkinter import ttk, messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import networkx as nx

# =====================================
# DATA RUTE
# =====================================

rute_data = [
    ["RBH", "Ngarai Sianok", 1.2, 6, 120],
    ["RBH", "Jam Gadang", 3, 10, 60],
    ["Jam Gadang", "Pasar Atas", 2, 5, 45],
]

# =====================================
# WINDOW
# =====================================

root = tk.Tk()
root.title("Admin Wisata Bukittinggi")
root.geometry("1400x800")
root.configure(bg="#EAF4FF")

# =====================================
# STYLE
# =====================================

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    rowheight=28,
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    font=("Segoe UI", 10, "bold")
)

# =====================================
# HEADER
# =====================================

header = tk.Frame(root, bg="#1565C0", height=80)
header.pack(fill="x")

judul = tk.Label(
    header,
    text="SISTEM ADMIN WISATA KOTA BUKITTINGGI",
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

input_frame = tk.Frame(
    main_frame,
    bg="white",
    bd=2,
    relief="ridge"
)

input_frame.pack(
    side="left",
    fill="y",
    padx=(0, 10)
)

title_input = tk.Label(
    input_frame,
    text="Kelola Data Wisata",
    font=("Segoe UI", 14, "bold"),
    bg="white",
    fg="#0D47A1"
)

title_input.pack(pady=10)

# =====================================
# FUNCTION LABEL & ENTRY
# =====================================

def create_label(text):

    tk.Label(
        input_frame,
        text=text,
        font=("Segoe UI", 10),
        bg="white"
    ).pack(anchor="w", padx=15, pady=(10, 0))


def create_entry():

    entry = tk.Entry(
        input_frame,
        font=("Segoe UI", 10),
        width=30
    )

    entry.pack(padx=15, pady=5)

    return entry


create_label("Tempat Asal")
entry_asal = create_entry()

create_label("Tempat Tujuan")
entry_tujuan = create_entry()

create_label("Jarak Tempuh (KM)")
entry_jarak = create_entry()

create_label("Waktu Tempuh (Menit)")
entry_waktu = create_entry()

create_label("Lama Kunjungan (Menit)")
entry_kunjungan = create_entry()

# =====================================
# CLEAR ENTRY
# =====================================

def clear_entry():

    entry_asal.delete(0, tk.END)
    entry_tujuan.delete(0, tk.END)
    entry_jarak.delete(0, tk.END)
    entry_waktu.delete(0, tk.END)
    entry_kunjungan.delete(0, tk.END)

# =====================================
# RIGHT FRAME
# =====================================

container = tk.Frame(
    main_frame,
    bg="white",
    bd=2,
    relief="ridge"
)

container.pack(
    side="right",
    fill="both",
    expand=True
)

canvas_main = tk.Canvas(container, bg="white")

scroll_y = ttk.Scrollbar(
    container,
    orient="vertical",
    command=canvas_main.yview
)

scroll_x = ttk.Scrollbar(
    container,
    orient="horizontal",
    command=canvas_main.xview
)

scrollable_frame = tk.Frame(
    canvas_main,
    bg="white"
)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas_main.configure(
        scrollregion=canvas_main.bbox("all")
    )
)

canvas_main.create_window(
    (0, 0),
    window=scrollable_frame,
    anchor="nw"
)

canvas_main.configure(
    yscrollcommand=scroll_y.set,
    xscrollcommand=scroll_x.set
)

canvas_main.pack(
    side="left",
    fill="both",
    expand=True
)

scroll_y.pack(side="right", fill="y")
scroll_x.pack(side="bottom", fill="x")

right_frame = scrollable_frame

# =====================================
# TABLE
# =====================================

table_frame = tk.Frame(
    right_frame,
    bg="white"
)

table_frame.pack(
    fill="x",
    padx=10,
    pady=10
)

columns = (
    "Asal",
    "Tujuan",
    "Jarak",
    "Waktu Tempuh",
    "Lama Kunjungan"
)

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=10
)

for col in columns:

    tree.heading(col, text=col)

    tree.column(
        col,
        width=180,
        anchor="center"
    )

scroll_table_y = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=tree.yview
)

scroll_table_x = ttk.Scrollbar(
    table_frame,
    orient="horizontal",
    command=tree.xview
)

tree.configure(
    yscrollcommand=scroll_table_y.set,
    xscrollcommand=scroll_table_x.set
)

tree.pack(side="top", fill="x")

scroll_table_y.pack(side="right", fill="y")
scroll_table_x.pack(side="bottom", fill="x")

# =====================================
# TAMPILKAN DATA
# =====================================

def tampilkan_data():

    tree.delete(*tree.get_children())

    for data in rute_data:

        tree.insert(
            "",
            "end",
            values=data
        )

    update_grafik()

# =====================================
# TAMBAH DATA
# =====================================

def tambah_data():

    try:

        asal = entry_asal.get()
        tujuan = entry_tujuan.get()

        jarak = float(entry_jarak.get())
        waktu = int(entry_waktu.get())
        kunjungan = int(entry_kunjungan.get())

        rute_data.append([
            asal,
            tujuan,
            jarak,
            waktu,
            kunjungan
        ])

        tampilkan_data()

        clear_entry()

        messagebox.showinfo(
            "Sukses",
            "Data berhasil ditambahkan"
        )

    except:

        messagebox.showerror(
            "Error",
            "Input tidak valid"
        )

# =====================================
# HAPUS DATA
# =====================================

def hapus_data():

    selected = tree.selection()

    if not selected:

        messagebox.showwarning(
            "Peringatan",
            "Pilih data terlebih dahulu"
        )

        return

    item = tree.item(selected)

    values = item["values"]

    for data in rute_data:

        if data[0] == values[0] and data[1] == values[1]:

            rute_data.remove(data)

            break

    tampilkan_data()

    messagebox.showinfo(
        "Sukses",
        "Data berhasil dihapus"
    )

# =====================================
# UPDATE DATA
# =====================================

def update_data():

    selected = tree.selection()

    if not selected:

        messagebox.showwarning(
            "Peringatan",
            "Pilih data terlebih dahulu"
        )

        return

    try:

        item = tree.item(selected)

        old_values = item["values"]

        for data in rute_data:

            if data[0] == old_values[0] and data[1] == old_values[1]:

                data[0] = entry_asal.get()
                data[1] = entry_tujuan.get()
                data[2] = float(entry_jarak.get())
                data[3] = int(entry_waktu.get())
                data[4] = int(entry_kunjungan.get())

                break

        tampilkan_data()

        clear_entry()

        messagebox.showinfo(
            "Sukses",
            "Data berhasil diupdate"
        )

    except:

        messagebox.showerror(
            "Error",
            "Input tidak valid"
        )

# =====================================
# PILIH DATA
# =====================================

def pilih_data(event):

    selected = tree.selection()

    if selected:

        item = tree.item(selected)

        values = item["values"]

        clear_entry()

        entry_asal.insert(0, values[0])
        entry_tujuan.insert(0, values[1])
        entry_jarak.insert(0, values[2])
        entry_waktu.insert(0, values[3])
        entry_kunjungan.insert(0, values[4])

tree.bind(
    "<<TreeviewSelect>>",
    pilih_data
)

# =====================================
# BUTTON
# =====================================

btn_frame = tk.Frame(
    input_frame,
    bg="white"
)

btn_frame.pack(pady=20)

btn_tambah = tk.Button(
    btn_frame,
    text="Tambah",
    bg="#4CAF50",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    width=10,
    command=tambah_data
)

btn_tambah.grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)

btn_update = tk.Button(
    btn_frame,
    text="Update",
    bg="#2196F3",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    width=10,
    command=update_data
)

btn_update.grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)

btn_hapus = tk.Button(
    btn_frame,
    text="Hapus",
    bg="#F44336",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    width=10,
    command=hapus_data
)

btn_hapus.grid(
    row=1,
    column=0,
    padx=5,
    pady=5
)

btn_clear = tk.Button(
    btn_frame,
    text="Clear",
    bg="#9E9E9E",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    width=10,
    command=clear_entry
)

btn_clear.grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)


# =====================================
# GRAPH
# =====================================

# FRAME GRAPH
graph_frame = tk.Frame(
    right_frame,
    bg="white"
)

graph_frame.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

# FIGURE
fig = Figure(figsize=(9, 10), dpi=100)

# 3 subplot
ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)

canvas_chart = FigureCanvasTkAgg(
    fig,
    master=graph_frame
)

canvas_chart.get_tk_widget().pack(
    fill="both",
    expand=True
)

# =====================================
# UPDATE GRAFIK
# =====================================

def update_grafik():

    ax1.clear()
    ax2.clear()
    ax3.clear()

    # ==============================
    # GRAPH JARAK
    # ==============================

    G_jarak = nx.Graph()

    for data in rute_data:

        asal = data[0]
        tujuan = data[1]
        jarak = data[2]

        G_jarak.add_edge(
            asal,
            tujuan,
            weight=jarak
        )

    pos1 = nx.spring_layout(
        G_jarak,
        seed=10,
        k=1.5
    )

    nx.draw_networkx_nodes(
        G_jarak,
        pos1,
        ax=ax1,
        node_size=1500,
        node_color="skyblue"
    )

    nx.draw_networkx_edges(
        G_jarak,
        pos1,
        ax=ax1,
        width=3
    )

    nx.draw_networkx_labels(
        G_jarak,
        pos1,
        ax=ax1,
        font_size=7,
        font_weight="bold"
    )

    edge_labels_jarak = nx.get_edge_attributes(
        G_jarak,
        "weight"
    )

    nx.draw_networkx_edge_labels(
        G_jarak,
        pos1,
        edge_labels=edge_labels_jarak,
        ax=ax1,
        font_size=6
    )

    ax1.set_title(
        "Graph Jarak Tempuh (KM)",
        fontsize=14
    )

    ax1.axis("off")

    # ==============================
    # GRAPH WAKTU
    # ==============================

    G_waktu = nx.Graph()

    for data in rute_data:

        asal = data[0]
        tujuan = data[1]
        waktu = data[3]

        G_waktu.add_edge(
            asal,
            tujuan,
            weight=waktu
        )

    pos2 = nx.spring_layout(
        G_waktu,
        seed=20,
        k=1.5
    )

    nx.draw_networkx_nodes(
        G_waktu,
        pos2,
        ax=ax2,
        node_size=2500,
        node_color="lightgreen"
    )

    nx.draw_networkx_edges(
        G_waktu,
        pos2,
        ax=ax2,
        width=3
    )

    nx.draw_networkx_labels(
        G_waktu,
        pos2,
        ax=ax2,
        font_size=9,
        font_weight="bold"
    )

    edge_labels_waktu = nx.get_edge_attributes(
        G_waktu,
        "weight"
    )

    nx.draw_networkx_edge_labels(
        G_waktu,
        pos2,
        edge_labels=edge_labels_waktu,
        ax=ax2,
        font_size=8
    )

    ax2.set_title(
        "Graph Waktu Tempuh (Menit)",
        fontsize=14
    )

    ax2.axis("off")

    # ==============================
    # GRAPH LAMA KUNJUNGAN
    # ==============================

    G_kunjungan = nx.Graph()

    for data in rute_data:

        asal = data[0]
        tujuan = data[1]
        kunjungan = data[4]

        G_kunjungan.add_edge(
            asal,
            tujuan,
            weight=kunjungan
        )

    pos3 = nx.spring_layout(
        G_kunjungan,
        seed=30,
        k=1.5
    )

    nx.draw_networkx_nodes(
        G_kunjungan,
        pos3,
        ax=ax3,
        node_size=2500,
        node_color="orange"
    )

    nx.draw_networkx_edges(
        G_kunjungan,
        pos3,
        ax=ax3,
        width=3
    )

    nx.draw_networkx_labels(
        G_kunjungan,
        pos3,
        ax=ax3,
        font_size=9,
        font_weight="bold"
    )

    edge_labels_kunjungan = nx.get_edge_attributes(
        G_kunjungan,
        "weight"
    )

    nx.draw_networkx_edge_labels(
        G_kunjungan,
        pos3,
        edge_labels=edge_labels_kunjungan,
        ax=ax3,
        font_size=8
    )

    ax3.set_title(
        "Graph Lama Kunjungan (Menit)",
        fontsize=14
    )

    ax3.axis("off")

    # RAPATKAN GRAPH
    fig.tight_layout(pad=4)

    # REFRESH
    canvas_chart.draw()

# =====================================
# FOOTER
# =====================================

footer = tk.Frame(
    root,
    bg="#1565C0",
    height=35
)

footer.pack(fill="x")

footer_label = tk.Label(
    footer,
    text="Admin Panel - Implementasi Algoritma Best First Search",
    bg="#1565C0",
    fg="white",
    font=("Segoe UI", 10)
)

footer_label.pack(pady=6)

# =====================================
# START
# =====================================

tampilkan_data()

root.mainloop()
