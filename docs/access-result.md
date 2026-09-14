# 웹 서비스 외부 접속 증거

> 방식 (B) 선택: `GET http://<퍼블릭IP>/health` 응답 확인

---

## 접속 정보

| 항목 | 값 |
|------|----|
| 퍼블릭 IP | `<퍼블릭IP>` |
| 서버 | EC2 (`ap-northeast-2a`) |
| 웹 서버 | Nginx |
| 접속 방식 | HTTP GET /health |

---

## 접속 명령

```bash
curl -v http://<퍼블릭IP>/health
```

---

## 기대 응답 (예시)

```
*   Trying <퍼블릭IP>:80...
* Connected to <퍼블릭IP> port 80
> GET /health HTTP/1.1
> Host: <퍼블릭IP>
> User-Agent: curl/...
>
< HTTP/1.1 200 OK
< Server: nginx/...
< Content-Type: text/plain
<
OK
```

---

## 스크린샷

> 실제 배포 후 스크린샷을 이 위치에 삽입한다.

```
[스크린샷: 브라우저 또는 터미널 curl 결과]
<access-result-screenshot.png 파일 첨부>
```

---

## 확인 결과

- [ ] HTTP 200 응답 수신
- [ ] `Server: nginx` 헤더 포함
- [ ] 퍼블릭 IP로 외부 접근 성공

---

> **작성 방법**: 실제 AWS 배포 완료 후 `<퍼블릭IP>` 자리에 실제 IP를 입력하고,
> curl/브라우저 결과 스크린샷 파일을 이 파일과 같은 `docs/` 폴더에 추가한다.
> 스크린샷 파일명 예: `access-result-screenshot.png`
