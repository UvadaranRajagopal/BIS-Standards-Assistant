# backend/app/audit/audit_chain.py

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Tuple, Optional, List


class AuditChain:
    """
    Tamper-evident audit logger using SHA-256 hash chains.

    Each entry contains the hash of the previous entry.
    Modifying, deleting, inserting, or corrupting an entry
    can therefore be detected during integrity verification.
    """

    def __init__(self, db_path: str = "./audit_log.jsonl"):
        """
        Initialize audit chain.

        Args:
            db_path: Path to store audit log (JSONL format)
        """
        self.db_path = Path(db_path)

        # Ensure parent directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Get hash of last entry
        self.last_hash = self._get_last_hash()

    def _get_last_hash(self) -> str:
        """Get hash of last entry, or GENESIS if no entries exist."""
        if not self.db_path.exists():
            return "GENESIS"

        with open(self.db_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

            if lines:
                last_entry = json.loads(lines[-1])
                return last_entry.get("hash", "GENESIS")

        return "GENESIS"

    def _get_count(self) -> int:
        """Get total number of entries in the log."""
        if not self.db_path.exists():
            return 0

        with open(self.db_path, "r", encoding="utf-8") as f:
            return sum(1 for _ in f)

    def append(
        self,
        user_id: str,
        action: str,
        data: Dict[str, Any]
    ) -> Dict:
        """
        Append a new entry to the audit chain.
        """

        timestamp = datetime.utcnow().isoformat()
        prev_hash = self.last_hash

        entry = {
            "index": self._get_count(),
            "timestamp": timestamp,
            "user_id": user_id,
            "action": action,
            "data": data,
            "prev_hash": prev_hash
        }

        # Calculate SHA-256 hash
        entry_hash = hashlib.sha256(
            json.dumps(
                entry,
                sort_keys=True
            ).encode("utf-8")
        ).hexdigest()

        entry["hash"] = entry_hash

        # Append entry to audit log
        with open(
            self.db_path,
            "a",
            encoding="utf-8"
        ) as f:
            f.write(json.dumps(entry) + "\n")

        self.last_hash = entry_hash

        return entry

    def verify_integrity(self) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Verify the entire audit chain.

        Instead of returning only a generic error message,
        this method identifies the exact audit event where
        the integrity problem was detected.

        Returns:
            (
                is_valid,
                details
            )

        Example valid result:
            (True, None)

        Example invalid result:
            (
                False,
                {
                    "issue_type": "DATA_MODIFIED",
                    "event_index": 3,
                    "message": "...",
                    "action": "...",
                    "timestamp": "..."
                }
            )
        """

        if not self.db_path.exists():
            return True, None

        entries = []

        # ---------------------------------------------------------
        # STEP 1: Read every audit entry safely
        # ---------------------------------------------------------
        try:
            with open(
                self.db_path,
                "r",
                encoding="utf-8"
            ) as f:

                for line_number, line in enumerate(f):
                    line = line.strip()

                    if not line:
                        continue

                    try:
                        entries.append(json.loads(line))

                    except json.JSONDecodeError:
                        return False, {
                            "issue_type": "CORRUPTED_RECORD",
                            "event_index": line_number,
                            "message": (
                                "An audit record contains invalid "
                                "JSON data."
                            ),
                            "severity": "CRITICAL"
                        }

        except OSError as exc:
            return False, {
                "issue_type": "AUDIT_FILE_ERROR",
                "event_index": None,
                "message": str(exc),
                "severity": "CRITICAL"
            }

        prev_hash = "GENESIS"

        # ---------------------------------------------------------
        # STEP 2: Verify every event
        # ---------------------------------------------------------
        for position, entry in enumerate(entries):

            event_index = entry.get("index", position)

            action = entry.get(
                "action",
                "Unknown Action"
            )

            timestamp = entry.get(
                "timestamp",
                "Unknown"
            )

            # -----------------------------------------------------
            # CHECK 1:
            # Verify event index
            # -----------------------------------------------------
            if event_index != position:
                return False, {
                    "issue_type": "EVENT_SEQUENCE_CHANGED",
                    "event_index": event_index,
                    "position": position,
                    "action": action,
                    "timestamp": timestamp,
                    "message": (
                        f"Expected event index {position}, "
                        f"but found {event_index}."
                    ),
                    "severity": "HIGH"
                }

            # -----------------------------------------------------
            # CHECK 2:
            # Verify previous hash
            # -----------------------------------------------------
            stored_prev_hash = entry.get("prev_hash")

            if stored_prev_hash != prev_hash:
                return False, {
                    "issue_type": "CHAIN_BROKEN",
                    "event_index": event_index,
                    "position": position,
                    "action": action,
                    "timestamp": timestamp,
                    "expected_previous_hash": prev_hash,
                    "actual_previous_hash": stored_prev_hash,
                    "message": (
                        f"Hash chain broken at audit event "
                        f"{event_index}. The previous hash does "
                        f"not match the expected chain."
                    ),
                    "severity": "CRITICAL"
                }

            # -----------------------------------------------------
            # CHECK 3:
            # Recalculate current event hash
            # -----------------------------------------------------
            stored_hash = entry.get("hash")

            entry_without_hash = {
                key: value
                for key, value in entry.items()
                if key != "hash"
            }

            expected_hash = hashlib.sha256(
                json.dumps(
                    entry_without_hash,
                    sort_keys=True
                ).encode("utf-8")
            ).hexdigest()

            # -----------------------------------------------------
            # Hash mismatch = event data was changed
            # -----------------------------------------------------
            if stored_hash != expected_hash:

                return False, {
                    "issue_type": "DATA_MODIFIED",
                    "event_index": event_index,
                    "position": position,
                    "action": action,
                    "timestamp": timestamp,
                    "stored_hash": stored_hash,
                    "calculated_hash": expected_hash,
                    "message": (
                        f"Audit event {event_index} appears to "
                        f"have been modified. The calculated "
                        f"SHA-256 hash does not match the stored hash."
                    ),
                    "severity": "CRITICAL"
                }

            # Continue chain
            prev_hash = stored_hash

        # ---------------------------------------------------------
        # Everything is valid
        # ---------------------------------------------------------
        return True, None

    def get_all_entries(self) -> List[Dict]:
        """Get all audit log entries."""

        if not self.db_path.exists():
            return []

        entries = []

        with open(
            self.db_path,
            "r",
            encoding="utf-8"
        ) as f:

            for line in f:
                line = line.strip()

                if not line:
                    continue

                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

        return entries

    def get_entries_by_user(
        self,
        user_id: str
    ) -> List[Dict]:
        """Get all entries for a specific user."""

        all_entries = self.get_all_entries()

        return [
            entry
            for entry in all_entries
            if entry.get("user_id") == user_id
        ]


# -------------------------------------------------------------
# Global audit logger
# -------------------------------------------------------------

audit_logger = AuditChain()


def log_audit_event(
    action: str,
    user_id: str,
    data: dict
):
    """
    Convenience function for creating an audit event.

    Uses the existing AuditChain append mechanism.
    """

    return audit_logger.append(
        user_id=user_id,
        action=action,
        data=data
    )