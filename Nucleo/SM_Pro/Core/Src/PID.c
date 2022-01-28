/*
 * PID.c
 *
 *  Created on: Jan 27, 2022
 *      Author: Stanley
 */

#include "PID.h"
//
//float control(float e)
//{
////	float ui = Ki*Tp*e+ui_p;
////	float uk = Kp*e;
////	float ud = Kd *(e-e_p);
//}
//
//void PID_init(float Tp, float Kp, float Ki, float Kd)
//{
//
//}


void PID_Init(PID_STRUCT *PID, float Tp, float Kp, float Ki, float Kd)
{
	PID->Tp = Tp;
	PID->Kp = Kp;
	PID->Ki = Ki;
	PID->Kd = Kd;
	PID->e_p = 0;
	PID->ui_p = 0;
	PID->max_temp = 100;
	PID->room_temp = 24;
}


float control(PID_STRUCT *PID,float e)
{
	float ui = PID->Ki*PID->Tp*e+PID->ui_p;
	float uk = PID->Kp*e;
	float ud = PID->Kd *(e-PID->e_p);

	PID->e_p = e;
	PID->ui_p = ui;

	return ui+uk+ud;
}

