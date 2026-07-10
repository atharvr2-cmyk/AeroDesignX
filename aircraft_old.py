import config


class Aircraft:

    def __init__(self):

        self.mass = config.MASS
        self.payload = config.PAYLOAD

        self.speed = config.CRUISE_SPEED

        self.range = config.RANGE
        self.endurance = config.ENDURANCE

        self.wing_area = config.WING_AREA
        self.aspect_ratio = config.ASPECT_RATIO
        self.taper_ratio = config.TAPER_RATIO

        self.cl = config.CL
        self.cd = config.CD

    @property
    def weight(self):
        return self.mass * 9.81