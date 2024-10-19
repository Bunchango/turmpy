import random

class ColorEngine:
    def __init__(self):
        # Use a set to track unique colors, starting with black and white
        self.generated_colors = {(255, 255, 255), (0, 0, 0)}  # WHITE and BLACK

    def _generate_unique_color(self):
        """Generates and returns a new unique RGB color."""
        while True:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            if color not in self.generated_colors:
                self.generated_colors.add(color)
                return color  # Return the new unique color

    def generate_colors(self, n: int):
        """
        Generates 'n' unique colors. If 'n' is greater than the current number of
        generated colors, it will generate additional unique colors.
        If n is less, remove until match, but BLACK and WHITE are never removed.
        """
        if n > 256**3:  # Maximum possible unique RGB colors
            raise ValueError("Cannot generate more than 16,777,216 unique RGB colors.")

        # Generate unique colors until we have at least 'n' colors
        while len(self.generated_colors) < n:
            self._generate_unique_color()

        # If we have more than 'n' colors, remove excess but don't remove BLACK and WHITE
        while len(self.generated_colors) > n:
            # Convert set to a list and remove colors that are not BLACK or WHITE
            non_protected_colors = [color for color in self.generated_colors if color not in [(255, 255, 255), (0, 0, 0)]]

            if non_protected_colors:
                color_to_remove = non_protected_colors.pop()  # Remove an arbitrary non-protected color
                self.generated_colors.remove(color_to_remove)
            else:
                break  # No more non-protected colors to remove, break out of the loop

        # Return a list of the required number of unique colors
        return list(self.generated_colors)[:n]
