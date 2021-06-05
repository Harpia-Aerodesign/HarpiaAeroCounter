import urllib

from git_manager import GitManager
from config import OVERLEAF_PASSWORD, OVERLEAF_USER, PROJECTS_OVERLEAF, SAE_COUNTER_GITHUB, SAE_COUNTER_PATH, UNTRACKED_PATH


class HarpiaAeroCounter:
    def __init__(self):
        self.sae_counter_manager = GitManager(SAE_COUNTER_GITHUB, SAE_COUNTER_PATH)
        self.projects_list = PROJECTS_OVERLEAF
        for project in self.projects_list:
            project['repo'] = GitManager(
                project['url'],
                project['path'],
                urllib.parse.quote(OVERLEAF_USER),
                urllib.parse.quote(OVERLEAF_PASSWORD)
            )

    def loop(self):
        redo = False
        self.sae_counter_manager.pull()
        if (self.sae_counter_manager.has_changes):
            redo = True # Precisa atualizar tudo.
        else:
            for project in self.projects_list:
                project['repo'].pull()
                if project['repo'].has_changes or redo:
                    print(project['name'], "        mudou")
                    # Compilar o PDF aqui
                    # Contar as palavras aqui
                    project['repo'].has_changes = False
                    redo = False
                else:
                    print(project['name'], "    não mudou")


if __name__ == "__main__":
    harpiaAeroCounter = HarpiaAeroCounter()
    harpiaAeroCounter.loop()
