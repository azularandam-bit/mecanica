import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML, display, clear_output
import ipywidgets as widgets


def simular_caida_observadores(y1, y2, v1, g, dt, t_max):
    """Simula la caída libre de un paquete y muestra la animación."""
    if dt <= 0:
        print("Error: dt debe ser mayor que 0.")
        return
    if t_max <= 0:
        print("Error: t_max debe ser mayor que 0.")
        return
    if y1 <= y2:
        print("Error: La Ventana 1 (y1) debe estar más arriba que la Ventana 2 (y2).")
        return
    if v1 <= 0:
        print("Error: La velocidad medida en la Ventana 1 debe ser mayor que 0.")
        return

    H = y1 + (v1 ** 2) / (2 * g)

    v2 = np.sqrt(v1 ** 2 + 2 * g * (y1 - y2))
    v_impacto = np.sqrt(2 * g * H)
    t_suelo = np.sqrt(2 * H / g)

    if t_max < t_suelo:
        t_max = t_suelo + 1.0

    t = np.arange(0, t_max + dt, dt)

    x_pos = 0.0
    y_paquete, v_paquete = [], []
    t_vuelo = []

    t_obs1 = np.sqrt(2 * (H - y1) / g)
    t_obs2 = np.sqrt(2 * (H - y2) / g)

    impacto_registrado = False
    frame_impacto = None

    for i, ti in enumerate(t):
        if ti <= t_suelo:
            yi = H - 0.5 * g * ti ** 2
            vi = -g * ti
            y_paquete.append(yi)
            v_paquete.append(vi)
            t_vuelo.append(ti)
        else:
            if not impacto_registrado:
                impacto_registrado = True
                frame_impacto = i
            y_paquete.append(0.0)
            v_paquete.append(v_paquete[-1] if v_paquete else 0.0)
            t_vuelo.append(ti)

    xmin = -15
    xmax = 15
    ymin = -5
    ymax = H + 10

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect("equal", adjustable="box")

    ax.grid(color="lime", linestyle="--", alpha=0.18)
    for spine in ax.spines.values():
        spine.set_color("lime")
    ax.tick_params(colors="lime")
    ax.set_title("Simulación Caída Libre: Observadores en Edificio", color="lime", fontsize=14)
    ax.set_xlabel("Posición x", color="lime")
    ax.set_ylabel("Altura y", color="lime")

    edificio_rect = plt.Rectangle((-4, 0), 8, H, fill=False, edgecolor="cyan", linestyle="-", linewidth=1.5, alpha=0.4)
    ax.add_patch(edificio_rect)

    ax.axhline(H, color="green", linestyle="--", alpha=0.7, label=f"Azotea H = {H:.2f} m")
    ax.axhline(y1, color="orange", linestyle=":", alpha=0.7, label=f"Ventana 1 (y1 = {y1} m)")
    ax.axhline(y2, color="red", linestyle=":", alpha=0.7, label=f"Ventana 2 (y2 = {y2} m)")

    trayectoria, = ax.plot([], [], color="cyan", linewidth=2.4, label="Trayectoria del Paquete")
    paquete, = ax.plot([], [], "s", color="red", markersize=10, label="Módulo de Carga")

    texto_tiempo = ax.text(0.02, 0.96, "", transform=ax.transAxes, color="lime", fontsize=11, va="top")
    texto_estado = ax.text(0.02, 0.90, "", transform=ax.transAxes, color="white", fontsize=11, va="top")
    texto_info = ax.text(0.02, 0.80, "", transform=ax.transAxes, color="cyan", fontsize=10, va="top")

    boom1 = plt.Circle((0, 0), 0, color="yellow", alpha=0.8, visible=False)
    boom2 = plt.Circle((0, 0), 0, color="red", alpha=0.4, visible=False)
    ax.add_patch(boom1)
    ax.add_patch(boom2)

    leg = ax.legend(loc="upper right", facecolor="black", edgecolor="lime")
    for txt in leg.get_texts():
        txt.set_color("white")

    total_frames = len(t) + 15

    def update(frame):
        if frame < len(t):
            idx = frame
            ti = t[idx]
            yi = y_paquete[idx]
            vi = v_paquete[idx]

            trayectoria.set_data([0] * (idx + 1), y_paquete[:idx + 1])
            paquete.set_data([0], [yi])

            texto_tiempo.set_text(f"Tiempo = {ti:.2f} s")

            if abs(yi - y1) < 0.6:
                estado_str = f"¡PASANDO VENTANA 1! v1 = {v1:.2f} m/s"
            elif abs(yi - y2) < 0.6:
                estado_str = f"¡PASANDO VENTANA 2! v2 = {v2:.2f} m/s"
            elif yi <= 0:
                estado_str = "ESTADO: IMPACTO EN EL SUELO"
            else:
                estado_str = "ESTADO: En caída libre"

            texto_estado.set_text(estado_str)
            texto_info.set_text(
                f"Altura actual y = {yi:.2f} m\n"
                f"Rapidez instantánea = {abs(vi):.2f} m/s\n"
                f"Altura calculada H = {H:.2f} m"
            )

            boom1.set_visible(False)
            boom2.set_visible(False)
        else:
            k = frame - len(t) + 1
            boom1.set_visible(True)
            boom2.set_visible(True)

            boom1.set_radius(0.5 * k)
            boom2.set_radius(1.0 * k)

            texto_tiempo.set_text(f"Impacto a los {t_suelo:.2f} s")
            texto_estado.set_text("ESTADO: IMPACTO REGISTRADO")
            texto_info.set_text(f"Velocidad de impacto final = -{v_impacto:.2f} m/s")

        return trayectoria, paquete, boom1, boom2, texto_tiempo, texto_estado, texto_info

    ani = FuncAnimation(fig, update, frames=total_frames, interval=60, blit=True)
    plt.close(fig)

    print("=" * 55)
    print("      RESULTADOS DE LA SIMULACIÓN DE CAÍDA LIBRE      ")
    print("=" * 55)
    print(f" Altura Ventana 1 (y1):         {y1:.2f} m  (t = {t_obs1:.2f} s)")
    print(f" Velocidad medida en V1 (v1):   {v1:.2f} m/s")
    print(f" Altura Ventana 2 (y2):         {y2:.2f} m  (t = {t_obs2:.2f} s)")
    print(f" Velocidad calculada en V2 (v2):{v2:.2f} m/s")
    print("-" * 55)
    print(f" ALTURA TOTAL CALCULADA (H):    {H:.2f} m")
    print(f" Tiempo total hasta el suelo:   {t_suelo:.2f} s")
    print(f" Velocidad de impacto:          {-v_impacto:.2f} m/s")
    print("=" * 55)

    display(HTML(ani.to_jshtml()))


# INTERFAZ GRÁFICA INTERACTIVA CON WIDGETS

y1_box = widgets.FloatText(value=30.0, description='y1 (Ventana 1):', style={'description_width': 'initial'})
y2_box = widgets.FloatText(value=10.0, description='y2 (Ventana 2):', style={'description_width': 'initial'})
v1_box = widgets.FloatText(value=14.0, description='v1 (Velocidad 1):', style={'description_width': 'initial'})
g_box = widgets.FloatText(value=9.81, description='Gravedad (g):', style={'description_width': 'initial'})
dt_box = widgets.FloatText(value=0.05, description='Paso dt:', style={'description_width': 'initial'})
tmax_box = widgets.FloatText(value=6.0, description='Tiempo máx:', style={'description_width': 'initial'})

boton = widgets.Button(description="Ejecutar Simulación del Edificio", button_style='success')
salida = widgets.Output()


def ejecutar(b):
    with salida:
        clear_output(wait=True)
        simular_caida_observadores(
            y1_box.value,
            y2_box.value,
            v1_box.value,
            g_box.value,
            dt_box.value,
            tmax_box.value,
        )


boton.on_click(ejecutar)


if __name__ == "__main__":
    display(widgets.VBox([
        widgets.HTML("<h3>Simulación de Caída Libre: Dos Observadores en Edificio</h3>"),
        widgets.HBox([
            widgets.VBox([y1_box, y2_box, v1_box]),
            widgets.VBox([g_box, dt_box, tmax_box]),
        ]),
        boton,
        salida,
    ]))
else:
    display(widgets.VBox([
        widgets.HTML("<h3>Simulación de Caída Libre: Dos Observadores en Edificio</h3>"),
        widgets.HBox([
            widgets.VBox([y1_box, y2_box, v1_box]),
            widgets.VBox([g_box, dt_box, tmax_box]),
        ]),
        boton,
        salida,
    ]))


# End of file.
