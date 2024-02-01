# stt-api-server-2315
STT 기본모델 API 테스트 서버(BE)입니다.  
[swagger페이지 링크](https://stt.bs-soft.co.kr/docs)

## requirements  
`dockerfile`과 `requirements.txt`에 모두 표기

## 실행방법  

1. 저장소 복제
~~~bash
git clone https://github.com/bssoft-dev/stt-api-server-2315.git  
~~~  
2. (옵션1) GPU를 사용하는 경우 - gpus 옵션을 주고 실행(`all` 또는 `device=0`등)
~~~bash
docker run --gpus all -d -v $(pwd)/stt-api-server-2315:/bssoft -p port:port --name name bssoftdev/bssoft-sound-process sleep infinity
~~~  
3. (옵션2) GPU를 사용하지 않는 경우 - config를 cpu로 변경하고 실행
~~~bash
vi stt-api-server-2315/config.ini
# device = gpu 부분을 cpu로 변경 및 저장한다
docker run -d -v $(pwd)/stt-api-server-2315:/bssoft --network=host bssoftdev/bssoft-sound-process
~~~

## config.ini 설명
`[host]` 서버 실행 url과 port 설정  
`[dirs]` 파일 업로드, 로그, 임시 파일, 타겟 파일 위치 설정  
`[ml]` device: `cpu` 혹은 `gpu`, model: 사용 모델 위치  
`[tcp]` tcp 소켓 통신을 위함(utils/processor.py) 현재는 사용하지 않음
