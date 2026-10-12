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
    busqueda = busqueda.lower()
    resultados = []

    for codigo, nombre in packs.items():
        if busqueda in codigo.lower() or busqueda in nombre.lower():
            resultados.append(f"{codigo} - {nombre}")

    if resultados:
        mensaje = "\n".join(resultados)
        await interaction.response.send_message(f"```{mensaje}```")
    else:
        await interaction.response.send_message("No se encontraron resultados.")

@bot.tree.command(name="list", description="Muestra todos los packs por categoría")
@solo_servidor_permitido()
async def list_packs(interaction: discord.Interaction):
    partes = []
    mensaje = ""

    # FREE PACKS
    mensaje += "========== KIT GRATUITO ==========\n"
    for codigo, nombre in packs.items():
        if codigo.startswith("FP"):
            linea = f"{codigo} - {nombre}\n"
            if len(mensaje) + len(linea) > 1900:
                partes.append(mensaje)
                mensaje = ""
            mensaje += linea
    mensaje += "\n"

    # EXPANSIONES
    mensaje += "========== PACKS DE EXPANSIÓN ==========\n"
    for codigo, nombre in packs.items():
        if codigo.startswith("EP"):
            linea = f"{codigo} - {nombre}\n"
            if len(mensaje) + len(linea) > 1900:
                partes.append(mensaje)
                mensaje = ""
            mensaje += linea
    mensaje += "\n"

    # CONTENIDO
    mensaje += "========== PACKS DE CONTENIDO ==========\n"
    for codigo, nombre in packs.items():
        if codigo.startswith("GP"):
            linea = f"{codigo} - {nombre}\n"
            if len(mensaje) + len(linea) > 1900:
                partes.append(mensaje)
                mensaje = ""
            mensaje += linea
    mensaje += "\n"

    # KITS Y ACCESORIOS
    mensaje += "====== PACKS DE ACCESORIOS Y KITS ======\n"
    for codigo, nombre in packs.items():
        if codigo.startswith("SP"):
            linea = f"{codigo} - {nombre}\n"
            if len(mensaje) + len(linea) > 1900:
                partes.append(mensaje)
                mensaje = ""
            mensaje += linea

    if mensaje:
        partes.append(mensaje)

    await interaction.response.send_message(f"```{partes[0]}```")
    for parte in partes[1:]:
        await interaction.followup.send(f"```{parte}```")

@bot.tree.command(name="expansiones", description="Muestra solo los Packs de Expansión")
@solo_servidor_permitido()
async def expansiones(interaction: discord.Interaction):
    mensaje = "========== PACKS DE EXPANSIÓN ==========\n"
    for codigo, nombre in packs.items():
        if codigo.startswith("EP"):
            mensaje += f"{codigo} - {nombre}\n"
    await interaction.response.send_message(f"```{mensaje}```")

@bot.tree.command(name="contenido", description="Muestra solo los Packs de Contenido")
@solo_servidor_permitido()
async def contenido(interaction: discord.Interaction):
    mensaje = "========== PACKS DE CONTENIDO ==========\n"
    for codigo, nombre in packs.items():
        if codigo.startswith("GP"):
            mensaje += f"{codigo} - {nombre}\n"
    await interaction.response.send_message(f"```{mensaje}```")

@bot.tree.command(name="kits", description="Muestra solo los Kits y Accesorios")
@solo_servidor_permitido()
async def kits(interaction: discord.Interaction):
    mensaje = "====== PACKS DE ACCESORIOS Y KITS ======\n"
    for codigo, nombre in packs.items():
        if codigo.startswith("SP"):
            mensaje += f"{codigo} - {nombre}\n"
    await interaction.response.send_message(f"```{mensaje}```")

@bot.tree.command(name="gratuitos", description="Muestra solo los Kits Gratuitos")
@solo_servidor_permitido()
async def gratuitos(interaction: discord.Interaction):
    mensaje = "========== KIT GRATUITO ==========\n"
    for codigo, nombre in packs.items():
        if codigo.startswith("FP"):
            mensaje += f"{codigo} - {nombre}\n"
    await interaction.response.send_message(f"```{mensaje}```")

@bot.tree.command(name="cronologia", description="Lista todos los packs por fecha de lanzamiento")
@solo_servidor_permitido()
async def cronologia(interaction: discord.Interaction):
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

    for codigo, nombre in packs_ordenados:
        fecha = fechas.get(codigo, "No disponible")
        mensaje += f"{fecha}  {codigo} - {nombre}\n"

    await interaction.response.send_message(f"```{mensaje[:1900]}```")

@bot.tree.command(name="ayuda", description="Muestra la lista de comandos disponibles")
@solo_servidor_permitido()
async def ayuda(interaction: discord.Interaction):
    mensaje = (
        "========== COMANDOS DISPONIBLES ==========\n"
        "/dlc <búsqueda>  — Busca packs por nombre o código\n"
        "/list            — Muestra todos los packs por categoría\n"
        "/expansiones     — Muestra solo los Packs de Expansión\n"
        "/contenido       — Muestra solo los Packs de Contenido\n"
        "/kits            — Muestra solo los Kits y Accesorios\n"
        "/gratuitos       — Muestra solo los Kits Gratuitos\n"
        "/infor <código>  — Muestra el detalle de un pack específico\n"
        "/cronologia      — Lista todos los packs por fecha de lanzamiento\n"
        "/ayuda           — Muestra esta lista de comandos\n"
    )
    await interaction.response.send_message(f"```{mensaje}```")

@bot.tree.command(name="infor", description="Muestra el detalle de un pack específico")
@app_commands.describe(codigo="Código del pack (ej. EP01)")
@solo_servidor_permitido()
async def infor(interaction: discord.Interaction, codigo: str):
    codigo = codigo.upper()

    if codigo not in packs:
        await interaction.response.send_message(f"No se encontró ningún pack con el código `{codigo}`.")
        return

    nombre = packs[codigo]

    if codigo.startswith("EP"):
        tipo = "Pack de Expansión"
        precio = "~$39.99 USD"
    elif codigo.startswith("GP"):
        tipo = "Pack de Contenido"
        precio = "~$19.99 USD"
    elif codigo.startswith("SP"):
        tipo = "Pack de Accesorios / Kit"
        precio = "~$9.99 USD" if int(codigo[2:]) <= 18 else "~$4.99 USD"
    elif codigo.startswith("FP"):
        tipo = "Free Pack"
        precio = "Gratis"
    else:
        tipo = "Desconocido"
        precio = "~$4.99 USD"

    fecha = fechas.get(codigo, "No disponible")
    await interaction.response.send_message(f"```Código  : {codigo}\nNombre  : {nombre}\nTipo    : {tipo}\nLanzado : {fecha}\nPrecio  : {precio} (precio aproximado)```")

# ==========================================
# INICIAR BOT Y SERVIDOR WEB
# ==========================================

if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
