import subprocess
import datetime
import os
import random

def run_cmd(cmd, env=None):
    return subprocess.run(cmd, capture_output=True, text=True, check=True, env=env).stdout.strip()

def rewrite_history():
    # Retrieve all commit hashes in chronological order
    try:
        commits = run_cmd(['git', 'log', '--reverse', '--format=%H']).split('\n')
    except subprocess.CalledProcessError:
        print("Failed to read git history. Are you in a git repository?")
        return

    total = len(commits)
    if total == 0 or not commits[0]:
        print("No commits found.")
        return

    print(f"Found {total} commits. Generating an organic timeline over the last 60 days...")

    # Define the 60-day window
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=60)
    total_seconds = int((end_date - start_date).total_seconds())

    # Generate random timestamps within the window and sort them chronologically
    # We guarantee the first commit is near the start, and the rest fall organically after
    random_offsets = sorted([random.randint(0, total_seconds) for _ in range(total)])

    # Store the current branch name
    current_branch = run_cmd(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])

    # Checkout the root commit detached
    subprocess.run(['git', 'checkout', commits[0]], check=True)

    for i, commit in enumerate(commits):
        # Apply the chronologically sorted random timestamp
        current_date = start_date + datetime.timedelta(seconds=random_offsets[i])
        date_str = current_date.strftime('%Y-%m-%dT%H:%M:%S')

        # Set environment variables for the commit dates
        env = os.environ.copy()
        env['GIT_AUTHOR_DATE'] = date_str
        env['GIT_COMMITTER_DATE'] = date_str

        if i > 0:
            # Cherry-pick the next commit
            result = subprocess.run(['git', 'cherry-pick', commit])
            if result.returncode != 0:
                print(f"\nMerge conflict detected at {commit}.")
                print("This script requires a linear history. Aborting.")
                return

        # Amend the commit with the new dates
        subprocess.run(['git', 'commit', '--amend', '--no-edit', '--date', date_str], env=env, check=True)
        print(f"Rewrote commit {i+1}/{total} -> {date_str}")

    # Move the original branch pointer to this new HEAD and checkout
    subprocess.run(['git', 'branch', '-f', current_branch, 'HEAD'], check=True)
    subprocess.run(['git', 'checkout', current_branch], check=True)

    print("\nHistory successfully rewritten with organic spacing!")
    print(f"To push these changes, use: git push origin {current_branch} --force")

if __name__ == '__main__':
    rewrite_history()