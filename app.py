import flet as ft

def main(page: ft.Page):
    page.title = "RISO CPC Calculator"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    
    page.window_width = 410
    page.window_height = 800
    page.window_resizable = True

    PRIMARY_PURPLE = "#5B1E63"
    TEXT_DARK = "#1E293B"
    BG_WHITE = "#FFFFFF"

    yield_settings = {
        "GL (5 bottles)": {"K": 104000, "C": 148600, "M": 189600, "Y": 167200, "G": 400000},
        "FT Black": {"K": 110000, "C": 0, "M": 0, "Y": 0, "G": 0},
        "FT (4 bottles)": {"K": 99000, "C": 107900, "M": 160100, "Y": 112300, "G": 112300},
        "Valezus T1200 (5 bottles)": {"K": 106200, "C": 141000, "M": 186000, "Y": 165000, "G": 400000},
        "GD (5 bottles)": {"K": 91200, "C": 119700, "M": 170600, "Y": 146400, "G": 300000},
        "FW (4 bottles)": {"K": 93000, "C": 88000, "M": 112000, "Y": 89000, "G": 0}
    }
    
    selected_model = {"name": "GL (5 bottles)"}
    selected_coverage = {"value": 15.0}
    selected_currency = {"symbol": "€"}

    # 1. شاشة الترحيب (Welcome Screen)
    def show_welcome():
        page.clean()
        
        welcome_content = ft.Column([
            ft.Container(height=100),
            ft.Container(
                content=ft.Column([
                    ft.Text("RISO CPC", size=28, weight="bold", color=PRIMARY_PURPLE, text_align=ft.TextAlign.CENTER),
                    ft.Text("Calculator & Cost Analysis", size=16, weight="w500", color=PRIMARY_PURPLE, text_align=ft.TextAlign.CENTER),
                    ft.Container(height=15),
                    ft.Text(
                        "Calculate precise printing costs per copy (CPP), evaluate ink consumption, and manage advanced yield parameters for professional RISO printing systems.",
                        size=13,
                        color=TEXT_DARK,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=30),
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Text("Start", size=16, weight="bold", color="white"),
                            ft.Icon(ft.Icons.ARROW_FORWARD, color="white", size=18)
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                        on_click=lambda _: show_home(),
                        bgcolor=PRIMARY_PURPLE,
                        color="white",
                        height=50,
                        width=280,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=ft.Colors.with_opacity(0.60, BG_WHITE), # شفافة أكثر
                padding=25,
                border_radius=20,
                width=360,
                shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.1, "black"))
            ),
            ft.Container(height=40),
            ft.Text("Developed by Ibrahim Shadfan", size=11, color=PRIMARY_PURPLE, weight="bold"),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll="auto")

        page.add(
            ft.Container(
                content=welcome_content,
                image=ft.DecorationImage(src="background_01.png", fit="cover"),
                expand=True,
                alignment=ft.alignment.Alignment(0, 0)
            )
        )
        page.update()

    # 2. الشاشة الرئيسية (Home Screen)
    def show_home():
        page.clean()

        model_dropdown = ft.Dropdown(
            value=selected_model["name"],
            options=[ft.dropdown.Option(m) for m in yield_settings.keys()],
            width=320,
            height=46,
            bgcolor="#F8FAFC",
            border_radius=12,
            border=ft.InputBorder.NONE,
            text_style=ft.TextStyle(color=TEXT_DARK, weight="bold", size=13),
            content_padding=12
        )

        coverage_input = ft.TextField(
            value=str(selected_coverage["value"]),
            width=320,
            height=46,
            bgcolor="#F8FAFC",
            border_radius=12,
            border=ft.InputBorder.NONE,
            text_style=ft.TextStyle(color=TEXT_DARK, weight="bold", size=13),
            content_padding=12
        )

        vol_input = ft.TextField(
            hint_text="e.g. 10,000",
            value="500,000",
            width=320,
            height=46,
            bgcolor="#F8FAFC",
            border_radius=12,
            border=ft.InputBorder.NONE,
            text_style=ft.TextStyle(color=TEXT_DARK, weight="bold", size=13),
            hint_style=ft.TextStyle(color="#94A3B8"),
            content_padding=12
        )

        err_text = ft.Text("", color="red", size=12, text_align=ft.TextAlign.CENTER)

        def proceed(e):
            try:
                vol = int(vol_input.value.strip().replace(",", ""))
                cov = float(coverage_input.value.strip())
                selected_model["name"] = model_dropdown.value
                selected_coverage["value"] = cov
                show_cost_table(vol, cov, selected_model["name"])
            except Exception as ex:
                err_text.value = "Please enter valid numbers"
                page.update()

        main_content = ft.Column([
            ft.Container(height=30),
            
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.TextButton("← Welcome", on_click=lambda _: show_welcome(), style=ft.ButtonStyle(color=PRIMARY_PURPLE)),
                        ft.Container(expand=True),
                    ]),
                    ft.Text("Printer Model", size=12, weight="bold", color=PRIMARY_PURPLE),
                    model_dropdown,
                    ft.Container(height=2),

                    ft.Text("Ink Coverage (%)", size=12, weight="bold", color=PRIMARY_PURPLE),
                    coverage_input,
                    ft.Container(height=2),

                    ft.Text("Number of Copies", size=12, weight="bold", color=PRIMARY_PURPLE),
                    vol_input,
                    
                    ft.Container(height=2),
                    err_text,
                    ft.Container(height=2),

                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.TABLE_CHART, color="white", size=18),
                            ft.Text("Calculate CPC", size=15, weight="bold", color="white"),
                            ft.Icon(ft.Icons.CHEVRON_RIGHT, color="white", size=18)
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                        on_click=proceed,
                        bgcolor=PRIMARY_PURPLE,
                        color="white",
                        height=48,
                        width=320,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
                    ),
                    ft.Container(height=2),
                    ft.Row([
                        ft.Text("", size=11),
                        ft.TextButton(
                            content=ft.Text("⚙️ Advanced Yield & Currency", size=11, color=PRIMARY_PURPLE),
                            on_click=lambda _: show_settings()
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ], horizontal_alignment=ft.CrossAxisAlignment.START),
                bgcolor=ft.Colors.with_opacity(0.55, BG_WHITE), # تم تخفيف الشفافية لتظهر الخلفية بوضوح
                padding=15,
                border_radius=20,
                width=360,
                shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.1, "black"))
            ),

            ft.Container(height=10),

            ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Icon(ft.Icons.TRENDING_DOWN, color=PRIMARY_PURPLE, size=20),
                        ft.Container(height=2),
                        ft.Text("Reduce Costs", size=10, color=TEXT_DARK, text_align=ft.TextAlign.CENTER, weight="w500")
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=110),
                    
                    ft.VerticalDivider(width=1, color="#D8B4FE"),

                    ft.Column([
                        ft.Icon(ft.Icons.ECO_OUTLINED, color=PRIMARY_PURPLE, size=20),
                        ft.Container(height=2),
                        ft.Text("Eco-Friendly", size=10, color=TEXT_DARK, text_align=ft.TextAlign.CENTER, weight="w500")
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=110),
                    
                    ft.VerticalDivider(width=1, color="#D8B4FE"),

                    ft.Column([
                        ft.Icon(ft.Icons.BAR_CHART, color=PRIMARY_PURPLE, size=20),
                        ft.Container(height=2),
                        ft.Text("High Volumes", size=10, color=TEXT_DARK, text_align=ft.TextAlign.CENTER, weight="w500")
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=110),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=2, height=55),
                bgcolor=ft.Colors.with_opacity(0.55, BG_WHITE),
                border_radius=15,
                padding=5
            ),

            ft.Container(height=10),
            ft.Text("RISO  |  PEOPLE  |  IDEAS  |  PRINTING", size=10, color=PRIMARY_PURPLE, weight="bold"),
            ft.Text("Developed by Ibrahim Shadfan (TESCO Jordan)", size=10, color=PRIMARY_PURPLE, weight="bold"),
            ft.Container(height=15),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll="auto")

        page.add(
            ft.Container(
                content=main_content,
                image=ft.DecorationImage(src="background_01.png", fit="cover"),
                expand=True,
                alignment=ft.alignment.Alignment(0, 0)
            )
        )
        page.update()

    # 3. شاشة الإعدادات المتقدمة
    def show_settings():
        page.clean()
        
        currency_dropdown = ft.Dropdown(
            value=selected_currency["symbol"],
            options=[
                ft.dropdown.Option("€", text="Euro (€)"),
                ft.dropdown.Option("$", text="US Dollar ($)"),
                ft.dropdown.Option("£", text="British Pound (£)"),
                ft.dropdown.Option("د.أ", text="Jordanian Dinar (د.أ)"),
                ft.dropdown.Option("د.إ", text="UAE Dirham (د.إ)"),
                ft.dropdown.Option("SAR", text="Saudi Riyal (SAR)"),
                ft.dropdown.Option("¥", text="Japanese Yen (¥)")
            ],
            width=320,
            height=48,
            bgcolor="#F8FAFC",
            border_radius=10,
            text_style=ft.TextStyle(color=TEXT_DARK, weight="bold")
        )

        fields_list = [
            ft.Container(height=20),
            ft.Text("Advanced Settings", size=20, weight="bold", color=PRIMARY_PURPLE),
            ft.Container(height=10),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Select Currency", weight="bold", size=13, color=PRIMARY_PURPLE),
                    currency_dropdown
                ], spacing=8),
                padding=15,
                bgcolor=ft.Colors.with_opacity(0.55, BG_WHITE),
                border_radius=12,
                width=350
            ),
            ft.Container(height=10),
            ft.Text("Custom Yield Settings", size=16, weight="bold", color=PRIMARY_PURPLE),
            ft.Container(height=5),
        ]
        
        settings_fields = {}
        for model, colors in yield_settings.items():
            model_card_items = [ft.Text(f"Model: {model}", weight="bold", size=13, color=PRIMARY_PURPLE)]
            settings_fields[model] = {}
            for color, val in colors.items():
                if val > 0:
                    tf = ft.TextField(
                        label=f"{color} Yield",
                        value=str(val),
                        width=320,
                        height=48,
                        text_style=ft.TextStyle(color=TEXT_DARK, weight="bold"),
                        label_style=ft.TextStyle(color="#475569")
                    )
                    model_card_items.append(tf)
                    settings_fields[model][color] = tf
            
            fields_list.append(
                ft.Container(
                    content=ft.Column(model_card_items, spacing=8),
                    padding=15,
                    bgcolor=ft.Colors.with_opacity(0.55, BG_WHITE),
                    border_radius=12,
                    width=350
                )
            )
            fields_list.append(ft.Container(height=8))

        def save_settings(e):
            selected_currency["symbol"] = currency_dropdown.value
            for model, colors in settings_fields.items():
                for color, tf in colors.items():
                    try:
                        yield_settings[model][color] = int(tf.value)
                    except:
                        pass
            show_home()

        fields_list.extend([
            ft.Container(height=10),
            ft.ElevatedButton(
                content=ft.Text("Save & Back", size=14, weight="bold", color="white"),
                on_click=save_settings,
                bgcolor=PRIMARY_PURPLE,
                height=45, width=320,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
            ),
            ft.Container(height=10),
            ft.TextButton("← Back to Home", on_click=lambda _: show_home(), style=ft.ButtonStyle(color=PRIMARY_PURPLE)),
            ft.Container(height=20)
        ])

        page.add(
            ft.Container(
                content=ft.Column(fields_list, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll="auto"),
                image=ft.DecorationImage(src="background_01.png", fit="cover"),
                expand=True,
                alignment=ft.alignment.Alignment(0, 0)
            )
        )
        page.update()

    # 4. شاشة عرض النتائج والجدول (Cost Table)
    def show_cost_table(vol, cov, model):
        page.clean()
        y_vals = yield_settings.get(model, list(yield_settings.values())[0])
        model_prefix = model.split()[0]
        curr = selected_currency["symbol"]

        coverage_factor = cov / 15.0

        k_yield = y_vals.get("K", 0)
        black_qty = round((vol / k_yield) * coverage_factor, 2) if k_yield > 0 else 0.0

        color_qty = 0.0
        for color, y_val in y_vals.items():
            if color != "K" and y_val > 0:
                color_qty += (vol / y_val) * coverage_factor
        color_qty = round(color_qty, 2)

        initial_items = [
            {"item": f"Main Engine {model_prefix}9730" if model_prefix == "GL" else f"Main Engine {model_prefix}", "qty": 1.0, "cost": 38000.0},
            {"item": "High Capacity Feeder", "qty": 1.0, "cost": 5000.0},
            {"item": "High Capacity Stacker", "qty": 1.0, "cost": 8000.0},
        ]

        if k_yield > 0:
            initial_items.append({"item": f"{model_prefix} Black ink", "qty": black_qty, "cost": 300.0})
        
        if color_qty > 0:
            initial_items.append({"item": f"{model_prefix} Color ink", "qty": color_qty, "cost": 300.0})

        initial_items.extend([
            {"item": "FS2100C", "qty": 1.0, "cost": 2500.0},
            {"item": "Spare Parts", "qty": 1.0, "cost": 250.0}
        ])

        ui_rows = []
        lbl_grand_total = ft.Text(f"{curr} 0.00", size=14, weight="bold", color=PRIMARY_PURPLE)
        lbl_cpp = ft.Text(f"{curr} 0.000000", size=16, weight="bold", color="#2563EB")

        def calculate_all(e=None):
            try:
                grand_total = 0
                for row_obj in ui_rows:
                    q = float(row_obj["qty_field"].value)
                    c = float(row_obj["cost_field"].value)
                    t = q * c
                    row_obj["total_text"].value = f"{curr} {t:,.2f}"
                    grand_total += t
                
                cpp = grand_total / vol if vol > 0 else 0
                lbl_grand_total.value = f"{curr} {grand_total:,.2f}"
                lbl_cpp.value = f"{curr} {cpp:.6f}"
                page.update()
            except:
                pass

        data_rows = []
        for item_data in initial_items:
            tf_qty = ft.TextField(
                value=str(item_data["qty"]), 
                width=60, height=35, 
                text_size=11, 
                text_style=ft.TextStyle(color=TEXT_DARK, weight="bold"),
                text_align=ft.TextAlign.RIGHT, 
                content_padding=4
            )
            tf_cost = ft.TextField(
                value=f"{item_data['cost']:.2f}", 
                width=75, height=35, 
                text_size=11, 
                text_style=ft.TextStyle(color=TEXT_DARK, weight="bold"),
                text_align=ft.TextAlign.RIGHT, 
                content_padding=4
            )
            lbl_total = ft.Text(f"{curr} {item_data['qty'] * item_data['cost']:,.2f}", size=11, weight="bold", color=TEXT_DARK)

            ui_rows.append({"qty_field": tf_qty, "cost_field": tf_cost, "total_text": lbl_total})
            tf_qty.on_change = calculate_all
            tf_cost.on_change = calculate_all

            data_rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(item_data["item"], size=10, color=TEXT_DARK, weight="w500")),
                    ft.DataCell(tf_qty),
                    ft.DataCell(tf_cost),
                    ft.DataCell(lbl_total),
                ])
            )

        calculate_all()

        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Item", weight="bold", size=10, color="white", text_align=ft.TextAlign.CENTER)),
                ft.DataColumn(ft.Text("Qty", weight="bold", size=10, color="white", text_align=ft.TextAlign.CENTER)),
                ft.DataColumn(ft.Text("Cost", weight="bold", size=10, color="white", text_align=ft.TextAlign.CENTER)),
                ft.DataColumn(ft.Text("Total", weight="bold", size=10, color="white", text_align=ft.TextAlign.CENTER)),
            ],
            rows=data_rows,
            heading_row_color=PRIMARY_PURPLE,
            heading_row_height=35,
            data_row_min_height=40,
            data_row_max_height=45,
            column_spacing=5,
        )

        summary_box = ft.Container(
            content=ft.Column([
                ft.Row([ft.Text("Total Cost", size=13, weight="bold", color=TEXT_DARK), lbl_grand_total], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=1),
                ft.Row([ft.Text("CPP", size=14, weight="bold", color=PRIMARY_PURPLE), lbl_cpp], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ]),
            padding=15,
            bgcolor=ft.Colors.with_opacity(0.55, BG_WHITE),
            border_radius=12,
            width=350
        )

        table_content = ft.Column([
            ft.Container(height=20),
            ft.Text(f"Model: {model} | Vol: {vol:,} | Cov: {cov}%", size=11, weight="bold", color=PRIMARY_PURPLE),
            ft.Container(height=5),
            ft.Container(content=table, bgcolor=ft.Colors.with_opacity(0.55, BG_WHITE), border_radius=12, padding=10),
            ft.Container(height=10),
            summary_box,
            ft.Container(height=15),
            ft.TextButton("← Back to Calculator", on_click=lambda _: show_home(), style=ft.ButtonStyle(color=PRIMARY_PURPLE)),
            ft.Container(height=20)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll="auto")

        page.add(
            ft.Container(
                content=table_content,
                image=ft.DecorationImage(src="background_01.png", fit="cover"),
                expand=True,
                alignment=ft.alignment.Alignment(0, 0)
            )
        )
        page.update()

    # تشغيل التطبيق بعرض شاشة الترحيب أولاً
    show_welcome()

ft.app(target=main, assets_dir="assets")