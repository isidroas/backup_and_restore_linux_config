- submodule with pass
- add timestamp to backup folder, to allow multiple at same time
- Undertand some suffix like '.append_only' to not write the entire by the begining
- Hacer carpeta de test (utilizar docker? realmente no hace falta)
- https://realpython.com/python-pathlib/
- Usuarios
    - add other users in /home that overwrites configurations in \_any_user
    - Si no se especifica algun usuario, cogerlo de $USER 
    ```bash
    apply_and_backup /    src   --source-user   isidro             --target-user   isidro,all_users 
    # si ese archivo no existe en isidro, se mira en all_users, si tampoco existe, no se copia
    
    apply_and_backup src  /     --source-user   isidro,all_users   --target-user   isidro
    ```
    - Implementacion
    ```python
    def exists_in_other_higher_priority_user(file_path,list_of_users):
        user = get_user(file_path)
    
        index_actual_user = list_of_users.index(user)
        higher_level_users = list_of_users[index_actual_user+1:]
        for user in higher_level_users:
            new_path, _ = change_path(file_path, user) 
            if os.file_exists(new_path):
                return True
    
        return False
    
    
    
    for file_path in os.walk( smaller_dir ):
        user = get_user(file_path)
        if not user in wanted_users:
            break
    
        if exists_in_other_higher_priority_user(file_path):
            break
    
        # Copy from source to dest
        # we need to transform the path of dest, to take into account the users
    ```
- Pseudocodigo
```
for file in os.walk(iteration_directory):
    iteration_user = get_user(file)
    if not iteration_user in iteration_priority or file_existis_in_higher_priority_user:
        break

    if iterate_over_source:
        file_src = file
        file_dst = change_user(file, generic_user)
    else
        file_dst = file
        file_src = change_user(file, generic_user)

    copy(file_src, folder(file_dst))
```
