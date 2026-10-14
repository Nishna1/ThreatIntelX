from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
from database import engine, SessionLocal
from feeds import sample_iocs

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Threat Intelligence Platform"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {
        "message": "Threat Intelligence Platform Running"
    }


@app.post("/load-feed")
def load_feed(db: Session = Depends(get_db)):

    for item in sample_iocs:

        existing = (
            db.query(models.IOC)
            .filter(models.IOC.value == item["value"])
            .first()
        )

        if not existing:

            new_ioc = models.IOC(
                type=item["type"],
                value=item["value"],
                source=item["source"],
                severity=item["severity"]
            )

            db.add(new_ioc)

    db.commit()

    return {
        "status": "feed imported"
    }


@app.get("/iocs")
def get_iocs(db: Session = Depends(get_db)):

    return db.query(models.IOC).all()


@app.get("/search/{value}")
def search_ioc(
        value: str,
        db: Session = Depends(get_db)
):

    result = (
        db.query(models.IOC)
        .filter(models.IOC.value == value)
        .first()
    )

    if result:
        return result

    return {
        "message": "IOC not found"
    }


@app.get("/stats")
def stats(db: Session = Depends(get_db)):

    total = db.query(models.IOC).count()

    return {
        "total_iocs": total
    }
@app.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):

    total = db.query(models.IOC).count()

    critical = (
        db.query(models.IOC)
        .filter(models.IOC.severity == "critical")
        .count()
    )

    high = (
        db.query(models.IOC)
        .filter(models.IOC.severity == "high")
        .count()
    )

    medium = (
        db.query(models.IOC)
        .filter(models.IOC.severity == "medium")
        .count()
    )

    return {
        "total_iocs": total,
        "critical": critical,
        "high": high,
        "medium": medium
    }

