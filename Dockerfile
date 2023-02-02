From python:3.9  # Docker의 python버전을 설정

ENV PYTHONUNBUFFERED 1

RUN apt-get -y update
RUN apt-get -y install vim  #docker 안에서 vim설치를 안하도록

RUN mkdir /skyeye-docker-server  #docker안에서 skyeye-docker-server 폴더 생성
ADD . /skyeye-docker-server  #현재 디렉토리를 통째로 skyeye-docker-server 폴더에 복사

WORKDIR /skyeye-docker-server  #작업 디렉토리 설정

RUN pip install --upgrade pip  #pip 업그레이드
RUN pip install -r requirements.txt  #필수 패키지 설치

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "server.wsgi:application"]