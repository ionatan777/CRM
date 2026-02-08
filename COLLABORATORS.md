# 👥 Guía de Colaboradores - WhatsBackup

## 🎯 Cómo Añadir Colaboradores al Proyecto

### Método 1: Desde GitHub Web (Recomendado)

#### Paso 1: Ir a Configuración del Repositorio
1. Ve a tu repositorio: https://github.com/ionatan777/CRM
2. Haz clic en **"Settings"** (Configuración) - última pestaña arriba
3. En el menú lateral izquierdo, haz clic en **"Collaborators"** (Colaboradores)

#### Paso 2: Añadir Colaborador
4. Haz clic en el botón verde **"Add people"** (Añadir personas)
5. Escribe el **nombre de usuario de GitHub** o **email** del colaborador
6. Selecciona el usuario correcto de la lista
7. Haz clic en **"Add [usuario] to this repository"**

#### Paso 3: Confirmar Invitación
8. GitHub enviará un email de invitación al colaborador
9. El colaborador debe aceptar la invitación desde:
   - El email recibido, o
   - https://github.com/ionatan777/CRM (verá un banner de invitación)

#### Paso 4: Nivel de Acceso
Por defecto, los colaboradores tienen **Write access** (pueden hacer push). Puedes cambiar esto:
- **Read**: Solo lectura, no pueden hacer cambios
- **Write**: Pueden hacer push y pull requests
- **Admin**: Control total del repositorio

---

### Método 2: Desde Git Config (Avanzado)

Si tienes un equipo grande, puedes usar **GitHub Organizations** o **Teams**:

1. Crea una organización en GitHub
2. Transfiere el repositorio a la organización
3. Crea equipos con diferentes niveles de acceso
4. Añade miembros a los equipos

---

## 👨‍💻 Roles Sugeridos para WhatsBackup

### 🔴 Admin (Tú)
- Control total del repositorio
- Puede modificar settings, añadir colaboradores
- Acepta pull requests finales

### 🟡 Full Developer (Desarrolladores de confianza)
- Puede hacer push directo a `main`
- Puede revisar y aprobar PRs
- Acceso a todas las ramas

### 🟢 Contributor (Colaboradores externos)
- Puede hacer fork del proyecto
- Envía pull requests
- No puede hacer push directo

---

## 📋 Checklist para Nuevos Colaboradores

Cuando añadas a alguien, compárteles esto:

- [ ] Aceptar invitación de GitHub
- [ ] Clonar el repositorio: `git clone https://github.com/ionatan777/CRM.git`
- [ ] Leer el `README.md` completo
- [ ] Configurar entorno local (ver `QUICKSTART.md`)
- [ ] Crear rama nueva: `git checkout -b feature/nombre-feature`
- [ ] Hacer cambios y commit
- [ ] Push a su rama: `git push origin feature/nombre-feature`
- [ ] Crear Pull Request en GitHub
- [ ] Esperar revisión antes de merge

---

## 🔄 Workflow Colaborativo Recomendado

### Branching Strategy

```
main                    # Producción (protegida)
  ├── develop          # Desarrollo activo
  │   ├── feature/oauth         # Nueva funcionalidad
  │   ├── feature/stripe        # Sistema de pagos
  │   └── bugfix/login-error    # Corrección de bugs
```

### Proceso de Contribución

1. **Crear rama desde `develop`**:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/nombre-descriptivo
   ```

2. **Hacer cambios y commits**:
   ```bash
   git add .
   git commit -m "feat: descripción clara del cambio"
   ```

3. **Push a GitHub**:
   ```bash
   git push origin feature/nombre-descriptivo
   ```

4. **Crear Pull Request**:
   - Ir a GitHub
   - Click en "Compare & pull request"
   - Base: `develop` ← Compare: `feature/nombre-descriptivo`
   - Describir los cambios
   - Asignar reviewer (tú)

5. **Code Review**:
   - Tú revisas el código
   - Solicitas cambios si es necesario
   - Apruebas cuando esté listo

6. **Merge**:
   - Hacer merge a `develop`
   - Cuando `develop` esté estable → merge a `main`

---

## 🛡️ Proteger la Rama Main

**IMPORTANTE**: Deberías proteger `main` para evitar pushes directos:

1. Ve a **Settings** → **Branches**
2. Click en **"Add rule"**
3. Branch name pattern: `main`
4. Activa:
   - ✅ Require a pull request before merging
   - ✅ Require approvals (1 aprobación mínimo)
   - ✅ Require status checks to pass
5. Click **"Create"**

Ahora nadie (ni tú) puede hacer push directo a `main`. Todo debe pasar por Pull Request.

---

## 📝 Convenciones de Commits

Usa **Conventional Commits** para mantener historial limpio:

```bash
feat: añadir Google OAuth login
fix: corregir error en backup automático
docs: actualizar README con nuevas instrucciones
style: formatear código con prettier
refactor: reorganizar estructura de carpetas
test: añadir tests para plan service
chore: actualizar dependencias
```

---

## 🤝 Quiénes Deberían Ser Colaboradores

### ✅ Añade como colaborador:
- Desarrolladores que trabajarán contigo regularmente
- Diseñadores que necesiten acceso al código del frontend
- DevOps que manejarán deployment

### ❌ NO añadas como colaborador:
- Usuarios que solo reportan bugs (usa GitHub Issues)
- Desarrolladores externos ocasionales (usa PRs de forks)
- Personas que solo necesitan ver el código (hazlo público o comparte link)

---

## 🔗 Enlaces Útiles

- **Repositorio**: https://github.com/ionatan777/CRM
- **Issues**: https://github.com/ionatan777/CRM/issues
- **Pull Requests**: https://github.com/ionatan777/CRM/pulls
- **Configuración**: https://github.com/ionatan777/CRM/settings/access

---

## 📧 Invitar por Email

Si el colaborador no tiene cuenta de GitHub:

1. En **Collaborators**, ingresa su email
2. GitHub enviará invitación para crear cuenta
3. Una vez creada, tendrá acceso automático

---

## ⚠️ Seguridad

**NUNCA COMPARTAS**:
- ❌ Archivo `.env` (credenciales)
- ❌ Tokens de API (WhatsApp, Stripe)
- ❌ Contraseñas de base de datos
- ❌ Secret keys de JWT

**ASEGÚRATE**:
- ✅ `.env` está en `.gitignore`
- ✅ Los colaboradores crean su propio `.env` local
- ✅ Las credenciales de producción las manejas solo tú

---

**¿Listo para colaborar?** 🚀
