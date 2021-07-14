#include <signal.h>
#include <unistd.h>
#include <iostream>
#include <stdlib.h>
#include <stdio.h>

#define num 8
static int result[num] = {0,};
static int j = 0;

void sig_handler(int signo, siginfo_t *si, void*p){

    if(si->si_code == SI_QUEUE)
    {
        printf("User RTS signal %d\n", si->si_pid);
        printf("Sig  Number %d\n",     si->si_signo);
        printf("User Data is %d\n",    si->si_value.sival_int);
        // 시그널이 큐잉되는지 확인하기 위한 코드
        result[j] = si->si_value.sival_int;
        j+=1;
        std::cout << "record" <<std::endl;
        
    }
    else{
        printf("Not realtime signal %d\n",signo);
    }    
}

int main(){

    char buf[10] = {0,};
    FILE* fd;

    struct sigaction sigact;
    int *sendnice; // Ssendingsig 역할

    std::cout<<"pid = "<<getpid()<<std::endl;

    sigemptyset(&sigact.sa_mask);
    sigact.sa_flags = SA_SIGINFO;
    sigact.sa_restorer = NULL;
    sigact.sa_sigaction = sig_handler;

    

    std::cout << "wait for signal" << std::endl;

    if(sigaction(SIGRTMIN, &sigact, 0)==1) // 시그널을 받아 이를 처리할 시그널 핸들러를 지정하고 플래그를 설정
    {
        std::cout << "Singanl Eror" <<std::endl;
        exit(0);

    }

    /*==================SWITCH====================*/
    while(1){
    fd=fopen("resultprint.txt","r");
    if(fd){
        if(fread(buf,1,sizeof(buf),fd)){    // one or more : true
            break;
        }
    }
    fclose(fd);
    }
    /*==================SWITCH====================*/

    for(int i = 0 ; i< num; i++){
        std::cout << result[i] << std::endl;
    }
    
}
