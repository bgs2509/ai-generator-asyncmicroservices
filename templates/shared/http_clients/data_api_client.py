"""HTTP client for Data Service communication.

Implements the HTTP-only data access pattern:
- Business services NEVER access databases directly
- All data operations go through Data Service HTTP API

Usage:
    from shared.http_clients import DataApiClient

    async with DataApiClient(base_url) as client:
        user = await client.get("/users/123", UserResponse)
"""
from typing import Any, TypeVar

import httpx
from pydantic import BaseModel

from shared.utils.logger import create_logger
from shared.utils.request_id import get_request_id

logger = create_logger(__name__)
T = TypeVar("T", bound=BaseModel)


class DataApiClient:
    """Async HTTP client for Data Service.

    Automatically propagates X-Request-ID for distributed tracing.
    """

    def __init__(self, base_url: str, timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "DataApiClient":
        await self.connect()
        return self

    async def __aexit__(self, *args) -> None:
        await self.close()

    async def connect(self) -> None:
        """Initialize the HTTP client."""
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers={"Content-Type": "application/json"},
        )
        logger.info("Data API client connected", extra={"base_url": self.base_url})

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None
            logger.info("Data API client closed")

    def _get_headers(self) -> dict[str, str]:
        """Get headers with request ID for correlation."""
        headers = {}
        request_id = get_request_id()
        if request_id:
            headers["X-Request-ID"] = request_id
        return headers

    async def get(
        self,
        path: str,
        response_model: type[T] | None = None,
    ) -> T | dict[str, Any]:
        """Send GET request to Data Service."""
        if not self._client:
            raise RuntimeError("Client not connected. Call connect() first.")

        response = await self._client.get(path, headers=self._get_headers())
        response.raise_for_status()

        data = response.json()
        if response_model:
            return response_model.model_validate(data)
        return data

    async def post(
        self,
        path: str,
        payload: BaseModel | dict[str, Any],
        response_model: type[T] | None = None,
    ) -> T | dict[str, Any]:
        """Send POST request to Data Service."""
        if not self._client:
            raise RuntimeError("Client not connected. Call connect() first.")

        json_data = payload.model_dump() if isinstance(payload, BaseModel) else payload
        response = await self._client.post(
            path,
            json=json_data,
            headers=self._get_headers(),
        )
        response.raise_for_status()

        data = response.json()
        if response_model:
            return response_model.model_validate(data)
        return data

    async def put(
        self,
        path: str,
        payload: BaseModel | dict[str, Any],
        response_model: type[T] | None = None,
    ) -> T | dict[str, Any]:
        """Send PUT request to Data Service."""
        if not self._client:
            raise RuntimeError("Client not connected. Call connect() first.")

        json_data = payload.model_dump() if isinstance(payload, BaseModel) else payload
        response = await self._client.put(
            path,
            json=json_data,
            headers=self._get_headers(),
        )
        response.raise_for_status()

        data = response.json()
        if response_model:
            return response_model.model_validate(data)
        return data

    async def delete(self, path: str) -> None:
        """Send DELETE request to Data Service."""
        if not self._client:
            raise RuntimeError("Client not connected. Call connect() first.")

        response = await self._client.delete(path, headers=self._get_headers())
        response.raise_for_status()
