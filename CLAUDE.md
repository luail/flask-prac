# 프로젝트 규칙 (CLAUDE.md)

## 프로젝트 개요
GitHub 트렌딩 저장소를 크롤링해서 Flask API로 제공하는 서버
학습 목적: 스펙 주도 개발 + 서브에이전트 워크플로우 익히기

## 기술 스택
- Python 3.11, Flask 3.x
- BeautifulSoup4, requests (크롤링)
- Pydantic (DTO 검증)

## 개발 프로세스 (필수)
1. 작업 시작 전 반드시 SPEC.md 읽기
2. 스펙에 없는 내용은 임의로 구현하지 말고 질문
3. 구현 완료 후 SPEC.md의 체크리스트 업데이트

## 에이전트 규칙
- 작업 전 .claude/memory/ 에서 관련 파일만 읽기 (전체 X)
- 작업 후 memory/ 업데이트 필수
- 각 에이전트는 자신의 역할 범위만 수행

## 코딩 규칙
- 함수 하나당 하나의 역할
- 크롤링 전 robots.txt 확인
- 에러는 반드시 핸들링하고 의미있는 메시지 반환
- 커밋 메시지: feat/fix/refactor 접두사 사용