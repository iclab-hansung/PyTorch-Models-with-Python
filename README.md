## 하나의 모델에 대한 추론을 진행하는 nice value값을 가지는
## 프로세스 여러개를 동시 실행하여 끝나는 순서를 알아보는 코드

### solo_run_python.py : 모델 1개에 대한 추론을 수행. 프로세스 실행시 -20~19사이의 값을 입력하여 해당 프로세스의 nice value값을 설정
### result.cpp : 끝나는 순서에 대한 결과를 resultprint.txt 파일에 기록
### run_python_script.sh : 여러 프로세스를 동시 실행시키기 위한 쉘 스크립트 파일

실행순서
1.switch_python 파일은 전체 내용삭제
2.result.cpp 실행
3.sudo로 쉘 스크립트 파일 실행
4.switch.txt파일에 아무값이나 입력
5.resultprint.txt에서 결과확인
