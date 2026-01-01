

async def extract_text_from_file(file_path: str) -> str:
    """Extract text from a .txt file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text
