# import matplotlib.pyplot as plt
# from matplotlib import colors
# import numpy as np
#
# data = np.random.rand(10, 10)*20
#
# # create discrete colormap
# cmap = colors.ListedColormap(['red', 'blue','yellow'])
# bounds = [0,10,20]
# norm = colors.BoundaryNorm(bounds, cmap.N)
#
# fig, ax = plt.subplots()
# ax.imshow(data, cmap=cmap, norm=norm)
#
# # draw gridlines
# ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
# ax.set_xticks(np.arange(-.5, 10, 1))
# ax.set_yticks(np.arange(-.5, 10, 1))
#
# plt.show()


# import pygame
#
# # Define some colors
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# GREEN = (0, 255, 0)
# RED = (255, 0, 0)
#
# # This sets the WIDTH and HEIGHT of each grid location
# WIDTH = 20
# HEIGHT = 20
#
# # This sets the margin between each cell
# MARGIN = 5
#
# # Create a 2 dimensional array. A two dimensional
# # array is simply a list of lists.
# grid = []
# for row in range(10):
#     # Add an empty array that will hold each cell
#     # in this row
#     grid.append([])
#     for column in range(10):
#         grid[row].append(0)  # Append a cell
#
# # Set row 1, cell 5 to one. (Remember rows and
# # column numbers start at zero.)
# grid[1][9] = 1
#
# # Initialize pygame
# pygame.init()
#
# # Set the HEIGHT and WIDTH of the screen
# WINDOW_SIZE = [255, 255]
# screen = pygame.display.set_mode(WINDOW_SIZE)
#
# # Set title of screen
# pygame.display.set_caption("Array Backed Grid")
#
# # Loop until the user clicks the close button.
# done = False
#
# # Used to manage how fast the screen updates
# clock = pygame.time.Clock()
#
# # -------- Main Program Loop -----------
# while not done:
#     for event in pygame.event.get():  # User did something
#         if event.type == pygame.QUIT:  # If user clicked close
#             done = True  # Flag that we are done so we exit this loop
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             # User clicks the mouse. Get the position
#             pos = pygame.mouse.get_pos()
#             # Change the x/y screen coordinates to grid coordinates
#             column = pos[0] // (WIDTH + MARGIN)
#             row = pos[1] // (HEIGHT + MARGIN)
#             # Set that location to one
#             grid[row][column] = 1
#             print("Click ", pos, "Grid coordinates: ", row, column)
#
#     # Set the screen background
#     screen.fill(BLACK)
#
#     # Draw the grid
#     for row in range(10):
#         for column in range(10):
#             color = WHITE
#             if grid[row][column] == 1:
#                 color = GREEN
#             pygame.draw.rect(screen,
#                              color,
#                              [(MARGIN + WIDTH) * column + MARGIN,
#                               (MARGIN + HEIGHT) * row + MARGIN,
#                               WIDTH,
#                               HEIGHT])
#
#     # Limit to 60 frames per second
#     clock.tick(60)
#
#     # Go ahead and update the screen with what we've drawn.
#     pygame.display.flip()
#
# # Be IDLE friendly. If you forget this line, the program will 'hang'
# # on exit.
# pygame.quit()



import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
f = plt.figure()
f.set_figwidth(50)
f.set_figheight(50)
grid_size = 0.002
x1 = np.arange(-73.59, -73.55, grid_size)
y1 = np.arange(45.49, 45.530, grid_size)

# read coordinates from file and put them into two lists, similar to this
x_coordinates = np.random.uniform(x1.min(), x1.max(), size=8)
y_coordinates = np.random.uniform(y1.min(), y1.max(), size=8)
pivot_value = 1
# create a colormap with two colors, vmin and vmax are chosen so that their center is the pivot value
cmap = ListedColormap(['indigo', 'gold'])
# create a 2d histogram with xs and ys as bin boundaries
binvalues, _, _, _ = plt.hist2d(x_coordinates, y_coordinates, bins=[x1, y1], cmap=cmap, vmin=0, vmax=2*pivot_value)
print(plt.hist2d(x_coordinates, y_coordinates, bins=[x1, y1], cmap=cmap, vmin=0, vmax=2*pivot_value))

binvalues = binvalues.astype(int)
#print('vmax',binvalues.vmax)
print('x1_min',x1.min(),'x1.max',x1.max(),'y1_min',y1.min(),'y1.max',y1.max())
print('x1,y1',x1,y1)
print('length',len(x_coordinates))
print(x_coordinates)
print(y_coordinates)
print(binvalues)
for i in range(len(x1) - 1):
    for j in range(len(y1) - 1):
        plt.text((x1[i] + x1[i + 1]) / 2, (y1[j] + y1[j + 1]) / 2, binvalues[i, j],
                 color='white' if binvalues[i, j] < pivot_value else 'black',
                 ha='center', va='center', size=8)

plt.show()