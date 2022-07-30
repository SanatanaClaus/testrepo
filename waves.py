#wave propogation in a medium



import numpy as np
import pygame ,sys,math







#consider a grid of length*length element:

HEIGHT = 400
WIDTH = 400 #note that the height and width necessarily have to be divided by length of the elements
LENGTH = 5
DROPOFF = 0.1
SCREEN = dict() #the dictionary that holds all the positions and the oscillator objects
MAX_AMPLITUDE  = 5
POSITIONS = SCREEN.keys()
DIF = np.array([[LENGTH,LENGTH],[LENGTH,-LENGTH],[-LENGTH,LENGTH],[-LENGTH,-LENGTH],[0,LENGTH],[0,-LENGTH],[LENGTH,0],[-LENGTH,0]],dtype = np.int16)
TDIF = np.concatenate((2*DIF , np.array([[-2*LENGTH,LENGTH],[-2*LENGTH,-LENGTH],[-LENGTH,2*LENGTH],[LENGTH,2*LENGTH],[2*LENGTH,LENGTH],[2*LENGTH,-LENGTH],[LENGTH,-2*LENGTH],[-LENGTH,-2*LENGTH]])))

NORM2 = 1

class PositionError(Exception):
        def __str__(self):
                return "The oscillators can't be added as they are in different psoitions"
                pass



class oscillator():

        


        def __init__(self,position,amplitude) -> None:
                self.amplitude = amplitude 
                self.position = np.array(position,dtype =np.int16)
                self.position_x,self.position_y = position
                pass

        def propogate(self): #propogates the amplitude
                if self.amplitude == 0:
                        return np.array([])                
                a= np.array([oscillator(self.position - x,self.amplitude*DROPOFF) for x in DIF])
                a=np.concatenate((a,np.array([oscillator(self.position - x,self.amplitude*-DROPOFF) for x in TDIF])))
                #print(a.shape)
                self.amplitude = 0 
                return a

        def __add__(self,other):
                if type(other) != type(self):
                        raise TypeError
                if np.array_equal(self.position ,other.position) == False:
                        raise PositionError
                return oscillator(self.position,self.amplitude+other.amplitude)
        pass


        def __sub__(self,other):
                if type(other) != type(self):
                        raise TypeError
                if np.array_equal(self.position ,other.position) == False:
                        raise PositionError
                return oscillator(self.position,self.amplitude - other.amplitude)
        pass


#hsv to color converter
#to map the amplitude the intensituy in  the color 
def rgbtuple(h,s,v):
        def hsv_to_rgb(h, s, v):
                if s == 0.0: return (v, v, v)
                i = int(h*6.) # XXX assume int() truncates!
                f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
                if i == 0: return (v, t, p)
                if i == 1: return (q, v, p)
                if i == 2: return (p, v, t)
                if i == 3: return (p, q, v)
                if i == 4: return (t, p, v)
                if i == 5: return (v, p, q)

        return tuple(round(i*255) for i in hsv_to_rgb(h,s,v))

def amplitudemapper(amp):
        pass
        if amp>=0:
                return rgbtuple(0.1,0.9,(math.atan(3*amp/NORM2)*2/math.pi))
        else:
                return rgbtuple(0.9,0.9,(math.atan(-3*amp/NORM2)*2/math.pi))



#to initialize all the elements at zero amplitude.

def initialize():
        #a = HEIGHT // LENGTH
        #b = WIDTH // LENGTH

        for x in range(HEIGHT)[::LENGTH]:
                for y in range(WIDTH)[::LENGTH]:
                        SCREEN.update({f"{x},{y}":oscillator((x,y),0)})
                        
        pass



#execution in pygame
pygame.init()
screen =  pygame.display.set_mode((HEIGHT,WIDTH))
pygame.display.set_caption("Waves by means of Young propogation")
clock = pygame.time.Clock()


a = pygame.Surface((LENGTH,LENGTH))

#set up the sources
initialize()

SCREEN["180,200"].amplitude = 1
SCREEN["220,200"].amplitude = -1
#SCREEN["200,200"].amplitude = 1
#SCREEN["220,270"].amplitude = -1

n =0

if __name__ == "__main__":
        while True:
                #making sure the magnitude does not increase to much
                if NORM2 > 1000.0:
                        for x in SCREEN:
                                SCREEN[x].amplitude = SCREEN[x].amplitude / NORM2
                        NORM2 = 1
                
                #SCREEN["255,255"].amplitude = math.sin(2*n)
                cache = np.array([])
                #exiting the simulation
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                

        
                norm =0
        
                #displaying everything on the screen
                for pos in POSITIONS:
                        if np.abs(SCREEN[pos].amplitude) > norm:
                                norm = np.abs(SCREEN[pos].amplitude)

                        
                        a.fill(amplitudemapper(SCREEN[pos].amplitude))

                        #just testing
                        #if SCREEN[pos].amplitude != 0.0:
                                #a.fill(rgbtuple(30,0.8,0.7))
                        #else:
                                #a.fill((0,0,0))

                        screen.blit(a,(SCREEN[pos].position_x , SCREEN[pos].position_y))
                
                

                #the calculation part
                for posit in POSITIONS:
                        cache =np.concatenate((cache,SCREEN[posit].propogate()))
                
                for osc in cache:
                        try:
                                SCREEN[f"{osc.position_x},{osc.position_y}"] += osc 

                        except KeyError:
                                continue
                
                
                """print(n)
                for xi in cache:
                        print(xi.amplitude)
                        print("")"""

                n+=1
                if norm !=  0.0:
                        NORM2 = norm

                """print("\n{}\n{}\n".format(NORM2, SCREEN["355,255"].amplitude))"""
                
                
                pygame.display.update()
                clock.tick(2)


