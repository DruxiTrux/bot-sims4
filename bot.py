import discord
from discord.ext import commands
import json

# ==========================================
# CARGAR BASE DE DATOS
# ==========================================

with open("packs.json", "r", encoding="utf-8") as archivo:

    packs = json.load(archivo)

# ==========================================
# TOKEN DEL BOT
# ==========================================

import os

TOKEN = os.getenv("TOKEN")

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

    mensaje += "========== FREE PACKS ==========\n"

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
# INICIAR BOT
# ==========================================

bot.run(TOKEN)