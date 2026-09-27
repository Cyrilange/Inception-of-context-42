_this project has been made by csalamit_

#### ARTHITECTURE


                    INCEPTION-OF-CONTEXT
                             │
             ┌───────────────┴───────────────┐
             │                               │
             ▼                               ▼
       ┌───────────┐                   ┌───────────┐
       │    IoC    │                   │  Ollama   │
       │  Python   │◄──── HTTP ──────►│           │
       │ FastAPI   │                   │ qwen2.5   │
       │ ChromaDB  │                   │ qwen2.5-  │
       │ Watcher   │                   │ coder     │
       └───────────┘                   └───────────┘
             │
             ▼
        demo project

#### 

### Part 1 — Indexing & Synchronization

The goal of Part 1 is to build a local, structured representation of the target codebase that can be queried by the AI system.

It covers:

* Discovering and filtering source files.
* Splitting code into logical chunks.
* Generating local embeddings.
* Storing chunks, embeddings, and metadata in ChromaDB.
* Keeping the index synchronized with file creations, modifications, and deletions.

This indexed codebase will serve as the foundation for the RAG system in Part 2 and the code generation loop in Part 3.
