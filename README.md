## Specification

```
Python				3.6.4
pip					18.1
cryptography  		2.4.2  
Flask				1.0.2
Flask-Login 	    0.4.1  
Flask-Migrate		2.3.0  
Flask-SQLAlchemy	2.3.2  
Flask-WTF			0.14.2 
PyMySQL         	0.9.2  
SQLALchemy			1.2.14
Werkzeug			0.14.1
WTForms         	2.2.1  
```

## MySQL 환경 구축

### MySQL 서버 시작/중지하기

```
$ mysql.server start
Starting MySQL
.. SUCCESS! 
$ mysql.server stop
Shutting down MySQL
.. SUCCESS! 
$ _
```

### MySQL 접속 후 사용자 생성/권한 부여하기

```shell
$ sudo mysql
mysql> create user 'hotel'@'localhost' identified by 'paris';
mysql> grant all privileges on *.* to 'hotel'@'localhost';
```

## Python Virtual environment 구축

* 필수는 아니지만 가상환경을 사용하면 패키지를 깔끔하게 관리할 수 있음.

###가상환경 만들기

```shell
$ python3 -m venv venv
```

* 트러블 슈팅

```shell
Error: Command '~~' returned non-zero exit status 1
$ python3 -m venv --without-pip venv
```

### 가상환경 활성화/비활성화

* 왼쪽에 가상환경 디렉토리 이름이 뜨면 성공

```shell
$ source venv/bin/activate
(venv) $ _
(venv) $ deactivate
$ _
```

* Windows 버전 활성화

```powershell
venv\Scripts\activate.bat
```

### 환경변수 설정

```
$ export FLASK_APP=hotelpb.py
$ echo $FLASK_APP
hotelpb.py
$ _
```



## Flask, 확장기능 설치

```shell
$ pip install flask
$ pip install cryptography
$ pip install pymysql
$ pip install flask-login
$ pip install flask-migrate
$ pip install flask-sqlalchemy
$ pip install flask-wtf
$ pip install wtforms
$ pip install werkzeug
```



## Flask Migration

* RDB(MySQL) -> ORM(SQLAlchemy) 전환을 위해 migration이 필요함

```

```

