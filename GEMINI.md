# Gemini Context: BizTone Converter

## 프로젝트 개요

이 프로젝트는 AI 기반 웹 솔루션인 "BizTone 변환기"로, 사용자의 일상 언어를 전문적인 비즈니스 커뮤니케이션으로 변환하도록 설계되었습니다. Groq AI API를 활용하여 다양한 대상(상사, 동료, 고객)에 맞는 적절한 어조로 텍스트를 변환합니다.

- **백엔드**: Flask 웹 프레임워크를 사용하는 Python 기반 서버입니다. 프론트엔드를 제공하고, RESTful API 엔드포인트(`/api/convert`)를 제공하며, Groq AI API 호출 로직을 처리합니다.
- **프론트엔드**: 바닐라 HTML, JavaScript(ES6+), Tailwind CSS(CDN을 통해)로 스타일링된 단일 페이지 애플리케이션입니다. 텍스트 입력, 대상 선택 및 변환된 출력을 볼 수 있는 사용자 친화적인 인터페이스를 제공합니다.
- **AI 통합**: 핵심 변환 로직은 Groq AI API를 통한 `moonshotai/kimi-k2-instruct-0905` 모델에 의해 구동됩니다. 백엔드에는 각 통신 대상에 맞춰진 프롬프트 엔지니어링이 포함됩니다.

## 빌드 및 실행

### 1. 백엔드 설정

백엔드는 Python과 여러 패키지가 필요한 Flask 애플리케이션입니다.

- **전제 조건**:
    - Python 3.x
    - 프로젝트 루트에 Groq AI API 키가 포함된 `.env` 파일:
      ```
      GROQ_API_KEY="여기에-API-키를-입력하세요"
      ```

- **설치**:
  `backend` 디렉토리에서 필요한 Python 패키지를 설치합니다:
  ```bash
  pip install -r backend/requirements.txt
  ```

- **서버 실행**:
  `app.py` 스크립트를 실행하여 Flask 개발 서버를 시작합니다:
  ```bash
  python backend/app.py
  ```
  서버는 `http://127.0.0.1:5000`에서 시작됩니다.

### 2. 프론트엔드 액세스

프론트엔드는 Flask 백엔드에서 직접 제공하는 정적 애플리케이션입니다. 백엔드 서버가 실행 중이면 웹 브라우저에서 다음 URL로 이동하여 애플리케이션에 액세스할 수 있습니다:

- **URL**: `http://127.0.0.1:5000`

## 개발 규칙

- **프로젝트 구조**: 코드베이스는 `frontend` 및 `backend` 디렉토리로 명확하게 분리되어 모듈성을 높입니다.
- **API**: 백엔드는 `text` 및 `target`(`Upward`, `Lateral`, `External`)이 포함된 JSON 페이로드를 허용하고 변환된 텍스트를 반환하는 단일 API 엔드포인트 `POST /api/convert`를 노출합니다.
- **프론트엔드 로직**: 모든 클라이언트 측 로직은 `frontend/js/script.js`에 포함됩니다. 사용자 입력을 처리하고, 백엔드에 비동기 `fetch` 호출을 수행하며, 결과로 DOM을 업데이트합니다.
- **스타일링**: UI는 `index.html` 파일에 직접 Tailwind CSS 유틸리티 클래스를 사용하여 스타일링됩니다. 원래 `style.css`는 더 이상 사용되지 않습니다.
- **문서화**: `PRD.md` 및 `프로그램개요서.md` 파일은 목표, 요구 사항, 아키텍처 및 릴리스 계획을 설명하는 포괄적인 프로젝트 문서 역할을 합니다.