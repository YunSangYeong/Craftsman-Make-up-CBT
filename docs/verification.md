# 검증 기록

## 재사용 근거

2026-10-27 최신 main 확인: YunSangYeong/electrician-cbt `76b990b8720adfa85c22a0a8f699b17094aa357b`.
표준 v1.4.0의 폴더 전체를 복사했다. 기준 앱은 표준이 고정한
`b9a682ccff1b460334b78d5bfad9375b7ec4fbb6`의 App, model, CSS, 도구 설정과 테스트·Pages workflow다.
원본 프로젝트에 대한 수정·푸시·배포는 하지 않았다. MIT 코드 고지를 보존했다.
대상 초기 상태는 README만 있고 AGENTS.md와 로컬 변경은 없었다. 기존 README의 제목·소개를 보존해 확장했다.

## 공식 규칙과 자료 접근

공식 확인 시도 대상: https://www.q-net.or.kr/crf005.do?id=crf00503&jmCd=7967
실제 결과: curl exit 56, `CONNECT tunnel failed, response 403`, HTTP 000.
공식 본문을 읽지 못했으므로 과목명·규칙·현행 출제기준 확인은 **차단/미완료**다.
이 URL의 종목 대응까지 확인 완료했다고 주장하지 않는다. 공식 원문 기출과 재배포 조건도 확인하지 못했다.
Q-Net 두 도메인을 환경 설정 초안에 추가했으나 저장은 현재 실행 환경의 적용·공개 게시와 다르다.

앱 `src/qualification.ts`의 60문항·60분·객관식 4지선다·100점 환산·60점 이상 합격·과락 없음은
**AI 일반 지식에 따른 학습용 가정**이다. 원본 전기 시험의 규칙을 대상의 공식 사실로 인용하지 않는다.
메이크업 개론/공중위생관리학/화장품학은 학습 영역 구분이며 공식 명칭·배분 확인은 미완료다.
전 영역 통합 무작위 60개 추출, 과목별 균등 할당 없음. 미응답은 오답이며 점수 표시만 소수 첫째 자리 반올림한다.
합격 판정은 반올림 전 정답 비율로 한다. 임상 진단·처방이나 미확인 법령의 수치를 문항에 넣지 않았다.
공식 규칙이 확인되면 별도 변경·검증이 필요하다.

## 문제은행 검토 범위

기본 JSON 실제 **1,000개**, 내부 검토 1,000개, 부족 0개. 공식 출제기준 대조·외부 전문가 검수는 미완료다.
메이크업 개론 440 / 공중위생관리학 280 / 화장품학 280.
원문 기출 0 / 복원 0 / 자체 제작 1,000 / 계산 0 / 숫자 조건 변형 0 / 변형 family 0.
검증 대기 기본 문항 0 / 개인 로컬 등록분 집계 제외.

기존 개념·상황형 90개는 ID부터 출처 메타데이터까지 보존했다.
추가 910개는 scripts/makeup-expanded.txt의 91개 단원 × 10개 설명 판별 문항이다.
설명별로 한 문제만 만들며, 보기 순서 재배열과 숫자 변형으로 수량을 늘리지 않는다.
원고의 설명-정답 관계와 같은 단원의 오답 개념 설명을 함께 해설로 제공한다.
상세 단원 수와 검토 범위는 [bank-review.md](bank-review.md)를 본다.

문항은 AI 일반 지식으로 직접 작성했다. 외부 교재·공식 자료를 읽었다고 인용하지 않았다.
작성 원고는 scripts/makeup-items.txt 및 scripts/makeup-expanded.txt, 결정적 생성기는 scripts/generate-bank.py다.
보기 위치는 고정 ID 기준으로 결정하며 출제 연도·회차는 모두 null이다.
sourceUrl은 실제 보존 브랜치의 원고 위치이며 외부 정답 증명이 아니다.
자체 문항·양식은 CC BY 4.0이며 앱의 MIT 고지를 보존한다.

내부 검토에서는 설명의 구별 가능성·개념 오류·과도한 단정·정답 누출을 확인했다.
정규화 본문, ID, 본문+정렬 보기 중복 0. 동일 개념의 다른 적용 상황과 반대 개념을 비교하는 문항은 포함한다.
1,000개를 서로 독립된 1,000개 개념이라고 주장하지 않는다. 의미 검토는 작성 에이전트의 내부 검토다.
외부 전문가의 독립 검수, 공식 기준 대조, 법령 판본 대조, 난이도·시험 대표성 검증은 **미실행**이다.

## 로컬 인수

환경: Node 24.19.0, npm 11.9.0, Linux /usr/bin/chromium.
작업 디렉터리 /workspace/Craftsman-Make-up-CBT.

- npm ci --cache /workspace/.npm-cache: 성공, lockfile 기반 110 packages.
- npm test: 20개 통과. 중복·형식·합격 경계 35/36 정답·시간·만료 답안·단일 제출·순회·가져오기·복구.
- npm run build: TypeScript + Vite 프로덕션 빌드 성공.
- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e:
  Chromium PC 및 Pixel 7 에뮬레이션. 두 모드 실제 답안·Space keydown/keyup·포커스·마지막 문제 보호,
  새로고침·만료·결과·오답 복습·북마크·통계·JSON/CSV·오류 원자성·초기화·저장 손상/실패 확인.
  작은 메뉴는 390×480, 740×360, 390×360 글자 확대 조건에서 실제 mouse.wheel 입력과
  CDP touchStart/move/end 스와이프를 별도로 사용했다. scrollTop 직접 대입은 사용하지 않았다.
  아래 이동 후 백업 파일 다운로드·초기화 대화상자 취소, 위로 복귀 후 대시보드 클릭 및 배경 고정 확인.
  터치 미지원 desktop 프로젝트의 터치 3건만 의도적으로 skip. 모바일 터치 3건은 실행 대상이다.
- 실기기 Android/iOS, WebKit, iframe 키보드/저장 제약: 미실행. 지원을 검증했다고 주장하지 않는다.

최종 실행 결과와 원격/배포 결과는 README의 상태 기록을 함께 본다.


## 현재 검증 결과와 이전 배포 첫 차단

최종 전체 검사: 단위 20 passed (exit 0), 브라우저 29 passed / 3 intentionally skipped / 0 failed (exit 0),
프로덕션 TypeScript/Vite build exit 0. 실제 개발 서버도 시작하여 HTTP 응답과 PC·모바일 제목을 확인했다.
PC 1440×1000와 모바일 390×844 화면을 캡처하고 시각 검토했다. 메뉴의 3개 화면 조건은 휠·모바일 터치 모두 통과했다.
로컬 검사 중 배너 회귀 검사가 통계 보관 안내까지 오탐한 적이 있어 금지된 면책 문구 기준으로 수정 후 전체 재검증했다.

초기 구현 배포 사전 확인 당시 GH_TOKEN은 설정됨(값 미출력), GITHUB_TOKEN은 미설정이었다.
기존 인증으로 실행한 첫 명령:
`gh api repos/YunSangYeong/Craftsman-Make-up-CBT --jq '{full_name,default_branch,permissions,has_pages}'`
종료 코드 1, 실제 오류:
`Get "https://api.github.com/repos/YunSangYeong/Craftsman-Make-up-CBT": Forbidden`
현재 적용 HTTP 정책에 api.github.com은 포함되지 않았다. 원격 Git 읽기가 된다는 사실과 API 접근은 구분한다.
이 응답만으로 Pages 미설정이나 토큰 권한 부족을 확정하지 않는다.
첫 차단 뒤 API 재요청·Pages 조회·workflow 실행·main 푸시·재배포/대체 경로는 수행하지 않았다.
CI/Pages 실행은 시작하지 않았으며 현재 게시 상태와 공개 화면은 미확인이다.
GitHub 코드 보존은 `codex/makeup-cbt-standard` 브랜치로만 진행한다. workflow는 main push/PR/수동만 받으므로
이 브랜치 단순 push는 Actions·Pages를 유발하지 않는다. PR도 생성하지 않는다.
출처 원고 링크는 실제 보존 브랜치를 가리키며 main에 반영됐다고 주장하지 않는다.
사용자 첫 조치: 이 클라우드 환경의 네트워크 허용 도메인에 api.github.com을 추가한다.
이후 마무리는 사용자 담당이며 새로운 명시적 실행 요청 전에는 에이전트가 재시도하지 않는다.

환경 재사용용 install_script(npm ci)와 start_skill(기존 checkout, dev 서버 재시작, readiness/test 명령)을 저장했다.
Q-Net 도메인 추가도 초안으로만 저장했다. 설정 저장은 실행 환경 적용·Publish·GitHub Pages 게시가 아니다.


## 1,000문항 확대 시 확인

- 첫 90개 JSON 객체의 고정 SHA-256: `6733487203b338e0f8ee81e1b55279dca94c20a662eec2531997a2646c4b5844`. 단위 테스트로 보존 검증.
- 추가 원고 910개와 실제 정답 번호·설명·출처 일치 검증. 정규화 설명 중복과 답안 누출 없음.
- 새 수량 1,000개와 50페이지, 마지막 MU-1000의 해설·출처를 PC/모바일에서 확인.
- 전체 브라우저 회귀: 29 통과 / 3 의도적 제외. 이후 강화한 마지막 문항 검사도 해당 PC/모바일 사례에서 재검증.
- 빌드는 성공했으나 정적 문항을 포함한 JS 약 2.06 MB (gzip 약 202 kB)로 Vite의 500 kB 청크 권고 경고가 있음. 이를 숨기거나 기준을 바꾸지 않음.
- 현재 요청은 문제은행 확대이며 앞선 배포 차단을 해제하는 요청이 아님. 배포 API 재시도·main 푸시·workflow 실행 없음.
