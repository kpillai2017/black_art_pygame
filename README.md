# README #
[Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)  

### Python port of Jazon Yamamoto's Black Art of Multi Platform Game Programming ###
This is a Python port of The Black Art of Multi Player Game Programming by Jazon Yamamoto. SDL functionality is wrapped within pygame.

### How do I get set up? ###

**Summary of set up**  
Development environment is **pyenv** and **direnv** on *Ubuntu*.
---
**Install and configure pyenv**  
1.Run ```bash sudo apt-get update && sudo apt-get upgrade```  
2.Run ```bash sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev git```  
3.Run ```bash curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash```  
4.Add this to **~/.bashrc** at the end of the file  
```bash
    export PATH="~/.pyenv/bin:$PATH"
    val "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
```
5.Run the following after restarting the console. The ressponse will be installed python versions.
```bash pyenv versions```  
---
**Install and configure direnv**  
1.Run ```bash sudo apt-get update && sudo apt-get upgrade```  
2.Run ```bash sudo apt-get install direnv```  
3.Run ```bash sudo apt-get install virtualenv```  
4.Add this to **~/.bashrc** at the end of the file  
```bash
    show_virtual_env() {
        if [ -n "$VIRTUAL_ENV" ]; then
            echo "($(basename $VIRTUAL_ENV))"
        fi
    }
    PS1='$(show_virtual_env)'$PS1
    eval "$(direnv hook bash)"
```  
7.Add this to **~/.direnvrc** at the end of the file  
```bash
    use_python() {
        local python_root=$(pyenv root)/versions/$1
        load_prefix "$python_root"
        if [[ -x "$python_root/bin/python" ]]; then
            layout python "$python_root/bin/python"
        else
            echo "Error: $python_root/bin/python can't be executed."
            exit
        fi
    }
```
---
**Set up your development folder**  
1.Run ```bash pyenv install 3.7.4``` or any other python version (run ```bash pyenv install --list``` for available versions to install)  
2.In your development folder, create **~/.envrc** file with content:
```bash use python 3.7.4```  
3.You'll need to type: **direnv allow** for direnv to access the **.envrc** file.  
4.Now, your python environment is set up! When you enter/exit the folder, the python virtual environment activates/deactivates automatically!  
5.In your development folder, type the following to install pygame (and other modules):
```bash
    pip install pygame
```
or
```bash
    pip install -r requiremnts.txt
```

