# Credenciales de Prueba - WhatsBackup

## Opción 1: Usuario de Prueba (Recomendado)

Puedes crear un usuario usando la API de registro:

### Usando PowerShell:
```powershell
$body = @{
    email = "test@whatsbackup.com"
    password = "test123"
    full_name = "Usuario Test"
    phone_number = "+573001234567"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/v1/auth/register" -Method POST -Body $body -ContentType "application/json"
```

### Usando el navegador (Swagger UI):
1. Ir a: http://localhost:8000/docs
2. Buscar el endpoint `POST /api/v1/auth/register`
3. Click en "Try it out"
4. Llenar los datos:
```json
{
  "email": "test@whatsbackup.com",
  "password": "test123",  
  "full_name": "Usuario Test",
  "company_name": "Mi Empresa"
}
```
5. Click en "Execute"

## Opción 2: Crear directamente en Python

Ejecutar desde el directorio del proyecto:
```bash
python -c "from app.db.session import SessionLocal; from app.models.user import User; from app.core.security import get_password_hash; db = SessionLocal(); u = User(email='test@whatsbackup.com', hashed_password=get_password_hash('test123'), full_name='Usuario Test', plan_type='express'); db.add(u); db.commit(); print('Usuario creado!')"
```

## Credenciales Sugeridas

Una vez creado, usa:
- **Email**: test@whatsbackup.com  
- **Password**: test123

## Acceder a la aplicación

1. Ir a: http://localhost:5173
2. Ingresar con las credenciales de arriba
3. Seleccionar un plan (Express o Pro)
4. ¡Comenzar a usar WhatsBackup!
