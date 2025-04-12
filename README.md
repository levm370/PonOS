## PonOS
*PonOS* - это *операционная система* на Python, требующая запуска через эмулятор PonosC16X2 (**PonOSBox**).\
Ну в общем всё на [яндех дзене канале](https://dzen.ru/chezafignya).\
Так же есть [сайт с релизами](https://levm370.github.io/ponos-info/).\
Для запуска нужно ввести в терминале:\
`python3 ponosbox ponos.py`\
Так же в PonOS можно компилировать C++ и др. а так же Python напрямую.\
Для этого скрипт должен лежать в директории system.\
Как запустить Python:\
`pwexec script.py` - или другой скрипт\
Другие языки запускать сложнее. Нужен скрипт компилятора, например, на BASH:\
```
#!/bin/bash
# Shebang обязательно
in=$1
out="ponos.a.out"
gcc $in -o $out
```
Его нужно положить в system.\
*нужно выполнить chmod для этого скрипта*\
Компилятор создан. Далее в терминале PonOS нужно выполнить:\
`write system/<ИМЯ_C_ФАЙЛА>.c`\
и ввести там код.\
Далее, выполняем: `export system/<ИМЯ_C_ФАЙЛА>.c`\
Готово. Вводим `hwexec <скрипт_компилятора> <имя_c-файла>` и перемещаем ponos.a.out в system.\
Для запуска вводим `hwexec ponos.a.out`.
