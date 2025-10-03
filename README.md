# 🔒 Document Verification System (Blockchain-based Python Application)


## 📄 1. Project Overview

The Document Verification System is a beginner-friendly, console-based Python application that uses a simple blockchain to verify documents. When a user provides a file path, the app computes its SHA-256 hash and stores it as a block on the chain. Users can later verify if a document has been seen before by comparing its hash against the blockchain. The chain persists to a local JSON file for reuse across sessions.

---

## 🎯 2. Objectives

- Provide a minimal, educational blockchain for document verification
- Compute and store document hashes securely (SHA-256)
- Verify whether a file was previously added to the chain
- Persist the blockchain to JSON for durability between runs
- Offer optional file extension restrictions via a simple menu
- Validate blockchain integrity (links and hashes) on demand

---

## 🧱 3. System Architecture

### 🔹 Components

| Component | Description |
|-----------|-------------|
| `Block` | Dataclass with `index`, `timestamp`, `data` (document hash), `previous_hash`, `hash` |
| `Blockchain` | Manages the chain: create genesis block, add blocks, validate integrity, save/load JSON |
| File Hashing | Streams file bytes to compute file SHA-256 efficiently |
| CLI Menu | Console-driven flows to add/verify documents, print/validate chain, configure extensions |
| Persistence | Read/write `blockchain.json` with a simple list of blocks |

---

## 🧪 4. Functional Modules

| Module | Responsibilities |
|--------|-------------------|
| Add Document | Hash a file and append the hash as a new block (if not already present) |
| Verify Document | Check whether a file’s hash exists anywhere in the chain |
| Print Blockchain | Display readable details: index, timestamp, hashes |
| Validate Integrity | Ensure each block’s `previous_hash` links correctly and hashes match recomputation |
| Configure Extensions | Optionally allow only specific file extensions (e.g., `.pdf,.docx,.png`) |
| Persistence | Auto-save after mutations and on exit; manual save option |

---

## 🗂️ 5. Data Format

**Storage File:** `blockchain.json`

Each block is stored as a JSON object:

```json
[
  {
    "index": 0,
    "timestamp": "2025-09-15Z",
    "data": "GENESIS",
    "previous_hash": "0000000000000000000000000000000000000000000000000000000000000000",
    "hash": "<sha256>"
  },
  {
    "index": 1,
    "timestamp": "2025-09-15Z",
    "data": "<document_sha256>",
    "previous_hash": "<sha256_of_genesis>",
    "hash": "<sha256>"
  }
]
```

---

## 🖥️ 6. Sample Output (Console Snapshot)

```
============================================================
Document Verification System (Blockchain)
============================================================
1) Add document
2) Verify document
3) Print blockchain
4) Validate blockchain integrity
5) Configure allowed extensions
6) Save blockchain now
7) Exit
[All file extensions are allowed]
Tip: Use option 5 to restrict uploads (e.g., .pdf,.docx,.png).

Choose an option (1-7):
```

Examples of confirmations and errors:

```
Document added successfully.
Document already verified.
Document not found in the blockchain.
File not found. Please check the path and try again.
```

---

## 🚀 7. How to Run

### Prerequisites
- Python 3.9+ (works on Windows/macOS/Linux)

### Setup (optional virtual environment)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### Run the App
```bash
python app.py
```

### Tip
- Restrict uploads by choosing option 5 and entering extensions like: `.pdf,.docx,.png` (leave empty to allow all).

---

## 🧾 8. Example Workflow

1) Choose “Add document” and provide a file path (e.g., `sample.txt`).  
2) The app computes SHA-256 and adds a block if not already present.  
3) Choose “Verify document” later to confirm if the same file exists in the chain.  
4) Use “Validate blockchain integrity” to check chain links and hashes.  
5) Use “Save blockchain now” to persist immediately (auto-save also occurs on add and exit).

---

## 🧪 9. Chain Integrity Rules

- Genesis block uses `previous_hash` of 64 zeros and index `0`.
- Each subsequent block must point to the exact `hash` of the previous block.
- A block’s `hash` must equal the SHA-256 of its content (`index`, `timestamp`, `data`, `previous_hash`).

---

## 🤝 10. Contributing

Pull requests are welcome! Feel free to fork the repository and submit improvements.

**Contributions are welcome! Follow these steps:**
1. Fork the project.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature description"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## 📧 11. Contact

For queries or suggestions:
- 📧 Email: spreveen123@gmail.com
- 🌐 LinkedIn: www.linkedin.com/in/preveen-s-17250529b/

---

## 🌟 12. Show your support

If you find this project helpful or interesting, please consider giving it a ⭐ on GitHub!

---

