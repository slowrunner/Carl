#include <GoPiGo3.h>   // for GoPiGo3
#include <stdio.h>     // for printf
#include <unistd.h>    // for usleep
#include <signal.h>    // for catching exit signals
 

#define NO_LIMIT_SPEED 1000

GoPiGo3 GPG; 

void exit_signal_handler(int signo);

int main(){

	signal(SIGINT, exit_signal_handler); // register the exit function for Ctrl+C



	GPG.detect();
        bool keepLooping = true;

        do {
	    char c = getchar();
	    // printf("Char: %c \n", c);
	    switch(c){
		case 'w':
			GPG.set_motor_dps(MOTOR_LEFT + MOTOR_RIGHT, NO_LIMIT_SPEED);
			break;
		case 'x' :
			GPG.set_motor_dps(MOTOR_LEFT + MOTOR_RIGHT, NO_LIMIT_SPEED * -1);
			break;
		case 'd' :
			GPG.set_motor_dps(MOTOR_LEFT, NO_LIMIT_SPEED);
			GPG.set_motor_dps(MOTOR_RIGHT, 0);
			break;
		case 'a' : 
			GPG.set_motor_dps(MOTOR_LEFT, 0);
			GPG.set_motor_dps(MOTOR_RIGHT, NO_LIMIT_SPEED);
			break;
		case 'q' : 
			GPG.set_motor_dps(MOTOR_LEFT + MOTOR_RIGHT, 0);
			keepLooping = false;
                        break;
                case ' ' :
			GPG.set_motor_dps(MOTOR_LEFT + MOTOR_RIGHT, 0);
                        break;
                case 's' :
			GPG.set_motor_dps(MOTOR_LEFT + MOTOR_RIGHT, 0);
                        break;
	    }
        } while (keepLooping);
}

void exit_signal_handler(int signo){
	  if(signo == SIGINT){
         GPG.reset_all();    // Reset everything so there are no run-away motors
         exit(-2);
	  }
}
