import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# Diccionario de colores y configuraciones visuales
C = {
    "bg":      "#0f1117", "panel":  "#1a1d27", "input":  "#252836",
    "accent":  "#4f8ef7", "hover":  "#3a6fd8", "dim":    "#1e3a6e",
    "fg":      "#e8eaf0", "fg2":    "#8b8fa8", "border": "#2e3148",
    "success": "#4ecdc4", "warn":   "#f7b731",
}

# Fuentes del sistema (títulos, subtítulos, botones, etc)
FT = ("Segoe UI", 14, "bold")
FS = ("Segoe UI", 9,  "bold")
FL = ("Segoe UI", 9)
FE = ("Segoe UI", 10)
FB = ("Segoe UI", 9,  "bold")
FC = ("Consolas", 10)


class App:
    def __init__(self, root):
        self.root = root
        root.title("Calculadora de Potencias de relaciones")
        root.geometry("680x750")
        root.minsize(580, 680)
        root.configure(bg=C["bg"])

        # Configuración permitir desplazamiento 
        canvas = tk.Canvas(root, bg=C["bg"], highlightthickness=0)
        sb = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
        f = tk.Frame(canvas, bg=C["bg"])
        
        
        f.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=f, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        
        # permitir el scroll con la rueda del mouse
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # Carga de los paneles de la interfaz
        self._header(f)
        self._panel_dominio(f)
        self._panel_pares(f)
        self._panel_potencia(f)
        self._panel_consola(f)



    def _card(self, parent, title):
  
        w = tk.Frame(parent, bg=C["bg"])
        w.pack(fill=tk.X, padx=20, pady=6)
        tk.Label(w, text=title.upper(), font=FS, bg=C["bg"], fg=C["fg2"]).pack(anchor=tk.W, pady=(0,4))
        
        outer = tk.Frame(w, bg=C["panel"], highlightbackground=C["border"], highlightthickness=1)
        outer.pack(fill=tk.X)
        
        inner = tk.Frame(outer, bg=C["panel"])
        inner.pack(fill=tk.X, padx=16, pady=12)
        return inner

    def _entry(self, parent, ph="", width=0):
        kw = dict(font=FE, bg=C["input"], fg=C["fg"], insertbackground=C["fg"],
                  relief="flat", bd=0, highlightthickness=1,
                  highlightbackground=C["border"], highlightcolor=C["accent"],
                  selectbackground=C["dim"])
        if width:
            kw["width"] = width
            
        e = tk.Entry(parent, **kw)
        
        if ph: # Lógica para mostrar/ocultar el texto por defecto 
            e.insert(0, ph)
            e.config(fg=C["fg2"])
            e.bind("<FocusIn>",  lambda _, en=e, p=ph: (en.delete(0, tk.END), en.config(fg=C["fg"])) if en.get()==p else None)
            e.bind("<FocusOut>", lambda _, en=e, p=ph: (en.insert(0, p), en.config(fg=C["fg2"])) if not en.get() else None)
        return e

    def _out(self, text, color=C["success"]):
        tag = color.replace("#","t")
        self.consola.tag_configure(tag, foreground=color)
        self.consola.insert(tk.END, text+"\n", tag)
        self.consola.see(tk.END)

    # Secciones del UI

    def _header(self, parent):
        h = tk.Frame(parent, bg=C["bg"])
        h.pack(fill=tk.X, padx=24, pady=(20, 4))
        tk.Label(h, text="Matematicas discretas y sus aplicaciones", font=("Segoe UI",8,"bold"),
                 bg=C["dim"], fg=C["accent"], padx=8, pady=3).pack(anchor=tk.W)
        tk.Label(h, text="Potencia de Relaciones", font=FT,
                 bg=C["bg"], fg=C["fg"]).pack(anchor=tk.W, pady=(6,2))
        tk.Label(h, text="Calcula Rⁿ mediante composición y muestra cada paso.",
                 font=FL, bg=C["bg"], fg=C["fg2"]).pack(anchor=tk.W)
        tk.Frame(h, height=1, bg=C["border"]).pack(fill=tk.X, pady=(14,0))

    def _panel_dominio(self, parent):
        card = self._card(parent, "1  ·  Dominio del conjunto")
        tk.Label(card, text="Elementos separados por comas", font=FL,
                 bg=C["panel"], fg=C["fg2"]).pack(anchor=tk.W, pady=(0,5))
        self.set_entry = self._entry(card, ph="ej. 1, 2, 3, 4")
        self.set_entry.pack(fill=tk.X)

    def _panel_pares(self, parent):
        card = self._card(parent, "2  ·  Relación inicial  R¹")
        tk.Label(card, text="Hasta 5 pares ordenados (a, b) ",
                 font=FL, bg=C["panel"], fg=C["fg2"]).pack(anchor=tk.W, pady=(0,8))
        
        self.pares = []
        for i in range(5):
            row = tk.Frame(card, bg=C["panel"])
            row.pack(fill=tk.X, pady=3)
            
            tk.Label(row, text=f"Par {i+1}", font=("Segoe UI",8,"bold"),
                     bg=C["dim"], fg=C["accent"], width=5, padx=4, pady=2).pack(side=tk.LEFT, padx=(0,10))
            tk.Label(row, text="(", font=("Segoe UI",12), bg=C["panel"], fg=C["fg2"]).pack(side=tk.LEFT)
            
            ex = self._entry(row, width=9)
            ex.pack(side=tk.LEFT, padx=3)
            
            tk.Label(row, text=",", font=("Segoe UI",12), bg=C["panel"], fg=C["fg2"]).pack(side=tk.LEFT)
            
            ey = self._entry(row, width=9)
            ey.pack(side=tk.LEFT, padx=3)
            
            tk.Label(row, text=")", font=("Segoe UI",12), bg=C["panel"], fg=C["fg2"]).pack(side=tk.LEFT)
            
            self.pares.append((ex, ey))

    def _panel_potencia(self, parent):
        card = self._card(parent, "3  ·  Potencia")
        row = tk.Frame(card, bg=C["panel"])
        row.pack(fill=tk.X)
        
        tk.Label(row, text="Calcular R elevada a la potencia  n =",
                 font=FL, bg=C["panel"], fg=C["fg"]).pack(side=tk.LEFT)
                 
        self.pot_entry = self._entry(row, width=7)
        self.pot_entry.pack(side=tk.LEFT, padx=(8,0))
        
        btn = tk.Button(card, text="  Calcular  →", font=FB,
                        bg=C["accent"], fg="#fff", activebackground=C["hover"],
                        activeforeground="#fff", relief="flat", cursor="hand2",
                        padx=18, pady=8, bd=0, command=self.calcular)
        btn.pack(anchor=tk.E, pady=(12,0))
        
        btn.bind("<Enter>", lambda e: btn.config(bg=C["hover"]))
        btn.bind("<Leave>", lambda e: btn.config(bg=C["accent"]))

    def _panel_consola(self, parent):
        card = self._card(parent, "4  ·  Procedimiento y resultado")
        bar = tk.Frame(card, bg="#0a0c12", padx=10, pady=6)
        bar.pack(fill=tk.X)
        
        # Botones decorativos
        for col in ("#fc5c65","#f7b731","#4ecdc4"): 
            tk.Label(bar, text="●", fg=col, bg="#0a0c12", font=("Segoe UI",9)).pack(side=tk.LEFT, padx=2)
            
        tk.Label(bar, text="output — calculadora_relaciones", font=("Consolas",8),
                 bg="#0a0c12", fg=C["fg2"]).pack(side=tk.LEFT, padx=12)
                 
        self.consola = scrolledtext.ScrolledText(
            card, height=12, font=FC, bg="#0a0c12", fg=C["success"],
            insertbackground=C["success"], relief="flat", padx=14, pady=10,
            wrap=tk.WORD, bd=0, selectbackground=C["dim"])
        self.consola.pack(fill=tk.BOTH, expand=True)
        
        self._out("Ingresa el dominio, los pares de R¹ y la potencia n,\n"
                  "luego presiona  'Calcular →'  para ver el procedimiento.", C["fg2"])

    # parte lógica
    def _componer(self, R_prev, R_base, paso):
        """
        Realiza la composición R^paso = R^(paso-1) ∘ R_base.
        Para cada (a,b) ∈ R_prev y (b,c) ∈ R_base  →  (a,c) ∈ R^paso.
        """
        resultado = set()
        self._out(f"\n┌─  Calculando R^{paso}  " + "─"*28, C["fg2"])
        hubo = False
        
        
        for a, b in sorted(R_prev):
            for c, d in sorted(R_base):
                if b == c:  # 'b' es el elemento puente entre los dos pares
                    resultado.add((a, d))
                    hubo = True
                    # Muestra: par (a,b) de R^prev  +  par (b,d) de R  →  nuevo par (a,d)
                    self._out(f"│  ({a},{b}) ∧ ({c},{d})  →  ({a},{d}) ∈ R^{paso}", C["fg"])
                    
        if not hubo:
            self._out("│  Sin elemento puente (b = c).  R^n = ∅ a partir de aquí.", C["warn"])
            
        return resultado

    def calcular(self):
        """Valida las entradas del usuario y ejecuta el cálculo de la potencia."""
        self.consola.delete(1.0, tk.END)

        # Validación del dominio
        raw = self.set_entry.get().strip()
        if not raw or raw == "ej. 1, 2, 3, 4":
            return messagebox.showerror("Campo vacío", "El dominio no puede estar vacío.")
        dominio = {e.strip() for e in raw.split(",")}

        # Recolección de pares ordenados y validación
        R = set()
        for ex, ey in self.pares:
            x, y = ex.get().strip(), ey.get().strip()
            if x and y:
                # Comprobamos que los elementos ingresados existan dentro del dominio
                if x not in dominio or y not in dominio:
                    return messagebox.showerror("Error de dominio",
                        f"El par ({x},{y}) tiene elementos fuera del dominio.")
                R.add((x, y))
            elif x or y:
                return messagebox.showerror("Par incompleto",
                    "Completa ambos campos del par o deja la fila vacía.")
                    
        if not R:
            return messagebox.showerror("Sin relación", "Registra al menos un par ordenado.")

        # validación de la potencia 'n'
        try:
            n = int(self.pot_entry.get())
            assert n > 0
        except Exception:
            return messagebox.showerror("Potencia inválida",
                "La potencia 'n' debe ser un número entero mayor a cero.")

       
        fmt = lambda s: "{ " + ", ".join(f"({a},{b})" for a,b in sorted(s)) + " }"
        sep = "═" * 46
        self._out(sep, C["border"])
        self._out(f"  R¹ = {fmt(R)}", C["success"])
        self._out(f"  Objetivo: calcular R^{n}", C["fg2"])
        self._out(sep, C["border"])

        # en caso de que la potencia solicitada sea 1
        if n == 1:
            self._out(f"\n  n = 1  →  R^1 es la relación inicial.", C["fg2"])
            self._out(f"\n  RESULTADO:  R^1 = {fmt(R)}", C["success"])
            self._out(sep, C["border"])
            return

        # Cálculo de composición
        R_actual = R.copy()
        for paso in range(2, n + 1):
            R_actual = self._componer(R_actual, R, paso)
            if R_actual:
                self._out(f"└─  R^{paso} = {fmt(R_actual)}", C["accent"])
            else:
                # Si entra aquí, la relación está vacía y no hay pares para componer
                self._out(f"└─  R^{paso} = ∅  (conjunto vacío)", C["warn"])
                self._out("  Toda potencia superior también será ∅.", C["fg2"])
                break

        # Impresión del resultado final
        self._out(f"\n{sep}", C["border"])
        if R_actual:
            self._out(f"  Resultado final:  R^{n} = {fmt(R_actual)}", C["success"])
        else:
            self._out(f"  Resultado final:  R^{n} = ∅", C["warn"])
        self._out(sep, C["border"])


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()