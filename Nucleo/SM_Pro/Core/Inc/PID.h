/*
 * PID.h
 *
 *  Created on: Jan 27, 2022
 *      Author: Stanley
 */

#ifndef INC_PID_H_
#define INC_PID_H_
#include <math.h>

typedef struct PID_STRUCT
{
	float Tp;
	float max_temp;
	float room_temp;
//	float k_ob;
//	float Ts;

	float Kp;
	float Ki;
	float Kd;

	float ui_p;
	float e_p;
	float error;



}PID_STRUCT;

float error_corection(float var);
float temperature_to_impuls(float var);
void PID_Init(PID_STRUCT *PID, float Tp, float Kp, float Ki, float Kd);
float control(PID_STRUCT *PID,float e);
int PID_PWM(PID_STRUCT *PID,float target,float current);
#endif /* INC_PID_H_ */
