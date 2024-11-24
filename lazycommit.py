import os
import git
from generate_message import generate_commit_message

def lazycommit(repo_path):
    repo = git.Repo(repo_path)
    print("hello")
    if repo.is_dirty():
        repo_root = repo.working_tree_dir
        changed_files = [item.a_path for item in repo.index.diff(None)]
        
        for file_path in changed_files:
            abs_file_path = os.path.join(repo_root, file_path)

            # Ambil konten lama dari Git
            try:
                old_content = repo.git.show(f'HEAD:{file_path}')
            except git.exc.GitCommandError:
                old_content = ""  # File baru, tidak ada versi lama

            # Ambil konten baru dari file
            if os.path.exists(abs_file_path):
                with open(abs_file_path, 'r') as file:
                    new_content = file.read()

                # Generate pesan commit otomatis
                commit_message = generate_commit_message(file_path, old_content, new_content)
                print(commit_message)
                # Tambahkan file ke staging
                repo.git.add(file_path)

                # Commit file
                repo.git.commit('-m', commit_message)
            else:
                print(f"File {file_path} not found. Skipping...")

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
