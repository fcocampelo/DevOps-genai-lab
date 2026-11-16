"""OrderService - microsserviço didático para o projeto integrador DevOps + GenAI.

O bug em ``calculate_shipping`` é INTENCIONAL: o pipeline deve detectá-lo para que
um agente GenAI analise o log e o diff do Pull Request.
"""

from fastapi import FastAPI

app = FastAPI(title="OrderService", version="1.0.0")


def calculate_shipping(base_price: float, tax_rate: str) -> float:
    """Calcula o frete acrescido da taxa administrativa.

    Falha controlada: ``tax_rate`` chega como ``str`` e é somada diretamente a
    um ``float``. A correção esperada é converter a taxa antes da soma.
    """
    return base_price + tax_rate  # type: ignore[operator]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/shipping")
def shipping(base_price: float, tax_rate: str) -> dict[str, float]:
    return {"shipping": calculate_shipping(base_price, tax_rate)}
