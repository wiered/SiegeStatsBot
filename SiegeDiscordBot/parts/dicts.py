"""
--- This file just contains some dictionaries
"""

import json

with open('roles_Ids.json', encoding='utf-8') as json_file:
    roles_Ids = json.load(json_file)

ranks_pics = {
	'No matches played this season': 'https://img.apitab.com/plain/quality:50/resize:fit:0:250/bG9jYWw6Ly8vMjUyYWRhNjMtNDQzOS00ZmI3LWIzZjktNDY0YWZlNTA3MGY2.webp',
	'unranked'                     : 'https://img.apitab.com/plain/quality:50/resize:fit:0:250/bG9jYWw6Ly8vMjUyYWRhNjMtNDQzOS00ZmI3LWIzZjktNDY0YWZlNTA3MGY2.webp',
	'copper'                       : 'https://img.apitab.com/plain/quality:50/resize:fit:0:250/bG9jYWw6Ly8vNmE5MDg5N2MtYmE4MS00ZDIzLWJkZjAtMDQ3MmI2YjRiOGQ4.webp',
	'bronze'                       : 'https://img.apitab.com/plain/quality:50/resize:fit:0:250/bG9jYWw6Ly8vNDllOTQ2N2MtN2E5Yy00ODA2LWIxNDktMWMwMWQ5OTRkNDNh.webp',
	'silver'                       : 'https://img.apitab.com/plain/quality:50/resize:fit:0:250/bG9jYWw6Ly8vNGJjOWM5MmQtYTJiMS00ODA4LWIxZjEtMTBmZDFiMThjM2Ux.webp',
	'gold'                         : 'https://img.apitab.com/plain/quality:50/resize:fit:0:250/bG9jYWw6Ly8vNGZlZGEwOGQtNjVlOC00NWY3LTg4OGYtMGVkYTcyZDdmMGMw.webp',
	'platinum'                     : 'https://img.apitab.com/plain/quality:50/resize:fit:0:250/bG9jYWw6Ly8vODQxZjViM2YtYTI2ZC00NWI5LWE3N2EtYTg4MjljNzMxMDFj.webp',
	'diamond'                      : 'https://img.apitab.com/plain/quality:50/resize:fit:0:250/bG9jYWw6Ly8vNGI3YmJhZTgtZTcyMC00ZTg3LWFjNjQtM2NlNmZiODUxYjJk.webp',
	'champion'                     : 'https://img.apitab.com/plain/quality:50/resize:fit:0:250/bG9jYWw6Ly8vZTFmYzZlYjItOGM1OS00OTY2LWE0OTgtZjBiMTQ0MDEwMGMw.webp'
}

ranks = ["No matches played this season", "unranked", "copper", "bronze", "silver", "gold", "platinum", "diamond", "champion"]