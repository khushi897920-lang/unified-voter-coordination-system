from sqlalchemy.orm import Session
from models import StateVoter
from reference_layer import (
    get_reference,
    mark_in_transfer,
    activate_state,
    deactivate_reference
)


def request_migration(reference_id: str, new_state: str, db: Session):
    """
    Initiates migration request from a new state.
    """
    ref = get_reference(reference_id, db)

    if not ref:
        return {"status": "FAILED", "reason": "Reference not found"}

    if ref.status != "ACTIVE":
        return {"status": "FAILED", "reason": "Voter not eligible for migration"}

    # Lock voter to prevent parallel activation
    locked = mark_in_transfer(reference_id, db)
    if not locked:
        return {"status": "FAILED", "reason": "Unable to lock voter"}

    return {
        "status": "PENDING_APPROVAL",
        "from_state": ref.current_state,
        "to_state": new_state
    }


def approve_migration(reference_id: str, from_state: str, to_state: str, db: Session):
    """
    Old state approves migration; voter becomes active in new state.
    """
    # Deactivate voter in old state
    old_record = (
        db.query(StateVoter)
        .filter(
            StateVoter.reference_id == reference_id,
            StateVoter.state == from_state,
            StateVoter.status == "ACTIVE"
        )
        .first()
    )

    if not old_record:
        return {"status": "FAILED", "reason": "Old state record not found"}

    old_record.status = "INACTIVE"
    db.commit()

    # Activate reference in new state
    activate_state(reference_id, to_state, db)

    # Create or update voter record in new state
    new_record = StateVoter(
        reference_id=reference_id,
        state=to_state,
        status="ACTIVE"
    )
    db.add(new_record)
    db.commit()

    return {"status": "APPROVED", "active_state": to_state}
def reject_migration(reference_id: str, db: Session):
    """
    Rejects a migration request and unlocks the voter.
    """
    # Unlock voter
    ref = get_reference(reference_id, db)
    if ref and ref.status == "IN-TRANSFER":
        ref.status = "ACTIVE"
        db.commit()
        return {"status": "REJECTED", "reason": "Migration rejected by old state"}

    return {"status": "FAILED", "reason": "Migration not in progress"}