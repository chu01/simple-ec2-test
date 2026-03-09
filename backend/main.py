from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()
# Docker uses the service name 'db' as the hostname
DATABASE_URL = "postgresql://user:pass@db:5432/testdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Click(Base):
    __tablename__ = "clicks"
    id = Column(Integer, primary_key=True)
    count = Column(Integer, default=0)

Base.metadata.create_all(bind=engine)

@app.get("/api/click")
def get_click():
    db = SessionLocal()
    click = db.query(Click).first() or Click(count=0)
    click.count += 1
    db.add(click)
    db.commit()
    return {"total_clicks": click.count}