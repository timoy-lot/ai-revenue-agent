import subprocess
import os

def publish_to_amplify():
    """Commits and pushes generated markdown articles to GitHub for AWS Amplify auto-deployment."""
    try:
        print("🐙 Stage, commit, and push updates to GitHub for AWS Amplify...")
        
        # Git Commands
        subprocess.run(["git", "add", "output/"], check=True)
        subprocess.run(["git", "commit", "-m", "feat: auto-publish new generated articles"], check=True)
        subprocess.run(["git", "push"], check=True)
        
        print("🚀 Code pushed to GitHub! AWS Amplify will auto-build and publish your updates.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git push failed or no new changes to commit: {e}")
        return False

if __name__ == "__main__":
    publish_to_amplify()