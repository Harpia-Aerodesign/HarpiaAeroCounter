from posixpath import join
import urllib
import os
import re

from pprint import pprint
from glob import glob
from subprocess import Popen, DEVNULL, STDOUT
from git_manager import GitManager
from config import OVERLEAF_PASSWORD, OVERLEAF_USER, PROJECTS_OVERLEAF, SAE_COUNTER_GITHUB, SAE_COUNTER_PATH, UNTRACKED_PATH


class HarpiaAeroCounter:
    LOG_HEAD = [
        'Words',
        'Non-Words',
        'Figures Files',
        'Fig. Words',
        'Non-Words Fig.',
        'Num. of Pages',
        'Num. of Special Pages',
        'Words in Math Mode'
    ]

    LOG_KEYS = [
        'words',
        'non_words',
        'fig_files',
        'fig_words',
        'non_words_fig',
        'npages',
        'n_special_pages',
        'math_words'
    ]

    def __init__(self):
        self.sae_counter_manager = GitManager(SAE_COUNTER_GITHUB, SAE_COUNTER_PATH)
        self.projects_list = PROJECTS_OVERLEAF
        self.content = {}
        for project in self.projects_list:
            project['repo'] = GitManager(
                project['url'],
                project['path'],
                urllib.parse.quote(OVERLEAF_USER),
                urllib.parse.quote(OVERLEAF_PASSWORD)
            )

    def compiler(self, project):
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

    def counter(self, project):
        Popen(
            ["python", "PyAeroCounter.py", "-i", "../"+project['path']+".pdf"],
            cwd=self.sae_counter_manager.path,
            stdout=DEVNULL,
            stderr=STDOUT
        ).wait()
        for fname in glob(os.path.join(self.sae_counter_manager.path, '*.txt')):
            os.rename(
                fname,
                os.path.join(UNTRACKED_PATH, project['path']+"_"+fname.split("/")[-1])
            )

    def loop(self):
        redo = False
        self.sae_counter_manager.pull()
        if (self.sae_counter_manager.has_changes):
            redo = True # Precisa atualizar tudo.
        for project in self.projects_list:
            project['repo'].pull()
            if project['repo'].has_changes or redo:
                print("{name}{spaces}mudou".format(name=project['name'], spaces=" "*(40-len(project['name']))))
                self.compiler(project)  # Compilando o PDF.
                self.counter(project)   # Contando as palavras.
            else:
                print("{name}{spaces}ok".format(name=project['name'], spaces=" "*(43-len(project['name']))))
            with open(os.path.join(UNTRACKED_PATH, project['path']+"_logfile.txt"), 'r') as fd:
                lines = fd.readlines()
                int_values = [int(s) for s in " ".join(lines).split() if s.isdigit()]
                self.content[project['path']] = dict(zip(HarpiaAeroCounter.LOG_KEYS, int_values))
                self.content[project['path']]['name'] = project['name']
        redo = False

    def print(self):
        print("\n")
        print("#"*230)
        print("#" + "\t\t".join(["\t\t\t"] + HarpiaAeroCounter.LOG_HEAD) + "   #")
        print("#" + "-"*228 + "#")
        for values in self.content.values():
            posfix = "\t" * int((29-len(values['name']))/8)
            print("# {name}{posfix}\t\t{words}\t\t{non_words}\t\t\t{fig_files}\t\t\t{fig_words}\t\t\t{non_words_fig}\t\t\t{npages}\t\t\t{n_special_pages}\t\t\t\t{math_words}\t             #".format(posfix=posfix, **values))
        print("#"*230)
        print("\n")


if __name__ == "__main__":
    harpiaAeroCounter = HarpiaAeroCounter()
    harpiaAeroCounter.loop()
    harpiaAeroCounter.print()
