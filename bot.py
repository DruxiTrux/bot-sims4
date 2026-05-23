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

SERVIDOR_ID = 1448484344174743595

# ==========================================
# ROLES PERMITIDOS
# ==========================================

ROLES_PERMITIDOS = {
    1458283509499170878,
    1457897762250166425,
    1465447064107221003,
    1448750130567057508,
    1463996153174691910,
}

def tiene_rol_permitido(ctx):
    roles_usuario = {role.id for role in ctx.author.roles}
    return bool(roles_usuario & ROLES_PERMITIDOS)

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
    intents=intents
)

# ==========================================
# FILTRO GLOBAL: SOLO SERVIDOR PERMITIDO
# ==========================================

@bot.check
async def solo_servidor_permitido(ctx):
    return ctx.guild is not None and ctx.guild.id == SERVIDOR_ID

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

    if not tiene_rol_permitido(ctx):
        return

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

    if not tiene_rol_permitido(ctx):
        return

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

    if not tiene_rol_permitido(ctx):
        return

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

    if not tiene_rol_permitido(ctx):
        return

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

    if not tiene_rol_permitido(ctx):
        return

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

    if not tiene_rol_permitido(ctx):
        return

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
# COMANDO: !ayuda
# ==========================================

@bot.command()
async def ayuda(ctx):

    if not tiene_rol_permitido(ctx):
        return

    mensaje = (
        "========== COMANDOS DISPONIBLES ==========\n"
        "!dlc <búsqueda>  — Busca packs por nombre o código\n"
        "!list            — Muestra todos los packs por categoría\n"
        "!expansiones     — Muestra solo los Packs de Expansión\n"
        "!contenido       — Muestra solo los Packs de Contenido\n"
        "!kits            — Muestra solo los Kits y Accesorios\n"
        "!gratuitos       — Muestra solo los Kits Gratuitos\n"
        "!info <código>   — Muestra el detalle de un pack específico\n"
        "!ayuda           — Muestra esta lista de comandos\n"
    )

    await ctx.send(f"```{mensaje}```")

# ==========================================
# COMANDO: !info
# ==========================================

@bot.command()
async def info(ctx, codigo: str):

    if not tiene_rol_permitido(ctx):
        return

    codigo = codigo.upper()

    if codigo not in packs:
        await ctx.send(f"No se encontró ningún pack con el código `{codigo}`.")
        return

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

    await ctx.send(f"```Código  : {codigo}\nNombre  : {nombre}\nTipo    : {tipo}\nLanzado : {fecha}```")

# ==========================================
# INICIAR BOT
# ==========================================

bot.run(TOKEN)
