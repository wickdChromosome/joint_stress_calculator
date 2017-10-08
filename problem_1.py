#!/usr/bin/env python3

def problem_1():
    '''
    Calculates all relevant stesses and variables for the problem,
    uses gui
    '''

    #import stuff
    from appJar import gui
    import numpy
    import csv
    import sympy
    import logging
    from sympy.solvers.solveset import linsolve

    #set up logger
    logging.basicConfig(filename='debug.txt',level=logging.INFO)
    logging.info("Starting up..")

    #define placeholders for basic vars in problem

    joint_area = 0

    arm_length = 0
    dumbb_wght = 0
    arm_wght = 0

    min_force_angle = 0
    max_force_angle = 0


    #get gui to populate vars
    def gui_input():

        #launch gui with tables, save vars
        app = gui()

        app.setBg("#121212", override=False)
        app.setFg("#ffffff", override=False)

        app.startPanedFrame('p1')

        app.startFrame('imageframe')
        app.addImage('picture', 'shoulderjoint.gif')
        app.stopFrame()

        app.setBg("#121212", override=True)
        app.setFg("#ffffff", override=True)

        #add labels for joint stuff in gui
        app.addLabel("Shoulder raise simulation", "Glenohumeral Joint")

        app.addLabelEntry("Height(m)")
        app.addLabelEntry("Weight(kg)")
        app.addLabelEntry("Maximum arm angle(deg)")
        app.addLabelEntry("Weight of dumbbell(kg)")


        app.setBg("#121212", override=True)
        app.setFg("#ffffff", override=True)

        app.startPanedFrame('p2')

        app.setFg("#ffffff", override=True)
        axes = app.addPlot('chart', 0, 0)
        app.addLabel('l1', 'Please enter user data')


        def onpress(button):
            '''
            Describe what happens when button gets pressed
            '''
            if button == 'Deltoidal Muscle Force':

                height = float(app.getEntry("Height(m)"))
                weight = float(app.getEntry("Weight(kg)"))
                max_force_angle = int(app.getEntry("Maximum arm angle(deg)"))
                dumbb_wght = float(app.getEntry("Weight of dumbbell(kg)"))


                Lf = height * 0.156 #length of forearm
                Lu = height * 0.174 #length of upper arm

                Mf = weight * 0.016
                Mu = weight * 0.028

                arm_length = Lf + Lu
                arm_wght = Mu + Mu

                logging.info("arm wght: " + str(arm_wght))

                [Fjx_list, Fjy_list, T0_list, Pcom_list, sigma_list] = calc_basics(max_force_angle, arm_length, dumbb_wght, arm_wght, Lf, Lu, Mf, Mu)

                x_data = range(0, max_force_angle)

                #plot new stuff
                app.updatePlot('chart', x_data, T0_list)
                app.setLabel('l1', 'Arm angle(Deg) vs Deltoidal muscle tension(N)')
                app.setLabelFg('l1', 'white')


            elif button == 'Deltoidal Muscle Stress':

                height = float(app.getEntry("Height(m)"))
                weight = float(app.getEntry("Weight(kg)"))
                max_force_angle = int(app.getEntry("Maximum arm angle(deg)"))
                dumbb_wght = float(app.getEntry("Weight of dumbbell(kg)"))


                Lf = height * 0.156 #length of forearm
                Lu = height * 0.174 #length of upper arm

                Mf = weight * 0.016
                Mu = weight * 0.028

                arm_length = Lf + Lu
                arm_wght = Mu + Mu



                [Fjx_list, Fjy_list, T0_list, Pcom_list, sigma_list] = calc_basics(max_force_angle, arm_length, dumbb_wght, arm_wght, Lf, Lu, Mf, Mu)


                x_data = range(0, max_force_angle)

                #plot new stuff
                app.updatePlot('chart', x_data, sigma_list)
                app.setLabel('l1', 'Arm angle(Deg) vs Muscle Stress(N/m^2)')

            elif button == "Shoulder Joint Stress Y":


                height = float(app.getEntry("Height(m)"))
                weight = float(app.getEntry("Weight(kg)"))
                max_force_angle = int(app.getEntry("Maximum arm angle(deg)"))
                dumbb_wght = float(app.getEntry("Weight of dumbbell(kg)"))


                Lf = height * 0.156 #length of forearm
                Lu = height * 0.174 #length of upper arm



                Mf = weight * 0.016
                Mu = weight * 0.028

                arm_length = Lf + Lu
                arm_wght = Mu + Mu

                [Fjx_list, Fjy_list, T0_list, Pcom_list, sigma_list] = calc_basics(max_force_angle, arm_length, dumbb_wght, arm_wght, Lf, Lu, Mf, Mu)

                x_data = range(0, max_force_angle)

                #plot new stuff
                app.updatePlot('chart', x_data, Fjy_list)
                app.setLabel('l1', 'Arm angle(Deg) vs Shoulder Y joint Force(N)')




            elif button == "Shoulder Joint Stress X":

                height = float(app.getEntry("Height(m)"))
                weight = float(app.getEntry("Weight(kg)"))
                max_force_angle = int(app.getEntry("Maximum arm angle(deg)"))
                dumbb_wght = float(app.getEntry("Weight of dumbbell(kg)"))

                Lf = height * 0.156 #length of forearm
                Lu = height * 0.174 #length of upper arm

                Mf = weight * 0.016
                Mu = weight * 0.028

                arm_length = Lf + Lu
                arm_wght = Mu + Mu


                [Fjx_list, Fjy_list, T0_list, Pcom_list, sigma_list] = calc_basics(max_force_angle, arm_length, dumbb_wght, arm_wght, Lf, Lu, Mf, Mu)


                x_data = range(0, max_force_angle)

                #plot new stuff
                app.updatePlot('chart', x_data, Fjx_list)
                app.setLabel('l1', 'Arm angle(Deg) vs Shoulder X joint Force(N)')


            elif button == 'COM radial distance':

                height = float(app.getEntry("Height(m)"))
                weight = float(app.getEntry("Weight(kg)"))
                max_force_angle = int(app.getEntry("Maximum arm angle(deg)"))
                dumbb_wght = float(app.getEntry("Weight of dumbbell(kg)"))


                Lf = height * 0.156 #length of forearm
                Lu = height * 0.174 #length of upper arm

                Mf = weight * 0.016
                Mu = weight * 0.028

                arm_length = Lf + Lu
                arm_wght = Mu + Mu

                [Fjx_list, Fjy_list, T0_list, Pcom_list, sigma_list] = calc_basics(max_force_angle, arm_length, dumbb_wght, arm_wght, Lf, Lu, Mf, Mu)

                x_data = range(0, max_force_angle)

                #plot new stuff
                app.updatePlot('chart', x_data, Pcom_list)
                app.setLabel('l1', 'Arm angle(Deg) vs COM radial distance(m)')






        app.addButtons(["Deltoidal Muscle Force", "Deltoidal Muscle Stress","Shoulder Joint Stress X", "Shoulder Joint Stress Y", "COM radial distance"], onpress)

        app.setBg("#121212", override=True)
        app.setFg("#ffffff", override=True)

        app.stopPanedFrame()


        app.go()


    def calc_basics(max_force_angle, arm_length, dumbb_wght, arm_wght, Lf, Lu, Mf, Mu):

        Lm = 0.0645

        #declare sym vars
        Fjy = sympy.Symbol('Fjy')
        Fjx = sympy.Symbol('Fjx')

        T0 = sympy.Symbol('T0')
        T1 = sympy.Symbol('T1')
        sigma = sympy.Symbol('sigma')
        logging.info('Symbols defined')

        #define placeholders
        Fjx_list = []
        Fjy_list = []
        T0_list = []
        T1_list = []
        sigma_list = []
        Pcom_list = []
        logging.info("defined placeholder lists")

        delt_angle = numpy.linspace(0, 10 ,max_force_angle + 1)
        logging.info(str(delt_angle[0]))


        #linear distribution for deltoid muscle angles, 0-10 degrees
        #deltoid_angle_list = numpy.linspace(0,10, num=91, endpoint=True)
        #logging.info('Made linspace for deltoidal force angles')

        #gravity
        g = 9.8

        #for each angle
        for angle in range(1, max_force_angle + 1):

            logging.info("Processing angle:" + str(angle))

            #define where positions are
            arm_pos = (Lf * Mf + Lu * Mu)/(arm_wght)
            dumbb_pos = arm_length

            #COM weight
            Wcom = dumbb_wght + arm_wght
            logging.info('Got COM mass: ' + str(Wcom))

            #COM pos changes with arm rotation
            Pcom = (arm_wght * arm_pos + dumbb_wght * dumbb_pos)/(arm_wght + dumbb_wght) * numpy.sin(numpy.deg2rad(angle))
            logging.info('Got COM position: ' + str(Pcom))
            logging.info(str(arm_wght) + ' and ' + str(arm_pos) + ' and ' + str(dumbb_wght) +  ' and ' + str(arm_wght) +' and '+ str(numpy.deg2rad(angle)))

            #PCSAs and muscle areas
            PCSA0 = 0.0017#deltoids

            #stress eqns
            eqn_stress_deltoids = T0 - PCSA0 * sigma

            #get force in Y
            eqn_y =  numpy.cos(numpy.deg2rad(angle - delt_angle[angle])) * T0 - arm_wght * g - dumbb_wght * g - Fjy
            logging.info(str(eqn_y))
            logging.info('y eqn defined')

            #get force in X
            eqn_x = Fjx - numpy.sin(numpy.deg2rad(angle - delt_angle[angle])) * T0
            logging.info(str(eqn_x))
            logging.info('x eqn defined')


            #get moments eqn
            eqn_m = numpy.sin(numpy.deg2rad(delt_angle[angle])) * Lm * T0 - arm_wght * g * arm_pos * numpy.sin(numpy.deg2rad(angle)) - g * dumbb_wght * dumbb_pos * numpy.sin(numpy.deg2rad(angle))
            logging.info(str(eqn_m))
            logging.info('m eqn defined')


            logging.info('Defined equations')

            #set up sys eqns
            output = linsolve([eqn_y, eqn_x, eqn_m, eqn_stress_deltoids], (Fjx, Fjy, T0, sigma))
            print(output)



            logging.info('Solved equations')
            logging.info(str(output))
            #init list
            out_list = [0, 0, 0, 0]


            for cell in output:
                out_list[0] = cell[0]
                out_list[1] = cell[1]
                out_list[2] = cell[2]
                out_list[3] = cell[3]



                logging.info('Calculated basic vars: ' + ' Fjx: ' + str(cell[0]) + ' Fjy: ' + str(cell[1]) + ' T0: ' + str(cell[2]) + ' Pcom: ' + str(Pcom))

                Fjx_list.append(cell[0])
                Fjy_list.append(cell[1])
                T0_list.append(cell[2])
                sigma_list.append(cell[3])
                Pcom_list.append(Pcom)

        return [Fjx_list, Fjy_list, T0_list, Pcom_list, sigma_list]



    gui_input()






problem_1()


