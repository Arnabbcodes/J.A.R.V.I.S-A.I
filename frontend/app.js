
const API_BASE = "http://127.0.0.1:8000";

const el = {
  coreBtn:      document.getElementById('coreBtn'),
  statusText:   document.getElementById('statusText'),
  statusSub:    document.getElementById('statusSub'),
  console:      document.getElementById('console'),
  textInput:    document.getElementById('textInput'),
  textSend:     document.getElementById('textSend'),
  connDot:      document.getElementById('connDot'),
  connLabel:    document.getElementById('connLabel'),
  clock:        document.getElementById('clock'),
  uptime:       document.getElementById('uptime'),
  latency:      document.getElementById('latency'),
  mApi:         document.getElementById('mApi'),
  mApiBar:      document.getElementById('mApiBar'),
  mNeural:      document.getElementById('mNeural'),
  mNeuralBar:   document.getElementById('mNeuralBar'),
  mVoice:       document.getElementById('mVoice'),
  procState:    document.getElementById('procState'),
  quickCommands:document.getElementById('quickCommands'),
  micHint:      document.getElementById('micHint'),
};

let bootTime = Date.now();

function pad(n){ return n.toString().padStart(2, '0'); }

function tickClock(){
  const now = new Date();
  el.clock.textContent = `${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`;

  const upSec = Math.floor((Date.now() - bootTime) / 1000);
  const h = Math.floor(upSec / 3600), m = Math.floor((upSec % 3600) / 60), s = upSec % 60;
  el.uptime.textContent = `${pad(h)}:${pad(m)}:${pad(s)}`;
}
setInterval(tickClock, 1000);
tickClock();

function logLine(tag, text, kind){
  const line = document.createElement('div');
  line.className = `console-line ${kind}`;
  line.innerHTML = `<span class="line-tag">${tag}</span><span class="line-text"></span>`;
  line.querySelector('.line-text').textContent = text;
  el.console.appendChild(line);
  el.console.scrollTop = el.console.scrollHeight;
}

function setState(state){
  document.body.classList.remove('state-listening', 'state-thinking', 'state-speaking');
  el.procState.textContent = 'Idle';

  if (state === 'listening'){
    document.body.classList.add('state-listening');
    el.statusText.textContent = 'Listening…';
    el.statusSub.textContent = 'Speak your command now';
    el.procState.textContent = 'Listening';
  } else if (state === 'thinking'){
    document.body.classList.add('state-thinking');
    el.statusText.textContent = 'Thinking…';
    el.statusSub.textContent = 'Processing your request';
    el.procState.textContent = 'Thinking';
  } else if (state === 'speaking'){
    document.body.classList.add('state-speaking');
    el.statusText.textContent = 'Speaking…';
    el.statusSub.textContent = 'JARVIS is responding';
    el.procState.textContent = 'Speaking';
  } else {
    el.statusText.textContent = 'System Ready';
    el.statusSub.textContent = 'Tap the core or press the mic to speak';
  }
}
setState('idle');

function speak(text){
  return new Promise((resolve) => {
    if (!('speechSynthesis' in window)){
      resolve();
      return;
    }
    setState('speaking');
    const utter = new SpeechSynthesisUtterance(text);
    utter.rate = 1.02;
    utter.onend = () => { setState('idle'); resolve(); };
    utter.onerror = () => { setState('idle'); resolve(); };
    window.speechSynthesis.cancel(); // stop any overlapping speech first
    window.speechSynthesis.speak(utter);
  });
}

async function sendCommand(text){
  if (!text || !text.trim()) return;

  logLine('YOU', text, 'user');
  setState('thinking');

  const started = performance.now();
  try{
    const res = await fetch(`${API_BASE}/api/command`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    });

    const elapsed = Math.round(performance.now() - started);
    el.latency.textContent = `${elapsed} ms`;

    if (!res.ok){
      throw new Error(`Server responded ${res.status}`);
    }

    const data = await res.json();
    logLine('JARVIS', data.reply, 'jarvis');

    if (data.action === 'open_url' && data.url){
      window.open(data.url, '_blank', 'noopener');
    }
    if (data.action === 'desktop_only'){
      logLine('SYS', 'Tip: desktop-only commands work when you run main.py directly on your machine.', 'system');
    }

    await speak(data.reply);

    if (data.exit){
      logLine('SYS', 'Session ended by JARVIS.', 'system');
    }
  } catch (err){
    console.error(err);
    logLine('SYS', `Could not reach the backend at ${API_BASE}. Is server.py running?`, 'error');
    setState('idle');
  }
}
const SpeechRecognitionAPI = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognizer = null;
let isListening = false;

if (SpeechRecognitionAPI){
  recognizer = new SpeechRecognitionAPI();
  recognizer.lang = 'en-IN';        // matches main.py's recognize_google(..., language='en-in')
  recognizer.continuous = false;
  recognizer.interimResults = false;

  recognizer.onstart = () => {
    isListening = true;
    setState('listening');
  };

  recognizer.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    sendCommand(transcript);
  };

  recognizer.onerror = (event) => {
    logLine('SYS', `Voice input error: ${event.error}`, 'error');
    setState('idle');
  };

  recognizer.onend = () => {
    isListening = false;
    if (document.body.classList.contains('state-listening')){
      setState('idle');
    }
  };
} else {
  el.micHint.textContent = '🎙️ Voice input isn\'t supported in this browser — try Chrome or Edge. You can still type commands below.';
}

el.coreBtn.addEventListener('click', () => {
  if (!recognizer){
    el.textInput.focus();
    return;
  }
  if (isListening){
    recognizer.stop();
  } else {
    try{
      recognizer.start();
    } catch(e){
      // start() throws if called twice in quick succession; ignore
    }
  }
});
el.textSend.addEventListener('click', () => {
  const val = el.textInput.value;
  el.textInput.value = '';
  sendCommand(val);
});
el.textInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter'){
    const val = el.textInput.value;
    el.textInput.value = '';
    sendCommand(val);
  }
});

el.quickCommands.addEventListener('click', (e) => {
  const btn = e.target.closest('button[data-cmd]');
  if (!btn) return;
  sendCommand(btn.dataset.cmd);
});
async function checkHealth(){
  try{
    const started = performance.now();
    const res = await fetch(`${API_BASE}/api/health`);
    const elapsed = Math.round(performance.now() - started);

    if (res.ok){
      el.connDot.classList.remove('offline');
      el.connDot.classList.add('online');
      el.connLabel.textContent = 'System Online';
      el.mApi.textContent = 'Connected';
      el.mApiBar.style.width = '92%';
      el.mNeural.textContent = 'Active';
      el.mNeuralBar.style.width = '85%';
      el.mVoice.textContent = recognizer ? 'Ready' : 'Text Only';
      el.latency.textContent = `${elapsed} ms`;
    } else {
      throw new Error('unhealthy');
    }
  } catch(err){
    el.connDot.classList.remove('online');
    el.connDot.classList.add('offline');
    el.connLabel.textContent = 'Backend Offline';
    el.mApi.textContent = 'Disconnected';
    el.mApiBar.style.width = '5%';
  }
}
checkHealth();
setInterval(checkHealth, 15000);
