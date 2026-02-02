from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI()

# Configurar CORS para permitir peticiones desde la extensión
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, restringe esto al ID de la extensión
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProductData(BaseModel):
    title: str | None = None
    price: str | None = None
    rating: str | None = None
    reviewCount: str | None = None
    brand: str | None = None
    url: str

@app.post("/analyze")
async def analyze_product(product: ProductData):
    print(f"Analizando: {product.title}")
    
    score = 10
    reason = []
    
    # --- LOGICA DE DETECCIÓN (SIMPLIFICADA) ---
    
    # 1. Detección de "Sopa de Letras" (Marcas desconocidas en mayúsculas)
    # Ejemplo: Si la marca es "XGODY" o "JOYROOM"
    clean_brand = product.brand.replace("Visita la tienda de ", "").strip()
    if clean_brand.isupper() and len(clean_brand) < 8:
        score -= 3
        reason.append(f"La marca '{clean_brand}' parece genérica/desconocida.")

    # 2. Análisis del Título (Spam de palabras clave)
    if product.title and len(product.title) > 150:
        score -= 2
        reason.append("El título es excesivamente largo (táctica típica de spam SEO).")

    # 3. Detección de Review Farming (Muchos reviews, marca rara)
    reviews_clean = int(product.reviewCount.replace(",", "").replace(".", "").split()[0]) if product.reviewCount else 0
    if reviews_clean > 5000 and score < 8:
        score -= 3
        reason.append("Sospecha: Demasiadas reseñas para una marca poco conocida (posible reciclaje de reseñas).")

    # --- MOTOR DE RECOMENDACIÓN (MONETIZACIÓN) ---
    recommendation = None
    
    # Si el score es bajo, sugerimos algo mejor (Aquí va tu enlace de afiliado)
    if score < 7:
        recommendation = {
            "name": "Sony WH-CH520 (Verificado)",
            # IMPORTANTE: Aquí pones tu enlace de Amazon Associates
            "affiliate_link": "https://www.amazon.es/dp/B0BS1QCF54?tag=TU_TAG_AFILIADO-21"
        }
        final_reason_text = " ".join(reason)
    else:
        final_reason_text = "El producto parece legítimo. La marca tiene buena reputación."

    return {
        "score": score,
        "reason": final_reason_text,
        "recommendation": recommendation
    }

# Para correr el servidor: uvicorn server:app --reload