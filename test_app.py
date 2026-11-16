"""Testes do OrderService.

O teste de cálculo deve falhar enquanto a falha controlada estiver ativa.
"""

from fastapi.testclient import TestClient

from app import app, calculate_shipping

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_calculate_shipping() -> None:
    assert calculate_shipping(10.0, "2.5") == 12.5
