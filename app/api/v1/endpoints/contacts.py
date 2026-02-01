from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.contact import Contact
from app.schemas.contact import Contact as ContactSchema, ContactCreate, ContactUpdate
from app.api.deps import get_current_user
import uuid

router = APIRouter()

@router.post("/", response_model=ContactSchema)
def create_contact(
    contact: ContactCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_obj = Contact(
        name=contact.name,
        phone=contact.phone,
        tenant_id=current_user.tenant_id,
        metadata_=contact.metadata_
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/", response_model=list[ContactSchema])
def read_contacts(
    skip: int = 0, 
    limit: int = 100, 
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    contacts = db.query(Contact).filter(Contact.tenant_id == current_user.tenant_id).offset(skip).limit(limit).all()
    return contacts

@router.get("/{contact_id}", response_model=ContactSchema)
def read_contact(
    contact_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    contact = db.query(Contact).filter(
        Contact.id == uuid.UUID(contact_id), 
        Contact.tenant_id == current_user.tenant_id
    ).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

# CRM Features

from app.schemas.crm import TagCreate, NoteCreate, TagOut, NoteOut
from app.models.tag import Tag
from app.models.note import Note

@router.post("/{contact_id}/tags", response_model=TagOut)
def add_tag(
    contact_id: str,
    tag: TagCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    contact = db.query(Contact).filter(Contact.id == uuid.UUID(contact_id), Contact.tenant_id == current_user.tenant_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
        
    # Find or create Tag
    db_tag = db.query(Tag).filter(Tag.name == tag.name, Tag.tenant_id == current_user.tenant_id).first()
    if not db_tag:
        db_tag = Tag(name=tag.name, color=tag.color, tenant_id=current_user.tenant_id)
        db.add(db_tag)
        db.commit()
        db.refresh(db_tag)
    
    if db_tag not in contact.tags:
        contact.tags.append(db_tag)
        db.commit()
        
    return db_tag

@router.post("/{contact_id}/notes", response_model=NoteOut)
def add_note(
    contact_id: str,
    note: NoteCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    contact = db.query(Contact).filter(Contact.id == uuid.UUID(contact_id), Contact.tenant_id == current_user.tenant_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    db_note = Note(content=note.content, contact_id=contact.id, tenant_id=current_user.tenant_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note
