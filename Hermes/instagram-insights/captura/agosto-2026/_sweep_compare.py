# -*- coding: utf-8 -*-
import json, glob, os

GRID = ["DdHpheEGqK7","DdHb-QSA-Yk","DdHGTtXOHYI","DdG5vckRIDL","DdG2xo0g7H-","DclV0zcAUvH","DdF6nVitWpT","DdFvWYTt-Tt","DdFrbu6GzuQ","DdFdmIZttLZ","DdFXhdwp0L9-io7p3GXQboCHTN3BgsY_AtwXW00","DdFWnN_PIwX","DdFTPT0A6Ae","DdFB51QG1ab","DdEiFACRYd2","DdE3oLJAJHT","DdEt0rCNQ2D","DdEpSEvus9p","DdEmjK1EYQr","DdEYqAjlLOl","DdEWFKxmy3s","DdEOoeIA-Sy","DdD49Zym7Mn","DdC416etoOC","DdCOVv_C4E0","DdCLZybG5H0","DdBz6CURtK1","DdBvu4bmxMN","DclVoHkAc3R","DdBjGEym9yG","DdBh4HAGzy2","DdBUceIG8ZI","Dc__Me5v2ff","Dc_3WgKgiL2","Dc_0Qpzv_EK","DcbEPp2gwNj","Dc882sqOh4s","Dc6RWcvjngh","Dc6Ms-bvK-T","DcbEHlnA9uZ","Dc4jAUhG6O3","Dc4b0uqG1QH","Dc38Jj4xAVM","Dc3r-ZXP03B","Dc3onWLu4B0","Dc3bXQMAa7y","DclVejgguEv","Dc3BKykC_Tu","Dc1mz9Km1eJ","Dc1mvTHmz4l","Dc1lrmhyNpw","Dc1kWfYm75I","Dc1hQqGAeAK","Dc1emstG-Bq","Dc1Y4iXRR9X","Dc1VZw2GxF2","Dc1BgNyP3K0","DcbECTUAleR","Dc0v-ghAAmZ","Dczgro-tPe6","DczPZVhRCmy","DcySkdsPcLQ","DclVRnSg4Sm","Dcv1w1jvZT2","DcbD8kGAZY3","DcvigiDmx09","Dcrgb9wP9LW","DcrgQC6gknC","DcmUAaAG3Pi","DcmSbnuG9E-","DcmMX4pvjg7","DcmHJv_G-0A","Dcl1hMpDirN","DcliQzRDjNM","DclTCCwm8ff","DclSk4fG8C1","DclREC4m2H4","Dcjs2R4G_fX","DcjUaHrjhxv","Dchm6kFDjxS","DchK9ycv_Tu","DchIji9m9Ac","Dcg571dmzBL","Dcg2HcQm08f","Db-7_-OOxRu","DcdwpbfPsgs","DccD4y_m_vZ","DccDC3EG62U","DcbmO6GPfhb","DcbJmepx1nq","DcUSK-YAmSq","DcUJGqJG3tO","DcUEyDAgrbq","DbdwBOBOVJt","DcO_l7tAO80","DcOO0TDmyOI","DcMk8Krm62J","DcMIq5HDsYI","DcL6lpcjuj9","DcL1LKyDuDC","DcJ6tS4g0UF","DcJiRyDAzCg","DcCPbyLGzGd","DcCKmiUmxNg","Db_sK_am5Pd","Db_kkgSmw3s","DbdvwQLu4_o","Db-8Ogujpnd","Db-7sWxjt1W","Db-4DVIjkeD","Db9HcT8mxoP","Db83W6xKhbg","Db83BGyK7QT","Db8MNHGm5-k","Db6VNKkG0MC","Db6JsbUAFMa","Db5x5YFDhuk","Db5hQOLAmGU","DbdvooJOi2n","DbviPQ7jvsB","DbtOoFrjpJv","DbqfO-Ou0Qu","DbodANdm0Xy","Dbd6DYGA0y3","DberkiZtHhF","Dbd5-zNg1Ua","DaQjsu8AXoa","DbWYfocgr_e","DaQjl4OgUmt","DbN-z1yDrbv","DbJqmJHm40v","DbJNIiZG3PS","DbGtd7LA0RQ","DZ5duaUgszr","DbCASg0m0CY","Da6HF0UA0KB","Da5Y6QShckE","Da28kRAuJee","Da26cpKBvX8","DZ5dlG6gMXo","Da2kB89EXhL"]

master = json.load(open('../_acirv_agosto_progresso.json', encoding='utf-8'))
cands = master['candidatos'] if isinstance(master, dict) else master
def code_of(c):
    if isinstance(c, dict): return c.get('shortcode') or c.get('code')
    return c if isinstance(c, str) else None
master_codes = [code_of(c) for c in cands]
grid_set = set(GRID)

print('GRID total:', len(GRID))
print('MASTER total:', len(master_codes))
print('MASTER fora do grid:', [c for c in master_codes if c not in grid_set])
gmn = [c for c in GRID if c not in set(master_codes)]
print('GRID fora do master (candidatos a fora-de-janela/miss):', len(gmn))
print(gmn)
# índice do primeiro/último dentro do master na ordem do grid (reverse-chron)
positions = {c:i for i,c in enumerate(GRID)}
in_master_pos = sorted(positions[c] for c in master_codes if c in positions)
print('master no grid de pos', min(in_master_pos), 'a', max(in_master_pos))
print('vizinhos: antes=', GRID[min(in_master_pos)-1] if min(in_master_pos)>0 else None,
      '| depois=', GRID[max(in_master_pos)+1] if max(in_master_pos)+1<len(GRID) else None)
