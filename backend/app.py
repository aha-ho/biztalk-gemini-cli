import os
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from groq import Groq, APIError
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Flask 애플리케이션 초기화.
# 'frontend' 디렉토리를 static 및 template 폴더로 지정하여 정적 파일과 HTML 템플릿을 제공합니다.
app = Flask(__name__,
            static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend')),
            template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend')),
            static_url_path='/')
# 프론트엔드 모든 출처에서의 요청을 허용
CORS(app) 

# Groq 클라이언트 초기화
# API 키는 환경 변수 'GROQ_API_KEY'에서 자동으로 로드됩니다.
groq_client = None
try:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set.")
    groq_client = Groq(api_key=api_key)
    logging.info("Groq client initialized successfully.")
except ValueError as e:
    logging.error(f"Configuration Error: {e}")
except Exception as e:
    logging.error(f"Error initializing Groq client: {e}")

# 대상별 프롬프트 템플릿 정의
PROMPT_TEMPLATES = {
    "Upward": {
        "system": "당신은 상사에게 보고하는 정중하고 격식 있는 비즈니스 어투 변환 전문가입니다. 주어진 텍스트를 결론부터 명확하게 제시하는 보고 형식의 정중한 격식체로 변환해주세요. 불필요한 사족은 제거하고 핵심 내용을 간결하게 전달하는 데 집중합니다.",
        "user_template": "다음 내용을 상사에게 보고하는 방식으로 변환해 주세요:\n\n{text}"
    },
    "Lateral": {
        "system": "당신은 타팀 동료와 협업하는 친절하고 상호 존중하는 비즈니스 어투 변환 전문가입니다. 주어진 텍스트를 친근하면서도 요청 사항과 마감 기한을 명확히 전달하는 협조 요청 형식으로 변환해주세요. 긍정적이고 협력적인 분위기를 조성하는 데 중점을 둡니다.",
        "user_template": "다음 내용을 타팀 동료에게 협조 요청하는 방식으로 변환해 주세요:\n\n{text}"
    },
    "External": {
        "system": "당신은 고객 응대 전문 비즈니스 어투 변환 전문가입니다. 주어진 텍스트를 극존칭을 사용하며 전문성과 서비스 마인드를 강조하는 고객 응대 형식으로 변환해주세요. 안내, 공지, 사과 등 목적에 부합하게 신뢰감을 주는 어투를 사용합니다.",
        "user_template": "다음 내용을 고객에게 응대하는 방식으로 변환해 주세요:\n\n{text}"
    }
}

@app.route('/api/convert', methods=['POST'])
def convert_text():
    """
    텍스트 변환을 위한 API 엔드포인트.
    사용자 입력 텍스트를 선택된 대상에 맞춰 Groq AI API를 통해 변환합니다.
    """
    if groq_client is None:
        logging.error("Groq client is not initialized. Cannot process request.")
        return jsonify({"error": "서비스 준비 중입니다. 잠시 후 다시 시도해주세요."}), 503

    data = request.json
    original_text = data.get('text')
    target = data.get('target')

    if not original_text or not target:
        logging.warning("Bad request: 'text' or 'target' is missing.")
        return jsonify({"error": "텍스트와 변환 대상은 필수입니다."}), 400

    if target not in PROMPT_TEMPLATES:
        logging.warning(f"Bad request: Invalid target '{target}' provided.")
        return jsonify({"error": "유효하지 않은 변환 대상입니다."}), 400

    prompt_data = PROMPT_TEMPLATES[target]
    system_prompt = prompt_data["system"]
    user_prompt = prompt_data["user_template"].format(text=original_text)

    try:
        logging.info(f"Attempting to convert text for target: {target}")
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            model="moonshotai/kimi-k2-instruct-0905", # PRD에 명시된 모델 사용
            temperature=0.7, # 창의성 조절
            max_tokens=500, # 최대 응답 길이 제한
        )
        converted_text = chat_completion.choices[0].message.content
        logging.info(f"Successfully converted text for target: {target}")
        
        response_data = {
            "original_text": original_text,
            "converted_text": converted_text,
            "target": target
        }
        
        return jsonify(response_data), 200

    except APIError as e:
        logging.error(f"Groq API Error for target '{target}': {e}")
        return jsonify({"error": f"AI 변환 서비스 오류가 발생했습니다: {e.code}. 잠시 후 다시 시도해주세요."}), 500
    except Exception as e:
        logging.error(f"An unexpected error occurred during text conversion for target '{target}': {e}")
        return jsonify({"error": "알 수 없는 오류가 발생했습니다. 잠시 후 다시 시도해주세요."}), 500

@app.route('/')
def index():
    """
    루트 경로 요청 시 frontend/index.html 파일을 렌더링합니다.
    """
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)