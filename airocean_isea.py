from pyproj import Proj, transform
import math

class AirOceanISEA:
	t_b = 2.0 / math.sqrt(3.0)
	t_s = 10000000.0 / 1.5
	t_s = 9980570.124229396 / 1.5
	t_s = 9980600.0 / 1.5
	t_s = 9980590.04 / 1.5

	combos = [(1, 1, 0), (2, 2, 0), (3, 3, 0), (4, 4, 0), (5, 5, 0), (1, 1, 1), (2, 1, 1), (2, 2, 1), (3, 2, 1), (3, 3, 1), (4, 3, 1), (4, 4, 1), (5, 4, 1), (5, 5, 1), (6, 5, 1), (2, 1, 2), (3, 2, 2), (4, 3, 2), (5, 4, 2), (6, 5, 2)]

	tra = [
	#	dx	dy	a
	(	5,	1,	-1	),
	(	8,	2,	0	),
	(	10,	2,	0	),
	(	3,	1,	1	),
	(	4,	2,	0	),
	(	6,	4,	0	),
	(	7,	5,	0	),
	(	8,	4,	0	),
	(	9,	5,	0	),
	(	10,	4,	0	),
	(	11,	5,	0	),
	(	2,	4,	0	),
	(	3,	5,	0	),
	(	4,	4,	0	),
	(	5,	5,	0	),
	(	7,	7,	0	),
	(	8,	8,	1	),
	(	2,	8,	-1	),
	(	3,	7,	0	),
	(	5,	7,	0	),
	(	1,	7,	-1	),
	(	4,	8,	-1	)
	]

	def __init__(self, scale = 600.0):
		self.p1 = Proj(proj='longlat', datum='WGS84', ellps='WGS84')
		self.p2 = Proj(proj='isea', mode='plane', lon_0=-2.5, lat_0=2.5, azi=7.5)
		self.t_d = scale
		self.height = int(math.ceil(scale * 3. + 1.))
		self.width = int(math.ceil(scale * 5.5 * self.t_b + 1.))
	
	def __call__(self, lng, lat):
		p = transform(self.p1, self.p2, lng, lat)
		if math.isnan(p[0]) or math.isnan(p[1]):
			return None
		px = (p[0] / self.t_s + self.t_b * 2.5)
		py = (1.5 - p[1] / self.t_s)
		h = int(py)
		if h == 0:
			f = 1 + int(px / self.t_b)
			g = f
		elif h == 2:
			g = int(px / self.t_b + 0.5)
			f = g + 1
		else:
			f = int(0.5 + px / self.t_b + py / 2.0)
			g = int(1.5 + px / self.t_b - py / 2.0)
		try:
			tri = self.combos.index((f, g, h))
		except:
			print(i, j, lat, lng, px / self.t_b, py, f, g, h)
			return None
		ii = tri
		if tri >= 5 and tri < 15:
			ii = (tri - 5) // 2 + 10 - (tri % 2) * 5
		cx = (0.5 + ii % 5 + (ii // 10) * 0.5) * self.t_b
		cy = (2 - (ii // 10) + (ii // 5) * 2) / 3.0

		if (f, g, h) == (4, 3, 1) and px >= 3.0 * self.t_b:
			tri = 20
		elif (f, g, h) == (5, 4, 2) and px >= 4.0 * self.t_b and py >= 7.0 / 3.0 - (px / self.t_b - 4.0) / 1.5:
			tri = 21

		# dx, dy en coordenadas simplificadas; a en π/3
		dx, dy, a = self.tra[tri]
		qx = math.cos(a * math.pi / 3.0) * (px - cx) - math.sin(a * math.pi / 3.0) * (py - cy) + dx * self.t_b / 2.0
		qy = math.sin(a * math.pi / 3.0) * (px - cx) + math.cos(a * math.pi / 3.0) * (py - cy) + dy / 3.0

		return ((qx * self.t_d, qy * self.t_d))
