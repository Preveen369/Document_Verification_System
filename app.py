import hashlib
import json
import os
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional, Set


# -------------------------------
# Beginner-friendly Blockchain
# -------------------------------


@dataclass
class Block:
    """Represents a single block in the blockchain.

    Fields:
        index: The position of the block in the chain (0-based).
        timestamp: When the block was created (ISO string for readability).
        data: The data stored in the block. Here we store the document hash (SHA-256).
        previous_hash: The hash of the previous block in the chain.
        hash: The SHA-256 hash of this block (computed from the block content).
    """

    index: int
    timestamp: str
    data: str
    previous_hash: str
    hash: str


class Blockchain:
    """A very simple blockchain implementation for document verification."""

    def __init__(self) -> None:
        self.chain: List[Block] = []
        self._create_genesis_block()

    def _create_genesis_block(self) -> None:
        """Creates the first block (genesis block) with default values."""
        genesis_block = Block(
            index=0,
            timestamp=self._current_timestamp(),
            data="GENESIS",
            previous_hash="0" * 64,
            hash="",  # will be computed next
        )
        genesis_block.hash = self._compute_hash(genesis_block)
        self.chain.append(genesis_block)

    def _current_timestamp(self) -> str:
        """Returns current time as an ISO 8601 string for readability."""
        return datetime.utcnow().isoformat(timespec="seconds") + "Z"

    def _compute_hash(self, block: Block) -> str:
        """Computes SHA-256 hash of a block's content.

        The hash is based on: index, timestamp, data, previous_hash.
        We avoid including the current hash field to prevent recursion.
        """
        block_string = json.dumps(
            {
                "index": block.index,
                "timestamp": block.timestamp,
                "data": block.data,
                "previous_hash": block.previous_hash,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(block_string.encode("utf-8")).hexdigest()

    def get_last_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, data: str) -> Block:
        """Adds a new block to the chain with the given data (document hash)."""
        last_block = self.get_last_block()
        new_block = Block(
            index=last_block.index + 1,
            timestamp=self._current_timestamp(),
            data=data,
            previous_hash=last_block.hash,
            hash="",  # computed below
        )
        new_block.hash = self._compute_hash(new_block)
        self.chain.append(new_block)
        return new_block

    def is_document_in_chain(self, document_hash: str) -> bool:
        """Checks if a given document hash exists in any block's data field."""
        return any(block.data == document_hash for block in self.chain)

    def print_chain(self) -> None:
        """Prints the blockchain in a readable format.

        Displays: index, timestamp, and block hash. Also shows the document hash
        for clarity so users can see what was stored.
        """
        print("\n=== Blockchain ===")
        print(f"Blocks: {len(self.chain)}")
        if self.chain:
            last = self.get_last_block()
            print(f"Last Index: {last.index} | Last Hash: {last.hash}")
        for block in self.chain:
            print(f"Index: {block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Block Hash: {block.hash}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Document Hash (data): {block.data}")
            print("-" * 40)

    # -------------------------------
    # Persistence and validation
    # -------------------------------

    def to_dict(self) -> List[dict]:
        """Serializes the chain to a list of dictionaries."""
        return [asdict(block) for block in self.chain]

    @classmethod
    def from_dict(cls, data: List[dict]) -> "Blockchain":
        """Creates a Blockchain instance from a list of block dictionaries.

        If the provided data is invalid, a fresh chain with a new genesis block is returned.
        """
        bc = cls()
        # Replace genesis with loaded data if valid
        bc.chain = []
        try:
            for item in data:
                block = Block(
                    index=int(item["index"]),
                    timestamp=str(item["timestamp"]),
                    data=str(item["data"]),
                    previous_hash=str(item["previous_hash"]),
                    hash=str(item["hash"]),
                )
                bc.chain.append(block)
            if not bc.is_valid():
                # fallback to fresh chain
                bc = cls()
        except Exception:
            bc = cls()
        return bc

    def save_to_file(self, file_path: str) -> None:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load_from_file(cls, file_path: str) -> "Blockchain":
        if not os.path.isfile(file_path):
            return cls()
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                return cls()
            return cls.from_dict(data)
        except (json.JSONDecodeError, OSError):
            return cls()

    def is_valid(self) -> bool:
        """Validates the entire chain integrity.

        Checks:
        - The genesis block looks reasonable
        - Each block's previous_hash matches prior block's hash
        - Each block's hash matches recomputed hash
        """
        if not self.chain:
            return False
        # Basic genesis check
        genesis = self.chain[0]
        expected_genesis_prev = "0" * 64
        if genesis.index != 0 or genesis.previous_hash != expected_genesis_prev:
            return False
        if self._compute_hash(genesis) != genesis.hash:
            return False
        # Check links and hashes
        for i in range(1, len(self.chain)):
            prev = self.chain[i - 1]
            curr = self.chain[i]
            if curr.previous_hash != prev.hash:
                return False
            if self._compute_hash(curr) != curr.hash:
                return False
        return True


# -------------------------------
# File hashing utilities
# -------------------------------


def compute_file_sha256(file_path: str) -> str:
    """Computes the SHA-256 hash of a file in a memory-efficient way.

    Reads the file in chunks to support large files.
    """
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


# -------------------------------
# Simple CLI
# -------------------------------


def clear_console() -> None:
    """Clears the console screen in a cross-platform way (best effort)."""
    command = "cls" if os.name == "nt" else "clear"
    os.system(command)


def prompt_file_path() -> str:
    """Prompts user for a file path and returns it after basic trimming."""
    return input("Enter file path (e.g., sample.txt): ").strip().strip('"')


DEFAULT_CHAIN_PATH = "blockchain.json"


def is_allowed_extension(file_path: str, allowed_extensions: Optional[Set[str]]) -> bool:
    """Checks whether a file has an allowed extension.

    If allowed_extensions is None or empty, all extensions are allowed.
    Extensions should be provided including the dot, e.g., {".pdf", ".docx"}.
    """
    if not allowed_extensions:
        return True
    _, ext = os.path.splitext(file_path)
    return ext.lower() in allowed_extensions


def main() -> None:
    """Runs a simple interactive menu for document verification."""
    blockchain = Blockchain.load_from_file(DEFAULT_CHAIN_PATH)
    allowed_extensions: Optional[Set[str]] = None  # None/empty means allow all

    while True:
        print("\n" + "=" * 60)
        print("Document Verification System (Blockchain)")
        print("=" * 60)
        print("1) Add document")
        print("2) Verify document")
        print("3) Print blockchain")
        print("4) Validate blockchain integrity")
        print("5) Configure allowed extensions")
        print("6) Save blockchain now")
        print("7) Exit")
        if allowed_extensions:
            print(f"[Allowed extensions active: {', '.join(sorted(allowed_extensions))}]")
        else:
            print("[All file extensions are allowed]")
        print("Tip: Use option 5 to restrict uploads (e.g., .pdf,.docx,.png).\n")
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            file_path = prompt_file_path()
            if not file_path:
                print("\nPlease provide a valid file path.\n")
                continue
            try:
                if not os.path.isfile(file_path):
                    print("\nFile not found. Please check the path and try again.\n")
                    continue
                if not is_allowed_extension(file_path, allowed_extensions):
                    if allowed_extensions:
                        print(
                            "\nFile extension not allowed. Allowed: "
                            + ", ".join(sorted(allowed_extensions))
                            + "\n"
                        )
                    else:
                        print("\nFile extension not allowed.\n")
                    continue
                doc_hash = compute_file_sha256(file_path)
                if blockchain.is_document_in_chain(doc_hash):
                    print("\nDocument already verified.\n")
                else:
                    blockchain.add_block(doc_hash)
                    print("\nDocument added successfully.\n")
                    # Auto-save after mutation
                    try:
                        blockchain.save_to_file(DEFAULT_CHAIN_PATH)
                    except OSError as exc:
                        print(f"\nWarning: Failed to save chain: {exc}\n")
            except FileNotFoundError:
                print("\nFile not found. Please check the path and try again.\n")
            except PermissionError:
                print("\nPermission denied when reading the file.\n")
            except OSError as exc:
                print(f"\nAn OS error occurred: {exc}\n")

        elif choice == "2":
            file_path = prompt_file_path()
            if not file_path:
                print("\nPlease provide a valid file path.\n")
                continue
            try:
                if not os.path.isfile(file_path):
                    print("\nFile not found. Please check the path and try again.\n")
                    continue
                if not is_allowed_extension(file_path, allowed_extensions):
                    if allowed_extensions:
                        print(
                            "\nFile extension not allowed. Allowed: "
                            + ", ".join(sorted(allowed_extensions))
                            + "\n"
                        )
                    else:
                        print("\nFile extension not allowed.\n")
                    continue
                doc_hash = compute_file_sha256(file_path)
                if blockchain.is_document_in_chain(doc_hash):
                    print("\nDocument already verified.\n")
                else:
                    print("\nDocument not found in the blockchain.\n")
            except FileNotFoundError:
                print("\nFile not found. Please check the path and try again.\n")
            except PermissionError:
                print("\nPermission denied when reading the file.\n")
            except OSError as exc:
                print(f"\nAn OS error occurred: {exc}\n")

        elif choice == "3":
            blockchain.print_chain()

        elif choice == "4":
            if blockchain.is_valid():
                print("\nBlockchain is valid.\n")
            else:
                print("\nBlockchain is INVALID.\n")

        elif choice == "5":
            print(
                "\nEnter a comma-separated list of allowed extensions (e.g., .pdf,.docx,.png).\n"
                "Leave empty to allow all extensions.\n"
            )
            exts = input("Extensions: ").strip()
            if not exts:
                allowed_extensions = None
                print("\nAll extensions are now allowed.\n")
            else:
                # Normalize and filter
                parsed = set()
                for part in exts.split(","):
                    part = part.strip().lower()
                    if not part:
                        continue
                    if not part.startswith("."):
                        part = "." + part
                    parsed.add(part)
                allowed_extensions = parsed or None
                if allowed_extensions:
                    print(
                        "\nAllowed extensions set to: "
                        + ", ".join(sorted(allowed_extensions))
                        + "\n"
                    )
                else:
                    print("\nAll extensions are now allowed.\n")

        elif choice == "6":
            try:
                blockchain.save_to_file(DEFAULT_CHAIN_PATH)
                print(f"\nBlockchain saved to {DEFAULT_CHAIN_PATH}.\n")
            except OSError as exc:
                print(f"\nFailed to save: {exc}\n")

        elif choice == "7":
            # Auto-save on exit
            try:
                blockchain.save_to_file(DEFAULT_CHAIN_PATH)
            except OSError:
                pass
            print("\nGoodbye!\n")
            break

        else:
            print("\nInvalid option. Please choose a valid number.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)

