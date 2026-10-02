# -*- coding: utf-8 -*-
import json
from _sweep_compare import GRID, master_codes
mset = set(master_codes)
print('--- zona de agosto (pos 60..130) ---')
for i in range(60, 131):
    if i >= len(GRID): break
    mark = 'MASTER ' if GRID[i] in mset else '  ???? '
    print(f'{i:3d} {mark} {GRID[i]}')
print()
print('--- nao-master DENTRO de 67..123 ---')
sus = [GRID[i] for i in range(67,124) if GRID[i] not in mset]
print(sus)
