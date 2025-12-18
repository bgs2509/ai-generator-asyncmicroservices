"""Tests for health check endpoints."""

import pytest
from unittest.mock import AsyncMock, patch


class TestHealthEndpoints:
    """Test health check endpoints."""

    def test_health_check_returns_200(self, test_client):
        """Test liveness probe returns healthy status."""
        response = test_client.get("/health/")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "1.0.0"
        assert data["checks"] == {}

    @patch("src.api.v1.health.check_database_connection")
    def test_readiness_check_healthy(self, mock_db_check, test_client):
        """Test readiness probe when database is healthy."""
        mock_db_check.return_value = True

        response = test_client.get("/health/ready")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert data["checks"]["database"] == "healthy"

    @patch("src.api.v1.health.check_database_connection")
    def test_readiness_check_unhealthy(self, mock_db_check, test_client):
        """Test readiness probe when database is unhealthy."""
        mock_db_check.return_value = False

        response = test_client.get("/health/ready")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "unhealthy"
        assert data["checks"]["database"] == "unhealthy"

    @patch("src.api.v1.health.check_database_connection")
    def test_readiness_check_exception(self, mock_db_check, test_client):
        """Test readiness probe handles exceptions gracefully."""
        mock_db_check.side_effect = Exception("Connection failed")

        response = test_client.get("/health/ready")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "unhealthy"
        assert data["checks"]["database"] == "unhealthy"


class TestRootEndpoint:
    """Test root endpoint."""

    def test_root_returns_service_info(self, test_client):
        """Test root endpoint returns service information."""
        response = test_client.get("/")
        assert response.status_code == 200

        data = response.json()
        assert data["service"] == "data_mongo_api"
        assert data["version"] == "1.0.0"
        assert "environment" in data
