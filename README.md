<h1 align="center">
  <img src="docs/assets/bouncy-broda-wordmark.svg" alt="Bouncy Broda" width="520">
</h1>

## rebota.

<p align="center">
  <img src="docs/assets/bouncy-broda-gameplay.gif" alt="Demo de Bouncy Broda: el jugador mueve la pelota con A y D, rebota en varias plataformas y el marcador sube." width="514">
</p>

Cada rebote suma un punto. Llega a **70** para ganar. Si la pelota cae fuera de la pantalla, la partida termina.

## Controles

| Tecla | Acción |
| --- | --- |
| `A` / `D` | Mover la pelota a izquierda y derecha |
| `W` / `Espacio` | Activar el impulso tras el primer rebote |
| `P` | Pausar o reanudar |
| `Esc` | Salir |

## Ejecutar en Windows

Necesitas Python y estas dependencias:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install pygame numpy pywin32
python files\main.py
```

También puedes abrir `Bouncy_Broda.pyw` desde el explorador de archivos.

---

README y logotipo preparados con asistencia de IA. El GIF muestra una partida del juego original con controles preparados para la demo; el código del juego no se modificó.
