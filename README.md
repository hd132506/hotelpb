# hotelpb
Web-based Hotel database management tool

* 커맨드는 hotelpb 디렉토리에서 실행합니다.

## 가상환경 구축하기(선택)
``` 
$ python3 -m venv venv
```

## 가상환경 활성화/비활성화하기
```
$ source venv/bin/activate
(venv) $ _
(venv) $ deactivate
$ _
```
Windows 버전 활성화
```
$ venv\Scripts\activate
```
## 가상환경에서 flask 및 dotenv 패키지 설치하고 환경변수 설정하기
dotenv 패키지는 가상환경에서 환경변수 설정을 자동화해 줍니다.
```
(venv) $ pip install flask
(venv) $ pip install python-dotenv
```

## dotenv 설정하기
```
(venv) $ touch .flaskenv
```
.flaskenv 파일로 들어가 아래 코드 입력 후 저장
```
FLASK_APP=hotelpb.py
```

## 환경변수 설정 잘 됐는지 확인
```
(venv) $ echo $FLASK_APP
hotelpb.py
```
* 아무것도 뜨지 않을 경우
```
(venv) $ export FLASK_APP=hotelpb.py
(venv) $ echo $FLASK_APP
```
## 서버 실행 후 접속하기
```
(venv) $ flask run
```
http://localhost:5000/
