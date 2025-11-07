"""Common validation functions used across services.

Provides reusable validators for email, phone, UUID, and other
common data types. Use these instead of duplicating validation logic.

Example:
    >>> from shared.utils.validators import is_valid_email
    >>> if not is_valid_email(user_email):
    >>>     raise ValidationError("Invalid email address")
"""

import re
from typing import Optional
from uuid import UUID


def is_valid_email(email: str) -> bool:
    """Validate email address format.

    Args:
        email: Email address to validate

    Returns:
        True if email format is valid, False otherwise

    Example:
        >>> is_valid_email("user@example.com")
        True
        >>> is_valid_email("invalid-email")
        False
    """
    if not email or len(email) > 254:
        return False

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_phone(phone: str, country_code: str = "US") -> bool:
    """Validate phone number format.

    Args:
        phone: Phone number to validate
        country_code: ISO 3166-1 alpha-2 country code

    Returns:
        True if phone format is valid for country, False otherwise

    Example:
        >>> is_valid_phone("+1-555-123-4567", "US")
        True
        >>> is_valid_phone("123", "US")
        False

    Note:
        For production, consider using phonenumbers library for
        comprehensive international phone validation.
    """
    # Remove common separators
    cleaned = re.sub(r'[\s\-\(\)\.]', '', phone)

    if country_code == "US":
        # US: 10 digits, optional +1 prefix
        pattern = r'^(\+1)?[2-9]\d{9}$'
        return bool(re.match(pattern, cleaned))

    # Generic: 7-15 digits, optional + prefix
    pattern = r'^\+?\d{7,15}$'
    return bool(re.match(pattern, cleaned))


def is_valid_uuid(value: str) -> bool:
    """Validate UUID format.

    Args:
        value: String to validate as UUID

    Returns:
        True if valid UUID format, False otherwise

    Example:
        >>> is_valid_uuid("123e4567-e89b-12d3-a456-426614174000")
        True
        >>> is_valid_uuid("invalid-uuid")
        False
    """
    try:
        UUID(value)
        return True
    except (ValueError, AttributeError, TypeError):
        return False


def is_valid_url(url: str, require_https: bool = False) -> bool:
    """Validate URL format.

    Args:
        url: URL string to validate
        require_https: If True, only accept HTTPS URLs

    Returns:
        True if valid URL format, False otherwise

    Example:
        >>> is_valid_url("https://example.com/path")
        True
        >>> is_valid_url("not-a-url")
        False
    """
    if require_https:
        pattern = r'^https://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$'
    else:
        pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$'

    return bool(re.match(pattern, url))


def validate_password_strength(
    password: str,
    min_length: int = 8,
    require_uppercase: bool = True,
    require_lowercase: bool = True,
    require_digit: bool = True,
    require_special: bool = True,
) -> tuple[bool, Optional[str]]:
    """Validate password meets strength requirements.

    Args:
        password: Password to validate
        min_length: Minimum password length
        require_uppercase: Require at least one uppercase letter
        require_lowercase: Require at least one lowercase letter
        require_digit: Require at least one digit
        require_special: Require at least one special character

    Returns:
        Tuple of (is_valid, error_message)
        error_message is None if valid

    Example:
        >>> validate_password_strength("Weak123!")
        (True, None)
        >>> validate_password_strength("weak")
        (False, "Password must be at least 8 characters")
    """
    if len(password) < min_length:
        return False, f"Password must be at least {min_length} characters"

    if require_uppercase and not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"

    if require_lowercase and not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"

    if require_digit and not re.search(r'\d', password):
        return False, "Password must contain at least one digit"

    if require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"

    return True, None


def is_valid_slug(slug: str, max_length: int = 100) -> bool:
    """Validate URL-safe slug format.

    Args:
        slug: Slug string to validate
        max_length: Maximum allowed length

    Returns:
        True if valid slug format, False otherwise

    Example:
        >>> is_valid_slug("my-article-title")
        True
        >>> is_valid_slug("My Article!")
        False
    """
    if not slug or len(slug) > max_length:
        return False

    pattern = r'^[a-z0-9]+(?:-[a-z0-9]+)*$'
    return bool(re.match(pattern, slug))


def is_valid_hex_color(color: str) -> bool:
    """Validate hexadecimal color code.

    Args:
        color: Color string to validate (with or without #)

    Returns:
        True if valid hex color, False otherwise

    Example:
        >>> is_valid_hex_color("#FF5733")
        True
        >>> is_valid_hex_color("FF5733")
        True
        >>> is_valid_hex_color("ZZZ")
        False
    """
    # Remove # prefix if present
    color = color.lstrip('#')

    # Valid formats: RGB (3 chars) or RRGGBB (6 chars)
    if len(color) not in (3, 6):
        return False

    try:
        int(color, 16)
        return True
    except ValueError:
        return False


def is_valid_username(
    username: str,
    min_length: int = 3,
    max_length: int = 30,
    allow_underscore: bool = True,
) -> bool:
    """Validate username format.

    Args:
        username: Username to validate
        min_length: Minimum username length
        max_length: Maximum username length
        allow_underscore: Whether to allow underscores

    Returns:
        True if valid username format, False otherwise

    Example:
        >>> is_valid_username("john_doe")
        True
        >>> is_valid_username("ab")
        False
    """
    if not username or len(username) < min_length or len(username) > max_length:
        return False

    if allow_underscore:
        pattern = r'^[a-zA-Z0-9_]+$'
    else:
        pattern = r'^[a-zA-Z0-9]+$'

    return bool(re.match(pattern, username))


def is_valid_port(port: int) -> bool:
    """Validate network port number.

    Args:
        port: Port number to validate

    Returns:
        True if valid port (1-65535), False otherwise

    Example:
        >>> is_valid_port(8080)
        True
        >>> is_valid_port(70000)
        False
    """
    return 1 <= port <= 65535
