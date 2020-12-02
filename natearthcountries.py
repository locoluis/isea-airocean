from PIL import Image
import shapefile
import aggdraw
from airocean_isea import AirOceanISEA

"""
Requirements:

Pillow - https://python-pillow.org/
aggdraw - https://github.com/pytroll/aggdraw
shapefile - https://github.com/GeospatialPython/pyshp

Natural Earth shapefiles - https://www.naturalearthdata.com/downloads/10m-cultural-vectors/
- Admin 0 and Admin 1 - Countries without boundary lakes
(uncompress these files at the shapefiles folder)

"""

# Creates a map that's 2000 pixels tall
isea = AirOceanISEA(scale=1999.0/3.0)

im = Image.new("RGB", (isea.width, isea.height))

# I wish that aggdraw worked on indexed images.
draw = aggdraw.Draw(im)
draw.setantialias(False)

borderpen = aggdraw.Pen("#3366ff")
gridpen = aggdraw.Pen("#003366")
seabrush = aggdraw.Brush("#001122")
path = aggdraw.Path()

# Draw the sea and its borders
l = [(2, 0), (6, 0), (5, 3), (7, 3), (8, 0), (9, 3), (10, 0), (11, 3), (11, 6), (8, 6), (9, 9), (7, 9), (6, 6), (5, 9), (4, 8), (4, 6), (3, 7), (3, 9), (1, 9), (1.5, 7.5), (0, 6), (2, 6), (1, 3), (3, 3)]
first = True
for p in l:
	px = p[0] * isea.t_b / 2.0 * isea.t_d
	py = p[1] * isea.t_d / 3.0
	if first:
		path.moveto(px, py)
		first = False
	else:
		path.lineto(px, py)
draw.path(path, gridpen, seabrush)

# Draw the inner folding lines
ll = [
[(5, 3), (4, 0), (1.5, 7.5)],
[(2, 6), (3, 9)],
[(3, 3), (5, 9)],
[(4, 6), (5, 3), (6, 6), (7, 3), (8, 6), (9,3), (10, 6), (11, 3)],
[(8, 6), (7, 9)],
[(1, 3), (11, 3)],
[(2, 6), (11, 6)]
]
for l in ll:
	first = True
	for p in l:
		px = p[0] * isea.t_b / 2.0 * isea.t_d
		py = p[1] * isea.t_d / 3.0
		if first:
			path.moveto(px, py)
			first = False
		else:
			path.lineto(px, py)
	draw.path(path, gridpen, None)

# Draw the latitude-longitude grid
for i in range(35):
	lat = -85.0 + i * 5.0
	last = None
	path = None
	for j in range(14401):
		lng = -180.0 + j / 40.0
		p = isea(lng, lat)
		if (not last) or (not p) or (abs(last[0] - p[0]) > 2.0 or abs(last[1] - p[1]) > 2.0):
			if path:
				draw.path(path, gridpen, None)
			if p:
				path = aggdraw.Path()
				path.moveto(int(p[0]), int(p[1]))
		else:
			path.lineto(int(p[0]), int(p[1]))
		last = p
	if path:
		draw.path(path, gridpen, None)

for i in range(72):
	lng = -180.0 + i * 5.0
	last = None
	path = None
	for j in range(7201):
		lat = -90.0 + j / 40.0
		p = isea(lng, lat)
		if (not last) or (not p) or (abs(last[0] - p[0]) > 2.0 or abs(last[1] - p[1]) > 2.0):
			if path:
				draw.path(path, gridpen, None)
			if p:
				path = aggdraw.Path()
				path.moveto(int(p[0]), int(p[1]))
		else:
			path.lineto(int(p[0]), int(p[1]))
		last = p
	if path:
		draw.path(path, gridpen, None)

# Countries too small to be drawn, they're represented using circles
# This better be empty unless drawing a low-resolution map
small = [
"HK", "MO", "ME", "LB", "NC", "FJ", "KW", "TL", "BS", "VU", "FK",
"GM", "QA", "CY", "PS", "BN", "TT", "CV", "PF", "WS", "LU", "KM", "MU", "FO", "ST", "AN", "DM", "TO", "KI", "FM", "BH", "AD", "MP", "PW", "SC", "AG", "BB", "TC", "VC", "LC", "YT", "VI", "GD", "MT", "MV", "KY", "KN", "MS", "BL", "NU", "PM", "CK", "WF", "AS", "MH", "AW", "CW", "LI", "VG", "SH", "JE", "AI", "MF", "GG", "SM", "BM", "TV", "NR", "GI", "PN", "MC", "VA", "IM", "GU", "SG", "SX", "KN"
]
small = []

# Give country codes to each entry of the Natural Earth countries shapefile
codelist = [
"AW", "AF", "AO", "AI", "AL", "AX", "AD", "AE", "AR", "AM", "AS", "AQ", ("AU ATC", "AU_ATC"), "TF", "AG", "AU", "AT", "AZ", "BI", "BE", "BJ", "BF", "BD", "BG", "BH", "BS", "BA", ("CO BJN disputed", "CO_BJN"), "BL", "BY", "BZ", "BM", "BO", "BR", "BB", "BN", "BT", "BW", "CF", "CA", "CH", "CL", "CN", "CI", ("FR CLP", "FR_CLP"), "CM", "NIL", "CD", "CG", "CK", "CO", "KM", "CV", "CR", ("AU CSI", "AU_CSI"), "CU", "CW", "KY", ("CYN disputed", "CYN"), "CY", "CZ", "DE", "DJ", "DM", "DK", "DO", "DZ", "EC", "EG", "ER", "ESB", "ES", "EE", "ET", "FI", "FJ", "FK", "FR", "FO", "FM", "GA", "GB", "GE", "GG", "GH", "GI", "GN", "GM", "GW", "GQ", "GR", "GD", "GL", "GT", "GU", "GY", "HK", "HM", "HN", "HR", "HT", "HU", "ID", "IM", "IN", ("AU IOA", "AU_IOA"), "IO", "IE", "IR", "IQ", "IS", "IL", "IT", "JM", "JE", "JO", "JP", ("KZ KAB leased", "KZ_KAB"), ("IN KAS disputed", "IN_KAS"), "KZ", "KE", "KG", "KH", "KI", "KN", "KR", ("XK disputed", "XK"), "KW", "LA", "LB", "LR", "LY", "LC", "LI", "LK", "LS", "LT", "LU", "LV", "MO", "MF", "MA", "MC", "MD", "MG", "MV", "MX", "MH", "MK", "ML", "MT", "MM", "ME", "MN", "MP", "MZ", "MR", "MS", "MU", "MW", "MY", "NA", "NC", "NE", "NF", "NG", "NI", "NU", "NL", "NO", "NP", "NR", "NZ", "OM", "PK", "PA", "PN", "PE", ("PGA disputed", "PGA"), "PH", "PW", "PG", "PL", "PR", "KP", "PT", "PY", "PS", "PF", "QA", "RO", "RU", "RW", "EH", "SA", ("SCR disputed", "SCR"), "SD", "SS", "SN", ("CO SER disputed", "CO_SER"), "SG", "GS", "SH", "SB", "SL", "SV", "SM", ("SOL disputed", "SOL"), "SO", "PM", "RS", "ST", "SR", "SK", "SI", "SE", "SZ", "SX", "SC", "SY", "TC", "TD", "TG", "TH", "TJ", "TM", "TL", "TO", "TT", "TN", "TR", "TV", "TW", "TZ", "UG", "UA", "UM", "UY", "US", ("CU USG leased", "CU_USG"), "UZ", "VA", "VC", "VE", "VG", "VI", "VN", "VU", "WF", "WSB", "WS", "YE", "ZA", "ZM", "ZW",
]

# Color according to the country codes
colors = {
('AQ',): '#fff',
('UM', 'ESB', 'WSB', 'NIL', 'PGA', 'SCR'): '#aaa',
('FR', 'FR-CP', 'TL', 'PA', 'EC', 'BR', 'CL', 'HT', 'TT', 'DM', 'BB', 'AG', 'AT', 'RO', 'TR', 'AZ', 'HR', 'BE', 'AD', 'DK', 'GL', 'FO', 'PL', 'LV', 'JO', 'QA', 'KW', 'AF', 'NP', 'MM', 'MN', 'KH', 'JP', 'PH', 'BN', 'MV', 'SG', 'EG', 'MA', 'ML', 'TD', 'ER', 'GW', 'SL', 'GH', 'GQ', 'RW', 'KE', 'CG', 'ZM', 'ZA', 'TN', 'KM', 'PG', 'FJ', 'CK', 'GS', 'CW', 'BZ', 'VI', 'BL', 'BM', 'SJ', 'AX', 'X-KOS', 'XK', 'NF', 'TK', 'X-SOL', 'SOL', 'X-CYN', 'CYN'): '#C58879',
('CO', 'CO-BN', 'CO-SER', 'SV', 'US', 'CR', 'BO', 'PR', 'GU', 'MP', 'IE', 'NO', 'CZ', 'GR', 'UA', 'EE', 'LT', 'SI', 'RS', 'NC', 'LI', 'SM', 'VA', 'GP', 'MQ', 'RE', 'YT', 'WF', 'PF', 'CN', 'OM', 'IR', 'UZ', 'BD', 'ID', 'TH', 'PS', 'LB', 'HK', 'MO', 'LY', 'EH', 'NG', 'BF', 'GN', 'CF', 'BI', 'ET', 'AO', 'UG', 'MZ', 'SC', 'BW', 'CV', 'WS', 'NR', 'KY', 'US-G', 'TC', 'AI', 'BQ2', 'GF', 'JE', 'GI', 'HM'): '#E1A47B',
('HN', 'MX', 'JM', 'PE', 'GY', 'AR', 'BS', 'VC', 'KN', 'FI', 'ES', 'HU', 'AL', 'BG', 'IT', 'DE', 'IS', 'BY', 'BA', 'GE', 'KZ', 'X-KAB', 'TJ', 'CY', 'KP', 'IL', 'PK', 'IQ', 'YE', 'LK', 'BT', 'LA', 'MY', 'TW', 'AE', 'BH', 'MR', 'NE', 'GM', 'LR', 'TG', 'SD', 'SO', 'GA', 'CD', 'MW', 'ZW', 'SZ', 'MU', 'VU', 'FM', 'NU', 'KI', 'TV', 'MF', 'BQ1', 'PM', 'CC', 'GG', 'IM'): '#EAC791',
('AU', 'AU-AC', 'X-CSI', 'VE', 'CA', 'GT', 'NI', 'CU', 'DO', 'SR', 'PY', 'UY', 'VG', 'MS', 'SH', 'LC', 'GD', 'GB', 'FK', 'SE', 'SK', 'MD', 'MK', 'ME', 'RU', 'NL', 'AW', 'AN', 'LU', 'CH', 'PT', 'AM', 'MT', 'MC', 'SY', 'SA', 'TM', 'KG', 'IN', 'X-KAS', 'VN', 'KR', 'DZ', 'SN', 'CI', 'BJ', 'CM', 'SS', 'TZ', 'MG', 'NA', 'LS', 'DJ', 'ST', 'NZ', 'PN', 'SB', 'MH', 'TO', 'PW', 'AS', 'SX', 'BQ3', 'BV', 'CX', 'IO', 'TF'): '#F0E6BE'
}

# Paint in the countries
sf = shapefile.Reader("shapefiles/ne_10m_admin_0_countries_lakes")
records = sf.records()
shapes = sf.shapes()

centers = {}
for si in range(len(shapes)):
	centers[si] = None
	sh = shapes[si]
	codes = codelist[si]
	if type(codes) == tuple:
		codes, code3 = codes
	else:
		code3 = codes
	codes = codes.split(" ")
	code = codes[0]

	codes.append(code3)
	codes = set(codes)

	fill = '#00ff00';
	for k, v in colors.items():
		if set(k) & codes:
			fill = v
			break
	if fill == '#00ff00':
		print(records[si])
		
	cbrush = aggdraw.Brush(fill)
	path = aggdraw.Path()
	first = True
	i = 0
	last = None
	inside = False
	for p in sh.points:
		if p[1] < -89.95:
			if p[0] > 0:
				p = [180, -89.95]
			else:
				p = [-180, -89.95]
		q = isea(*p)
		if q:
			x = int(q[0])
			y = int(q[1])
			this = "%.1f,%.1f " % (x, y)
			if this != last:
				if first:
					path.moveto(x, y)
					first = False
				else:
					path.lineto(x, y)
			last = this
		i = i + 1
		if i in sh.parts or not q:
			last = None
			draw.path(path, cbrush, None)
			path = aggdraw.Path()
			first = True

	if not first:
		draw.path(path, cbrush, None)
		
	try:
		(slng, slat) = centroid(sh.points)
	except Exception as e:
		slat = slng = 0
		for p in sh.points:
			slng += p[0]
			slat += p[1]
		slng /= float(len(sh.points))
		slat /= float(len(sh.points))
	try:
		q = isea(slng, slat)
		centers[si] = (x, y)
	except Exception as e:
		print("<!-- BAD ", slng, slat, "-->")

# Paint in circles for small countries
for si in range(len(shapes)):
	sh = shapes[si]
	codes = codelist[si]
	if type(codes) == tuple:
		codes, code3 = codes
	else:
		code3 = codes
	codes = codes.split(" ")
	code = codes[0]
		
	if code not in small:
		continue
	xy = centers.get(si, None)
	if xy is not None:
		codes.append(code3)
		codes = set(codes)

		fill = '#00ff00';
		for k, v in colors.items():
			if set(k) & codes:
				fill = v
				break
		if fill == '#00ff00':
			print(codes)
			
		cbrush = aggdraw.Brush(fill)
		draw.ellipse((xy[0] - 4, xy[1] - 4, xy[0] + 4, xy[1] + 4), cbrush, None)

# Draw in specific subnational regions
sf = shapefile.Reader("shapefiles/ne_10m_admin_1_states_provinces_lakes")
records = sf.records()
shapes = sf.shapes()
n1codes = {
"NLD-5147": "BQ2", # Saba
"NLD-5148": "BQ3", # Sint Eustatius
"NLD-5149": "BQ1", # Bonaire
"BVT+00?": "BV",
"IOA-1928": "CC",
"IOA-2652": "CX",
"FRA-2000": "GF",
"FRA-4603": "GP",
"FRA-1442": "MQ",
"FRA-4601": "RE",
"NOR-901": "SJ",
"NZL-5472": "TK",
"FRA-4602": "YT"
}
for si in range(len(shapes)):
	sh = shapes[si]
	code = records[si][0]
	if code not in n1codes:
		continue
	code = n1codes[code]

	fill = '#00ff00';
	for k, v in colors.items():
		if code in k:
			fill = v
			break
	if fill == '#00ff00':
		print(code, records[si][0])
		
	cbrush = aggdraw.Brush(fill)
	path = aggdraw.Path()
	first = True
	i = 0
	last = None
	inside = False
	for p in sh.points:
		if p[1] < -89.95:
			if p[0] > 0:
				p = [180, -89.95]
			else:
				p = [-180, -89.95]
		q = isea(*p)
		if q:
			x = int(q[0])
			y = int(q[1])
			this = "%.1f,%.1f " % (x, y)
			if this != last:
				if first:
					path.moveto(x, y)
					first = False
				else:
					path.lineto(x, y)
			last = this
		i = i + 1
		if i in sh.parts:
			last = None
			draw.path(path, cbrush, None)
			path = aggdraw.Path()
			first = True

	if not first:
		draw.path(path, cbrush, None)
		
draw.flush()
im.save("natearthcountries.png")
