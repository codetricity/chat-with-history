
# LLM Cache Plan

1. **Goal** – Store and retrieve LLM conversations + documents more flexibly than ChatGPT’s built-in “projects/folders” model, without extra complexity or high cost.
2. **Constraint** – Cheap deployment on Fly.io, minimal moving parts, easy backups, future scalability.
3. **Decision** – Use SQLite as the **single source of truth**, with both:

   * **FTS5 (BM25)** for keyword search
   * **FAISS** for semantic (embedding) search
     → Blend results for **hybrid retrieval**.
4. **Advantages over ChromaDB** – One DB for all data, no extra server, ACID reliability, hybrid search in same place, portable `.db` file, simple ops with Litestream backups.
5. **FAISS vs sqlite-vec** –

   * FAISS: in-memory ANN index in your Python process, very fast, rebuildable from SQLite.
   * sqlite-vec: vector search built into SQLite (alternative if you want SQL-only queries).
6. **Hybrid Search Benefit** – BM25 = precise keywords, FAISS = meaning match; together cover both exact terms and semantic similarity.

---

## **Recommended Stack**

* **Backend:** FastAPI + Jinja2 templates (Fly Engine).
* **Database:** SQLite on a Fly Volume.
* **Embeddings:** Generated with **OpenRouter API** (store as float32 BLOBs in SQLite).
* **Conversations & Documents:**

  * Store as **chunks** in SQLite (`chunks` table)
  * Mirror into **FTS5** table for BM25 keyword search.
* **Semantic Search:** Store embeddings in SQLite; build **FAISS** index in app memory.
* **Retrieval:**

  1. Get top N keyword matches via BM25 (FTS5).
  2. Get top N semantic matches via FAISS cosine similarity.
  3. Blend scores (e.g., `0.35*BM25 + 0.65*cosine`) to produce final Top-K chunks.
* **Backups:** Litestream to S3/Backblaze for database; FAISS index can be rebuilt.

---


<img width="563" height="746" alt="Image" src="https://github.com/user-attachments/assets/633cfe55-1ae5-4bd3-b08a-583a9e855913" />

```mermaid
flowchart LR
  subgraph SQLite["SQLite (Fly Volume)"]
    A["users / tenants"]
    B["conversations"]
    C["messages"]
    D["documents"]
    E["chunks"]
    F["chunk_embeddings (BLOB float32)"]
    G["chunks_fts • FTS5"]
  end

```

```mermaid

flowchart LR
  subgraph FE["FastAPI + Jinja2 Templates / Fly Engine"]
    Q[User query]
    E1[Generate query embedding - OpenRouter]
    KWS[Keyword search - FTS5 BM25]
    SS[Semantic search - FAISS in Python]
    BLEND[Blend scores - BM25 + cosine]
    RES[Top-K chunks]
    LLM[Send to LLM with citations]
    Q --> E1
    Q --> KWS
    E1 --> SS
    KWS --> BLEND
    SS --> BLEND
    BLEND --> RES
    RES --> LLM
  end

  subgraph DB["SQLite on Fly Volume"]
    C1[chunks table - query and response text]
    C2[FTS5 index - BM25 keyword search]
    C3[chunk_embeddings - float32 BLOBs]
  end

  FE <--> DB
  C1 <--> C2
  C1 <--> C3
  C3 -->|load into memory| SS

  subgraph BACKUP["Backup"]
    L[Litestream to S3 or Backblaze]
  end

  DB --> L

```
