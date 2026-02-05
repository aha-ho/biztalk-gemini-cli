import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
from github import Github

# .env 파일에서 환경 변수 로드
load_dotenv()

app = Flask(__name__)
# 프론트엔드からの 모든 출처에서의 요청을 허용
CORS(app) 

# Groq 클라이언트 초기화
# API 키는 환경 변수 'GROQ_API_KEY'에서 자동으로 로드됩니다.
try:
    groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    print("Groq client initialized successfully.")
except Exception as e:
    groq_client = None
    print(f"Error initializing Groq client: {e}")

# GitHub 클라이언트 초기화
github_client = None
try:
    github_token = os.environ.get("GITHUB_TOKEN")
    if github_token:
        github_client = Github(github_token)
        print("GitHub client initialized successfully.")
    else:
        print("GITHUB_TOKEN environment variable not set. GitHub client not initialized.")
except Exception as e:
    print(f"Error initializing GitHub client: {e}")

@app.route('/api/convert', methods=['POST'])
def convert_text():
    """
    텍스트 변환을 위한 API 엔드포인트.
    Sprint 1에서는 실제 변환 로직 대신 더미 데이터를 반환합니다.
    """
    data = request.json
    original_text = data.get('text')
    target = data.get('target')

    if not original_text or not target:
        return jsonify({"error": "텍스트와 변환 대상은 필수입니다."}), 400

    # Sprint 1: 실제 Groq API 호출 대신 더미 응답 반환
    dummy_response = f"'{original_text}'를 '{target}'에게 보내는 말투로 변환한 결과입니다. (이것은 더미 응답입니다.)"
    
    response_data = {
        "original_text": original_text,
        "converted_text": dummy_response,
        "target": target
    }
    
    return jsonify(response_data)

@app.route('/api/create-repo', methods=['POST'])
def create_github_repo():
    """
    GitHub 리포지토리 생성을 위한 API 엔드포인트.
    """
    if not github_client:
        return jsonify({"error": "GitHub 클라이언트가 초기화되지 않았습니다. GITHUB_TOKEN을 설정해주세요."}), 500

    data = request.json
    repo_name = data.get('name')
    repo_description = data.get('description', '') # Description is optional

    if not repo_name:
        return jsonify({"error": "리포지토리 이름은 필수입니다."}), 400

    try:
        user = github_client.get_user()
        repo = user.create_repo(repo_name, description=repo_description)
        return jsonify({
            "message": f"리포지토리 '{repo_name}'가 성공적으로 생성되었습니다.",
            "repo_url": repo.html_url
        }), 201
    except Exception as e:
        return jsonify({"error": f"리포지토리 생성 중 오류 발생: {str(e)}"}), 500

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)