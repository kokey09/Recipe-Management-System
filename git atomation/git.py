import subprocess

repository_path = "D:\Desktop\ongoing_projects\Recipe-Management-System"  # Replace with your repository path
branch_name = "main"  # Replace with your branch name

def git_pull():
    git_pull_command = ["C:/Program Files/Git/bin/git.exe", "-C", repository_path, "pull", "origin", branch_name]
    subprocess.run(git_pull_command, check=True)
    print("Git pull successful")

def git_push():
    try:
        git_status_command = ["C:/Program Files/Git/bin/git.exe", "-C", repository_path, "status", "--porcelain"]
        status_output = subprocess.check_output(git_status_command, text=True)

        if not status_output.strip():
            print("No changes to commit. Working tree is clean.")
        else:
            commit_message = input('Your commit message: ')  # Replace with your commit message
            git_add_command = ["C:/Program Files/Git/bin/git.exe", "-C", repository_path, "add", "."]
            git_commit_command = ["C:/Program Files/Git/bin/git.exe", "-C", repository_path, "commit", "-m", commit_message]
            git_push_command = ["C:/Program Files/Git/bin/git.exe", "-C", repository_path, "push", "origin", branch_name]

            subprocess.run(git_add_command, check=True)
            subprocess.run(git_commit_command, check=True)
            subprocess.run(git_push_command, check=True)
            print("Git add, commit, and push successful")
    except subprocess.CalledProcessError as e:
        print(f"Error during Git operation: {e}")

while True:
    print()
    print('1 Git Pull')
    print('2 Git push')
    print("3. Exit")

    print()
    choice = input('Enter your choice: ')

    if choice == '1':
        git_pull()
    elif choice == '2':
        git_push()
    elif choice == '3':
        break
    else:
        print('error,input')





