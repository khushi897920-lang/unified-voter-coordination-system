from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import StateVoter
from reference_layer import create_reference, get_reference
from migration_workflow import request_migration, approve_migration
from voting_layer import allow_vote, mark_voted
from ai_advisory import detect_possible_duplicates, detect_suspicious_activity

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Unified Voter Coordination System (PoC)")


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------- BASIC ENDPOINTS -------------------

@app.get("/")
def root():
    return {"message": "Unified Voter Coordination System is running"}


# ------------------- REGISTRATION -------------------

@app.post("/register")
def register_voter(reference_id: str, state: str, db: Session = Depends(get_db)):
    existing = get_reference(reference_id, db)
    if existing:
        return {"status": "FAILED", "reason": "Voter already exists in reference layer"}

    create_reference(reference_id, state, db)

    voter = StateVoter(
        reference_id=reference_id,
        state=state,
        status="ACTIVE"
    )
    db.add(voter)
    db.commit()

    return {"status": "SUCCESS", "state": state}


# ------------------- MIGRATION -------------------

@app.post("/migration/request")
def migration_request(reference_id: str, new_state: str, db: Session = Depends(get_db)):
    return request_migration(reference_id, new_state, db)


@app.post("/migration/approve")
def migration_approve(
    reference_id: str,
    from_state: str,
    to_state: str,
    db: Session = Depends(get_db)
):
    return approve_migration(reference_id, from_state, to_state, db)


# ------------------- VOTING -------------------

@app.post("/vote/check")
def vote_check(reference_id: str, db: Session = Depends(get_db)):
    return allow_vote(reference_id, db)


@app.post("/vote/cast")
def vote_cast(reference_id: str, db: Session = Depends(get_db)):
    allowed = allow_vote(reference_id, db)
    if allowed["status"] != "ALLOWED":
        return allowed

    mark_voted(reference_id, db)
    return {"status": "VOTE_CASTED"}


# ------------------- AI ADVISORY -------------------

@app.get("/ai/duplicate-check")
def ai_duplicate_check(reference_id: str, db: Session = Depends(get_db)):
    return detect_possible_duplicates(reference_id, db)


@app.get("/ai/suspicious-activity")
def ai_suspicious_activity(state: str, db: Session = Depends(get_db)):
    return detect_suspicious_activity(state, db)
