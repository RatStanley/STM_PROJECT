/*
 * PID.c
 *
 *  Created on: Jan 27, 2022
 *      Author: Stanisław Ratajczak Artur Będziechowski
 */

#include "PID.h"

float error_corection(float var)
{
	return -0.2688+0.01299*var;
}


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
	PID->error = 0;
}

int PID_PWM(PID_STRUCT *PID,float target,float current)
{



	float e =target -  current + error_corection(current);


	PID->error = PID->error + e;

	float ui = 0;

	if( e < 0.3* target)
		ui = PID->Ki*PID->Tp*(e + PID->e_p)/2;
	float uk = PID->Kp*e ;
	float ud = PID->Kd *(e-PID->e_p);

	PID->e_p = e;
	PID->ui_p = ui;

	int uPID = (int)(ui+uk+ud);
	return uPID*12.53;
}
