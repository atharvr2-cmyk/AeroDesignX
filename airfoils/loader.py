"""
Airfoil Loader

Loads airfoil coordinates from a .dat file.
"""


class AirfoilLoader:
    def __init__(self, filepath):
        self.filepath = filepath

    def load_coordinates(self):
        """
        Load (x, y) coordinates from a DAT file.
        """

        coordinates = []

        with open(self.filepath, "r") as file:

            lines = file.readlines()

            # Skip the title line
            for line in lines[1:]:

                parts = line.split()

                if len(parts) == 2:

                    x = float(parts[0])
                    y = float(parts[1])

                    coordinates.append((x, y))

        return coordinates