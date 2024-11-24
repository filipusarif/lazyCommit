import os
import git
import mimetypes
from charset_normalizer import from_path
from generate_message import generate_commit_message

def read_file_with_encoding(file_path):
    """
    Membaca file dengan encoding yang terdeteksi.
    """
    try:
        result = from_path(file_path).best()
        if result:
            return str(result)  # Konten file sebagai string
        else:
            raise ValueError(f"Could not decode {file_path}")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def lazycommit(repo_path):
    repo = git.Repo(repo_path)
    print("hello")
    if repo.is_dirty():
        repo_root = repo.working_tree_dir
        changed_files = [item.a_path for item in repo.index.diff(None)]
        
        for file_path in changed_files:
            abs_file_path = os.path.join(repo_root, file_path)

            # Periksa apakah file adalah teks
            mime_type, _ = mimetypes.guess_type(abs_file_path)
            if mime_type and not mime_type.startswith("text"):
                print(f"Skipping binary file: {file_path}")
                continue

            # Ambil konten lama dari Git
            try:
                old_content = repo.git.show(f'HEAD:{file_path}')
            except git.exc.GitCommandError:
                old_content = ""  # File baru, tidak ada versi lama

            # Ambil konten baru dari file
            new_content = read_file_with_encoding(abs_file_path)
            if new_content is None:
                print(f"Could not read file: {file_path}. Skipping...")
                continue

            # Generate pesan commit otomatis
            commit_message = generate_commit_message(file_path, old_content, new_content)
            print(f"Generated commit message: {commit_message}")

            # Tambahkan file ke staging
            repo.git.add(file_path)

            # Commit file dengan pesan commit
            repo.git.commit('-m', commit_message)

        # Push perubahan
        origin = repo.remote(name='origin')
        origin.push()
        print("Push successful!")
    else:
        print("No changes detected in the repository.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Automate Git commits with lazycommit.")
    parser.add_argument("repo_path", type=str, help="Path to the Git repository.")
    args = parser.parse_args()

    lazycommit(args.repo_path)
