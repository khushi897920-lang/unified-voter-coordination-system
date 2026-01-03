from sqlalchemy.orm import Session
from models import ReferenceRegistry


def get_reference(reference_id: str, db: Session):
    """
    Fetch voter reference record from the national reference registry.
    """
    return db.query(ReferenceRegistry).filter(
        ReferenceRegistry.reference_id == reference_id
    ).first()


def create_reference(reference_id: str, state: str, db: Session):
    """
    Create a new reference entry when voter is first registered.
    """
    record = ReferenceRegistry(
        reference_id=reference_id,
        current_state=state,
        status="ACTIVE",
        election_flag=False
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def mark_in_transfer(reference_id: str, db: Session):
    """
    Lock voter during interstate migration to prevent double activation.
    """
    record = get_reference(reference_id, db)
    if record and record.status == "ACTIVE":
        record.status = "IN-TRANSFER"
        db.commit()
        return True
    return False


def activate_state(reference_id: str, new_state: str, db: Session):
    """
    Activate voter in the new state after successful migration.
    """
    record = get_reference(reference_id, db)
    if record:
        record.current_state = new_state
        record.status = "ACTIVE"
        db.commit()
        return True
    return False


def deactivate_reference(reference_id: str, db: Session):
    """
    Mark voter as inactive (used when voter migrates out or is blocked).
    """
    record = get_reference(reference_id, db)
    if record:
        record.status = "INACTIVE"
        db.commit()
        return True
    return False
def block_reference(reference_id: str, db: Session):
    """
    Block voter reference from being used in any future operations.
    """
    record = get_reference(reference_id, db)
    if record:
        record.status = "BLOCKED"
        db.commit()
        return True
    return False