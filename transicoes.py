import pygame
from pygame.surfarray import *
from pygame.locals import *


RES = (640,480)
COLOUR_MAP = [[]] * 256

def blinds(map, size, screen, fade):
    "Using a 256 colour palette, this function will draw a blinds effect accross the screen, leaving a black background..."


    # Claculate the width of each "blind"
    blind_cut = size[0]/8

    #:::::Initial setup for the first blind:::::



    # Draw a black column on the far right column of the screen
    map[size[0]-1][0:size[1]] = 0

    # Grab the colour on the column "inside" of what will become the blind 
    # (white in this example, but I'm trying to be palette agnostic)...
    current_col = map[size[0]-1][0]

    # Fill the "inside" of the blind 'fade' shades darker...
    for i in range (1,blind_cut):
        map[size[0]-(i+1)][0:size[1]]= current_col - fade

    # Fill the start of this blind with black so we have something to find in our loop...
    map[size[0]-blind_cut][0:size[1]]= 0



    #:::::Initial Blind Setup Completed:::::


    # That's the first blind created, we now go into our "find and fill" loop until the screen has transitioned...
    # We'll trip this sentinal when wecan figure out we're finished...
    fin = 0
    while not(fin):

        # From left to right of the screen, move in blind_cut steps...
        for i in range (0,size[0]-1,blind_cut):
            
            # And see if we've found the start of a blind (a black column)
            if (map[i][0]== 0):
                # We've found the start of a blind!
                j = 1

                # move inward over the black columns...
                # until we find the blind which we'll need to fill...
                while (j<blind_cut) and (map[i+j][0]==0):
                    j+=1
                


                #-------------------------------------------------------------------------------------
                # Here's where we do our 'exit' checks, and prevent any out of bounds surfarray access
                #-------------------------------------------------------------------------------------
                    
                # If we've traveresed the full width of a blind and found nothing to fill, we know 
                # we can ignore this one and continue with the loop...
                if (j == blind_cut):

                    # But! We need to make sure we're not at the far left of the screen...
                    # if that's the case, we know we're done here... :-)
                    if(i==0):
                        fin = 1
                        break
                    # Ok, the transition isn't complete yet, so we'll just jump out of this loop...
                    else:
                        break
                
                #-------------------------------------------------------------------------------------
                # Here's the "business" end of the blinds routine...
                #-------------------------------------------------------------------------------------
                
                
                # we've found the inside of the blind, so, we decrease it's width
                # by adding a black coloumn to the left and right of the blind... 
                map[i+j][0:size[1]] = 0
                map[(i+blind_cut)-(j)][0:size[1]] = 0
    

                # Now we've got to fill the inside of the blind, so grab it's current colour...
                current_col = map[i+j+1][0]

                # ...and fill the inside of the blind 'fade' shades darker...
                for k in range((i+j+1),(i+(blind_cut-j))-1):
                    map[k][0:size[1]] = current_col - fade


                # if we've reached the criteria where we make a new blind
                if j==5:
                    # start it off, this will give us something to trip over in the next iteration of the loop
                    map[i-blind_cut][0:size[1]]=0


                #-------------------------------------------------------------------------------------

        # Blit this iteration to the screen and show it...
        blit_array(screen, map)
        pygame.display.update()



































