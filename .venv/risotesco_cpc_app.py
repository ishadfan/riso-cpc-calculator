import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class RisoCPCCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("RISO & TESCO - Ink Cost Per Page (CPC) Calculator")
        self.geometry("900x850")
        self.minsize(800, 700)

        # Main Layout container
        self.create_header()
        self.create_top_parameters_section()
        self.create_items_table_section()
        self.create_result_section()

    def create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color=("#1f538d", "#143d59"), corner_radius=0)
        header_frame.pack(fill="x", padx=0, pady=0)

        # Branding: RISO & TESCO
        title_label = ctk.CTkLabel(header_frame, text="RISO  ✖  TESCO", font=("Arial", 24, "bold"), text_color="white")
        title_label.pack(pady=(12, 2))

        subtitle_label = ctk.CTkLabel(header_frame, text="حاسبة كلفة الطباعة للورقة الواحدة (Cost Per Copy / Page Calculator)", font=("Arial", 13), text_color="#e0e0e0")
        subtitle_label.pack(pady=(0, 12))

    def create_top_parameters_section(self):
        params_frame = ctk.CTkFrame(self)
        params_frame.pack(fill="x", padx=20, pady=15)

        # Grid inside params
        params_frame.columnconfigure(1, weight=1)
        params_frame.columnconfigure(3, weight=1)

        # Page Volume
        lbl_vol = ctk.CTkLabel(params_frame, text="حجم الطباعة (Page Volume):", font=("Arial", 13, "bold"))
        lbl_vol.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.page_vol_entry = ctk.CTkEntry(params_frame, placeholder_text="5000000")
        self.page_vol_entry.insert(0, "5000000")
        self.page_vol_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        # Coverage %
        lbl_cov = ctk.CTkLabel(params_frame, text="نسبة تغطية الحبر (Coverage %):", font=("Arial", 13, "bold"))
        lbl_cov.grid(row=0, column=2, sticky="w", padx=10, pady=10)
        self.coverage_entry = ctk.CTkEntry(params_frame, placeholder_text="15")
        self.coverage_entry.insert(0, "15")
        self.coverage_entry.grid(row=0, column=3, sticky="ew", padx=10, pady=10)

        # Riso Model selection
        lbl_model = ctk.CTkLabel(params_frame, text="موديل آلة ريزو (RISO Model):", font=("Arial", 13, "bold"))
        lbl_model.grid(row=1, column=0, sticky="w", padx=10, pady=10)
        
        self.model_var = ctk.StringVar(value="GL730 (GL full set - 167,000 pages)")
        self.model_menu = ctk.CTkOptionMenu(
            params_frame, 
            values=[
                "GL730 (GL full set - 167,000 pages)",
                "FT Series (FT full set - 120,000 pages)",
                "Valezus T1200 (164,000 pages)",
                "GD Series (GD full set - 166,000 pages)",
                "FT Black (110,000 pages)",
                "FW Series (FW full set - 110,000 pages)"
            ],
            variable=self.model_var,
            width=280
        )
        self.model_menu.grid(row=1, column=1, columnspan=3, sticky="ew", padx=10, pady=10)

    def create_items_table_section(self):
        # Table frame for items, qty, cost/item
        table_container = ctk.CTkFrame(self)
        table_container.pack(fill="both", expand=True, padx=20, pady=10)

        lbl_table_title = ctk.CTkLabel(table_container, text="بنود التكلفة (Items & Prices Input)", font=("Arial", 15, "bold"))
        lbl_table_title.pack(anchor="w", padx=10, pady=(10, 5))

        # Scrollable area for items
        self.items_scroll = ctk.CTkScrollableFrame(table_container, height=260)
        self.items_scroll.pack(fill="both", expand=True, padx=10, pady=5)

        # Headers
        headers_frame = ctk.CTkFrame(self.items_scroll, fg_color="transparent")
        headers_frame.pack(fill="x", pady=2)
        ctk.CTkLabel(headers_frame, text="العنصر (Item)", font=("Arial", 12, "bold"), width=250, anchor="w").pack(side="left", padx=5)
        ctk.CTkLabel(headers_frame, text="الكمية (Qty)", font=("Arial", 12, "bold"), width=100).pack(side="left", padx=5)
        ctk.CTkLabel(headers_frame, text="التكلفة للوحدة (€)", font=("Arial", 12, "bold"), width=120).pack(side="left", padx=5)

        # Default items based on the Excel screenshot
        self.default_items = [
            {"item": "Main Engine GL9730", "qty": 1.0, "cost": 38000.0},
            {"item": "High Capacity Feeder", "qty": 1.0, "cost": 5000.0},
            {"item": "High Capacity Stacker", "qty": 1.0, "cost": 8000.0},
            {"item": "GL Black ink", "qty": 48.08, "cost": 300.0},
            {"item": "GL Color ink", "qty": 102.42, "cost": 300.0},
            {"item": "FS2100C", "qty": 1.0, "cost": 2500.0},
            {"item": "Spare Parts", "qty": 1.0, "cost": 250.0},
        ]

        self.row_widgets = []
        for row_data in self.default_items:
            row_f = ctk.CTkFrame(self.items_scroll, fg_color="transparent")
            row_f.pack(fill="x", pady=4)

            item_name_entry = ctk.CTkEntry(row_f, width=250)
            item_name_entry.insert(0, row_data["item"])
            item_name_entry.pack(side="left", padx=5)

            qty_entry = ctk.CTkEntry(row_f, width=100)
            qty_entry.insert(0, str(row_data["qty"]))
            qty_entry.pack(side="left", padx=5)

            cost_entry = ctk.CTkEntry(row_f, width=120)
            cost_entry.insert(0, str(row_data["cost"]))
            cost_entry.pack(side="left", padx=5)

            self.row_widgets.append((item_name_entry, qty_entry, cost_entry))

    def create_result_section(self):
        res_frame = ctk.CTkFrame(self, fg_color=("#f0f0f0", "#2b2b2b"))
        res_frame.pack(fill="x", padx=20, pady=15)

        calc_btn = ctk.CTkButton(res_frame, text="احسب تكلفة الورقة الواحدة (Calculate CPP)", command=self.calculate, fg_color="#1f538d", height=45, font=("Arial", 15, "bold"))
        calc_btn.pack(fill="x", padx=15, pady=10)

        self.total_cost_label = ctk.CTkLabel(res_frame, text="إجمالي التكلفة الكلية (Total Cost): € 0.00", font=("Arial", 14, "bold"))
        self.total_cost_label.pack(anchor="w", padx=20, pady=2)

        self.cpp_label = ctk.CTkLabel(res_frame, text="كلفة الورقة الواحدة (Cost Per Page - CPP): € 0.00000", font=("Arial", 16, "bold"), text_color="#d9534f")
        self.cpp_label.pack(anchor="w", padx=20, pady=(2, 12))

    def calculate(self):
        try:
            page_volume = float(self.page_vol_entry.get())
            if page_volume <= 0:
                messagebox.showerror("خطأ", "يجب أن يكون حجم الطباعة أكبر من صفر.")
                return

            total_cost = 0.0
            for item_name_e, qty_e, cost_e in self.row_widgets:
                qty = float(qty_e.get() or 0)
                unit_cost = float(cost_e.get() or 0)
                total_cost += (qty * unit_cost)

            cpp = total_cost / page_volume

            # Update results
            self.total_cost_label.configure(text=f"إجمالي التكلفة الكلية (Total Cost): € {total_cost:,.2f}")
            self.cpp_label.configure(text=f"كلفة الورقة الواحدة (Cost Per Page - CPP): € {cpp:.5f}")

        except ValueError:
            messagebox.showerror("خطأ في البيانات", "يرجى التأكد من إدخال أرقام صحيحة في الحقول العدديّة.")

if __name__ == "__main__":
    app = RisoCPCCalculator()
    app.mainloop()