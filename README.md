# 🎮 Guía DLCs — Bot de Discord para The Sims 4

Bot de Discord para consultar información sobre los packs, expansiones y kits de **The Sims 4**.

---

## 📋 Comandos disponibles

| Comando | Descripción |
|---|---|
| `!dlc <búsqueda>` | Busca packs por nombre o código |
| `!list` | Muestra todos los packs organizados por categoría |
| `!expansiones` | Muestra solo los Packs de Expansión (EP) |
| `!contenido` | Muestra solo los Packs de Contenido (GP) |
| `!kits` | Muestra solo los Kits y Packs de Accesorios (SP) |
| `!gratuitos` | Muestra solo los Kits Gratuitos (FP) |
| `!infor <código>` | Muestra el detalle completo de un pack |
| `!cronologia` | Lista todos los packs ordenados por fecha de lanzamiento |
| `!ayuda` | Muestra la lista de comandos disponibles |

### Ejemplo de `!infor`
```
Código  : EP01
Nombre  : ¡A Trabajar!
Tipo    : Pack de Expansión
Lanzado : 31/03/2015
Precio  : ~$39.99 USD (precio aproximado)
```

---

## 📁 Estructura del proyecto

```
├── bot.py          # Código principal del bot
├── packs.json      # Base de datos de packs (código → nombre)
├── fechas.json     # Fechas de lanzamiento por código
└── README.md       # Este archivo
```

---

## ⚙️ Configuración

El bot requiere una variable de entorno con el token de Discord:

```
TOKEN=tu_token_aqui
```

---

## 🚀 Iniciar el bot

```bash
python bot.py
```

---

## 🔒 Restricciones

El bot está configurado para funcionar **únicamente** en los servidores autorizados. Cualquier servidor no autorizado será ignorado automáticamente.

---

## 💰 Precios aproximados por categoría

| Categoría | Precio |
|---|---|
| Pack de Expansión (EP) | ~$39.99 USD |
| Pack de Contenido (GP) | ~$19.99 USD |
| Pack de Accesorios (SP01–SP18) | ~$9.99 USD |
| Kit (SP20+) | ~$4.99 USD |
| Kit Gratuito (FP) | Gratis |

> Los precios son aproximados y pueden variar según región u ofertas activas.
