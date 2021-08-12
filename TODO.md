- submodule with pass
- add timestamp to backup folder, to allow multiple at same time
- Undertand some suffix like '.append_only' to not write the entire by the begining
- Hacer carpeta de test (utilizar docker? realmente no hace falta)
- Hacer generador común para restore y backup, en el que el skip de los ficheros sea transparente
- Users overriding
    - At least one user should be mandatory in arguments
    - How to specify a positional multiple argument? using commas?
        'backup  ~/home_config_files/src  _any_user,isidro'
