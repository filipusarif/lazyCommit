from difflib import unified_diff

def analyze_changes(old_content, new_content):
    """
    Menganalisis perubahan antara dua konten string.
    """
    diff = list(unified_diff(old_content.splitlines(), new_content.splitlines(), lineterm=''))
    added_lines = [line[1:] for line in diff if line.startswith('+') and not line.startswith('+++')]
    removed_lines = [line[1:] for line in diff if line.startswith('-') and not line.startswith('---')]
    
    return added_lines, removed_lines


def generate_commit_message(file_path, old_content, new_content):
    """
    Membuat pesan commit otomatis berdasarkan perubahan antara versi lama dan baru dari file.
    """

    
    added_lines, removed_lines = analyze_changes(old_content, new_content)
    message_parts = []
    
    if added_lines:
        message_parts.append(f"Added {len(added_lines)} lines to {file_path}")
    if removed_lines:
        message_parts.append(f"Removed {len(removed_lines)} lines from {file_path}")

    if any('color' in line.lower() for line in added_lines + removed_lines):
        message_parts.append(f"Modified styles/colors in {file_path}")
    if any('function' in line.lower() for line in added_lines):
        message_parts.append(f"Added function(s) in {file_path}")
    if any('class' in line.lower() for line in added_lines + removed_lines):
        message_parts.append(f"Modified class definitions in {file_path}")
    
    return "; ".join(message_parts) if message_parts else f"Updated {file_path}"
