# 웹 서비스 외부 접속 증거

> 방식 (A) 선택: 브라우저에서 `http://<퍼블릭IP>` 접속

---

## 1. 접속 정보

| 항목 | 값 |
|------|----|
| 퍼블릭 IP | `13.54.93.162` |
| 포트 | `80` (HTTP) |
| 서버 | EC2 (`ap-northeast-2a`, Ubuntu) |
| 웹 서버 | Nginx 1.28.3 |
| 접속 방식 | (A) 웹 브라우저에서 `http://13.54.93.162` 접속 |

---

## 2. 브라우저 외부 접속 증거 스크린샷 (A방식)

![웹 서비스 외부 접속 결과 (A방식 브라우저 접속)](./screenshot/trouble_shooting_2.png)

### 화면 출력 내용

```text
Welcome to nginx!

If you see this page, the nginx web server is successfully installed and working.
Further configuration is required.

For online documentation and support please refer to nginx.org.
Commercial support is available at nginx.com.

Thank you for using nginx.
```

---

## 3. HTTP 응답 헤더 검증 (200 OK)

```bash
curl -I http://13.54.93.162
```

```http
HTTP/1.1 200 OK
Server: nginx/1.28.3 (Ubuntu)
Date: Sat, 12 Sep 2026 10:46:23 GMT
Content-Type: text/html
Content-Length: 615
Last-Modified: Sat, 12 Sep 2026 09:55:11 GMT
Connection: keep-alive
ETag: "6aa5217f-267"
Accept-Ranges: bytes
```

---

## 4. 확인 결과

- [x] 브라우저 주소창에서 `http://13.54.93.162` 외부 접속 성공
- [x] Nginx 기본 페이지("Welcome to nginx!") 정상 표시 확인
- [x] HTTP 200 OK 정상 응답 및 `Server: nginx/1.28.3 (Ubuntu)` 헤더 확인
- [x] 보안 그룹 HTTP(80) 0.0.0.0/0 허용 규칙을 통한 전 세계 외부 접근 검증 완료

