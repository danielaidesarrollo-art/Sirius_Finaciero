# Comandos de Despliegue: Daniel AI Stellar Core

Ejecuta estos comandos en tu terminal de PowerShell para aplicar la solución al núcleo `Sirius_Financial`.

### Opción A: Despliegue vía Git (Recomendado para CI/CD)

Este comando activará el disparador automático de Cloud Build que se ve en tu imagen.

```powershell
# Navegar al repositorio
cd "C:\Users\johan\.gemini\antigravity\scratch\Daniel-AI-Cores\Sirius_Financial"

# Agregar cambios (incluye la nueva carpeta 'shared' bundled)
git add .

# Crear el commit de reparación
git commit -m "Fix: Bundle shared dependencies and update Dockerfile for 3rd Gen Architecture"

# Empujar los cambios
git push origin main
```

### Opción B: Despliegue Directo (Fuerza Bruta)

Usa esto si quieres saltarte el trigger y ver el resultado **inmediatamente**.

```powershell
# Construir la imagen en la nube
gcloud builds submit --tag gcr.io/daniel-ai-stellar-2026-483302/daniel-ai-stellar-core . --project daniel-ai-stellar-2026-483302

# Desplegar en Cloud Run
gcloud run deploy daniel-ai-stellar-core `
  --image gcr.io/daniel-ai-stellar-2026-483302/daniel-ai-stellar-core `
  --region us-central1 `
  --project daniel-ai-stellar-2026-483302 `
  --allow-unauthenticated
```
