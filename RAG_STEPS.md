# RAG with Pinecone — build steps

Scope: your content only (CV + projects), no multi-tenant namespaces yet (that comes later, for the SaaS project).

---

## Step 1 — Pinecone account + API key ✅ done

**Qué hacemos:** creamos la cuenta y conseguimos la key para poder usar el servicio.

1. Andá a https://www.pinecone.io/ → crear cuenta gratis.
2. Creá un proyecto (o usá el default).
3. Copiá el **API key** desde el dashboard.
4. Agregalo a `.env`: `PINECONE_API_KEY=...`

---

## Step 2 — Install dependency ✅ done

```bash
uv add pinecone
```

---

## Step 3 — Add setting to config ✅ done

**Qué hacemos:** igual que hicimos con `anthropic_api_key`, sumamos el de Pinecone a `Settings`.

In `app/config.py`:
```python
pinecone_api_key: str
pinecone_index_name: str = "personal-site-content"
```

---

## Step 4 — Prepare your content ✅ done

**Qué hacemos:** escribir tu CV/proyectos como texto plano, en pedazos ("chunks") — cada chunk es un párrafo con una idea completa (ej. un proyecto = un chunk, tu experiencia = otro chunk). Esto va a ser lo que se busca después.

Sugerido: un archivo `content/knowledge.py` o `.md` con una lista de strings, uno por chunk. Lo armamos juntos cuando llegues acá.

---

## Step 5 — Create the Pinecone index + ingestion script ✅ done

**Qué hacemos:** un script que toma tus chunks, los convierte en embeddings (vectores numéricos) con OpenAI, y los sube a un índice de Pinecone. Se corre una sola vez (o cada vez que actualices contenido), no en cada request.

---

## Step 6 — Add a retrieval step to the graph ✅ done

**Qué hacemos:** antes de que cada especialista responda, buscamos en Pinecone los chunks más parecidos a la pregunta, y se los pasamos al LLM como contexto adicional — en vez de contenido fijo en el prompt.

---

## Step 7 — Test ⬜ pending

Probar que las respuestas usen el contenido recuperado, no el hardcodeado (vamos a sacar el hardcodeado en este paso).
