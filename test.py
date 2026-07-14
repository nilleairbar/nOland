import pygame, sys, random

class main:
    def __init__(self):

        pygame.init()
        pygame.display.set_caption("Physics Visualizer") #window caption (name of the window)
        self.particles = []
        self.dispColour = (32, 34, 46)
        self.scaleFactor = 6
        self.windowSize = (1280,720) #Screen res
        self.gameWindow = pygame.display.set_mode((self.windowSize)) #set display
        self.clockObject = pygame.time.Clock()
        self.mousePressed = False
        self.pixelWindow = pygame.Surface((tuple(ii//self.scaleFactor for ii in self.windowSize)))

    def createParticle(self):
        self.colours={0:(255, 247, 93),1:(255, 192, 31),2:(254, 101, 13),3:(230, 123, 57),4:(243, 60, 4),5:(218, 31, 5),6:(102, 8, 8),7:(42, 44, 56),8:(32, 34, 46),9:(32, 34, 46),10:(32, 34, 46),11:(32, 34, 46)}
        self.locaiton = [ii//self.scaleFactor for ii in pygame.mouse.get_pos()]
        self.velocity = ((random.randint(0,50)/100 - 0.25), -0.25)
        self.timer = random.randint(1,4)/20
        self.particles.append([self.locaiton, self.velocity, self.timer])

    def run(self):
        while True:

        #------------ EXIT THE GAME WHEN QUIT PRESSED ------------

            for event in pygame.event.get():
                if event.type == pygame.QUIT: #get input
                    pygame.quit()
                    exit() #use sys calls to exit

        #------------ MAIN GAME LOOP -----------------------------

            if pygame.mouse.get_pressed()[0]:
                for ii in range(3):
                    self.createParticle()

            for particle in reversed(self.particles):
                if particle[2] >= 3:
                    self.particles.remove(particle)
                particle[0][0] += particle[1][0] - random.randint(0,10)/50
                particle[0][1] += particle[1][1] - random.randint(0,20)/20
                particle[2] += 0.1 + random.randint(0,2)/10
                pygame.draw.circle(self.pixelWindow, (self.colours[int(particle[2]+random.randint(0,1))]), particle[0], particle[2])


        #------------ UPDATE THE DISPLAY SURFACE FOR 120 FPS ------

            self.gameWindow.blit(pygame.transform.scale(self.pixelWindow, self.windowSize), (0,0))
            pygame.display.update()
            self.pixelWindow.fill(self.dispColour)
            self.clockObject.tick(30) #Run at 60 fps

if __name__ == "__main__":
    main().run()