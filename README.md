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
mysql> create user 'team'@'localhost' identified by 'paris';
mysql> grant all privileges on *.* to 'hotel'@'localhost';
mysql> 
```

## Python Virtual environment 구축

- 필수는 아니지만 가상환경을 사용하면 패키지를 깔끔하게 관리할 수 있음.

### 가상환경 만들기

```shell
$ python3 -m venv venv
```

- 트러블 슈팅

```shell
Error: Command '~~' returned non-zero exit status 1
$ python3 -m venv --without-pip venv
```

### 가상환경 활성화/비활성화

- 왼쪽에 가상환경 디렉토리 이름이 뜨면 성공

```shell
$ source venv/bin/activate
(venv) $ _
(venv) $ deactivate
$ _
```

- Windows 버전 활성화

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
(venv) $ pip install flask
(venv) $ pip install cryptography
(venv) $ pip install pymysql
(venv) $ pip install flask-login
(venv) $ pip install flask-migrate
(venv) $ pip install flask-sqlalchemy
(venv) $ pip install flask-wtf
(venv) $ pip install wtforms
(venv) $ pip install werkzeug
```



## Flask Migration

- RDB(MySQL) -> ORM(SQLAlchemy) 전환을 위해 migration이 필요함

첫 설정하기

```shell
(venv) $ flask db init
```



- models.py 수정 후 반드시 실행

```shell
(venv) $ flask db migrate
(venv) $ flask db upgrade
```



## 데이터 추가/삭제하기

- 객체 속성/타입이 models.py에 정의되어 있는 속성과 맞는지, migration을 했는지 확인해야함.

```python
from app import db
from app.models import Employee

# Insert문
e = Employee(id=123, first_name="John", last_name="Lee", username="john")
e.set_password('john1')

# DB에 추가/커밋
db.session.add(e)
db.session.commit()

# 테이블의 데이터 삭제하기
removee = Employee.query.all()
for r in removee:
    db.session.delete(r)
db.session.commit()
```



## Flask 서버 실행하기

```shell
(venv) $ run flask
```

http://127.0.0.1:5000

http://127.0.0.1:5000/login