def validate_password(value: str) -> str:
    if not any(char.isdigit() for char in value):
        raise ValueError("Password must contain at least one digit.")
    if not any(char.islower() for char in value):
        raise ValueError("Password must contain at least one lowercase letter.")
    if not any(char.isupper() for char in value):
        raise ValueError("Password must contain at least one uppercase letter.")
    if not any(not char.isalnum() for char in value):
        raise ValueError("Password must contain at least one special character.")
    return value
