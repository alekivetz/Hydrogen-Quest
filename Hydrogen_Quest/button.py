class Button:
    def __init__(self, pos, text_input, font, base_colour, hover_colour):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_colour, self.hover_colour = base_colour, hover_colour
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_colour)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        if (position[0] in range(self.text_rect.left, self.text_rect.right)
                and position[1] in range(self.text_rect.top, self.text_rect.bottom)):
            return True
        return False

    def change_colour(self, position):
        if (position[0] in range(self.text_rect.left, self.text_rect.right)
                and position[1] in range(self.text_rect.top, self.text_rect.bottom)):
            self.text = self.font.render(self.text_input, True, self.hover_colour)
        else:
            self.text = self.font.render(self.text_input, True, self.base_colour)