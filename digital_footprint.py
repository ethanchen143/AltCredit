def process_tiktok_data(data: dict) -> dict:
    """
    Process TikTok data. Normalize fields, validate, etc.
    """
    processed = {
        "username": data.get("username"),
        "followers": int(data.get("followers", 0)),
        "engagement": float(data.get("engagement", 0)),
        # Extend with additional fields if needed
    }
    return processed