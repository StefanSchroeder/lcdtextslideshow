#! /usr/bin/env python

# Use a small window to display text files in slideshow fashion.
# The files must match a filename pattern and are shown for a 
# couple of seconds. The script quits after a longer time.
import pygame
import glob
import sys

WIDTH = 480
HEIGHT = 320
AUTOQUIT_SECONDS = 20
NEXTSLIDE_SECONDS = 3
FONT_SIZE = 24
BACKGROUND_COLOR = (255, 255, 255)
FOREGROUND_COLOR  = (0,0,0)
FILE_PATTERN = "f*.txt"
YDELTA = FONT_SIZE
XOFFSET = 0 # left margin
SLIDECHANGEEVENT = pygame.USEREVENT + 1
QUITEVENT = pygame.USEREVENT + 2

Current_slide = 0
Page = []

######################################################################
def debug_string(s):
    print(s)

######################################################################
def make_font(fonts, size):
    available = pygame.font.get_fonts()
#    print available
    choices = map(lambda x:x.lower().replace(' ', ''), fonts)
    for choice in choices:
        if choice in available:
            return pygame.font.SysFont(choice, size)
    debug_string("The configured font is not available. Pick one from this list:")
    print(available)
    debug_string("Falling back to system default.")
    return pygame.font.Font(None, size)
    
######################################################################
def create_text(text, fonts, size, color):
    font = make_font(fonts, size)
    image = font.render(text, True, color)
    return image

######################################################################
def slidechange(updatevalue):
    global Current_slide
    global Page
    if updatevalue == 0:
        Current_slide = 0
    else:
        Current_slide = Current_slide + updatevalue
    Current_slide = Current_slide % NUMBER_OF_PAGES

    debug_string("Switching to slide: " + str(Current_slide))
    screen.fill(BACKGROUND_COLOR)
    line = 0
    for t in Page[Current_slide]:
        #t.get_height() 
        screen.blit(t, (XOFFSET, line*YDELTA ))
        line+=1
    pygame.display.flip()

######################################################################
def fetch_filecontent(filename):
    with open(filename) as f:
        content = f.readlines()
    
    # Remove literal newline
    content = [x.strip() for x in content] 
    # Remove empty lines
    content = [x for x in content if x != ""]
    
    texts = []
    for t in content:
        texts.append(create_text(t, font_preferences, FONT_SIZE, FOREGROUND_COLOR))
    return texts

######################################################################

all_files = sorted(glob.glob(FILE_PATTERN))

if not all_files:
    print("FATAL: There are no text files matching the pattern for display.")
    sys.exit()

NUMBER_OF_PAGES = len(all_files)
debug_string("Number of pages: " + str(NUMBER_OF_PAGES))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
clock = pygame.time.Clock()
done = False

font_preferences = [ "liberationsansnarrow", "free serif" ]

for filename in all_files:
    debug_string(filename)
    Page.append(fetch_filecontent(filename))

pygame.time.set_timer(SLIDECHANGEEVENT,NEXTSLIDE_SECONDS * 1000)
pygame.time.set_timer(QUITEVENT, AUTOQUIT_SECONDS  * 1000)

slidechange(0)

while not done:
    for event in pygame.event.get():

        if event.type == SLIDECHANGEEVENT:
            slidechange(+1)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            slidechange(+1)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            slidechange(-1)
        if event.type == QUITEVENT: 
            done = True
        if event.type == pygame.QUIT: 
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True
        if event.type == pygame.MOUSEBUTTONUP:
            (x,y) = pygame.mouse.get_pos()
            if x<WIDTH/2:
                slidechange(-1)
            else:
                slidechange(+1)

    clock.tick(5)

