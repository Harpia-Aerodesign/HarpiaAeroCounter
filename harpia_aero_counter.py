import urllib
import os

from subprocess import Popen, DEVNULL, STDOUT
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
        for project in self.projects_list:
            project['repo'].pull()
            if project['repo'].has_changes or redo:
                print(project['name'], "\t\t    mudou")
                # Compilar o PDF aqui
                Popen(
                    ["pdflatex", "-interaction=nonstopmode", "main.tex"],
                    cwd=project['repo'].path,
                    stdout=DEVNULL,
                    stderr=STDOUT
                ).wait()
                os.rename(
                    os.path.join(project['repo'].path, 'main.pdf'),
                    os.path.join(UNTRACKED_PATH, project['path']+".pdf")
                )
                # Contar as palavras aqui
                # Mostrar os resultados
            else:
                print(project['name'], "\t\tnão mudou")
        redo = False


if __name__ == "__main__":
    harpiaAeroCounter = HarpiaAeroCounter()
    harpiaAeroCounter.loop()
