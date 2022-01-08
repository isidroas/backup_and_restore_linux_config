- Undertand some suffixes like
    - .APPEND
    - .PREPEND
- Make tests for CI:
  - Docker?
- Functional programming
  - Make a common generator for restore.py and backup.py.
  - It could handle the skipping of some files
- Check that users exist
- Users overriding
    - At least one user should be mandatory in arguments
- Remove the option of allow non user configs (outside of /home/<user<) ?
  - This could simplify things
  - Also the argument could be the path, instead of a name that has not autocomplete
- No entiendo la manera de hacer backup de este: https://github.com/holman/dotfiles 
- El nombre que le pone la comunidad a este tipo de archivos de denomina dotfiles
  Ejemplos:
  - https://github.com/LukeSmithxyz/voidrice
  - https://github.com/jessfraz/dotfiles
  - https://github.com/amacgregor/dot-files
  - https://github.com/craftzdog/dotfiles-public

- Una utilidad que puede tener mi funcionalidad de agrupar dotfiles,
   - es que puedes compartir en github publicamente los tuyos, pero que tengas otro repo privado.
   - Separar el trabajo y lo personal

- La gente lo que hará es volcar la carpeta .dotfiles al systema, para ello no te hace falta tener un programa especial, pero para hacerlo en el sentido inverso (backup) si te hace falta