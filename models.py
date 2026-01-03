from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class StateVoter(Base):
    __tablename__ = "state_voters"

    id = Column(Integer, primary_key=True, index=True)
    reference_id = Column(String, index=True)
    state = Column(String)
    status = Column(String)  # ACTIVE / INACTIVE / BLOCKED


class ReferenceRegistry(Base):
    __tablename__ = "reference_registry"

    reference_id = Column(String, primary_key=True, index=True)
    current_state = Column(String)
    status = Column(String)  # ACTIVE / IN-TRANSFER / INACTIVE / BLOCKED
    election_flag = Column(Boolean, default=False)
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    reference_id = Column(String, index=True)
    action = Column(String)  # e.g., "TRANSFER_INITIATED", "STATUS_CHANGED"
    details = Column(String)  # Additional details about the action