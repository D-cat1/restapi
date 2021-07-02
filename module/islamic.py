import json
from pathlib import Path




def suratJSON(nosurat):
    no = int(nosurat)
    if no > 114:
        return {'error': True, 'Alasan': 'melebihi maksimum surat, nomor surat terakhir adalah 114'}
    else:
        filop = open('./module/surah/{}.json'.format(nosurat))
        return json.load(filop)