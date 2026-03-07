from flask import Flask, render_template, request
import math

app = Flask(__name__)

# ============================================================
# RUTA PRINCIPAL
# ============================================================
@app.route("/")
def index():
    modulo = request.args.get("modulo")
    return render_template("index.html", resultado=None, modulo=modulo, formula=None, error=None)


# ============================================================
# RUTA DE CÁLCULO
# ============================================================
@app.route("/calcular", methods=["POST"])
def calcular():
    modulo = request.form.get("modulo")
    formula = request.form.get("formula")
    resultado = None
    error = None

    try:
        # ── LEY DE OHM ──────────────────────────────────────
        if modulo == "ohm":
            if formula == "voltaje":
                i = float(request.form.get("corriente"))
                r = float(request.form.get("resistencia"))
                resultado = f"Voltaje = {i * r:.4f} V"
            elif formula == "corriente":
                v = float(request.form.get("voltaje"))
                r = float(request.form.get("resistencia"))
                resultado = f"Corriente = {v / r:.4f} A"
            elif formula == "resistencia":
                v = float(request.form.get("voltaje"))
                i = float(request.form.get("corriente"))
                resultado = f"Resistencia = {v / i:.4f} Ω"

        # ── POTENCIA ─────────────────────────────────────────
        elif modulo == "potencia":
            if formula == "p_vi":
                v = float(request.form.get("voltaje"))
                i = float(request.form.get("corriente"))
                resultado = f"Potencia = {v * i:.4f} W"
            elif formula == "p_i2r":
                i = float(request.form.get("corriente"))
                r = float(request.form.get("resistencia"))
                resultado = f"Potencia = {i**2 * r:.4f} W"
            elif formula == "p_v2r":
                v = float(request.form.get("voltaje"))
                r = float(request.form.get("resistencia"))
                resultado = f"Potencia = {v**2 / r:.4f} W"
            elif formula == "v_pi":
                p = float(request.form.get("potencia"))
                i = float(request.form.get("corriente"))
                resultado = f"Voltaje = {p / i:.4f} V"
            elif formula == "i_pv":
                p = float(request.form.get("potencia"))
                v = float(request.form.get("voltaje"))
                resultado = f"Corriente = {p / v:.4f} A"
            elif formula == "i_raiz":
                p = float(request.form.get("potencia"))
                r = float(request.form.get("resistencia"))
                resultado = f"Corriente = {(p / r)**0.5:.4f} A"
            elif formula == "r_pi2":
                p = float(request.form.get("potencia"))
                i = float(request.form.get("corriente"))
                resultado = f"Resistencia = {p / i**2:.4f} Ω"
            elif formula == "r_v2p":
                v = float(request.form.get("voltaje"))
                p = float(request.form.get("potencia"))
                resultado = f"Resistencia = {v**2 / p:.4f} Ω"
            elif formula == "v_raiz":
                p = float(request.form.get("potencia"))
                r = float(request.form.get("resistencia"))
                resultado = f"Voltaje = {(p * r)**0.5:.4f} V"

        # ── KIRCHHOFF ────────────────────────────────────────
        elif modulo == "kirchhoff":
            if formula == "i1":
                it = float(request.form.get("i_total"))
                r1 = float(request.form.get("r1"))
                r2 = float(request.form.get("r2"))
                resultado = f"Corriente rama 1 = {it * (r2 / (r1 + r2)):.4f} A"
            elif formula == "i2":
                it = float(request.form.get("i_total"))
                r1 = float(request.form.get("r1"))
                r2 = float(request.form.get("r2"))
                resultado = f"Corriente rama 2 = {it * (r1 / (r1 + r2)):.4f} A"
            elif formula == "v1":
                vt = float(request.form.get("v_total"))
                r1 = float(request.form.get("r1"))
                r2 = float(request.form.get("r2"))
                resultado = f"Voltaje en R1 = {vt * (r1 / (r1 + r2)):.4f} V"
            elif formula == "v2":
                vt = float(request.form.get("v_total"))
                r1 = float(request.form.get("r1"))
                r2 = float(request.form.get("r2"))
                resultado = f"Voltaje en R2 = {vt * (r2 / (r1 + r2)):.4f} V"
            elif formula == "i_total":
                i1 = float(request.form.get("i1"))
                i2 = float(request.form.get("i2"))
                resultado = f"Corriente total = {i1 + i2:.4f} A"
            elif formula == "v_total":
                v1 = float(request.form.get("v1"))
                v2 = float(request.form.get("v2"))
                v3 = float(request.form.get("v3"))
                resultado = f"Voltaje total = {v1 + v2 + v3:.4f} V"

        # ── POTENCIA DISIPADA ────────────────────────────────
        elif modulo == "disipada":
            if formula == "p_i2r":
                i = float(request.form.get("corriente"))
                r = float(request.form.get("resistencia"))
                resultado = f"Potencia disipada = {i**2 * r:.4f} W"
            elif formula == "p_v2r":
                v = float(request.form.get("voltaje"))
                r = float(request.form.get("resistencia"))
                resultado = f"Potencia disipada = {v**2 / r:.4f} W"
            elif formula == "r_pi2":
                p = float(request.form.get("potencia"))
                i = float(request.form.get("corriente"))
                resultado = f"Resistencia = {p / i**2:.4f} Ω"
            elif formula == "r_v2p":
                v = float(request.form.get("voltaje"))
                p = float(request.form.get("potencia"))
                resultado = f"Resistencia = {v**2 / p:.4f} Ω"
            elif formula == "i_raiz":
                p = float(request.form.get("potencia"))
                r = float(request.form.get("resistencia"))
                resultado = f"Corriente = {(p / r)**0.5:.4f} A"
            elif formula == "v_raiz":
                p = float(request.form.get("potencia"))
                r = float(request.form.get("resistencia"))
                resultado = f"Voltaje = {(p * r)**0.5:.4f} V"

        # ── RESISTENCIAS EQUIVALENTES ────────────────────────
        elif modulo == "resistencias":
            if formula == "serie2":
                r1 = float(request.form.get("r1"))
                r2 = float(request.form.get("r2"))
                resultado = f"R equivalente = {r1 + r2:.4f} Ω"
            elif formula == "serie3":
                r1 = float(request.form.get("r1"))
                r2 = float(request.form.get("r2"))
                r3 = float(request.form.get("r3"))
                resultado = f"R equivalente = {r1 + r2 + r3:.4f} Ω"
            elif formula == "paralelo2":
                r1 = float(request.form.get("r1"))
                r2 = float(request.form.get("r2"))
                resultado = f"R equivalente = {(r1 * r2) / (r1 + r2):.4f} Ω"
            elif formula == "paralelo3":
                r1 = float(request.form.get("r1"))
                r2 = float(request.form.get("r2"))
                r3 = float(request.form.get("r3"))
                resultado = f"R equivalente = {1 / (1/r1 + 1/r2 + 1/r3):.4f} Ω"

        # ── CAÍDA DE TENSIÓN ─────────────────────────────────
        elif modulo == "caida":
            if formula == "v_ir":
                i = float(request.form.get("corriente"))
                r = float(request.form.get("resistencia"))
                resultado = f"Caída de tensión = {i * r:.4f} V"
            elif formula == "v1_serie":
                vt = float(request.form.get("v_total"))
                r1 = float(request.form.get("r1"))
                r2 = float(request.form.get("r2"))
                resultado = f"Caída en R1 = {vt * (r1 / (r1 + r2)):.4f} V"
            elif formula == "v2_serie":
                vt = float(request.form.get("v_total"))
                r1 = float(request.form.get("r1"))
                r2 = float(request.form.get("r2"))
                resultado = f"Caída en R2 = {vt * (r2 / (r1 + r2)):.4f} V"
            elif formula == "i1_paralelo":
                it = float(request.form.get("i_total"))
                r1 = float(request.form.get("r1"))
                r2 = float(request.form.get("r2"))
                resultado = f"Corriente rama 1 = {it * (r2 / (r1 + r2)):.4f} A"
            elif formula == "i2_paralelo":
                it = float(request.form.get("i_total"))
                r1 = float(request.form.get("r1"))
                r2 = float(request.form.get("r2"))
                resultado = f"Corriente rama 2 = {it * (r1 / (r1 + r2)):.4f} A"
            elif formula == "i_vr":
                v = float(request.form.get("voltaje"))
                r = float(request.form.get("resistencia"))
                resultado = f"Corriente = {v / r:.4f} A"
            elif formula == "v_total_serie":
                v1 = float(request.form.get("v1"))
                v2 = float(request.form.get("v2"))
                v3 = float(request.form.get("v3"))
                resultado = f"Voltaje total = {v1 + v2 + v3:.4f} V"
            elif formula == "i_total_paralelo":
                i1 = float(request.form.get("i1"))
                i2 = float(request.form.get("i2"))
                i3 = float(request.form.get("i3"))
                resultado = f"Corriente total = {i1 + i2 + i3:.4f} A"

        # ── CÓDIGO DE COLORES ────────────────────────────────
        elif modulo == "colores":
            COLORES = {
                "negro":   {"valor": 0, "multiplicador": 1,          "tolerancia": None},
                "marron":  {"valor": 1, "multiplicador": 10,         "tolerancia": "±1%"},
                "rojo":    {"valor": 2, "multiplicador": 100,        "tolerancia": "±2%"},
                "naranja": {"valor": 3, "multiplicador": 1000,       "tolerancia": None},
                "amarillo":{"valor": 4, "multiplicador": 10000,      "tolerancia": None},
                "verde":   {"valor": 5, "multiplicador": 100000,     "tolerancia": "±0.5%"},
                "azul":    {"valor": 6, "multiplicador": 1000000,    "tolerancia": "±0.25%"},
                "violeta": {"valor": 7, "multiplicador": 10000000,   "tolerancia": "±0.1%"},
                "gris":    {"valor": 8, "multiplicador": None,       "tolerancia": "±0.05%"},
                "blanco":  {"valor": 9, "multiplicador": None,       "tolerancia": None},
                "dorado":  {"valor": None, "multiplicador": 0.1,     "tolerancia": "±5%"},
                "plateado":{"valor": None, "multiplicador": 0.01,    "tolerancia": "±10%"},
            }

            def formatear_ohm(valor):
                if valor >= 1_000_000:
                    return f"{valor/1_000_000:.3g} MΩ"
                elif valor >= 1_000:
                    return f"{valor/1_000:.3g} kΩ"
                else:
                    return f"{valor:.3g} Ω"

            if formula == "4bandas":
                b1 = request.form.get("banda1", "").lower()
                b2 = request.form.get("banda2", "").lower()
                b3 = request.form.get("banda3", "").lower()
                b4 = request.form.get("banda4", "").lower()
                if not all([b1, b2, b3, b4]):
                    error = "Seleccioná todas las bandas."
                else:
                    v1 = COLORES[b1]["valor"]
                    v2 = COLORES[b2]["valor"]
                    mult = COLORES[b3]["multiplicador"]
                    tol  = COLORES[b4]["tolerancia"]
                    if v1 is None or v2 is None or mult is None:
                        error = "Combinación de bandas inválida para 4 bandas."
                    else:
                        valor = (v1 * 10 + v2) * mult
                        resultado = f"Resistencia = {formatear_ohm(valor)}  |  Tolerancia = {tol if tol else 'N/A'}"

            elif formula == "5bandas":
                b1 = request.form.get("banda1", "").lower()
                b2 = request.form.get("banda2", "").lower()
                b3 = request.form.get("banda3", "").lower()
                b4 = request.form.get("banda4", "").lower()
                b5 = request.form.get("banda5", "").lower()
                if not all([b1, b2, b3, b4, b5]):
                    error = "Seleccioná todas las bandas."
                else:
                    v1 = COLORES[b1]["valor"]
                    v2 = COLORES[b2]["valor"]
                    v3 = COLORES[b3]["valor"]
                    mult = COLORES[b4]["multiplicador"]
                    tol  = COLORES[b5]["tolerancia"]
                    if v1 is None or v2 is None or v3 is None or mult is None:
                        error = "Combinación de bandas inválida para 5 bandas."
                    else:
                        valor = (v1 * 100 + v2 * 10 + v3) * mult
                        resultado = f"Resistencia = {formatear_ohm(valor)}  |  Tolerancia = {tol if tol else 'N/A'}"

        # ── FILTROS RC / RL ──────────────────────────────────
        elif modulo == "filtros":
            if formula == "rc_fc":
                r  = float(request.form.get("resistencia"))
                c  = float(request.form.get("capacitancia"))
                fc = 1 / (2 * math.pi * r * c)
                resultado = f"Frecuencia de corte = {fc:.4f} Hz  ({fc/1000:.6f} kHz)"

            elif formula == "rc_r":
                fc = float(request.form.get("frecuencia"))
                c  = float(request.form.get("capacitancia"))
                r  = 1 / (2 * math.pi * fc * c)
                resultado = f"Resistencia = {r:.4f} Ω"

            elif formula == "rc_c":
                fc = float(request.form.get("frecuencia"))
                r  = float(request.form.get("resistencia"))
                c  = 1 / (2 * math.pi * fc * r)
                if c >= 1e-3:
                    c_str = f"{c*1e3:.4f} mF"
                elif c >= 1e-6:
                    c_str = f"{c*1e6:.4f} µF"
                elif c >= 1e-9:
                    c_str = f"{c*1e9:.4f} nF"
                else:
                    c_str = f"{c*1e12:.4f} pF"
                resultado = f"Capacitancia = {c_str}"

            elif formula == "rc_xc":
                f  = float(request.form.get("frecuencia"))
                c  = float(request.form.get("capacitancia"))
                xc = 1 / (2 * math.pi * f * c)
                resultado = f"Reactancia capacitiva Xc = {xc:.4f} Ω"

            elif formula == "rl_fc":
                r  = float(request.form.get("resistencia"))
                l  = float(request.form.get("inductancia"))
                fc = r / (2 * math.pi * l)
                resultado = f"Frecuencia de corte = {fc:.4f} Hz  ({fc/1000:.6f} kHz)"

            elif formula == "rl_r":
                fc = float(request.form.get("frecuencia"))
                l  = float(request.form.get("inductancia"))
                r  = 2 * math.pi * fc * l
                resultado = f"Resistencia = {r:.4f} Ω"

            elif formula == "rl_l":
                fc = float(request.form.get("frecuencia"))
                r  = float(request.form.get("resistencia"))
                l  = r / (2 * math.pi * fc)
                if l >= 1:
                    l_str = f"{l:.4f} H"
                elif l >= 1e-3:
                    l_str = f"{l*1e3:.4f} mH"
                else:
                    l_str = f"{l*1e6:.4f} µH"
                resultado = f"Inductancia = {l_str}"

            elif formula == "rl_xl":
                f  = float(request.form.get("frecuencia"))
                l  = float(request.form.get("inductancia"))
                xl = 2 * math.pi * f * l
                resultado = f"Reactancia inductiva Xl = {xl:.4f} Ω"

        # ── CONVERSIÓN DE UNIDADES ───────────────────────────
        elif modulo == "conversion":
            v        = float(request.form.get("valor"))
            origen   = request.form.get("unidad_origen", "")
            destino  = request.form.get("unidad_destino", "")

            if not origen or not destino:
                error = "Seleccioná la unidad de origen y la unidad de destino."
            else:
                # Tabla de factores: cada unidad → su valor en la unidad base del grupo
                FACTORES = {
                    # Resistencia (base: Ω)
                    "ohm": 1, "kohm": 1e3, "mohm": 1e6,
                    # Voltaje (base: V)
                    "uv": 1e-6, "mv": 1e-3, "v": 1, "kv": 1e3,
                    # Corriente (base: A)
                    "ua": 1e-6, "ma": 1e-3, "a": 1,
                    # Frecuencia (base: Hz)
                    "hz": 1, "khz": 1e3, "mhz": 1e6, "ghz": 1e9,
                    # Capacitancia (base: F)
                    "pf": 1e-12, "nf": 1e-9, "uf": 1e-6, "mf": 1e-3, "f": 1,
                    # Inductancia (base: H)
                    "uh": 1e-6, "mh": 1e-3, "h": 1,
                    # Potencia (base: W)
                    "mw": 1e-3, "w": 1, "kw": 1e3,
                }
                SIMBOLOS = {
                    "ohm":"Ω","kohm":"kΩ","mohm":"MΩ",
                    "uv":"µV","mv":"mV","v":"V","kv":"kV",
                    "ua":"µA","ma":"mA","a":"A",
                    "hz":"Hz","khz":"kHz","mhz":"MHz","ghz":"GHz",
                    "pf":"pF","nf":"nF","uf":"µF","mf":"mF","f":"F",
                    "uh":"µH","mh":"mH","h":"H",
                    "mw":"mW","w":"W","kw":"kW",
                }
                if origen not in FACTORES or destino not in FACTORES:
                    error = "Unidad no reconocida."
                else:
                    # Convertir: pasar a base y luego a destino
                    valor_base    = v * FACTORES[origen]
                    valor_destino = valor_base / FACTORES[destino]
                    # Formato inteligente
                    def fmt(n):
                        if n == 0: return "0"
                        if abs(n) >= 1e9:  return f"{n:.6e}"
                        if abs(n) >= 1:    return f"{n:.6g}"
                        return f"{n:.6e}"
                    resultado = (f"{v} {SIMBOLOS[origen]}  =  "
                                 f"{fmt(valor_destino)} {SIMBOLOS[destino]}")

    except (ValueError, TypeError):
        error = "Ingresá valores numéricos válidos en todos los campos."
    except ZeroDivisionError:
        error = "Error: división por cero. Verificá los valores ingresados."

    return render_template("index.html",
                           resultado=resultado,
                           error=error,
                           modulo=modulo,
                           formula=formula)


# ============================================================
if __name__ == "__main__":
    app.run(debug=False)
