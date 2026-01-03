from sqlalchemy.orm import Session
from models import StateVoter


def detect_possible_duplicates(reference_id: str, db: Session):
    """
    Simulates AI-based duplicate detection.
    Flags cases where the same reference appears in multiple states.
    """
    records = (
        db.query(StateVoter)
        .filter(StateVoter.reference_id == reference_id)
        .all()
    )

    if len(records) > 1:
        return {
            "alert": "POSSIBLE_DUPLICATE",
            "count": len(records),
            "message": "Voter reference found in multiple states. Human review required."
        }

    return {"alert": "CLEAR"}


def detect_suspicious_activity(state: str, db: Session):
    """
    Simulates detection of suspicious registration spikes in a state.
    """
    count = (
        db.query(StateVoter)
        .filter(
            StateVoter.state == state,
            StateVoter.status == "ACTIVE"
        )
        .count()
    )

    if count > 5:  # Threshold chosen only for PoC demonstration
        return {
            "alert": "SUSPICIOUS_ACTIVITY",
            "state": state,
            "message": "High number of active registrations detected. Manual audit suggested."
        }

    return {"alert": "NORMAL"}
def analyze_migration_patterns(reference_id: str, db: Session):
    """
    Simulates analysis of migration patterns for a voter.
    Flags if a voter has migrated multiple times in a short period.
    """
    records = (
        db.query(StateVoter)
        .filter(StateVoter.reference_id == reference_id)
        .all()
    )

    if len(records) > 3:  # Threshold chosen only for PoC demonstration
        return {
            "alert": "FREQUENT_MIGRATIONS",
            "count": len(records),
            "message": "Voter has migrated multiple times. Review recommended."
        }

    return {"alert": "STABLE"}