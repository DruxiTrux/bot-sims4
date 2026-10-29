# Guía DLCs — Bot de Discord para The Sims 4

Bot de Discord para consultar el catálogo de packs de **The Sims 4** mediante comandos de barra (`/`). Permite buscar packs por nombre o código, consultar fechas de lanzamiento y precios aproximados, y ver listas por categoría o cronología.

El bot solo responde en los servidores autorizados. Al usar comandos de barra, no necesita leer el contenido general de los mensajes para procesar comandos.

## Comandos

| Comando | Parámetro | Descripción |
|---|---|---|
| `/dlc` | `busqueda` | Busca packs por nombre o código. |
| `/infor` | `codigo` | Muestra el nombre, tipo, fecha de lanzamiento y precio aproximado de un pack. |
| `/list` | — | Muestra todos los packs organizados por categoría. |
| `/expansiones` | — | Muestra los Packs de Expansión (EP). |
| `/contenido` | — | Muestra los Packs de Contenido (GP). |
| `/kits` | — | Muestra los kits y Packs de Accesorios (SP). |
| `/gratuitos` | — | Muestra los packs gratuitos (FP). |
| `/cronologia` | — | Ordena los packs por fecha de lanzamiento. |
| `/ayuda` | — | Muestra la lista de comandos. |

### Ejemplos

```text
/dlc busqueda: perros
/infor codigo: EP01
```

La información de `/infor` tiene este formato:

```text
Código  : EP01
Nombre  : ¡A Trabajar!
Tipo    : Pack de Expansión
Lanzado : 31/03/2015
Precio  : ~$39.99 USD (precio aproximado)
```

## Datos del catálogo

- `packs.json`: códigos y nombres de los packs.
- `fechas.json`: fechas de lanzamiento en formato `DD/MM/AAAA`.

## Configuración y ejecución

1. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

2. Configura el secreto `TOKEN` con el token del bot de Discord. En Replit, guárdalo en **Tools → Secrets**; no lo escribas en el código ni lo publiques en GitHub.

3. Inicia el bot:

   ```bash
   python bot.py
   ```

Los comandos de barra se sincronizan con Discord al iniciar. El proyecto también incluye un pequeño servidor Flask para el endpoint de estado `/`, usando el puerto indicado por `PORT` o `10000` como valor predeterminado.

## Restricción de servidores

El bot solo procesa comandos en los servidores autorizados configurados en `bot.py`. En otros servidores responde que no está autorizado.

## Precios aproximados

| Categoría | Precio aproximado |
|---|---:|
| Pack de Expansión (EP) | ~$39.99 USD |
| Pack de Contenido (GP) | ~$19.99 USD |
| Packs SP01–SP18 | ~$9.99 USD |
| Kits SP20 en adelante | ~$4.99 USD |
| Pack gratuito (FP) | Gratis |

Los precios son orientativos y pueden variar según la región y las ofertas vigentes.
