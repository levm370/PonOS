import pygame

class GameObject:
    def __init__(self, x, y, width, height, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

class Renderer:
    def __init__(self, game_objects):
        self.game_objects = game_objects
    
    def render(self, surface):
        for obj in self.game_objects:
            obj.draw(surface)

class Updater:
    def __init__(self, game_objects):
        self.game_objects = game_objects
    
    def update(self):
        #for obj in self.game_objects:
        #    obj.update()  # Допустим, каждый объект сам определяет свою логику обновления
        pass
class MainLoop:
    def __init__(self, renderer, updater):
        self.renderer = renderer
        self.updater = updater
        self.running = True
    
    def start(self):
        pygame.init()
        pygame.display.set_caption('Ponos Display')
        screen = pygame.display.set_mode((640, 480))
        
        clock = pygame.time.Clock()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.updater.update()
            self.renderer.render(screen)
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()

#if __name__ == "__main__":
#    objects = [
#        GameObject(0, 0, 50, 100),
#        GameObject(10, 0, 75, 25)
#    ]
#    
#    renderer = Renderer(objects)
#    updater = Updater(objects)
#    main_loop = MainLoop(renderer, updater)
#    main_loop.start()
