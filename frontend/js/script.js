document.addEventListener('DOMContentLoaded', () => {
    const originalTextInput = document.getElementById('original-text');
    const convertedTextDiv = document.getElementById('converted-text');
    const convertBtn = document.getElementById('convert-btn');
    const copyBtn = document.getElementById('copy-btn');
    const charCounter = document.getElementById('char-counter');
    const targetAudienceSelect = document.getElementById('target-audience');

    const MAX_CHARS = 500;

    // Character counter
    originalTextInput.addEventListener('input', () => {
        const count = originalTextInput.value.length;
        charCounter.textContent = `${count} / ${MAX_CHARS}`;
        if (count > MAX_CHARS) {
            charCounter.style.color = '#D0021B';
        } else {
            charCounter.style.color = '#999';
        }
    });

    // Convert button click
    convertBtn.addEventListener('click', async () => {
        const text = originalTextInput.value;
        const target = targetAudienceSelect.value;

        if (!text.trim()) {
            alert('변환할 텍스트를 입력해주세요.');
            return;
        }

        if (text.length > MAX_CHARS) {
            alert(`입력 텍스트는 ${MAX_CHARS}자를 초과할 수 없습니다.`);
            return;
        }

        convertBtn.disabled = true;
        convertBtn.textContent = '변환 중...';
        convertedTextDiv.classList.remove('converted-text-placeholder');
        convertedTextDiv.textContent = 'AI가 문장을 다듬고 있습니다...';

        try {
            const response = await fetch('http://127.0.0.1:5000/api/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text, target }),
            });

            if (!response.ok) {
                throw new Error('서버에서 오류가 발생했습니다.');
            }

            const data = await response.json();
            convertedTextDiv.textContent = data.converted_text;

        } catch (error) {
            convertedTextDiv.textContent = `오류가 발생했습니다: ${error.message}`;
            convertedTextDiv.style.color = '#D0021B';
        } finally {
            convertBtn.disabled = false;
            convertBtn.textContent = '변환하기';
        }
    });

    // Copy button click
    copyBtn.addEventListener('click', () => {
        const textToCopy = convertedTextDiv.textContent;
        if (textToCopy && !convertedTextDiv.classList.contains('converted-text-placeholder')) {
            navigator.clipboard.writeText(textToCopy).then(() => {
                const originalText = copyBtn.textContent;
                copyBtn.textContent = '복사 완료!';
                setTimeout(() => {
                    copyBtn.textContent = originalText;
                }, 2000);
            }).catch(err => {
                console.error('복사 실패:', err);
                alert('텍스트 복사에 실패했습니다.');
            });
        }
    });

    // Create repo button click
    const createRepoBtn = document.getElementById('create-repo-btn');
    const repoNameInput = document.getElementById('repo-name');
    const repoDescInput = document.getElementById('repo-desc');

    createRepoBtn.addEventListener('click', async () => {
        const repoName = repoNameInput.value;
        const repoDesc = repoDescInput.value;

        if (!repoName.trim()) {
            alert('리포지토리 이름을 입력해주세요.');
            return;
        }

        createRepoBtn.disabled = true;
        createRepoBtn.textContent = '생성 중...';

        try {
            const response = await fetch('http://127.0.0.1:5000/api/create-repo', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name: repoName, description: repoDesc }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || '서버에서 오류가 발생했습니다.');
            }

            alert(`리포지토리 생성 성공! URL: ${data.repo_url}`);
            repoNameInput.value = '';
            repoDescInput.value = '';

        } catch (error) {
            alert(`오류가 발생했습니다: ${error.message}`);
        } finally {
            createRepoBtn.disabled = false;
            createRepoBtn.textContent = '생성하기';
        }
    });
});
