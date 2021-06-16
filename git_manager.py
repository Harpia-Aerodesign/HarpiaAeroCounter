import git
import os
from config import SAE_COUNTER_GITHUB, SAE_COUNTER_PATH, UNTRACKED_PATH

class GitManager:
    def __init__(self, github_url, path, username=None, password=None):
        self.has_changes = False
        if username is None:
            self.github_url = github_url
        else:
            self.github_url = github_url.format(username=username, password=password)
        self.path = os.path.join(UNTRACKED_PATH, path)
        self.repo = None

    def pull(self):
        try:
            self.repo = git.Repo(self.path)
            self.repo.git.reset('--hard')
            current = self.repo.head.commit
            self.repo.remotes.origin.pull()
            if current != self.repo.head.commit:
                self.has_changes = True
        except git.exc.NoSuchPathError:
            git.Repo.clone_from(self.github_url, self.path)
            self.has_changes = True


if __name__ == "__main__":
    # Exemplo de utilização.
    gitManager = GitManager(SAE_COUNTER_GITHUB, SAE_COUNTER_PATH)
    gitManager.pull()
    print(gitManager.has_changes)