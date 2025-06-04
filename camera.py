class Camera:
    def __init__(self, map_size, screen_size):
        self.position = (0, 0)
        self.scaling_factor = 1
        self.scaling_step = 0.1
        self.map_size = map_size
        self.screen_size = screen_size

    def return_render_coords(self):
        return ((-1 * self.map_size[0] // 2 - self.position[0]) * self.scaling_factor + self.screen_size[0] // 2, (-1 * self.map_size[1] // 2 - self.position[1]) * self.scaling_factor + self.screen_size[1] // 2)