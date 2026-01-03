from sqlalchemy.orm import Session
from models import ReferenceRegistry


def allow_vote(reference_id: str, db: Session):
    """
    Validates whether a voter is allowed to vote in the current election.
    """
    record = (
        db.query(ReferenceRegistry)
        .filter(ReferenceRegistry.reference_id == reference_id)
        .first()
    )

    if not record:
        return {"status": "DENIED", "reason": "Voter not found"}

    if record.status != "ACTIVE":
        return {"status": "DENIED", "reason": "Voter not active"}

    if record.election_flag:
        return {"status": "DENIED", "reason": "Already voted in this election"}

    return {"status": "ALLOWED"}


def mark_voted(reference_id: str, db: Session):
    """
    Marks voter as having voted in the current election cycle.
    """
    record = (
        db.query(ReferenceRegistry)
        .filter(ReferenceRegistry.reference_id == reference_id)
        .first()
    )

    if record:
        record.election_flag = True
        db.commit()
        return True

    return False
def reset_election_flags(db: Session):
    """
    Resets election flags for all voters at the start of a new election cycle.
    """
    db.query(ReferenceRegistry).filter(ReferenceRegistry.election_flag == True).update({"election_flag": False})
    db.commit()