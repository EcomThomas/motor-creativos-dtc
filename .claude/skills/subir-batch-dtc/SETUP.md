# SETUP — Subir batches desde tu Claude (una sola vez)

Esto te deja listo para usar la skill `subir-batch-dtc` en TU tienda. Todos trabajan
en el mismo workspace de ClickUp, pero cada quien monta en **su propia lista** con
**sus propios tokens**. Tus secretos y datos de cliente **nunca** se suben al repo.

## 1. Requisitos
- **Acceso al repo** `motor-creativos-dtc` (pídeselo al dueño en GitHub) y clónalo.
- **Python 3.10+** instalado (`python --version`).
- **Claude Code** abierto en la carpeta del repo.

## 2. Tus tokens → `.env`
En la raíz del repo:
```bash
cp .env.example .env
```
Edita `.env` y pon tu **CLICKUP_TOKEN**:
- ClickUp → clic en tu avatar → **Settings → Apps → API Token → Generate**.
- Es personal, empieza con `pk_`. Pégalo en la línea `CLICKUP_TOKEN=`.
- (Opcionales: `TRENDTRACK_TOKEN`, `FB_TOKEN`, `TWELVELABS_API_KEY` solo si los usas.)

> `.env` está gitignored: no se sube. Si prefieres tener los tokens en otra ruta,
> define la variable de entorno `MOTOR_SECRETS` apuntando a ese archivo.

## 3. Tu tienda → `config.local.json`
```bash
cp config.local.example.json config.local.json
```
Edita `config.local.json`:
- **`clickup_list_id`** — abre TU lista del flujo creativo en ClickUp; en la URL
  `.../v/li/<NUMERO>`, ese `<NUMERO>` es el id.
- **`clickup_status`** — normalmente `idea` (el estado inicial de los batches).
- **`drive_parent_folder_id`** — tu carpeta madre de briefs en Drive; de la URL
  `drive.google.com/drive/folders/<ID>`, ese `<ID>`.
- **`producto`** — nombre de tu producto (define la carpeta `casos/<slug>/`).
- **`spine_path`** — ruta al Spine de tu producto (ver paso 5).

> `config.local.json` está gitignored: es solo tuyo.

## 4. Conecta Google Drive en tu Claude
Para que la skill cree los Google Docs de los briefs, conecta el **conector de
Google Drive** en tu Claude (Settings → Connectors). Si no lo conectas, la skill
igual genera los briefs como archivos `.md` locales y tú los subes a mano.

## 5. Tu Spine (contexto de producto)
La skill necesita el **Spine**: mecanismo, villano, avatar, oferta y **léxico
prohibido / compliance** de tu producto. Es lo que evita que los creativos alucinen
o rompan compliance.
- Si ya lo tienes, guárdalo en la ruta que pusiste en `spine_path`
  (ej. `casos/<tu-producto>/input/spine.snapshot.json`). Plantilla en
  `plantillas/INPUT — Spine (plantilla).md`.
- Si no, pídele a tu Claude que lo arme desde tu research (o usa la skill
  `product-context` / `emotional-valence-research`) antes de generar batches.

## 6. Verifica
```bash
python -c "from scripts.motor_config import store, secrets_path, get_token; print('secretos:', secrets_path()); print('tienda:', store()); print('clickup token ok:', bool(get_token('CLICKUP_TOKEN')))"
```
Debe imprimir la ruta de TU archivo de secretos, tus datos de tienda y `True`. (No imprime
el token.) **Fíjate en la ruta de `secretos:`**: debe ser tu `.env` (o tu `MOTOR_SECRETS`).
Si apunta a otro archivo, tu `.env` no se está resolviendo — revisa el paso 2.

Prueba en seco con el bundle de ejemplo versionado (no crea nada en ClickUp):
```bash
python scripts/clickup_upload.py --bundle plantillas/bundle.example.json --start-num 1 --dry-run
```

## 7. Úsala
En tu Claude, pídele por ejemplo:
> *"Sube este batch a ClickUp"* · *"Monta un batch iterando este ganador"* ·
> *"Convierte estos 3 scripts ganadores en batches"*.

La skill `subir-batch-dtc` se encarga del resto: bundle → briefs (storyboard + prompt
por escena) → ClickUp `idea` → Drive → links enlazados.
