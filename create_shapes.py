import numpy as np
import matplotlib.pyplot as plt
import math
from dataclasses import dataclass

class create_shapes:
    "Class to create main circle, the outside ones and the final shape"

    def __init__(self,main_struct,ext_struct):
        self.center_main = main_struct.center
        self.radius_main = main_struct.radius
        self.points_main = main_struct.points

        self.distance_ext  = ext_struct.distance_ext
        self.points_ext    = ext_struct.points
        self.points_span   = ext_struct.points_span
        self.advancement   = ext_struct.advancement
        self.number_ext    = ext_struct.number_ext +1 #Compensate the fact that spaamming from 0 to 2pi creates two circle one over the other. TO fix because it increments the number of points..

        self.x_combined,self.y_combined = self.interaction_circles_2()

    def sorting_coordinates(x,y):
        # Sorting the x and y coordinates based on their angle. Will return a vector orderd s.t. x and y start from the coordinates associated to the lowest angle (-180)
        angles = np.arctan2(y, x)

        sort_idx = np.argsort(angles)

        x_sorted = x[sort_idx]
        y_sorted = y[sort_idx]
        
        return x_sorted,y_sorted
    
    def create_circle(self,center,radius,points):
        
        angle = np.linspace(0,2*np.pi,points)

        x = center[0] +  radius * np.cos(angle)
        y = center[1] +  radius * np.sin(angle)

        return x,y

    # def interaction_circles(self):
        
    #     d_main_ext = 1.5 * self.radius_main
    #     r_ext      = d_main_ext - self.radius_main 

    #     theta_ext   = np.linspace(0, 2*np.pi, self.points_ext)
    #     angle_ext_c = np.linspace(np.pi-0.5,2*np.pi,self.number_ext)

    #     x_ext_c,y_ext_c = self.create_circle()
    
    def interaction_circles_2(self):
        
        self.r_ext      = self.distance_ext - self.radius_main 
        
        # Angles of position external conferences centers
        angle_ext_c = np.linspace(0,2*np.pi,self.number_ext)
      
        # Position center external conferences
        self.x_ext_c = self.center_main[0] + self.distance_ext*np.cos(angle_ext_c)
        self.y_ext_c = self.center_main[1] + self.distance_ext*np.sin(angle_ext_c)
    

        N_points_span = self.points_span

        o1o3 = self.radius_main + self.r_ext - self.advancement

        # Angles created by the triangles when entering the circle
        angle_aperture = np.arccos( (self.r_ext**2 + o1o3**2 - self.radius_main**2)/ (2 * self.r_ext * o1o3) )
        angle_at_O     = np.arccos( (self.radius_main**2 + o1o3**2 - self.r_ext**2) / (2 * self.radius_main * o1o3) )

        # Position centers after advancement
        self.x_new_c = self.x_ext_c - self.advancement*np.cos(angle_ext_c)
        self.y_new_c = self.y_ext_c - self.advancement*np.sin(angle_ext_c)

        # Initial and final angle of the inner arc
        theta_intersect_1 = angle_ext_c - angle_at_O
        theta_intersect_2 = angle_ext_c + angle_at_O

        self.theta_main_outer = np.linspace(theta_intersect_2, theta_intersect_1 + 2*np.pi, self.points_ext)
        
        x_main = self.center_main[0] + self.radius_main * np.cos(self.theta_main_outer)
        y_main = self.center_main[1] + self.radius_main * np.sin(self.theta_main_outer)

        theta_span = np.linspace(angle_ext_c + np.pi + angle_aperture,
                                 angle_ext_c + np.pi - angle_aperture, N_points_span)

        self.x_inner = self.x_new_c + self.r_ext * np.cos(theta_span)
        self.y_inner = self.y_new_c + self.r_ext * np.sin(theta_span)

        self.x_combined = x_main[0]
        self.y_combined = y_main[0]
        'HERE PROBLEM'
        for i in range(1,self.number_ext):
            self.x_combined = np.concatenate([self.x_combined, x_main[:,i]])
            self.y_combined = np.concatenate([self.y_combined, y_main[:,i]])


        for i in range (self.number_ext):
            self.x_combined = np.concatenate([self.x_combined, self.x_inner[:,i]])
            self.y_combined = np.concatenate([self.y_combined, self.y_inner[:,i]])

        return  self.x_combined,self.y_combined
    

    def plotting_circles(self,options):

        plt.figure(figsize=(6,6))

        angle_main = np.linspace(0,2*np.pi,self.points_main)
        angle_ext  = np.linspace(0,2*np.pi,self.points_ext)

        x_main,y_main = self.create_circle(self.center_main,self.radius_main,self.points_main)

        x_ext = np.zeros((self.points_ext,self.number_ext))
        y_ext = np.zeros((self.points_ext,self.number_ext))

        x_ext_new = np.zeros((self.points_ext,self.number_ext))
        y_ext_new = np.zeros((self.points_ext,self.number_ext))

        # x_ext_new  = self.x_new_c +  self.r_ext*  np.cos(angle_ext)
        # y_ext_new  = self.y_new_c +  self.r_ext*  np.sin(angle_ext)

        for i in range(self.number_ext):
            x_ext[:,i],y_ext[:,i] = self.create_circle([self.x_ext_c[i],self.y_ext_c[i]],self.r_ext,self.points_ext)
            x_ext_new[:,i],y_ext_new[:,i] = self.create_circle([self.x_new_c[i],self.y_new_c[i]],self.r_ext,self.points_ext)
            
        match options:

            case "before":
                
                plt.plot(x_main,y_main, color='black')
                plt.plot(x_ext,y_ext, color='red', linestyle='--')

            case "after":

                plt.plot(x_main,y_main, color='black',linestyle='--',alpha=0.3)
                plt.plot(x_ext_new,y_ext_new, color='red',linestyle='--',alpha=0.3)
                plt.plot(self.x_combined,self.y_combined,color='blue',linestyle='dotted')
                # plt.plot(self.x_inner,self.y_inner,linestyle='dotted',color='orange')


            case "total":
                plt.plot(x_main,y_main, color='black',linestyle='--')
                plt.plot(x_ext_new,y_ext_new, color='red', linestyle='--')
                plt.plot(self.x_combined,self.y_combined,color='black')
                plt.plot(self.x_inner,self.y_inner,linestyle='dotted',color='orange')




        plt.axis('equal')
        plt.show()

        return