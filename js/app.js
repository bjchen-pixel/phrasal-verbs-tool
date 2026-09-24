/**
 * PhrasalFlow Application Controller
 * Modern interactive English Phrasal Verbs Learning Tool
 */

(function () {
  'use strict';

  // State Management
  const state = {
    allVerbs: [],
    particlesMeta: {},
    currentTab: 'cards', // 'cards' | 'flashcards' | 'quiz' | 'mindmap'
    activeVerbFilter: 'all',
    activeParticleFilter: 'all',
    activeStatusFilter: 'all', // 'all' | 'learning' | 'mastered' | 'starred'
    searchQuery: '',
    
    // User progress
    starred: new Set(JSON.parse(localStorage.getItem('phrasal_starred') || '[]')),
    mastered: new Set(JSON.parse(localStorage.getItem('phrasal_mastered') || '[]')),
    theme: localStorage.getItem('phrasal_theme') || 'dark',

    // Audio engine
    audioMode: localStorage.getItem('phrasal_audio_mode') || 'mp3', // 'mp3' | 'tts'
    audioSpeed: parseFloat(localStorage.getItem('phrasal_audio_speed') || '1.0'),
    currentAudio: null,
    activeAudioBtn: null,

    // Flashcard state
    flashcardDeck: [],
    flashcardIndex: 0,
    flashcardFlipped: false,

    // Quiz state
    quizMode: 'meaning', // 'meaning' | 'cloze' | 'listening'
    quizCount: 10,
    quizQuestions: [],
    quizIndex: 0,
    quizScore: 0,
    quizWrongItems: [],
    quizActive: false,
    quizAnswered: false
  };

  // DOM Elements cache
  const elements = {};

  function init() {
    // Check if data is present
    if (window.PHRASAL_DATA && window.PHRASAL_DATA.verbs) {
      state.allVerbs = window.PHRASAL_DATA.verbs;
      state.particlesMeta = window.PHRASAL_DATA.meta.particles || {};
    } else {
      console.error('Phrasal verbs data failed to load.');
      return;
    }

    cacheDOM();
    applyTheme(state.theme);
    bindEvents();
    renderStats();
    renderFilterButtons();
    renderCardsView();
    initFlashcardDeck();
    updateAudioModeUI();
  }

  function cacheDOM() {
    elements.app = document.getElementById('app');
    elements.themeToggle = document.getElementById('themeToggle');
    elements.audioSpeedBtn = document.getElementById('audioSpeedBtn');
    elements.statTotal = document.getElementById('statTotal');
    elements.statMastered = document.getElementById('statMastered');
    elements.statStarred = document.getElementById('statStarred');

    elements.navTabCards = document.getElementById('navTabCards');
    elements.navTabFlashcards = document.getElementById('navTabFlashcards');
    elements.navTabQuiz = document.getElementById('navTabQuiz');
    elements.navTabMindmap = document.getElementById('navTabMindmap');

    elements.viewCards = document.getElementById('viewCards');
    elements.viewFlashcards = document.getElementById('viewFlashcards');
    elements.viewQuiz = document.getElementById('viewQuiz');
    elements.viewMindmap = document.getElementById('viewMindmap');

    elements.searchInput = document.getElementById('searchInput');
    elements.verbPillsContainer = document.getElementById('verbPillsContainer');
    elements.cardsContainer = document.getElementById('cardsContainer');
    elements.cardsCountLabel = document.getElementById('cardsCountLabel');

    // Flashcard elements
    elements.flashcardInner = document.getElementById('flashcardInner');
    elements.flashcardProgressText = document.getElementById('flashcardProgressText');
    elements.flashcardProgressBar = document.getElementById('flashcardProgressBar');
    elements.fcFrontPhrase = document.getElementById('fcFrontPhrase');
    elements.fcFrontBadge = document.getElementById('fcFrontBadge');
    elements.fcFrontScenario = document.getElementById('fcFrontScenario');
    elements.fcFrontAudioBtn = document.getElementById('fcFrontAudioBtn');
    elements.fcBackChinese = document.getElementById('fcBackChinese');
    elements.fcBackMeaning = document.getElementById('fcBackMeaning');
    elements.fcBackExample = document.getElementById('fcBackExample');
    elements.fcBackExChinese = document.getElementById('fcBackExChinese');
    elements.fcBackAudioBtn = document.getElementById('fcBackAudioBtn');
    elements.fcBtnPrev = document.getElementById('fcBtnPrev');
    elements.fcBtnNext = document.getElementById('fcBtnNext');
    elements.fcBtnFlip = document.getElementById('fcBtnFlip');
    elements.fcBtnShuffle = document.getElementById('fcBtnShuffle');
    elements.fcBtnMaster = document.getElementById('fcBtnMaster');
    elements.fcBtnReview = document.getElementById('fcBtnReview');

    // Quiz elements
    elements.quizSetup = document.getElementById('quizSetup');
    elements.quizPlay = document.getElementById('quizPlay');
    elements.quizResult = document.getElementById('quizResult');
    elements.quizStartBtn = document.getElementById('quizStartBtn');
    elements.quizQuestionCountSelect = document.getElementById('quizQuestionCountSelect');
    elements.quizPrompt = document.getElementById('quizPrompt');
    elements.quizScenarioBadge = document.getElementById('quizScenarioBadge');
    elements.quizAudioPlayBtn = document.getElementById('quizAudioPlayBtn');
    elements.quizOptionsContainer = document.getElementById('quizOptionsContainer');
    elements.quizProgressText = document.getElementById('quizProgressText');
    elements.quizProgressBar = document.getElementById('quizProgressBar');
    elements.quizNextBtn = document.getElementById('quizNextBtn');
    elements.quizScoreDisplay = document.getElementById('quizScoreDisplay');
    elements.quizAccuracyDisplay = document.getElementById('quizAccuracyDisplay');
    elements.quizReviewMistakesBtn = document.getElementById('quizReviewMistakesBtn');
    elements.quizRestartBtn = document.getElementById('quizRestartBtn');

    // Mindmap
    elements.mindmapContainer = document.getElementById('mindmapContainer');

    // Toast
    elements.toast = document.getElementById('toastNotice');
  }

  function bindEvents() {
    // Theme toggle
    elements.themeToggle.addEventListener('click', toggleTheme);

    // Audio Speed cycle
    elements.audioSpeedBtn.addEventListener('click', cycleAudioSpeed);

    // Nav tabs
    elements.navTabCards.addEventListener('click', () => switchTab('cards'));
    elements.navTabFlashcards.addEventListener('click', () => switchTab('flashcards'));
    elements.navTabQuiz.addEventListener('click', () => switchTab('quiz'));
    elements.navTabMindmap.addEventListener('click', () => switchTab('mindmap'));

    // Search and Status filters
    elements.searchInput.addEventListener('input', (e) => {
      state.searchQuery = e.target.value.trim().toLowerCase();
      renderCardsView();
    });

    document.querySelectorAll('[data-status-filter]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('[data-status-filter]').forEach(b => b.classList.remove('active'));
        e.currentTarget.classList.add('active');
        state.activeStatusFilter = e.currentTarget.dataset.statusFilter;
        renderCardsView();
      });
    });

    // Flashcard events
    elements.flashcardInner.addEventListener('click', toggleFlashcardFlip);
    elements.fcBtnFlip.addEventListener('click', toggleFlashcardFlip);
    elements.fcBtnNext.addEventListener('click', nextFlashcard);
    elements.fcBtnPrev.addEventListener('click', prevFlashcard);
    elements.fcBtnShuffle.addEventListener('click', shuffleFlashcardDeck);
    elements.fcBtnMaster.addEventListener('click', () => {
      const current = state.flashcardDeck[state.flashcardIndex];
      if (current) toggleMastered(current.id, true);
      nextFlashcard();
    });
    elements.fcBtnReview.addEventListener('click', () => {
      const current = state.flashcardDeck[state.flashcardIndex];
      if (current) toggleMastered(current.id, false);
      nextFlashcard();
    });

    elements.fcFrontAudioBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const current = state.flashcardDeck[state.flashcardIndex];
      if (current) playAudio(current.audio, current.phrasal, e.currentTarget);
    });

    elements.fcBackAudioBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const current = state.flashcardDeck[state.flashcardIndex];
      if (current) playAudio(current.exampleAudio, current.example, e.currentTarget);
    });

    // Quiz mode selection
    document.querySelectorAll('.quiz-mode-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.quiz-mode-btn').forEach(b => b.classList.remove('active'));
        e.currentTarget.classList.add('active');
        state.quizMode = e.currentTarget.dataset.quizMode;
      });
    });

    elements.quizStartBtn.addEventListener('click', startQuiz);
    elements.quizNextBtn.addEventListener('click', advanceQuizQuestion);
    elements.quizRestartBtn.addEventListener('click', () => {
      elements.quizResult.style.display = 'none';
      elements.quizSetup.style.display = 'flex';
    });
    elements.quizReviewMistakesBtn.addEventListener('click', startMistakesQuiz);

    // Global keyboard shortcuts
    window.addEventListener('keydown', handleKeyShortcuts);
  }

  function handleKeyShortcuts(e) {
    if (e.target.tagName === 'INPUT') return;

    if (state.currentTab === 'flashcards') {
      if (e.code === 'Space') {
        e.preventDefault();
        toggleFlashcardFlip();
      } else if (e.code === 'ArrowRight') {
        e.preventDefault();
        nextFlashcard();
      } else if (e.code === 'ArrowLeft') {
        e.preventDefault();
        prevFlashcard();
      } else if (e.key === 'p' || e.key === 'P') {
        const current = state.flashcardDeck[state.flashcardIndex];
        if (current) {
          if (!state.flashcardFlipped) {
            playAudio(current.audio, current.phrasal, elements.fcFrontAudioBtn);
          } else {
            playAudio(current.exampleAudio, current.example, elements.fcBackAudioBtn);
          }
        }
      }
    }
  }

  // ==========================================================================
  // Themes & UI Helpers
  // ==========================================================================
  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    state.theme = theme;
    localStorage.setItem('phrasal_theme', theme);
    elements.themeToggle.innerHTML = theme === 'dark' ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
  }

  function toggleTheme() {
    applyTheme(state.theme === 'dark' ? 'light' : 'dark');
    showToast(`已切換至 ${state.theme === 'dark' ? '深色' : '淺色'} 模式`);
  }

  function cycleAudioSpeed() {
    const speeds = [0.75, 1.0, 1.25];
    const nextIdx = (speeds.indexOf(state.audioSpeed) + 1) % speeds.length;
    state.audioSpeed = speeds[nextIdx];
    localStorage.setItem('phrasal_audio_speed', state.audioSpeed);
    updateAudioModeUI();
    showToast(`語音播放速度：${state.audioSpeed}x`);
  }

  function updateAudioModeUI() {
    elements.audioSpeedBtn.innerHTML = `<i class="fas fa-tachometer-alt"></i> ${state.audioSpeed}x`;
  }

  function showToast(msg) {
    elements.toast.textContent = msg;
    elements.toast.classList.add('show');
    clearTimeout(elements.toast._timer);
    elements.toast._timer = setTimeout(() => {
      elements.toast.classList.remove('show');
    }, 2400);
  }

  function switchTab(tabId) {
    state.currentTab = tabId;
    [elements.navTabCards, elements.navTabFlashcards, elements.navTabQuiz, elements.navTabMindmap].forEach(b => b.classList.remove('active'));
    [elements.viewCards, elements.viewFlashcards, elements.viewQuiz, elements.viewMindmap].forEach(v => v.style.display = 'none');

    if (tabId === 'cards') {
      elements.navTabCards.classList.add('active');
      elements.viewCards.style.display = 'block';
      renderCardsView();
    } else if (tabId === 'flashcards') {
      elements.navTabFlashcards.classList.add('active');
      elements.viewFlashcards.style.display = 'block';
      initFlashcardDeck();
      renderCurrentFlashcard();
    } else if (tabId === 'quiz') {
      elements.navTabQuiz.classList.add('active');
      elements.viewQuiz.style.display = 'block';
    } else if (tabId === 'mindmap') {
      elements.navTabMindmap.classList.add('active');
      elements.viewMindmap.style.display = 'block';
      renderMindmap();
    }
  }

  function renderStats() {
    elements.statTotal.textContent = state.allVerbs.length;
    elements.statMastered.textContent = state.mastered.size;
    elements.statStarred.textContent = state.starred.size;
  }

  // ==========================================================================
  // Audio Controller (MP3 with Seamless Web Speech API Fallback)
  // ==========================================================================
  function playAudio(audioUrl, fallbackText, buttonElement) {
    if (state.currentAudio) {
      state.currentAudio.pause();
      state.currentAudio = null;
    }
    window.speechSynthesis && window.speechSynthesis.cancel();

    if (state.activeAudioBtn) {
      state.activeAudioBtn.classList.remove('playing');
    }

    if (buttonElement) {
      state.activeAudioBtn = buttonElement;
      buttonElement.classList.add('playing');
    }

    const onAudioEnd = () => {
      if (buttonElement) buttonElement.classList.remove('playing');
      state.currentAudio = null;
      state.activeAudioBtn = null;
    };

    if (audioUrl) {
      const audio = new Audio(audioUrl);
      audio.playbackRate = state.audioSpeed;
      state.currentAudio = audio;

      audio.play().then(() => {
        audio.onended = onAudioEnd;
      }).catch(err => {
        console.warn('Local audio play error, falling back to Web Speech API:', err);
        fallbackToTTS(fallbackText, onAudioEnd);
      });
    } else {
      fallbackToTTS(fallbackText, onAudioEnd);
    }
  }

  function fallbackToTTS(text, onEnd) {
    if (!('speechSynthesis' in window)) {
      onEnd && onEnd();
      return;
    }
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    utterance.rate = state.audioSpeed;

    // Pick a natural English voice if available
    const voices = window.speechSynthesis.getVoices();
    const enVoice = voices.find(v => v.lang.startsWith('en') && (v.name.includes('Natural') || v.name.includes('Neural') || v.name.includes('Samantha') || v.name.includes('Google')));
    if (enVoice) utterance.voice = enVoice;

    utterance.onend = onEnd;
    utterance.onerror = onEnd;
    window.speechSynthesis.speak(utterance);
  }

  // ==========================================================================
  // Filter Toolbar & Cards Rendering
  // ==========================================================================
  function renderFilterButtons() {
    // Unique root verbs
    const verbsSet = new Set(state.allVerbs.map(v => v.verb));
    const verbsList = ['all', ...Array.from(verbsSet).sort()];

    elements.verbPillsContainer.innerHTML = '';
    verbsList.forEach(v => {
      const btn = document.createElement('button');
      btn.className = `pill-btn ${v === state.activeVerbFilter ? 'active' : ''}`;
      btn.textContent = v === 'all' ? '全部動詞' : v.toUpperCase();
      btn.addEventListener('click', () => {
        state.activeVerbFilter = v;
        document.querySelectorAll('#verbPillsContainer .pill-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        renderCardsView();
      });
      elements.verbPillsContainer.appendChild(btn);
    });
  }

  function getFilteredVerbs() {
    return state.allVerbs.filter(item => {
      // Verb filter
      if (state.activeVerbFilter !== 'all' && item.verb !== state.activeVerbFilter) {
        return false;
      }
      // Particle filter
      if (state.activeParticleFilter !== 'all' && item.particle !== state.activeParticleFilter) {
        return false;
      }
      // Status filter
      if (state.activeStatusFilter === 'starred' && !state.starred.has(item.id)) {
        return false;
      }
      if (state.activeStatusFilter === 'mastered' && !state.mastered.has(item.id)) {
        return false;
      }
      if (state.activeStatusFilter === 'learning' && state.mastered.has(item.id)) {
        return false;
      }
      // Search query
      if (state.searchQuery) {
        const q = state.searchQuery;
        const match = item.phrasal.toLowerCase().includes(q) ||
          item.chineseMeaning.toLowerCase().includes(q) ||
          item.meaning.toLowerCase().includes(q) ||
          item.example.toLowerCase().includes(q) ||
          item.scenario.toLowerCase().includes(q);
        if (!match) return false;
      }
      return true;
    });
  }

  function renderCardsView() {
    const list = getFilteredVerbs();
    elements.cardsCountLabel.textContent = `共 ${list.length} 個片語`;
    elements.cardsContainer.innerHTML = '';

    if (list.length === 0) {
      elements.cardsContainer.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; color: var(--text-secondary);">
          <i class="fas fa-search" style="font-size: 2.5rem; margin-bottom: 12px; opacity: 0.4;"></i>
          <p style="font-size: 1.1rem; font-weight: 600;">沒有找到符合條件的片語</p>
          <p style="font-size: 0.85rem; margin-top: 4px;">請嘗試更換篩選條件或清除搜尋關鍵字</p>
        </div>
      `;
      return;
    }

    list.forEach(item => {
      const isStarred = state.starred.has(item.id);
      const isMastered = state.mastered.has(item.id);

      const card = document.createElement('div');
      card.className = 'card';
      card.innerHTML = `
        <div>
          <div class="card-top">
            <div class="card-title-wrap">
              <div class="phrase-heading">
                <span>${item.phrasal}</span>
                <span class="particle-badge" title="介系詞">${item.particle}</span>
              </div>
              <div class="chinese-meaning">${item.chineseMeaning}</div>
            </div>
            <div class="card-actions-quick">
              <button class="star-btn ${isStarred ? 'starred' : ''}" title="收藏星號">
                <i class="${isStarred ? 'fas' : 'far'} fa-star"></i>
              </button>
              <button class="mastered-btn ${isMastered ? 'mastered' : ''}" title="標記掌握狀態">
                <i class="${isMastered ? 'fas fa-check-circle' : 'far fa-circle'}"></i>
              </button>
            </div>
          </div>
          <div class="card-body" style="margin-top: 14px;">
            <div class="definition-box">${item.meaning}</div>
            <div class="example-box">
              <div class="example-en">"${item.example}"</div>
              <div class="example-zh">${item.exampleChinese}</div>
            </div>
          </div>
        </div>
        <div class="card-footer">
          <span class="scenario-tag"><i class="fas fa-tag"></i> ${item.scenario}</span>
          <div class="audio-controls-row">
            <button class="play-chip-btn btn-play-phrase" title="播放片語發音">
              <i class="fas fa-volume-up"></i> 片語
            </button>
            <button class="play-chip-btn btn-play-example" title="播放例句發音">
              <i class="fas fa-play"></i> 例句
            </button>
          </div>
        </div>
      `;

      // Event bindings
      const starBtn = card.querySelector('.star-btn');
      starBtn.addEventListener('click', () => {
        toggleStarred(item.id);
        const starredNow = state.starred.has(item.id);
        starBtn.className = `star-btn ${starredNow ? 'starred' : ''}`;
        starBtn.innerHTML = `<i class="${starredNow ? 'fas' : 'far'} fa-star"></i>`;
      });

      const masteredBtn = card.querySelector('.mastered-btn');
      masteredBtn.addEventListener('click', () => {
        toggleMastered(item.id);
        const masteredNow = state.mastered.has(item.id);
        masteredBtn.className = `mastered-btn ${masteredNow ? 'mastered' : ''}`;
        masteredBtn.innerHTML = `<i class="${masteredNow ? 'fas fa-check-circle' : 'far fa-circle'}"></i>`;
      });

      const playPhraseBtn = card.querySelector('.btn-play-phrase');
      playPhraseBtn.addEventListener('click', () => {
        playAudio(item.audio, item.phrasal, playPhraseBtn);
      });

      const playExampleBtn = card.querySelector('.btn-play-example');
      playExampleBtn.addEventListener('click', () => {
        playAudio(item.exampleAudio, item.example, playExampleBtn);
      });

      elements.cardsContainer.appendChild(card);
    });
  }

  function toggleStarred(id) {
    if (state.starred.has(id)) {
      state.starred.delete(id);
      showToast('已取消收藏');
    } else {
      state.starred.add(id);
      showToast('已加入星號收藏 ⭐');
    }
    localStorage.setItem('phrasal_starred', JSON.stringify(Array.from(state.starred)));
    renderStats();
  }

  function toggleMastered(id, forceValue) {
    const isNow = forceValue !== undefined ? forceValue : !state.mastered.has(id);
    if (isNow) {
      state.mastered.add(id);
      showToast('已標記為掌握 ✅');
    } else {
      state.mastered.delete(id);
      showToast('已移至待複習清單');
    }
    localStorage.setItem('phrasal_mastered', JSON.stringify(Array.from(state.mastered)));
    renderStats();
  }

  // ==========================================================================
  // 3D Flashcard Deck
  // ==========================================================================
  function initFlashcardDeck() {
    state.flashcardDeck = [...state.allVerbs];
    state.flashcardIndex = 0;
    state.flashcardFlipped = false;
    renderCurrentFlashcard();
  }

  function renderCurrentFlashcard() {
    if (state.flashcardDeck.length === 0) return;
    const item = state.flashcardDeck[state.flashcardIndex];

    // Reset flip
    state.flashcardFlipped = false;
    elements.flashcardInner.classList.remove('flipped');

    // Progress
    const total = state.flashcardDeck.length;
    const current = state.flashcardIndex + 1;
    elements.flashcardProgressText.textContent = `卡片 ${current} / ${total}`;
    elements.flashcardProgressBar.style.width = `${(current / total) * 100}%`;

    // Front
    elements.fcFrontPhrase.textContent = item.phrasal;
    elements.fcFrontBadge.textContent = item.particle.toUpperCase();
    elements.fcFrontScenario.innerHTML = `<i class="fas fa-tag"></i> ${item.scenario}`;

    // Back
    elements.fcBackChinese.textContent = item.chineseMeaning;
    elements.fcBackMeaning.textContent = item.meaning;
    elements.fcBackExample.textContent = `"${item.example}"`;
    elements.fcBackExChinese.textContent = item.exampleChinese;
  }

  function toggleFlashcardFlip() {
    state.flashcardFlipped = !state.flashcardFlipped;
    elements.flashcardInner.classList.toggle('flipped', state.flashcardFlipped);
  }

  function nextFlashcard() {
    if (state.flashcardIndex < state.flashcardDeck.length - 1) {
      state.flashcardIndex++;
      renderCurrentFlashcard();
    } else {
      showToast('🎉 已到達卡片庫結尾！');
    }
  }

  function prevFlashcard() {
    if (state.flashcardIndex > 0) {
      state.flashcardIndex--;
      renderCurrentFlashcard();
    }
  }

  function shuffleFlashcardDeck() {
    for (let i = state.flashcardDeck.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [state.flashcardDeck[i], state.flashcardDeck[j]] = [state.flashcardDeck[j], state.flashcardDeck[i]];
    }
    state.flashcardIndex = 0;
    renderCurrentFlashcard();
    showToast('🔀 已隨機重新洗牌！');
  }

  // ==========================================================================
  // Quiz Hub
  // ==========================================================================
  function startQuiz() {
    const pool = [...state.allVerbs];
    if (pool.length < 4) return;

    // Shuffle pool
    for (let i = pool.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [pool[i], pool[j]] = [pool[j], pool[i]];
    }

    const countVal = elements.quizQuestionCountSelect.value;
    const totalQ = countVal === 'all' ? pool.length : Math.min(parseInt(countVal, 10), pool.length);
    state.quizQuestions = pool.slice(0, totalQ);

    state.quizIndex = 0;
    state.quizScore = 0;
    state.quizWrongItems = [];
    state.quizActive = true;

    elements.quizSetup.style.display = 'none';
    elements.quizResult.style.display = 'none';
    elements.quizPlay.style.display = 'flex';

    renderQuizQuestion();
  }

  function startMistakesQuiz() {
    if (state.quizWrongItems.length === 0) return;
    state.quizQuestions = [...state.quizWrongItems];
    state.quizIndex = 0;
    state.quizScore = 0;
    state.quizWrongItems = [];
    state.quizActive = true;

    elements.quizResult.style.display = 'none';
    elements.quizPlay.style.display = 'flex';

    renderQuizQuestion();
  }

  function renderQuizQuestion() {
    state.quizAnswered = false;
    elements.quizNextBtn.disabled = true;

    const currentItem = state.quizQuestions[state.quizIndex];
    const total = state.quizQuestions.length;
    const current = state.quizIndex + 1;

    elements.quizProgressText.textContent = `第 ${current} 題 / 共 ${total} 題`;
    elements.quizProgressBar.style.width = `${(current / total) * 100}%`;
    elements.quizScenarioBadge.textContent = currentItem.scenario;

    // Pick 3 distractors
    const otherItems = state.allVerbs.filter(v => v.id !== currentItem.id);
    for (let i = otherItems.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [otherItems[i], otherItems[j]] = [otherItems[j], otherItems[i]];
    }
    const distractors = otherItems.slice(0, 3);

    // Render by quiz mode
    if (state.quizMode === 'meaning') {
      elements.quizPrompt.innerHTML = `請選擇 <strong>${currentItem.phrasal}</strong> 的正確中文釋義：`;
      elements.quizAudioPlayBtn.style.display = 'inline-flex';
      elements.quizAudioPlayBtn.onclick = () => playAudio(currentItem.audio, currentItem.phrasal, elements.quizAudioPlayBtn);

      const options = [
        { text: currentItem.chineseMeaning, isCorrect: true },
        ...distractors.map(d => ({ text: d.chineseMeaning, isCorrect: false }))
      ];
      renderQuizOptions(options, currentItem);

    } else if (state.quizMode === 'cloze') {
      elements.quizPrompt.innerHTML = `選出適合空格的片語動詞：<br><span style="font-size: 1.15rem; color: var(--text-accent); font-weight: normal; margin-top: 8px; display: inline-block;">"${currentItem.clozeSentence}"</span>`;
      elements.quizAudioPlayBtn.style.display = 'none';

      const options = [
        { text: currentItem.phrasal, isCorrect: true },
        ...distractors.map(d => ({ text: d.phrasal, isCorrect: false }))
      ];
      renderQuizOptions(options, currentItem);

    } else if (state.quizMode === 'listening') {
      elements.quizPrompt.innerHTML = `請仔細聽發音，選出聽到的片語動詞：`;
      elements.quizAudioPlayBtn.style.display = 'inline-flex';
      elements.quizAudioPlayBtn.onclick = () => playAudio(currentItem.audio, currentItem.phrasal, elements.quizAudioPlayBtn);
      // Auto play audio once
      playAudio(currentItem.audio, currentItem.phrasal, elements.quizAudioPlayBtn);

      const options = [
        { text: currentItem.phrasal, isCorrect: true },
        ...distractors.map(d => ({ text: d.phrasal, isCorrect: false }))
      ];
      renderQuizOptions(options, currentItem);
    }
  }

  function renderQuizOptions(options, currentItem) {
    // Shuffle options
    for (let i = options.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [options[i], options[j]] = [options[j], options[i]];
    }

    elements.quizOptionsContainer.innerHTML = '';
    options.forEach(opt => {
      const btn = document.createElement('button');
      btn.className = 'quiz-opt-btn';
      btn.innerHTML = `<span>${opt.text}</span> <i class="far fa-circle"></i>`;
      btn.addEventListener('click', () => {
        if (state.quizAnswered) return;
        checkQuizAnswer(opt.isCorrect, btn, currentItem);
      });
      elements.quizOptionsContainer.appendChild(btn);
    });
  }

  function checkQuizAnswer(isCorrect, selectedBtn, currentItem) {
    state.quizAnswered = true;
    elements.quizNextBtn.disabled = false;

    if (isCorrect) {
      state.quizScore++;
      selectedBtn.classList.add('correct');
      selectedBtn.querySelector('i').className = 'fas fa-check-circle';
      showToast('答對了！👏');
    } else {
      selectedBtn.classList.add('wrong');
      selectedBtn.querySelector('i').className = 'fas fa-times-circle';
      state.quizWrongItems.push(currentItem);
      showToast('再接再厲！');

      // Highlight correct answer
      document.querySelectorAll('.quiz-opt-btn').forEach(b => {
        const text = b.querySelector('span').textContent;
        if (text === currentItem.chineseMeaning || text === currentItem.phrasal) {
          b.classList.add('correct');
          b.querySelector('i').className = 'fas fa-check-circle';
        }
      });
    }

    // Disable all options
    document.querySelectorAll('.quiz-opt-btn').forEach(b => b.disabled = true);
  }

  function advanceQuizQuestion() {
    if (state.quizIndex < state.quizQuestions.length - 1) {
      state.quizIndex++;
      renderQuizQuestion();
    } else {
      endQuiz();
    }
  }

  function endQuiz() {
    state.quizActive = false;
    elements.quizPlay.style.display = 'none';
    elements.quizResult.style.display = 'flex';

    const total = state.quizQuestions.length;
    const score = state.quizScore;
    const acc = total > 0 ? Math.round((score / total) * 100) : 0;

    elements.quizScoreDisplay.textContent = `${score} / ${total}`;
    elements.quizAccuracyDisplay.textContent = `${acc}%`;

    if (state.quizWrongItems.length > 0) {
      elements.quizReviewMistakesBtn.style.display = 'inline-flex';
      elements.quizReviewMistakesBtn.textContent = `複習錯題 (${state.quizWrongItems.length} 題)`;
    } else {
      elements.quizReviewMistakesBtn.style.display = 'none';
    }
  }

  // ==========================================================================
  // Particle Mind Map
  // ==========================================================================
  function renderMindmap() {
    elements.mindmapContainer.innerHTML = '';
    const particleEntries = Object.entries(state.particlesMeta);

    particleEntries.forEach(([particle, meta]) => {
      // Find all verbs using this particle
      const matched = state.allVerbs.filter(v => v.particle === particle || v.primaryParticle === particle);

      const card = document.createElement('div');
      card.className = 'particle-card';
      card.innerHTML = `
        <div class="particle-header">
          <span class="particle-badge-big">${particle.toUpperCase()}</span>
          <span class="particle-count-tag">${matched.length} 個片語</span>
        </div>
        <div class="particle-metaphor">${meta.core}</div>
        <div class="particle-desc">${meta.desc}</div>
        <div class="particle-verbs-preview">
          ${matched.map(m => `<span class="mini-phrase-tag">${m.phrasal}</span>`).join('')}
        </div>
      `;

      card.addEventListener('click', () => {
        // Filter cards by this particle and switch to cards view
        state.activeParticleFilter = particle;
        state.activeVerbFilter = 'all';
        switchTab('cards');
        showToast(`已篩選介系詞「${particle.toUpperCase()}」相關片語`);
      });

      elements.mindmapContainer.appendChild(card);
    });
  }

  // Start initialization
  document.addEventListener('DOMContentLoaded', init);
})();
