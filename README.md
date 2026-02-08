# WhatsBackup - Protege tus Conversaciones de WhatsApp 🔒💼

**WhatsBackup** es la solución SaaS definitiva para negocios que venden por WhatsApp. Sistema de respaldo automático que protege todas tus conversaciones de WhatsApp Business con dos planes adaptados a tus necesidades.

---

## ✨ Propuesta de Valor

**"Aunque WhatsApp se caiga, tus mensajes de venta están seguros"**

### 💼 ¿Para quién?
Negocios que dependen de WhatsApp para ventas y servicio al cliente:
- 🛍️ Tiendas online que venden por WhatsApp
- 🏠 Agentes de bienes raíces
- 📦 Distribuidores y mayoristas
- 🔧 Proveedores de servicios
- 👔 Profesionales independientes

### 🎯 Problema que resuelve
- ❌ "Perdí el historial de pedidos cuando cambié de teléfono"
- ❌ "No encuentro esa conversación de hace 2 meses"
- ❌ "WhatsApp se cayó y no puedo acceder a mis mensajes"
- ❌ "Necesito documentar esta conversación para contabilidad"
- ❌ "Me banearon la cuenta y perdí todo"

---

## 🎯 Sistema de Planes Dual

### 🚀 Plan Express - $18/mes
**Perfecto para emprendedores y pequeños negocios**

- ✅ Conexión por **QR Code** (sin Meta Business API)
- ✅ Hasta **5,000 mensajes** respaldados
- ✅ Backup automático cada **12 horas**
- ✅ Búsqueda de mensajes completa
- ✅ Exportación a PDF
- ✅ Historial ilimitado
- 🔄 Tecnología: **Baileys** (WhatsApp Web)

### ⭐ Plan Pro - $35/mes
**Para negocios establecidos con alto volumen**

- ✅ Integración oficial **WhatsApp Business API**
- ✅ Mensajes **ilimitados**
- ✅ Backup automático cada **24 horas**
- ✅ Búsqueda avanzada
- ✅ Exportación masiva a PDF
- ✅ Soporte prioritario
- 🏢 Tecnología: **Meta Business API**

---

## 🚀 Características Principales

### 📥 Sistema de Backup Automático Inteligente
- **Express**: Respaldo cada 12 horas (ideal para negocios dinámicos)
- **Pro**: Respaldo cada 24 horas (óptimo para alto volumen)
- Schedulers automáticos que funcionan 24/7
- No pierdes mensajes aunque cambies de teléfono
- Tus datos seguros en base de datos PostgreSQL encriptada

### 🔍 Búsqueda Instantánea Avanzada
- Encuentra cualquier conversación en segundos
- Busca por nombre, teléfono, contenido o fecha
- Accede a tu historial aunque WhatsApp esté caído
- Filtros avanzados por contacto y período

### 📄 Exportación Profesional a PDF
- Genera PDFs profesionales de conversaciones
- Útil para:
  - 📋 Documentación legal
  - 💰 Auditorías contables
  - 📦 Registro de pedidos
  - ✍️ Comprobantes de acuerdos
- Marca de agua con timestamp

### 🔐 Continuidad Operativa Garantizada
- Accede a tus mensajes aunque WhatsApp esté offline
- Tu negocio nunca se detiene
- Backup redundante y seguro
- Autenticación JWT robusta

### 📊 Dashboard Completo
- Vista general de tus backups
- Estadísticas de mensajes respaldados
- Historial completo de respaldos
- Gestión de tu plan y suscripción

---

## 🛠️ Stack Tecnológico

### Backend
- **Python 3.12+** - Lenguaje principal
- **FastAPI** - Framework web async de alto rendimiento
- **SQLAlchemy 2.0** - ORM moderno
- **PostgreSQL 13+** - Base de datos robusta
- **Alembic** - Migraciones de base de datos
- **JWT + Bcrypt** - Autenticación segura

### Integraciones WhatsApp
- **WhatsApp Business API** - Integración oficial de Meta (Plan Pro)
- **Baileys** - Librería WhatsApp Web (Plan Express)
- **Node.js Express** - Servidor Baileys independiente

### Frontend
- **React 19** - Framework UI moderno
- **TypeScript 5** - Tipado estático
- **Vite** - Build tool ultrarrápido
- **Tailwind CSS v4** - Estilos utility-first
- **React Router** - Navegación SPA

### DevOps & Tools
- **Docker** - Containerización
- **Git/GitHub** - Control de versiones
- **Uvicorn** - ASGI server
- **npm** - Gestión de paquetes frontend

---

## 🚀 Guía de Instalación Rápida

### Prerrequisitos
- Node.js (v18+)
- Python (3.12+)
- PostgreSQL
- Cuenta de WhatsApp Business con API activada

### 1. Configuración del Backend (FastAPI)

```bash
cd c:\CRM
# Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos PostgreSQL
# Editar .env con tus credenciales

# Ejecutar migraciones
alembic upgrade head

# Iniciar servidor backend
uvicorn app.main:app --reload
```
*El backend correrá en `http://localhost:8000`*

### 2. Configuración del Servidor Baileys (Node.js)

```bash
cd c:\CRM\baileys-server
# Instalar dependencias
npm install

# Iniciar servidor Baileys
npm start
```
*El servidor Baileys correrá en `http://localhost:3000`*

### 3. Configuración del Frontend (React)

```bash
cd c:\CRM\frontend
# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```
*El frontend correrá en `http://localhost:5173`*

### 4. Configurar WhatsApp

#### Para Plan Express (QR Code):
1. Regístrate en la app
2. Selecciona "Plan Express"
3. Escanea el código QR con WhatsApp
4. ¡Listo! Backups cada 12 horas automáticamente

#### Para Plan Pro (Business API):
1. Ve a [Meta Business Manager](https://business.facebook.com)
2. Configura WhatsApp Business API
3. Obtén tu `Phone Number ID` y `Access Token`
4. En la app, selecciona "Plan Pro" y pega tus credenciales
5. ¡Listo! Backups cada 24 horas automáticamente

---

## 📂 Estructura del Proyecto

```
CRM/
├── app/                      # Backend FastAPI
│   ├── api/v1/endpoints/     # API Routes
│   │   ├── auth.py          # Registro/Login
│   │   ├── plans.py         # Gestión de planes
│   │   ├── whatsapp.py      # Pro Plan (Meta API)
│   │   ├── baileys.py       # Express Plan (Baileys)
│   │   ├── backups_wa.py    # Historial de backups
│   │   └── messages_wa.py   # Búsqueda/Exportación
│   ├── models/              # SQLAlchemy Models
│   │   ├── user.py          # Usuario + plan_type
│   │   ├── message.py       # Mensajes respaldados
│   │   ├── backup.py        # Backups + source
│   │   └── subscription.py  # Suscripciones
│   ├── services/            # Lógica de negocio
│   │   ├── plans.py         # Límites y upgrades
│   │   ├── whatsapp_backup.py
│   │   └── backup_service.py
│   ├── integrations/        # WhatsApp APIs
│   │   ├── whatsapp_api.py  # Meta Business API
│   │   └── whatsapp_baileys.py  # Baileys bridge
│   ├── schedulers/          # Backups automáticos
│   │   ├── express_backup.py  # Cada 12h
│   │   └── pro_backup.py      # Cada 24h
│   └── core/                # Config, auth, security
├── baileys-server/          # Servidor Node.js
│   ├── index.js            # Express server
│   ├── package.json        # Dependencies
│   └── sessions/           # WhatsApp sessions
├── frontend/                # React SPA
│   ├── src/
│   │   ├── pages/          # Páginas principales
│   │   │   ├── Login.tsx
│   │   │   ├── Pricing.tsx
│   │   │   ├── ConnectExpress.tsx
│   │   │   ├── ConnectPro.tsx
│   │   │   ├── DashboardHome.tsx
│   │   │   ├── BackupHistory.tsx
│   │   │   └── MessageSearch.tsx
│   │   ├── components/     # Componentes reutilizables
│   │   └── layouts/        # Layouts
│   └── package.json
├── alembic/                # Migraciones DB
├── scripts/                # Scripts utilidad
│   ├── test_models.py
│   └── migrate_to_whatsbackup.py
├── .env                    # Variables entorno
├── requirements.txt        # Python deps
└── README.md              # Este archivo
```

---

## 🔑 Acceso por Defecto

| Rol | Email | Contraseña |
|-----|-------|------------|
| Admin | `admin@whatsbackup.com` | `password123` |

---

## 📊 Flujo de Uso

### Onboarding
1. **Registro** → Usuario crea cuenta (email/contraseña)
2. **Selección de Plan** → Express ($18/mes) o Pro ($35/mes)
3. **Conexión WhatsApp**:
   - **Express**: Escanea QR code (Baileys)
   - **Pro**: Ingresa credenciales de Meta Business API

### Operación Diaria
4. **Backup Automático** → Schedulers trabajan 24/7
   - Express: cada 12 horas
   - Pro: cada 24 horas
5. **Dashboard** → Usuario ve estadísticas y últimos backups
6. **Buscar Mensajes** → Encuentra conversaciones por fecha/contacto/keyword
7. **Exportar PDF** → Descarga documentación legal profesional

### Gestión
8. **Upgrade de Plan** → De Express a Pro cuando sea necesario
9. **Configuración** → Personaliza frecuencia de backups
10. **Historial** → Revisa todos los backups anteriores

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
