class EwVector2D:
	vector = [0, 0]

	def __init__(self, vector):
		self.vector = vector

	def scalar_product(self, other_vector):
		result = 0

		for i in range(2):
			result += self.vector[i] * other_vector.vector[i]

		return result

	def add(self, other_vector):
		result = []

		for i in range(2):
			result.append( self.vector[i] + other_vector.vector[i] )

		return EwVector2D(result)

	def subtract(self, other_vector):
		result = []

		for i in range(2):
			result.append( self.vector[i] - other_vector.vector[i] )

		return EwVector2D(result)

	def norm (self):
		result = self.scalar_product(self)
		result = result ** 0.5
		return result

	def normalize(self):
		result = []

		norm = self.norm()

		if norm == 0:
			return EwVector2D([0, 0])

		for i in range(2):
			result.append(round(self.vector[i] / norm, 3))

		return EwVector2D(result)
