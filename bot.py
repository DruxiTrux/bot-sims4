# SERVIDOR FLASK (KEEP ALIVE PARA RENDER)
import os
import json
from threading import Thread
from flask import Flask
import discord
from discord import app_commands
from discord.ext import commands

# ==========================================
# SERVIDOR FLASK (KEEP ALIVE PARA RENDER)
# ==========================================

app = Flask('')

@app.route('/')
def home():
    return "¡Bot activo y funcionando 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

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

TOKEN = os.getenv("TOKEN")

# ==========================================
# SERVIDORES PERMITIDOS
# ==========================================

SERVIDORES_PERMITIDOS = {
    1448484344174743595,
    1512417855554195516,
}

# ==========================================
# INTENTS Y CREACIÓN DEL BOT
# ==========================================

intents = discord.Intents.default()

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print("¡Comandos Slash sincronizados correctamente!")

bot = MyBot()

# ==========================================
# DECORADOR DE VERIFICACIÓN PARA SERVIDORES
# ==========================================

def solo_servidor_permitido():
    async def predicate(interaction: discord.Interaction):
        if interaction.guild is None or interaction.guild.id not in SERVIDORES_PERMITIDOS:
            await interaction.response.send_message("Este bot solo puede usarse en servidores autorizados.", ephemeral=True)
            return False
        return True
    return app_commands.check(predicate)

# ==========================================
# BOT LISTO
# ==========================================

@bot.event
async def on_ready():
    print(f"Conectado como {bot.user}")

# ==========================================
# COMANDOS SLASH
# ==========================================

@bot.tree.command(name="dlc", description="Busca packs por nombre o código")
@app_commands.describe(busqueda="Nombre o código del pack que buscas")
@solo_servidor_permitido()
async def dlc(interaction: discord.Interaction, busqueda: str):
    await interaction.response.defer(ephemeral=False)
    try:
        busqueda = busqueda.lower()
        resultados = []

        for codigo, info in packs.items():
            nombre_es = info.get("nombre", "")
            nombre_en = info.get("nombre_en", "")
            
            if (busqueda in codigo.lower() or 
                busqueda in nombre_es.lower() or 
                busqueda in nombre_en.lower()):
                resultados.append(f"{codigo} - {nombre_es} ({nombre_en})")

        if resultados:
            mensaje = "\n".join(resultados)
            await interaction.followup.send(f"```{mensaje[:1900]}```")
        else:
            await interaction.followup.send("No se encontraron resultados.")
    except Exception as e:
        await interaction.followup.send(f"Ocurrió un error al buscar: {e}")

@bot.tree.command(name="list", description="Muestra todos los packs por categoría")
@solo_servidor_permitido()
async def list_packs(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    try:
        partes = []
        mensaje = ""

        # FREE PACKS / KITS GRATUITOS
        mensaje += "========== KIT GRATUITO ==========\n"
        for codigo, info in packs.items():
            if codigo.startswith("FP"):
                linea = f"{codigo} - {info['nombre']} ({info['nombre_en']})\n"
                if len(mensaje) + len(linea) > 1900:
                    partes.append(mensaje)
                    mensaje = ""
                mensaje += linea
        mensaje += "\n"

        # EXPANSIONES
        mensaje += "========== PACKS DE EXPANSIÓN ==========\n"
        for codigo, info in packs.items():
            if codigo.startswith("EP"):
                linea = f"{codigo} - {info['nombre']} ({info['nombre_en']})\n"
                if len(mensaje) + len(linea) > 1900:
                    partes.append(mensaje)
                    mensaje = ""
                mensaje += linea
        mensaje += "\n"

        # CONTENIDO
        mensaje += "========== PACKS DE CONTENIDO ==========\n"
        for codigo, info in packs.items():
            if codigo.startswith("GP"):
                linea = f"{codigo} - {info['nombre']} ({info['nombre_en']})\n"
                if len(mensaje) + len(linea) > 1900:
                    partes.append(mensaje)
                    mensaje = ""
                mensaje += linea
        mensaje += "\n"

        # KITS Y ACCESORIOS
        mensaje += "====== PACKS DE ACCESORIOS Y KITS ======\n"
        for codigo, info in packs.items():
            if codigo.startswith("SP"):
                linea = f"{codigo} - {info['nombre']} ({info['nombre_en']})\n"
                if len(mensaje) + len(linea) > 1900:
                    partes.append(mensaje)
                    mensaje = ""
                mensaje += linea

        if mensaje:
            partes.append(mensaje)

        await interaction.followup.send(f"```{partes[0]}```")
        for parte in partes[1:]:
            await interaction.followup.send(f"```{parte}```")
    except Exception as e:
        await interaction.followup.send(f"Ocurrió un error: {e}")

@bot.tree.command(name="expansiones", description="Muestra solo los Packs de Expansión")
@solo_servidor_permitido()
async def expansiones(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    try:
        mensaje = "========== PACKS DE EXPANSIÓN ==========\n"
        for codigo, info in packs.items():
            if codigo.startswith("EP"):
                mensaje += f"{codigo} - {info['nombre']} ({info['nombre_en']})\n"
        await interaction.followup.send(f"```{mensaje[:1900]}```")
    except Exception as e:
        await interaction.followup.send(f"Ocurrió un error: {e}")

@bot.tree.command(name="contenido", description="Muestra solo los Packs de Contenido")
@solo_servidor_permitido()
async def contenido(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    try:
        mensaje = "========== PACKS DE CONTENIDO ==========\n"
        for codigo, info in packs.items():
            if codigo.startswith("GP"):
                mensaje += f"{codigo} - {info['nombre']} ({info['nombre_en']})\n"
        await interaction.followup.send(f"```{mensaje[:1900]}```")
    except Exception as e:
        await interaction.followup.send(f"Ocurrió un error: {e}")

@bot.tree.command(name="kits", description="Muestra solo los Kits y Accesorios")
@solo_servidor_permitido()
async def kits(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    try:
        mensaje = "====== PACKS DE ACCESORIOS Y KITS ======\n"
        for codigo, info in packs.items():
            if codigo.startswith("SP"):
                mensaje += f"{codigo} - {info['nombre']} ({info['nombre_en']})\n"
        await interaction.followup.send(f"```{mensaje[:1900]}```")
    except Exception as e:
        await interaction.followup.send(f"Ocurrió un error: {e}")

@bot.tree.command(name="gratuitos", description="Muestra solo los Kits Gratuitos")
@solo_servidor_permitido()
async def gratuitos(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    try:
        mensaje = "========== KIT GRATUITO ==========\n"
        for codigo, info in packs.items():
            if codigo.startswith("FP"):
                mensaje += f"{codigo} - {info['nombre']} ({info['nombre_en']})\n"
        await interaction.followup.send(f"```{mensaje[:1900]}```")
    except Exception as e:
        await interaction.followup.send(f"Ocurrió un error: {e}")

@bot.tree.command(name="cronologia", description="Lista todos los packs por fecha de lanzamiento")
@solo_servidor_permitido()
async def cronologia(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    try:
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
        mensaje = "====== PACKS POR FECHA DE LANZAMIENTO ======\n"

        for codigo, info in packs_ordenados:
            fecha = fechas.get(codigo, "No disponible")
            mensaje += f"{fecha}  {codigo} - {info['nombre']} ({info['nombre_en']})\n"

        await interaction.followup
