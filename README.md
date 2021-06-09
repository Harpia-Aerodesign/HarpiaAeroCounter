# HarpiaAeroCounter
Contador de palavras para a Competição AeroDesign // Word counter for the Aerodesign Competition

Author:  Member of [Harpia Aerodesign](https://www.facebook.com/HarpiaAeroDesign)

            André Meneghelli Vale (andredalton@gmail.com)

## 1) WINDOWS: standalone application 

Windows is only for Counter Strike. If you want to fell pain, fell by yourself

## 2)  Dependencies

The python dependencies are on the file **requirements.txt**, to install you can run the follow command:

```bash
   pip install -r requirements.txt
```

 The LaTeX compiler dependencies are on **requirements.system**. Because I am a very lazy person I put the package **texmaker** and hope that all the LaTeX dependencies works fine. You could be able to install this dependencies with the follow command:

```bash
    xargs -a packages.txt sudo apt-get install
```

## 3) Configuration

There are no mysteries on configuration files, you just have to rename from ***config.sample.py*** to ***config.py***. 

```bash
    UNTRACKED_PATH = "repositories"

    COMPILER = "pdflatex"

    SAE_COUNTER_GITHUB = "https://github.com/comissao-aerodesign/PyAeroCounter.git"
    SAE_COUNTER_PATH = "PyAeroCounter"

    PROJECTS_OVERLEAF = [
        {
            'name': "<Project name>",
            'path': "<Project_folder>",
            'url': "https://git.overleaf.com/<YOUR_URL_OVERLEAF_GIT>"
        },
    ]

    OVERLEAF_USER = "<USER_NAME>"
    OVERLEAF_PASSWORD = "<PASSWORD>"
```

## 4) Running

After the instalation and configuration you must be able to run the counter manager with the follow command:

```bash
    python3 harpia_aero_counter.py
```

I recommend to use a python virtual environment to isolate the project dependencies from the native python installation.