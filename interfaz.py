import tkinter as tk
from tkinter import messagebox, ttk
from funciones import (registrar_movimiento, obtener_resumen_financiero, 
                       obtener_productos, registrar_producto, obtener_categorias,
                       eliminar_producto, eliminar_categoria, registrar_categoria, 
                       obtener_productos_por_categoria, registrar_gasto)

class AplicacionNegocio:

    def ventana_gasto(self):
        v = tk.Toplevel(self.root)
        v.title("Registrar Gasto Extra")
        v.geometry("300x250")

        tk.Label(v, text="Descripción del Gasto:", font=("Arial", 10)).pack(pady=5)
        ent_desc = tk.Entry(v)
        ent_desc.pack(pady=5, padx=20, fill="x")

        tk.Label(v, text="Monto (S/):", font=("Arial", 10)).pack(pady=5)
        ent_monto = tk.Entry(v)
        ent_monto.pack(pady=5, padx=20, fill="x")

        def guardar_gasto():
            desc = ent_desc.get().strip()
            try:
                monto = float(ent_monto.get())
                if desc and monto > 0:
                    registrar_gasto(desc, monto)
                    messagebox.showinfo("Éxito", f"Gasto '{desc}' registrado correctamente.")
                    v.destroy()
                else:
                    messagebox.showwarning("Error", "Ingresa una descripción y un monto válido.")
            except ValueError:
                messagebox.showerror("Error", "El monto debe ser un número (ej: 10.50)")

        tk.Button(v, text="Guardar Gasto", command=guardar_gasto, bg="#FF5722", fg="white").pack(pady=20)
    def __init__(self, root):
        self.root = root
        self.root.title("Control de Negocio Pro")
        self.root.geometry("950x600")

        tk.Label(root, text="Panel de Inventario", font=("Arial", 18, "bold")).pack(pady=10)

        # --- TABLA ---
        self.tree = ttk.Treeview(root, columns=("ID", "Nombre", "Categoría", "P. Compra", "P. Venta", "Stock"), show='headings')
        for col in ("ID", "Nombre", "Categoría", "P. Compra", "P. Venta", "Stock"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(pady=10, padx=10, fill="both", expand=True)

        # --- PANEL DE ACCIONES ---
        frame_acciones = tk.LabelFrame(root, text="Acciones")
        frame_acciones.pack(pady=10, padx=10, fill="x")

        tk.Button(frame_acciones, text="Añadir Producto", command=self.ventana_nuevo_producto, bg="#9C27B0", fg="white").grid(row=0, column=0, padx=10, pady=10)
        tk.Button(frame_acciones, text="Eliminar Producto", command=self.borrar_producto, bg="#f44336", fg="white").grid(row=0, column=1, padx=10)
        tk.Button(frame_acciones, text="Gestionar Categorías", command=self.ventana_categorias, bg="#607D8B", fg="white").grid(row=0, column=2, padx=10)
        tk.Button(frame_acciones, text="Registrar Venta", command=self.ventana_venta, bg="#4CAF50", fg="white").grid(row=0, column=3, padx=10)
        tk.Button(frame_acciones, text="Ver Reporte", command=self.mostrar_reporte, bg="#2196F3", fg="white").grid(row=0, column=4, padx=10)
        tk.Button(frame_acciones, text="Registrar Gasto", command=self.ventana_gasto, bg="#FF5722", fg="white", width=15).grid(row=0, column=5, padx=10)

        self.actualizar_tabla()

    def actualizar_tabla(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        for fila in obtener_productos(): self.tree.insert("", "end", values=fila)

    def borrar_producto(self):
        # Obtener el elemento seleccionado en la tabla
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un producto de la tabla primero")
            return
        
        item = self.tree.item(seleccion)
        id_prod = item['values'][0]
        nombre = item['values'][1]

        confirmar = messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar '{nombre}'?\nEsto borrará también su historial.")
        if confirmar:
            eliminar_producto(id_prod)
            self.actualizar_tabla()

    def ventana_categorias(self):
        v = tk.Toplevel(self.root)
        v.title("Gestionar Categorías")
        v.geometry("350x500")

        # --- SECCIÓN PARA AÑADIR ---
        frame_add = tk.LabelFrame(v, text="Nueva Categoría", padx=10, pady=10)
        frame_add.pack(pady=10, padx=10, fill="x")

        tk.Label(frame_add, text="Nombre:").pack()
        ent_nombre_cat = tk.Entry(frame_add)
        ent_nombre_cat.pack(pady=5, fill="x")

        def add_cat():
            nombre = ent_nombre_cat.get().strip()
            if nombre:
                registrar_categoria(nombre)
                ent_nombre_cat.delete(0, tk.END)
                actualizar_lista_local() # Refresca la lista abajo
                messagebox.showinfo("Éxito", f"Categoría '{nombre}' añadida")
            else:
                messagebox.showwarning("Error", "Escribe un nombre")

        tk.Button(frame_add, text="Añadir Categoría", command=add_cat, bg="#4CAF50", fg="white").pack()

        # --- SECCIÓN DE LISTA Y ELIMINACIÓN ---
        tk.Label(v, text="Categorías Existentes", font=("Arial", 10, "bold")).pack(pady=5)
        
        lista = tk.Listbox(v)
        lista.pack(pady=5, padx=10, fill="both", expand=True)
        
        def actualizar_lista_local():
            lista.delete(0, tk.END)
            for c in obtener_categorias():
                lista.insert(tk.END, f"{c[0]} - {c[1]}")

        def borrar_cat():
            try:
                # 1. Obtener la categoría seleccionada de la lista
                seleccion = lista.get(lista.curselection())
                id_cat = int(seleccion.split(" - ")[0])
                nombre_cat = seleccion.split(" - ")[1]

                # 2. Buscar si hay productos ligados a esta categoría
              
                productos_ligados = obtener_productos_por_categoria(id_cat)

                # 3. Construir el mensaje de advertencia
                if productos_ligados:
                    lista_prods = "\n- ".join(productos_ligados)
                    mensaje = (f"¡Atención! La categoría '{nombre_cat}' tiene estos productos:\n\n"
                               f"- {lista_prods}\n\n"
                               "¿Estás SEGURO de eliminarla? Los productos podrían quedar sin categoría.")
                else:
                    mensaje = f"¿Estás seguro de eliminar la categoría '{nombre_cat}'? No tiene productos asociados."

                # 4. Mostrar la advertencia
                confirmar = messagebox.askyesno("Confirmar Eliminación", mensaje)
                
                if confirmar:
                    eliminar_categoria(id_cat)
                    actualizar_lista_local()
                    messagebox.showinfo("Éxito", "Categoría eliminada.")
            except IndexError:
                messagebox.showerror("Error", "Por favor, selecciona una categoría de la lista.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {e}")
        tk.Button(v, text="Eliminar Seleccionada", command=borrar_cat, bg="#f44336", fg="white").pack(pady=10)

        # Cargar lista al abrir
        actualizar_lista_local()

    # ... (Mantener las funciones ventana_nuevo_producto, ventana_venta y mostrar_reporte igual que antes)
    def ventana_nuevo_producto(self):
        v = tk.Toplevel(self.root)
        v.title("Nuevo Producto")
        v.geometry("350x450")
        campos = ["Nombre:", "Precio Compra:", "Precio Venta:", "Stock Inicial:"]
        entradas = []
        for c in campos:
            tk.Label(v, text=c).pack(pady=2)
            e = tk.Entry(v); e.pack(pady=2); entradas.append(e)

        tk.Label(v, text="Categoría:").pack(pady=5)
        lista_cats = obtener_categorias() 
        combo_cat = ttk.Combobox(v, values=[c[1] for c in lista_cats], state="readonly")
        combo_cat.pack()

        def guardar():
            try:
                cat_id = next(c[0] for c in lista_cats if c[1] == combo_cat.get())
                registrar_producto(entradas[0].get(), float(entradas[1].get()), 
                                   float(entradas[2].get()), int(entradas[3].get()), cat_id, 1)
                self.actualizar_tabla(); v.destroy()
            except: messagebox.showerror("Error", "Datos incorrectos")

        tk.Button(v, text="Guardar", command=guardar, bg="purple", fg="white").pack(pady=20)

    def ventana_venta(self):
        v = tk.Toplevel(self.root)
        v.title("Venta")
        v.geometry("300x250")
        tk.Label(v, text="ID Producto:").pack()
        e_id = tk.Entry(v); e_id.pack()
        tk.Label(v, text="Cantidad:").pack()
        e_can = tk.Entry(v); e_can.pack()
        tk.Label(v, text="Precio Venta:").pack()
        e_pre = tk.Entry(v); e_pre.pack()

        def vender():
            try:
                registrar_movimiento(int(e_id.get()), int(e_can.get()), 'SALIDA', float(e_pre.get()))
                self.actualizar_tabla(); v.destroy()
            except: messagebox.showerror("Error", "Datos inválidos")
        tk.Button(v, text="Vender", command=vender, bg="green", fg="white").pack(pady=10)

    def mostrar_reporte(self):
        res = obtener_resumen_financiero()
        info = (f"Ventas Totales: S/ {res['ingresos']:.2f}\n"
                f"Gastos Extra: S/ {res['gastos_extra']:.2f}\n"
                f"GANANCIA NETA: S/ {res['ganancia_neta']:.2f}")
        messagebox.showinfo("Balance", info)

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionNegocio(root)
    root.mainloop()
