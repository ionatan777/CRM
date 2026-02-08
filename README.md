# WhatsBackup - Protege tus Conversaciones de WhatsApp 🔒

**WhatsBackup** es la póliza de seguro para negocios que venden por WhatsApp. Respalda automáticamente todas tus conversaciones de WhatsApp Business, asegurando que tus mensajes de venta estén seguros aunque la app se caiga.

---

## ✨ Propuesta de Valor

**"Aunque WhatsApp se caiga, tus mensajes de venta están seguros"**

### 💼 ¿Para quién?
Negocios que dependen de WhatsApp para ventas y servicio al cliente:
- Tiendas online que venden por WhatsApp
- Agentes de bienes raíces
- Distribuidores y mayoristas
- Proveedores de servicios

### 🎯 Problema que resuelve
- ❌ "Perdí el historial de pedidos cuando cambié de teléfono"
- ❌ "No encuentro esa conversación de hace 2 meses"
- ❌ "WhatsApp se cayó y no puedo acceder a mis mensajes"
- ❌ "Necesito documentar esta conversación para contabilidad"

---

## 🚀 Características Principales

### 📥 Backup Automático Diario
- Respaldo completo de TODAS tus conversaciones cada 24 horas
- No pierdes mensajes aunque cambies de teléfono
- Tus datos están seguros en tu propia base de datos

### 🔍 Búsqueda Instantánea
- Encuentra cualquier conversación de hace meses en segundos
- Busca por nombre, teléfono o contenido del mensaje
- Accede a tu historial aunque WhatsApp esté caído

### 📄 Exportación a PDF
- Exporta conversaciones completas para:
  - Documentación legal
  - Auditorías contables
  - Registro de pedidos
  - Comprobantes de acuerdos

### 🔐 Operación Continua
- Accede a tus mensajes aunque WhatsApp esté fuera de línea
- Continuidad operativa garantizada
- Tus ventas nunca se detienen

---

## 🛠️ Stack Tecnológico

### Backend
- **Python 3.12+** - Lenguaje principal
- **FastAPI** - Framework web async
- **SQLAlchemy** - ORM
- **PostgreSQL** - Base de datos
- **WhatsApp Business API** - Integración oficial de Meta

### Frontend
- **React 19** - Framework UI
- **TypeScript** - Tipado estático
- **Vite** - Build tool
- **Tailwind CSS v4** - Estilos modernos

---

## 🚀 Guía de Instalación Rápida

### Prerrequisitos
- Node.js (v18+)
- Python (3.12+)
- PostgreSQL
- Cuenta de WhatsApp Business con API activada

### 1. Configuración del Backend

```bash
cd c:\CRM
# Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Agregar reportlab para PDF export
pip install reportlab

# Iniciar servidor
uvicorn app.main:app --reload
```
*El backend correrá en `http://localhost:8000`*

### 2. Configuración del Frontend

```bash
cd c:\CRM\frontend
# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```
*El frontend correrá en `http://localhost:5174`*

### 3. Conectar WhatsApp Business

1. Ve a [Meta Business Manager](https://business.facebook.com)
2. Configura WhatsApp Business API
3. Obtén tu `Phone Number ID` y `Access Token`
4. En la app, ve a "Conectar WhatsApp" y pega tus credenciales
5. ¡Listo! Tu primer backup se creará automáticamente

---

## 📂 Estructura del Proyecto

```
/
├── app/              # Backend (FastAPI)
│   ├── api/          # Endpoints WhatsBackup
│   ├── models/       # User, Message, Backup
│   └── services/     # whatsapp_backup.py (core)
├── frontend/         # Cliente Web (React)
│   ├── src/
│   │   └── pages/    
│   │       ├── ConnectWhatsApp.tsx
│   │       ├── BackupHistory.tsx
│   │       └── MessageSearch.tsx
└── scripts/          # Utilidades
```

---

## 🔑 Acceso por Defecto

| Rol | Email | Contraseña |
|-----|-------|------------|
| Admin | `admin@whatsbackup.com` | `password123` |

---

## 📊 Flujo de Uso

1. **Conectar WhatsApp** → Usuario ingresa credenciales de Meta Business
2. **Backup Automático** → Sistema respalda mensajes cada 24 horas
3. **Buscar Mensajes** → Usuario encuentra conversaciones antiguas
4. **Exportar PDF** → Usuario descarga documentación legal

---

## 💡 Casos de Uso Reales

### 📱 Tienda Online
*"Perdí todos mis pedidos cuando formatée el teléfono"*
→ **WhatsBackup** te permite recuperar todo el historial de ventas

### 🏠 Agente Inmobiliario
*"Necesito probar que el cliente aceptó las condiciones"*
→ **WhatsBackup** exporta la conversación completa a PDF legal

### 📦 Distribuidor
*"No recuerdo cuántas cajas pidió hace 2 meses"*
→ **WhatsBackup** busca "cajas" y encuentra la conversación al instante

---

## 🔐 Seguridad

- ✅ Tus mensajes se almacenan en TU base de datos (no en servidores de terceros)
- ✅ Autenticación JWT robusta
- ✅ Conexión segura con WhatsApp Business API oficial
- ✅ Exportaciones PDF con marca de agua y timestamp

---

*Desarrollado para proteger tu negocio. Porque tus conversaciones son tu activo más valioso.*
