import numpy as np
import math
import PySimpleGUI as sg
import pandas as pd 

# GUI code
sg. theme('DarkPurple7')

# Excel read code

EXCEL_FILE = 'SCARA_DESIGN_DATA.xlsx'
df = pd.read_excel(EXCEL_FILE)

# Lay-out code

layout = [
   [sg.Push(), sg.Text('SCARA RRP MEXE CALCULATOR', font = ("Bahnschrift SemiBold SemiConden", 25)), sg.Push(), 
   sg.Button('Help?',font = ("Bahnschrift SemiBold SemiConden", 10))],

   [sg.Push(),sg.Text('Forward Kinematics Calculator', font = ("Bahnschrift SemiBold SemiConden",18)),sg.Push()],

   [sg.Text('Fill out the following fields:', font = ("Bahnschrift SemiBold SemiConden",15)),
     sg.Push(),sg.Push(), sg.Button('Click this before Solving Forward Kinematics',
     font = ("Bahnschrift SemiBold SemiConden",15), size=(35,0), button_color=('black','yellow')),sg.Push(), 
     sg.Push(), sg.Button('Solve Inverse Kinematics',font = ("Bahnschrift SemiBold SemiConden",12), size=(35,0), 
     button_color=('black','pink')),sg.Push()],
  
   [sg.Text('a1 = ', font = ("Bahnschrift SemiBold SemiConden", 10)),sg.InputText('', key = 'a1', size =(20,10)),
     sg.Text('Th1 = ',font = ("Bahnschrift SemiBold SemiConden", 10)),sg.InputText('',key='Th1', size=(20,10)),
     sg.Push(), sg.Button('Jacobian Matrix (J)', font = ("Bahnschrift SemiBold SemiConden", 12),size=(15,0),button_color=('white','blue')), 
     sg.Button('Det(J)',font = ("Bahnschrift SemiBold SemiConden", 12), size=(15,0), button_color=('white','pink')),
     sg.Button('Inverse of J',font = ("Bahnschrift SemiBold SemiConden", 12), size=(15,0), button_color=('white','orange')),
     sg.Button('Transpose of J', font = ("Bahnschrift SemiBold SemiConden", 12), size=(15,0), button_color=('white','red')), sg.Push()],

   [sg.Text('a2 = ', font = ("Bahnschrift SemiBold SemiConden", 10)),sg.InputText('',key='a2', size=(20,10)),
     sg.Text('Th2 = ',font = ("Bahnschrift SemiBold SemiConden", 10)),
     sg.InputText('',key='Th2',size=(20,10)),sg.Push(),sg.Button('Inverse Kinematics',font = ("Bahnschrift SemiBold SemiConden",12),
     size=(35,0), button_color=('white','green')), sg.Push()],

   [sg.Text('a3 = ', font = ("Bahnschrift SemiBold SemiConden", 10)),sg.InputText('',key='a3', size=(20,10)),
     sg.Text('d3 = ',font = ("Bahnschrift SemiBold SemiConden", 10)),
     sg.InputText('',key='d3',size=(20,10))],
    
   [sg.Text('a4 = ', font = ("Bahnschrift SemiBold SemiConden",10)),sg.InputText('',key='a4', size=(20,10)),
   sg.Push(),sg.Push(),sg.Button('Path and Trajectory Planning', font = ("Bahnschrift SemiBold SemiConden",12), size=(40,0), button_color=('white','black')), sg.Push()],

   [sg.Text('a5 = ', font = ("Bahnschrift SemiBold SemiConden",10)),sg.InputText('',key='a5', size=(20,10))],

   [sg.Button('Solve Forward Kinematics',tooltip = 'Go first to "Click this before Solving Foward Kinematics" !!!', font = ("Bahnschrift SemiBold SemiConden",12), button_color=('white','purple')), sg.Push()],
  
   [sg.Frame('Position Vector: ',[[
      sg.Text('X= ', font = ("Bahnschrift SemiBold SemiConden",10)),sg.InputText(key='X', size=(10,1)),
      sg.Text('Y= ', font = ("Bahnschrift SemiBold SemiConden",10)),sg.InputText(key='Y', size=(10,1)),
      sg.Text('Z= ', font = ("Bahnschrift SemiBold SemiConden",10)),sg.InputText(key='Z', size=(10,1))]])],
  
   [sg.Push(), sg.Frame('H0_3 Transformation Matrix = ',[[sg.Output(size=(60,12))]]),
      sg.Push(),sg.Image('SCARA_RRP_VARIANT.gif'),sg.Push()],
   [sg.Submit(font = ("Bahnschrift SemiBold SemiConden",10)),sg.Exit(font = ("Bahnschrift SemiBold SemiConden",10))] 
  
  ]

# Windows Code
window = sg.Window('SCARA MANIPULATOR (RRP)', layout, resizable = True)
 
#Variable Codes for disabling buttons

disable_J = window['Jacobian Matrix (J)']
disable_DetJ = window['Det(J)']
disable_IV = window ['Inverse of J']
disable_TJ = window ['Transpose of J']
disable_PT = window ['Path and Trajectory Planning']

while True:
    event,values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Help?':
        sg.popup('Instructions','How to use this application?','Step 1: Please enter the needed data', 'Step  2: Click the button "Click before Solving Kinematics."',
        'Step 3: Click the button "Solve Forward Kinematics"','Step 4: If you wish to save the answer, then manually type it in X=__,Y=__,Z=__, to save it in the Excel file.',
        'Step 4: If you want to solve Jacobian Matrix then click "Jacobian Matrix (J)"','Step 5: If you want to solve the Singularities, then click "Det(J)",note if Det(J)=0 then, "Inverse of J" button would not be available at all since it is non-invertible.',
        'Step 6: To solve the Torque-Force Analysis, click the  button "Transpose of J"','Step 7: If the singularities is positive then, "Inverese of J"  is available. To solve inverse of J, just simply click the button.',
        )


    if event ==('Click this before Solving Forward Kinematics'):
        disable_J.update(disabled=True)
        disable_DetJ.update(disabled=True)
        disable_IV.update(disabled=True)
        disable_TJ.update(disabled=True)
        disable_PT.update(disabled=True)
   




    if event == 'Solve Forward Kinematics' : 
        
        # Forward Kinematic Codes
      
        # link lengths in mm
        a1 = values['a1'] # For Testing, 50 mm
        a2 = values['a2'] # For Testing, 60 mm
        a3 = values['a3'] # For Testing, 50 mm
        a4 = values['a4'] # For Testing, 60 mm
        a5 = values['a5'] # For Testing, 50 mm

        # Joint Variable (Thetas in degrees & dinstance in cm)
        Th1 = values['Th1'] # For Testing, 0 degrees
        Th2 = values['Th2'] # For Testing, 90 degrees
        d3 =  values['d3']  # For Testing, 0 degrees

        Th1 = (float(Th1)/180.0)*np.pi  # Theta 1 in radian
        Th2 = (float(Th2)/180.0)*np.pi  # Theta 2 in radian
        
        # D-H Parametric Table
        DHPT = [
            [float(Th1),(0.0/180.0)*np.pi, float(a2), float(a1)],
            [float(Th2),(180.0/180.0)*np.pi, float(a4), float(a3)],
            [0, 0, 0, float(a5)+float(d3)]]

        # D-H Notation Formula for HTM
        i = 0
        H0_1 = [
            [np.cos(DHPT[i][0]), -np.sin(DHPT[i][0])*np.cos(DHPT[i][1]), np.sin(DHPT[i][0])*np.sin(DHPT[i][1]), DHPT[i][2]*np.cos(DHPT[i][0])],
            [np.sin(DHPT[i][0]), np.cos(DHPT[i][0])*np.cos(DHPT[i][1]), -np.cos(DHPT[i][0])*np.sin(DHPT[i][1]), DHPT[i][2]*np.sin(DHPT[i][0])],
            [0, np.sin(DHPT[i][1]), np.cos(DHPT[i][1]), DHPT[i][3]],
            [0, 0, 0, 1]]

        i = 1
        H1_2 = [
            [np.cos(DHPT[i][0]), -np.sin(DHPT[i][0])*np.cos(DHPT[i][1]), np.sin(DHPT[i][0])*np.sin(DHPT[i][1]), DHPT[i][2]*np.cos(DHPT[i][0])],
            [np.sin(DHPT[i][0]), np.cos(DHPT[i][0])*np.cos(DHPT[i][1]), -np.cos(DHPT[i][0])*np.sin(DHPT[i][1]), DHPT[i][2]*np.sin(DHPT[i][0])],
            [0, np.sin(DHPT[i][1]), np.cos(DHPT[i][1]), DHPT[i][3]],
            [0, 0, 0, 1]]

        i = 2
        H2_3 = [
            [np.cos(DHPT[i][0]), -np.sin(DHPT[i][0])*np.cos(DHPT[i][1]), np.sin(DHPT[i][0])*np.sin(DHPT[i][1]), DHPT[i][2]*np.cos(DHPT[i][0])],
            [np.sin(DHPT[i][0]), np.cos(DHPT[i][0])*np.cos(DHPT[i][1]), -np.cos(DHPT[i][0])*np.sin(DHPT[i][1]), DHPT[i][2]*np.sin(DHPT[i][0])],
            [0, np.sin(DHPT[i][1]), np.cos(DHPT[i][1]), DHPT[i][3]],
            [0, 0, 0, 1]]

        # Transformation Matrices from base to end-effector
        #print("HO_1 = ")
        #print(np.matrix(H0_1))
        #print("H1_2 = ")
        #print(np.matrix(H1_2))
        #print("H2_3 = ")
        #print(np.matrix(H2_3))
        H0_1 = np.matrix(H0_1)
        
        # Dot Product of H0_3 = HO_1*H1_2*H2_3
        H0_2 = np.dot(H0_1,H1_2)
        H0_3 = np.dot(H0_2,H2_3)

        # Transformation Matrix of the Manipulator
        print("H0_3 = ")
        print(np.matrix(H0_3))

        # Position Vector X Y Z

        X0_3 = H0_3[0,3]
        print("X = ", X0_3)

        Y0_3 = H0_3[1,3]
        print("Y = ", Y0_3)

        Z0_3 = H0_3[2,3]
        print("Z = ", Z0_3)

        disable_J.update(disabled=False)
        
   

    if event == 'Submit' :
        df = df.append(values, ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        sg.popup('Data Saved!')
       
       #JACOBIAN MATRIX CODE
    if event == "Jacobian Matrix (J)":
        Z_1 = [[0],[0],[1]] # The [0,0,1] vector
        d0_3 = H0_3[0:3,3:]
        
        # Row 1 - 3, Column 1
        
        R0_0 = [[1,0,0],[0,1,0],[0,0,1]]
        J1a = np.dot(R0_0,Z_1)
        
        
        J1 = [[(J1a[1,0]*d0_3[2,0])-(J1a[2,0]*d0_3[1,0])],
        [(J1a[2,0]*d0_3[0,0])-(J1a[0,0]*d0_3[2,0])],
        [(J1a[0,0]*d0_3[1,0])-(J1a[1,0]*d0_3[0,0])]]
        
        #print(np.matrix(R0_0))
        #print(np.matrix(J1a))
        #print(np.matrix(J1))

        # Row 1 - 3, Column 2
    
        R0_1a = np.dot(H0_1,1)
        R0_1 = R0_1a[0:3,0:3]
        d0_1 = R0_1a[0:3,3:]
        J2a = (np.dot(R0_1,Z_1))
        J2b = (np.subtract(d0_3,d0_1))

        J2 = [[(J2a[1,0]*J2b[2,0])-(J2a[2,0]*J2b[1,0])],
        [(J2a[2,0]*J2b[0,0])-(J2a[0,0]*J2b[2,0])],
        [(J2a[0,0]*J2b[1,0])-(J2a[1,0]*J2b[0,0])]]
        print(np.matrix(J2))

        # Row 1 - 3, Column 3
        R0_2 = H0_2[0:3,0:3]
        J3 = np.dot(R0_2,Z_1)
        #print(np.matrix(J3))

        J3a = [[0],[0],[0]]

        # Concatenate
        JM1 = np.concatenate((J1,J2,J3),1)
        # print(JM1)
        
        JM2 = np.concatenate((J1a,J2a,J3a),1)
        # print(JM2)
        
        J = np.concatenate((JM1,JM2),0)
        sg.popup("J = ", J)
        disable_J.update(disabled=True)
        disable_DetJ.update(disabled=False)
        disable_TJ.update(disabled=False)
        
    if event == "Det(J)":
        # Determinant
        DJ = np.linalg.det(JM1)
        print("DJ = ")
        print(DJ)
        sg.popup('D(J) =' "%.4f" % DJ), 
        
        if DJ == 0:
            disable_IV.update(disabled=True)
            sg.popup('Warning: This is Non-Invertible')
      
        
    if event == 'Inverse of J':
        # Inverse Velocity
        IV = np.linalg.inv(JM1)
        sg.popup('IV =', IV)
        #sg.popup('Warning: This is Non-Invertible')
        
    if event == 'Transpose of J' :
        # Transpose of J
        TJ = np.transpose(JM1)
        print("TJ = ")
        print(TJ)
        sg.popup('T(J)=', TJ)

window.close()
