from ctypes import *
from mmap import *

class Peripheral:
	class Readings(Structure):
		_fields_ = [
			("temperature_brain", c_ushort),
			("temperature_cns", c_ushort),
			("distance_floor", c_ushort),
			("distance_front", c_ushort),
			("acceleration", c_ushort * 3)
		]

	def __init__(self, pipe_path, shm_path):
		self.pipe = open(pipe_path, 'rb')
		with open(shm_path, 'rb') as shm_file:
			self.shm = mmap(shm_file.fileno(), 16, access=ACCESS_READ)
		self.readings = Readings.from_buffer(self.shm)

	def __enter__(self):
		return self

	def __exit__(self):
		self.close()

	def close(self):
		self.pipe.close()
		self.shm.close()

	def set_servo_pos(self, servo, pos):
		self.pipe.write(bytes(SYNCH, SET_SERVO | id, pos * 0xFF))

	def set_servo_power(self, servo, power):
		self.pipe.write(bytes(SYNCH, (ENABLE_SERVO if power else DISABLE_SERVO) | id))

	def set_wheels(self, value):
		self.pipe.write(bytes(SYNCH, SET_WHEELS, value)) #TODO

	def set_eyecolor(self, color):
		if len(color) != 3:
			raise TypeError("invalid color format")
		self.pipe.write(bytes(SYNCH, SET_EYECOLOR, *color))
