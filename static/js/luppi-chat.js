/**
 * LUPPI AI — client for Django intelligence API
 */
(function () {
  'use strict';

  const aiMessages = document.getElementById('sw-ai-messages');
  const aiInput = document.getElementById('sw-ai-input');
  const aiSendBtn = document.getElementById('sw-ai-send');
  const aiVoiceBtn = document.getElementById('sw-ai-voice');

  if (!aiMessages || !aiInput) return;

  const chatUrl = document.body.dataset.luppiChatUrl;
  if (!chatUrl) return;

  function getCsrfToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    if (meta) return meta.getAttribute('content');
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : '';
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  function addMessage(text, isUser) {
    const div = document.createElement('div');
    div.className = 'sw-msg' + (isUser ? ' sw-msg--user' : ' sw-msg--ai');
    div.innerHTML =
      '<div class="sw-msg__avatar">' + (isUser ? '👤' : '🌙') + '</div>' +
      '<div class="sw-msg__bubble">' + escapeHtml(text).replace(/\n/g, '<br>') + '</div>';
    aiMessages.appendChild(div);
    aiMessages.scrollTop = aiMessages.scrollHeight;
  }

  function showTyping() {
    const div = document.createElement('div');
    div.className = 'sw-msg sw-msg--ai';
    div.id = 'sw-typing';
    div.innerHTML =
      '<div class="sw-msg__avatar">🌙</div>' +
      '<div class="sw-typing"><span></span><span></span><span></span></div>';
    aiMessages.appendChild(div);
    aiMessages.scrollTop = aiMessages.scrollHeight;
  }

  function removeTyping() {
    document.getElementById('sw-typing')?.remove();
  }

  async function fetchLuppiReply(message) {
    const res = await fetch(chatUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      },
      credentials: 'same-origin',
      body: JSON.stringify({ message: message }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || 'Request failed');
    }
    return res.json();
  }

  let sending = false;

  async function sendMessageWithText(text) {
    const trimmed = (text || '').trim();
    if (!trimmed || sending) return;

    sending = true;
    addMessage(trimmed, true);
    aiInput.value = '';
    if (aiSendBtn) aiSendBtn.disabled = true;
    showTyping();

    const delay = 600 + Math.random() * 700;

    try {
      const [data] = await Promise.all([
        fetchLuppiReply(trimmed),
        new Promise((r) => setTimeout(r, delay)),
      ]);
      removeTyping();
      addMessage(data.reply, false);

      if (window._swVoiceOutput && 'speechSynthesis' in window) {
        const plain = data.reply.replace(/[🌙💙🙏]/g, '');
        const utt = new SpeechSynthesisUtterance(plain);
        utt.lang = 'hi-IN';
        utt.rate = 0.88;
        utt.pitch = 1.05;
        speechSynthesis.speak(utt);
      }
    } catch (e) {
      removeTyping();
      addMessage(
        'कुछ गड़बड़ हुई — फिर से try करो। अगर बार-बार हो, page refresh करो।',
        false
      );
      console.error('LUPPI:', e);
    } finally {
      sending = false;
      if (aiSendBtn) aiSendBtn.disabled = false;
      aiInput.focus();
    }
  }

  function sendMessage() {
    sendMessageWithText(aiInput.value);
  }

  if (aiSendBtn) aiSendBtn.addEventListener('click', sendMessage);
  aiInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  document.querySelectorAll('.sw-quick-prompt').forEach((btn) => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const prompt = btn.getAttribute('data-prompt');
      if (!prompt) return;
      sendMessageWithText(prompt);
    });
  });

  if (aiVoiceBtn) {
    let recognition = null;

    aiVoiceBtn.addEventListener('click', () => {
      if (aiVoiceBtn.classList.contains('active') && !aiVoiceBtn.classList.contains('listening')) {
        aiVoiceBtn.classList.remove('active');
        window._swVoiceOutput = false;
        return;
      }

      if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
        alert('Voice के लिए Chrome browser use करो।');
        return;
      }

      if (aiVoiceBtn.classList.contains('listening')) {
        recognition && recognition.stop();
        aiVoiceBtn.classList.remove('listening');
        aiVoiceBtn.textContent = '🎤';
        return;
      }

      aiVoiceBtn.classList.add('active');
      window._swVoiceOutput = true;

      const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognition = new SR();
      recognition.lang = 'hi-IN';
      recognition.continuous = false;
      recognition.interimResults = false;

      recognition.onstart = () => {
        aiVoiceBtn.classList.add('listening');
        aiVoiceBtn.textContent = '🔴';
      };
      recognition.onresult = (e) => {
        aiInput.value = e.results[0][0].transcript;
      };
      recognition.onend = () => {
        aiVoiceBtn.classList.remove('listening');
        aiVoiceBtn.textContent = '🎤';
        if (aiInput.value.trim()) sendMessage();
      };
      recognition.onerror = () => {
        aiVoiceBtn.classList.remove('listening');
        aiVoiceBtn.textContent = '🎤';
      };
      recognition.start();
    });
  }
})();
