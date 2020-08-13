# Importing Necessary Libraries
import pygame as pg
import neat
import os, sys, random
pg.font.init() # Initialising Fonts

# Some Global Variables
WIN_WIDTH = 500
WIN_HEIGHT = 800
FLOOR = 600
STATS_FONT = pg.font.SysFont("comicsans", 25)
MAX_SCORE = 0
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)

# Initialising Pygame Window and Caption
WIN = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pg.display.set_caption("Flappy Bird")
gen = 0

# Load Images, Scale them and Store in Global Variables
BIRD_IMGS = [pg.transform.scale2x(pg.image.load(os.path.join("imgs", "bird1.png"))), pg.transform.scale2x(pg.image.load(os.path.join("imgs", "bird2.png"))), pg.transform.scale2x(pg.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pg.transform.scale2x(pg.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pg.transform.scale2x(pg.image.load(os.path.join("imgs", "base.png")))
BG_IMGS = pg.transform.scale2x(pg.image.load(os.path.join("imgs", "bg.png")))



# Bird Class
class Bird:
	IMGS = BIRD_IMGS # List of Bird Images
	MAX_ROTATION = 25 # Angle to Rotate when Jumping
	ROT_VEL = 20 # Rotation Velocity
	ANIM_TIME = 5 # Animation Time

	# Initialising Bird Class
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.tilt = 0
		self.tick_count = 0
		self.velocity = 0
		self.height = self.y
		self.img_count = 0
		self.img = self.IMGS[0]


	def jump(self):
		self.velocity = -9 # Jump 9 Pixels up
		self.tick_count = 0
		self.height = self.y


	def move(self):
		self.tick_count += 1 # For Managing Bird Position at every frame

		displacement = self.velocity * (self.tick_count) + 1.5 * (self.tick_count**2) # Formula for calculating displacement for Arc Trajectory

		# Controlling  Bird Position within the Limits
		if displacement >= 16:
			displacement = 16

		if displacement < 0 :
			displacement -= 2

		self.y = self.y + displacement 

		# if going up, tilt the bird upwards
		if displacement < 0 or self.y < self.height + 50:
			if self.tilt < self.MAX_ROTATION:
				self.tilt = self.MAX_ROTATION

		# else, tilt it upwards
		else :
			if self.tilt > -90:
				self.tilt -= self.ROT_VEL


	def draw(self, win):
		self.img_count += 1

		# Flapping of wings of the bird by switching between the images 1, 2 and 3
		# making it look like the bird is flapping wings
		if self.img_count <= self.ANIM_TIME:
			self.img = self.IMGS[0]
		elif self.img_count <= self.ANIM_TIME*2:
			self.img = self.IMGS[1]
		elif self.img_count <= self.ANIM_TIME*3:
			self.img = self.IMGS[2]
		elif self.img_count <= self.ANIM_TIME*4:
			self.img = self.IMGS[1]
		elif self.img_count <= self.ANIM_TIME*4+1:
			self.img = self.IMGS[0]
			self.img_count = 0

		if self.tilt <= -80:
			self.img = self.IMGS[0]
			self.img_count = self.ANIM_TIME*2

		# Rotating the image from Center point
		rotated_image = pg.transform.rotate(self.img, self.tilt)
		new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)
		win.blit(rotated_image, new_rect.topleft)

	# Masking the image pixel for perfect collision mathematics
	def get_mask(self):
		return pg.mask.from_surface(self.img)


class Pipe:
	GAP = 200 # Between Upper Pipe and Lower Pipe
	VEL = 5 # Velocity of pipes moving


	def __init__(self, x):
		self.x = x
		self.height = 0

		self.top = 0
		self.bottom = 0

		self.PIPE_TOP = pg.transform.flip(PIPE_IMG, False, True) # Flipping the Pipe Image for Upper Pipe
		self.PIPE_BOTTOM = PIPE_IMG
		self.passed = False # Pipe passed bird or not
		self.set_height()

	# Set pipe height randomly each time between 40 px to 450 px
	def set_height(self):
		self.height = random.randrange(50, 450, 20)
		self.top = self.height - self.PIPE_TOP.get_height()
		self.bottom = self.height + self.GAP

	# Pretty Self explanatory tbh
	def move(self):
		self.x -= self.VEL

	# This too...
	def draw(self, win):
		win.blit(self.PIPE_TOP, (self.x, self.top))
		win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))


	# Umm... I think I am pretty good at naming Functions
	def collide(self, bird):
		bird_mask = bird.get_mask()
		top_mask = pg.mask.from_surface(self.PIPE_TOP)
		bottom_mask = pg.mask.from_surface(self.PIPE_BOTTOM)

		# Top and Bottom Offset for Collision Calculation
		top_offset = (self.x - bird.x, self.top - round(bird.y))
		bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

		# point of contact for top and bottom pipe with bird
		b_point = bird_mask.overlap(bottom_mask, bottom_offset)
		t_point = bird_mask.overlap(top_mask, top_offset)

		# if collide, return true, else false
		if t_point or b_point :
			return True
		return False


class Base:
	VEL = 5 # Same as Pipe Velocity
	WIDTH = BASE_IMG.get_width() 
	IMG = BASE_IMG


	def __init__(self, y):
		self.y = y
		self.x1 = 0 # X coordinates for 1st instance of the Base Img
		self.x2 = self.WIDTH # for 2nd instance of the Base Img


	def move(self):
		self.x1 -= self.VEL
		self.x2 -= self.VEL

		# if 1st img moves out of the screen, place it behind the 2nd image for reappearing again
		if self.x1 + self.WIDTH < 0:
			self.x1 = self.x2 + self.WIDTH

		if self.x2 + self.WIDTH < 0:
			self.x2 = self.x1 + self.WIDTH


	def draw(self, win):
		win.blit(self.IMG, (self.x1, self.y))
		win.blit(self.IMG, (self.x2, self.y))


# Create GamePLay Window and render stats
def draw_window(win, birds, pipes, base, score, maxscore, gen, nn_shape, fitness, activation, input_values, output,weight, bias):
	win.blit(BG_IMGS, (0, -200))

	for pipe in pipes:
		pipe.draw(win)

# ------------------RIGHT STATS--------------------------------------
	score = STATS_FONT.render(f'SCORE : {str(score)}', 1, COLOR_BLACK)
	win.blit(score, (WIN_WIDTH - 10 - score.get_width(), 10))

	mxscore = STATS_FONT.render(f'MAX SCORE : {str(maxscore)}', 1, COLOR_BLACK)
	win.blit(mxscore, (WIN_WIDTH - 10 - mxscore.get_width(), 10 + (2 * score.get_height())))

	generation = STATS_FONT.render(f'GENERATION : {str(gen)}', 1, COLOR_BLACK)
	win.blit(generation, (WIN_WIDTH - 10 - generation.get_width(), 10 + (4 * score.get_height())))

	nnshape = STATS_FONT.render(f'NN SHAPE : {str(nn_shape)}', 1, COLOR_BLACK)
	win.blit(nnshape, (WIN_WIDTH - 10 - nnshape.get_width(), 10 + (6 * score.get_height())))

	pop = STATS_FONT.render(f'POPULATION : {str(len(birds))}', 2, COLOR_BLACK)
	win.blit(pop, (WIN_WIDTH - 10 - nnshape.get_width(), 10 + (8 * score.get_height())))
# -------------------------LEFT STATS---------------------------------
	fit = STATS_FONT.render(f'BEST FITNESS : {str(fitness)[:5]}', 1, COLOR_RED)
	win.blit(fit, (10, 10))

	activ = STATS_FONT.render(f'ACTIVATION : {str(activation).upper()}', 1, COLOR_RED)
	win.blit(activ, (10, 10 + (2 * activ.get_height())))

	inv = STATS_FONT.render(f'INPUT : {str(input_values)}', 1, COLOR_RED)
	win.blit(inv, (10, 10 + (4 * inv.get_height())))

	out = STATS_FONT.render(f'OUTPUT : {str(output)}', 1, COLOR_RED)
	win.blit(out, (10, 10 + (6 * out.get_height())))

	biases = STATS_FONT.render(f'BIAS : {str(bias)}', 1, COLOR_RED)
	win.blit(biases, (10, 10 + (8 * biases.get_height())))

	weights = STATS_FONT.render(f'WEIGHT : {str(weight)}', 1, COLOR_RED)
	win.blit(weights, (10, 10 + (10 * weights.get_height())))
	base.draw(win)
	for bird in birds:
		bird.draw(win)

	pg.display.update()


# Main Game Loop
def fitness_func(genomes, config):
    global WIN, gen, MAX_SCORE
    win = WIN

    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # bird object that uses that network to play
    # all at the same time, so that each has relative indices to each other
    nets = []
    birds = []
    ge = []

    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config) # Create a Feed Forward Neural Network for each Genome
        nets.append(net)
        birds.append(Bird(230,350))
        ge.append(genome)

    base = Base(FLOOR)
    pipes = [Pipe(600)]
    score = 0

    clock = pg.time.Clock()

    run = True
    while run and len(birds) > 0:
        clock.tick(30)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
                quit()
                break

        # Pipe Index for keeping track of the upcoming pipe
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():  # determine whether to use the first or second
                pipe_ind = 1                                                                 # pipe on the screen for neural network input
		
		# give each bird a fitness of 0.1 for each frame it stays alive
        for x, bird in enumerate(birds):
            ge[x].fitness += 0.1
            bird.move()

            # send bird location, top pipe locat
            input_values = (bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom))
            output = nets[birds.index(bird)].activate(input_values)

            if output[0] > 0.7:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
                bird.jump()

        base.move()

        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            # check for collision
            for bird in birds:
                if pipe.collide(bird):
                    ge[birds.index(bird)].fitness -= 1
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            if score > MAX_SCORE:
            	MAX_SCORE = score
            # can add this line to give more reward for passing through a pipe (not required)
            for genome in ge:
                genome.fitness += 5
            pipes.append(Pipe(600))

        for r in rem:
            pipes.remove(r)

        for bird in birds:
            if bird.y + bird.img.get_height() - 10 >= FLOOR or bird.y < -50:
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))
        
        max_score = MAX_SCORE
        nn_shape = [3, 1]
        fitness = genome.fitness
        activation = genome.nodes[0].activation
        weight = genomes[0][-1].connections[(-1, 0)].weight
        bias = genome.nodes[0].bias

        draw_window(WIN, birds, pipes, base, score, max_score, gen, nn_shape, fitness, activation, input_values, output, weight, bias)
    gen += 1


def run(config_file):
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

	popl = neat.Population(config)

	popl.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	popl.add_reporter(stats)

	winner = popl.run(fitness_func, 50)


if __name__ == '__main__':
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, "NEAT-CONFIG.txt")

	run(config_path)