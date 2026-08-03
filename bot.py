import discord
from discord.ext import commands
import json

# ==========================================
# CARGAR BASE DE DATOS
# ==========================================

with open("packs.json", "r", encoding="utf-8") as archivo:
    packs = json.load(archivo)

with open("fechas.json", "r", encoding="utf-8") as archivo:
    fechas = json.load(archivo)

# ==========================================
# TOKEN DEL BOT
# ==========================================
import os

TOKEN = os.getenv("TOKEN")

# ==========================================
# SERVIDOR PERMITIDO
# ==========================================

SERVIDORES_PERMITIDOS = {
    1448484344174743595,
    1512417855554195516,
}

# ==========================================
# INTENTS
# ==========================================

intents = discord.Intents.default()
intents.message_content = True

# ==========================================
# CREAR BOT
# ==========================================

bot = commands.Bot(
    command_prefix="!",
    case_insensitive=True,
    intents=intents
)

# ==========================================
# FILTRO GLOBAL: SOLO SERVIDOR PERMITIDO
# ==========================================

@bot.check
async def solo_servidor_permitido(ctx):
    return ctx.guild is not None and ctx.guild.id in SERVIDORES_PERMITIDOS

# ==========================================
# BOT LISTO
# ==========================================

@bot.event
async def on_ready():

    print(f"Conectado como {bot.user}")

# ==========================================
# COMANDO: !dlc
# ==========================================

@bot.command()
async def dlc(ctx, *, busqueda):

    busqueda = busqueda.lower()

    resultados = []

    for codigo, nombre in packs.items():

        if (
            busqueda in codigo.lower()
            or
            busqueda in nombre.lower()
        ):

            resultados.append(
                f"{codigo} - {nombre}"
            )

    # ======================================
    # SI HAY RESULTADOS
    # ======================================

    if resultados:

        mensaje = "\n".join(resultados)

        await ctx.send(
            f"```{mensaje}```"
        )

    # ======================================
    # SI NO HAY RESULTADOS
    # ======================================

    else:

        await ctx.send(
            "No se encontraron resultados."
        )

# ==========================================
# COMANDO: !list
# ==========================================

@bot.command()
async def list(ctx):


    partes = []

    mensaje = ""

    # ======================================
    # FREE PACKS
    # ======================================

    mensaje += "========== KIT GRATUITO ==========\n"

    for codigo, nombre in packs.items():

        if codigo.startswith("FP"):

            linea = f"{codigo} - {nombre}\n"

            if len(mensaje) + len(linea) > 1900:

                partes.append(mensaje)
                mensaje = ""

            mensaje += linea

    mensaje += "\n"

    # ======================================
    # EXPANSIONES
    # ======================================

    mensaje += "========== PACKS DE EXPANSIÓN ==========\n"

    for codigo, nombre in packs.items():

        if codigo.startswith("EP"):

            linea = f"{codigo} - {nombre}\n"

            if len(mensaje) + len(linea) > 1900:

                partes.append(mensaje)
                mensaje = ""

            mensaje += linea

    mensaje += "\n"

    # ======================================
    # CONTENIDO
    # ======================================

    mensaje += "========== PACKS DE CONTENIDO ==========\n"

    for codigo, nombre in packs.items():

        if codigo.startswith("GP"):

            linea = f"{codigo} - {nombre}\n"

            if len(mensaje) + len(linea) > 1900:

                partes.append(mensaje)
                mensaje = ""

            mensaje += linea

    mensaje += "\n"

    # ======================================
    # KITS Y ACCESORIOS
    # ======================================

    mensaje += "====== PACKS DE ACCESORIOS Y KITS ======\n"

    for codigo, nombre in packs.items():

        if codigo.startswith("SP"):

            linea = f"{codigo} - {nombre}\n"

            if len(mensaje) + len(linea) > 1900:

                partes.append(mensaje)
                mensaje = ""

            mensaje += linea

    # ======================================
    # GUARDAR ÚLTIMA PARTE
    # ======================================

    if mensaje:

        partes.append(mensaje)

    # ======================================
    # ENVIAR TODAS LAS PARTES
    # ======================================

    for parte in partes:

        await ctx.send(
            f"```{parte}```"
        )

# ==========================================
# COMANDO: !expansiones
# ==========================================

@bot.command()
async def expansiones(ctx):


    partes = []
    mensaje = "========== PACKS DE EXPANSIÓN ==========\n"

    for codigo, nombre in packs.items():
        if codigo.startswith("EP"):
            linea = f"{codigo} - {nombre}\n"
            if len(mensaje) + len(linea) > 1900:
                partes.append(mensaje)
                mensaje = ""
            mensaje += linea

    if mensaje:
        partes.append(mensaje)

    for parte in partes:
        await ctx.send(f"```{parte}```")

# ==========================================
# COMANDO: !contenido
# ==========================================

@bot.command()
async def contenido(ctx):


    partes = []
    mensaje = "========== PACKS DE CONTENIDO ==========\n"

    for codigo, nombre in packs.items():
        if codigo.startswith("GP"):
            linea = f"{codigo} - {nombre}\n"
            if len(mensaje) + len(linea) > 1900:
                partes.append(mensaje)
                mensaje = ""
            mensaje += linea

    if mensaje:
        partes.append(mensaje)

    for parte in partes:
        await ctx.send(f"```{parte}```")

# ==========================================
# COMANDO: !kits
# ==========================================

@bot.command()
async def kits(ctx):


    partes = []
    mensaje = "====== PACKS DE ACCESORIOS Y KITS ======\n"

    for codigo, nombre in packs.items():
        if codigo.startswith("SP"):
            linea = f"{codigo} - {nombre}\n"
            if len(mensaje) + len(linea) > 1900:
                partes.append(mensaje)
                mensaje = ""
            mensaje += linea

    if mensaje:
        partes.append(mensaje)

    for parte in partes:
        await ctx.send(f"```{parte}```")

# ==========================================
# COMANDO: !gratuitos
# ==========================================

@bot.command()
async def gratuitos(ctx):


    partes = []
    mensaje = "========== KIT GRATUITO ==========\n"

    for codigo, nombre in packs.items():
        if codigo.startswith("FP"):
            linea = f"{codigo} - {nombre}\n"
            if len(mensaje) + len(linea) > 1900:
                partes.append(mensaje)
                mensaje = ""
            mensaje += linea

    if mensaje:
        partes.append(mensaje)

    for parte in partes:
        await ctx.send(f"```{parte}```")

# ==========================================
# COMANDO: !cronologia
# ==========================================

@bot.command()
async def cronologia(ctx):


    def parse_fecha(codigo):
        fecha = fechas.get(codigo, "")
        if not fecha or fecha == "No disponible":
            return (9999, 99, 99)
        try:
            d, m, a = fecha.split("/")
            return (int(a), int(m), int(d))
        except:
            return (9999, 99, 99)

    packs_ordenados = sorted(packs.items(), key=lambda x: parse_fecha(x[0]))

    partes = []
    mensaje = "====== PACKS POR FECHA DE LANZAMIENTO ======\n"

    for codigo, nombre in packs_ordenados:
        fecha = fechas.get(codigo, "No disponible")
        linea = f"{fecha}  {codigo} - {nombre}\n"
        if len(mensaje) + len(linea) > 1900:
            partes.append(mensaje)
            mensaje = ""
        mensaje += linea

    if mensaje:
        partes.append(mensaje)

    for parte in partes:
        await ctx.send(f"```{parte}```")

# ==========================================
# COMANDO: !ayuda
# ==========================================

@bot.command()
async def ayuda(ctx):


    mensaje = (
        "========== COMANDOS DISPONIBLES ==========\n"
        "!dlc <búsqueda>  — Busca packs por nombre o código\n"
        "!list            — Muestra todos los packs por categoría\n"
        "!expansiones     — Muestra solo los Packs de Expansión\n"
        "!contenido       — Muestra solo los Packs de Contenido\n"
        "!kits            — Muestra solo los Kits y Accesorios\n"
        "!gratuitos       — Muestra solo los Kits Gratuitos\n"
        "!infor <código>  — Muestra el detalle de un pack específico\n"
        "!cronologia      — Lista todos los packs por fecha de lanzamiento\n"
        "!ayuda           — Muestra esta lista de comandos\n"
    )

    await ctx.send(f"```{mensaje}```")

# ==========================================
# COMANDO: !infor
# ==========================================

@bot.command()
async def infor(ctx, codigo: str):


    codigo = codigo.upper()

    if codigo not in packs:
        await ctx.send(f"No se encontró ningún pack con el código `{codigo}`.")

    nombre = packs[codigo]

    if codigo.startswith("EP"):
        tipo = "Pack de Expansión"
    elif codigo.startswith("GP"):
        tipo = "Pack de Contenido"
    elif codigo.startswith("SP"):
        tipo = "Pack de Accesorios / Kit"
    elif codigo.startswith("FP"):
        tipo = "Free Pack"
    else:
        tipo = "Desconocido"

    fecha = fechas.get(codigo, "No disponible")

    if codigo.startswith("EP"):
        precio = "~$39.99 USD"
    elif codigo.startswith("GP"):
        precio = "~$19.99 USD"
    elif codigo.startswith("FP"):
        precio = "Gratis"
    elif codigo.startswith("SP") and int(codigo[2:]) <= 18:
        precio = "~$9.99 USD"
    else:
        precio = "~$4.99 USD"

    await ctx.send(f"```Código  : {codigo}\nNombre  : {nombre}\nTipo    : {tipo}\nLanzado : {fecha}\nPrecio  : {precio} (precio aproximado)```")

# ==========================================
# INICIAR BOT
# ==========================================

bot.run(TOKEN)
