from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware  
from pydantic import BaseModel
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import tempfile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

class DebitNoteData(BaseModel):
    sum_insured: float
    basic_premium_rate: float
    excess_protector: int
    radio_cassette: str
    windscreen_cover: str
    tl: int
    sd: int
    class_of_insurance: str
    policy_number: str
    name_of_insured: str
    occupation: str
    pin_number: str
    vehicle_covered: str
    engine_no: str
    chasis: str
    sitting_capacity: str
    color: str
    period_of_insurance: str
    terms_of_payment: str


    @app.get("/")
    async def home():
        return {
            "message": "Welcome to the Utility Cover API!",
            "description": "This API allows you to generate motor debit/risk notes in PDF format.",
            "endpoints": {
                "/generate-debit-note": "POST - Generate a debit note by providing the required data."
            }
        }

@app.post("/generate-debit-note")
async def generate_debit_note(data: DebitNoteData):
    filename = f"DebitNote_{data.vehicle_covered.replace(' ', '')}_{datetime.now().strftime('%d-%m-%Y')}.pdf"
    filepath = os.path.join(tempfile.gettempdir(), filename)

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    # Header
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, height - 40, "UTILITY COVER INSURANCE AGENCIES")
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, height - 60, "SUMMIT HOUSE, M13")
    c.drawCentredString(width / 2, height - 75, "P.O. BOX 4737 – 00100 NAIROBI")
    c.drawCentredString(width / 2, height - 90, "TEL: 020 310040/1 CELL: 0722 766 583 / 0733-766 583")
    c.drawCentredString(width / 2, height - 105, "Email: utilitycoverinsuranceagencies@gmail.com")

    # Main content
    y = height - 140
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "MOTOR DEBIT / RISK NOTE")

    y -= 30
    c.setFont("Helvetica", 10)
    calculated_basic_premium = (data.sum_insured * data.basic_premium_rate) / 100
    
    c.drawString(50, y, f"SUM INSURED:        Kshs. {data.sum_insured:,}")
    y -= 20
    c.drawString(50, y, f"BASIC PREMIUM RATE: {data.basic_premium_rate}%")
    y -= 20
    c.drawString(50, y, f"BASIC PREMIUM:      Kshs. {calculated_basic_premium:,}")
    y -= 20
    c.drawString(50, y, f"Excess Protector:   Kshs. {data.excess_protector:,}")
    y -= 20
    c.drawString(50, y, f"Radio Cassette:     {data.radio_cassette} (Free)")
    y -= 20
    c.drawString(50, y, f"Windscreen Cover:   {data.windscreen_cover} (Free)")
    y -= 20
    c.drawString(50, y, f"+TL:                Kshs. {data.tl:,}")
    y -= 20
    c.drawString(50, y, f"+SD:                Kshs. {data.sd:,}")

    total_premium = calculated_basic_premium + data.excess_protector + data.tl + data.sd

    y -= 30
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, f"Total premium:      Kshs. {total_premium:,}")

    # Additional Details
    y -= 40
    c.setFont("Helvetica", 10)
    fields = [
        ("CLASS OF INSURANCE", data.class_of_insurance),
        ("POLICY NUMBER", data.policy_number),
        ("NAME OF INSURED", data.name_of_insured),
        ("OCCUPATION", data.occupation),
        ("PIN NUMBER", data.pin_number),
        ("VEHICLE COVERED", data.vehicle_covered),
        ("ENGINE NO.", data.engine_no),
        ("CHASIS", data.chasis),
        ("SITTING CAPACITY", data.sitting_capacity),
        ("COLOR", data.color),
        ("PERIOD OF INSURANCE", data.period_of_insurance),
    ]
    
    for label, value in fields:
        c.drawString(50, y, f"{label}: {value}")
        y -= 20

    y -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Terms of Payment:")
    c.setFont("Helvetica", 10)
    y -= 20
    c.drawString(70, y, f"{data.terms_of_payment}")

    y -= 40
    c.drawString(50, y, f"Date Issued: {datetime.now().strftime('%d/%m/%Y')}")

    c.showPage()
    c.save()

    return FileResponse(filepath, filename=filename, media_type="application/pdf")