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
float error_corection(float var)
{
	return -0.2688+0.01299*var;
//			b0+b1*x
}
float temperature_to_impuls(float var)
{
//	return -9.647*var+ 0.5157*pow(var,2)-0.005115*pow(var,3)+ 1.852e-05*pow(var,4);
	return (12.52856*var - 326.83908);
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


float control(PID_STRUCT *PID,float e)
{
//	float ui = PID->Ki*PID->Tp*e+PID->ui_p;

	float ui = 0;
	if( e < 0.1* e)
		ui = PID->Tp*(PID->Ki*e+PID->Ki*PID->e_p)/2;
	ui = PID->Tp*(PID->Ki*e+PID->ui_p)/2;
	float uk = PID->Kp*e;
	float ud = PID->Kd *(e-PID->e_p);

	PID->e_p = e;
	PID->ui_p = ui;

	return temperature_to_impuls(ui+uk+ud);
}

//int PID_PWM(PID_STRUCT *PID,float target,float current)
//{
////	float e = ((12.52856*target - 326.83908)-(12.52856*current - 326.83908));
////	float error_corection = 3.1093e-04*pow(target,2)+1.0825*target-2.4524;
//
//
//	float e = (temperature_to_impuls(target+error_corection(target))-temperature_to_impuls(current));//-temperature_to_impuls(error_corection);//+target/1.8;
//
//
////	float temp = target - current;
////	float e = temperature_to_impuls(temp);
////	float ui = PID->Tp*(PID->Ki*e+PID->ui_p)/2;
//
//	PID->error = PID->error + e;
////	float ui = PID->Ki*PID->Tp*e+PID->ui_p;
////	float ui = PID->Tp*(PID->Ki*e+PID->Ki*PID->e_p)/2;
//	float ui = 0;
////	if( e < 0.3* temperature_to_impuls(target))
//		ui = PID->Tp*(PID->Ki*e+PID->Ki*PID->error)/2;// PID->Ki*PID->error;
//	float uk = PID->Kp*e;
//	float ud = PID->Kd *(e-PID->e_p);
//
//	PID->e_p = e;
//	PID->ui_p = ui;
////
////	return (int)(ui+uk+ud);
//	return (int)(ui+uk+ud);
//}

int PID_PWM(PID_STRUCT *PID,float target,float current)
{



	float e =target -  current + error_corection(current);


	PID->error = PID->error + e;

	float ui = 0;
//
//		ui = PID->Tp*(PID->Ki*e+PID->Ki*PID->error)/2;
	if( e < 0.3* target)
		ui = PID->Ki*PID->Tp*(e + PID->e_p)/2;//+PID->ui_p;
	float uk = PID->Kp*e ;
	float ud = PID->Kd *(e-PID->e_p);

	PID->e_p = e;
	PID->ui_p = ui;
//
//	return (int)(ui+uk+ud);
	int uPID = (int)(ui+uk+ud);//-30+error_corection(current);
	return uPID*12.53;
}
