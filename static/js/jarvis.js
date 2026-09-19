// J.A.R.V.I.S. Interactive Client Controller (Version 3.0 Multilingual & Resilient Voice)
document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const micBtn = document.getElementById('micBtn');
    const chatForm = document.getElementById('chatForm');
    const textInput = document.getElementById('textInput');
    const chatLog = document.getElementById('chatLog');
    const langSelect = document.getElementById('langSelect');
    const statusMessage = document.getElementById('statusMessage');
    const micIconStatus = document.getElementById('micIconStatus');
    const hudTime = document.getElementById('hudTime');
    const jarvisAudioPlayer = document.getElementById('jarvisAudioPlayer');
    const welcomeTime = document.getElementById('welcomeTime');
    const welcomeVoiceBtn = document.getElementById('welcomeVoiceBtn');
    const welcomeMsgBody = document.getElementById('welcomeMsgBody');
    const clearLogBtn = document.getElementById('clearLogBtn');
    const arcCore = document.getElementById('arcCore');

    // Settings Modal Elements
    const settingsBtn = document.getElementById('settingsBtn');
    const settingsModal = document.getElementById('settingsModal');
    const closeSettingsBtn = document.getElementById('closeSettingsBtn');
    const cancelSettingsBtn = document.getElementById('cancelSettingsBtn');
    const saveSettingsBtn = document.getElementById('saveSettingsBtn');
    const apiKeyInput = document.getElementById('apiKeyInput');

    // Notes Modal Elements
    const notesModalBtn = document.getElementById('notesModalBtn');
    const notesModal = document.getElementById('notesModal');
    const closeNotesBtn = document.getElementById('closeNotesBtn');
    const clearAllNotesBtn = document.getElementById('clearAllNotesBtn');
    const refreshNotesBtn = document.getElementById('refreshNotesBtn');
    const notesListContainer = document.getElementById('notesListContainer');
    const remindersListContainer = document.getElementById('remindersListContainer');

    // Visualizer Canvas
    const canvas = document.getElementById('audioVisualizer');
    const ctx = canvas.getContext('2d');
    let isSpeaking = false;
    let isListening = false;

    // Set Welcome Time
    const now = new Date();
    if (welcomeTime) {
        welcomeTime.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    // Live Digital Clock
    function updateClock() {
        const d = new Date();
        if (hudTime) {
            hudTime.textContent = d.toLocaleTimeString([], { hour12: false });
        }
    }
    setInterval(updateClock, 1000);
    updateClock();

    // -------------------------------------------------------------
    // 🔊 Audio Unlock & Web Audio API Synthesizer
    // -------------------------------------------------------------
    let audioCtx = null;
    function getAudioContext() {
        try {
            if (!audioCtx && (window.AudioContext || window.webkitAudioContext)) {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }
            if (audioCtx && audioCtx.state === 'suspended') {
                audioCtx.resume();
            }
        } catch (e) {
            console.warn('AudioContext not supported or failed to resume:', e);
        }
        return audioCtx;
    }

    // Unlock browser audio upon first click or touch anywhere on the page
    function unlockAudio() {
        getAudioContext();
        try {
            if (jarvisAudioPlayer && !window.audioUnlocked) {
                jarvisAudioPlayer.volume = 1.0;
                jarvisAudioPlayer.muted = false;
                // Safari/Mobile hack: attempt to play a silent/empty track to whitelist the element
                let p = jarvisAudioPlayer.play();
                if (p !== undefined) {
                    p.then(() => {
                        jarvisAudioPlayer.pause();
                    }).catch(e => {
                        // Expected to throw error if src is empty, but it still unlocks!
                    });
                }
                window.audioUnlocked = true;
            }
        } catch (e) {
            console.warn('Failed to unlock audio player:', e);
        }
    }
    document.addEventListener('click', unlockAudio, { once: false });
    document.addEventListener('keydown', unlockAudio, { once: false });

    // Bootup Power-on Chord
    function playBootupSFX() {
        try {
            const ctx = getAudioContext();
            const now = ctx.currentTime;
            [220, 330, 440, 880].forEach((freq, idx) => {
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(freq, now + idx * 0.08);
                osc.frequency.exponentialRampToValueAtTime(freq * 1.5, now + 0.6 + idx * 0.08);
                
                gain.gain.setValueAtTime(0.001, now);
                gain.gain.exponentialRampToValueAtTime(0.08, now + 0.1);
                gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.9);

                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(now + idx * 0.08);
                osc.stop(now + 1.0);
            });
        } catch (e) {}
    }

    // Sci-fi Chirp / Beep
    function playBeepSFX() {
        try {
            const ctx = getAudioContext();
            const now = ctx.currentTime;
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(880, now);
            osc.frequency.exponentialRampToValueAtTime(1760, now + 0.12);

            gain.gain.setValueAtTime(0.06, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.15);

            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(now);
            osc.stop(now + 0.16);
        } catch (e) {}
    }

    // Alarm / Reminder Bell SFX
    function playAlertSFX() {
        try {
            const ctx = getAudioContext();
            const now = ctx.currentTime;
            [587, 880, 1174].forEach((freq) => {
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(freq, now);
                gain.gain.setValueAtTime(0.12, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 1.2);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(now);
                osc.stop(now + 1.2);
            });
        } catch (e) {}
    }

    // -------------------------------------------------------------
    // 🎨 Canvas Audio Waveform Visualizer
    // -------------------------------------------------------------
    function resizeCanvas() {
        if (!canvas || !canvas.parentElement) return;
        canvas.width = canvas.parentElement.clientWidth;
        canvas.height = canvas.parentElement.clientHeight;
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    let wavePhase = 0;
    function drawVisualizer() {
        requestAnimationFrame(drawVisualizer);
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        const centerY = canvas.height / 2;
        const width = canvas.width;
        const barsCount = 36;
        const barWidth = width / barsCount;

        for (let i = 0; i < barsCount; i++) {
            let amplitude = 4;
            if (isSpeaking) {
                amplitude = Math.sin(wavePhase + i * 0.4) * 22 + Math.cos(wavePhase * 1.5 + i * 0.2) * 12;
            } else if (isListening) {
                amplitude = Math.sin(wavePhase * 2 + i * 0.5) * 16;
            }

            const barHeight = Math.max(4, Math.abs(amplitude));
            const x = i * barWidth;

            const gradient = ctx.createLinearGradient(0, centerY - barHeight, 0, centerY + barHeight);
            if (isListening) {
                gradient.addColorStop(0, '#ff0055');
                gradient.addColorStop(1, '#ff5500');
            } else {
                gradient.addColorStop(0, '#00f2fe');
                gradient.addColorStop(0.5, '#4facfe');
                gradient.addColorStop(1, '#0072ff');
            }

            ctx.fillStyle = gradient;
            ctx.shadowBlur = 8;
            ctx.shadowColor = isListening ? '#ff0055' : '#00f2fe';
            ctx.fillRect(x + 2, centerY - barHeight / 2, barWidth - 4, barHeight);
        }

        wavePhase += isSpeaking ? 0.15 : (isListening ? 0.2 : 0.03);
    }
    drawVisualizer();

    // -------------------------------------------------------------
    // 🎙️ Speech Recognition (Web Speech API) & Wake Word
    // -------------------------------------------------------------
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;

    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;

        function getLangCode() {
            const val = langSelect.value;
            if (val === 'hi') return 'hi-IN';
            if (val === 'en') return 'en-US';
            return 'mr-IN';
        }

        function safeStartListening() {
            if (!recognition || isSpeaking || isListening) return;
            try {
                recognition.lang = getLangCode();
                recognition.start();
            } catch (e) {
                // Recognition already active or starting
            }
        }

        recognition.onstart = () => {
            isListening = true;
            micBtn.classList.add('listening');
            micIconStatus.className = 'fa-solid fa-waveform-lines';
            const lang = langSelect.value;
            if (lang === 'hi') statusMessage.textContent = 'मैं सुन रहा हूँ... बोलिए // LISTENING...';
            else if (lang === 'en') statusMessage.textContent = 'Listening... Speak now';
            else statusMessage.textContent = 'मी ऐकत आहे... बोला // LISTENING...';
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript.trim();
            console.log('Recognized speech:', transcript);
            playBeepSFX();
            textInput.value = '';  // ← लगेच clear करा, voice text input मध्ये दिसू नये
            submitQuery(transcript);
        };


        recognition.onerror = (event) => {
            console.warn('Speech recognition status/error:', event.error);
            isListening = false;
            micBtn.classList.remove('listening');
            micIconStatus.className = 'fa-solid fa-microphone-lines';
            if (event.error !== 'no-speech') {
                statusMessage.textContent = 'आवाज स्पष्ट आला नाही. पुन्हा बोला किंवा टाइप करा.';
            } else {
                statusMessage.textContent = 'मायक्रोफोन बंद आहे. बोलण्यासाठी पुन्हा क्लिक करा.';
            }
            setTimeout(() => {
                if (typeof resumeWakeWordIfNeeded === 'function') resumeWakeWordIfNeeded();
            }, 300);
        };

        recognition.onend = () => {
            isListening = false;
            micBtn.classList.remove('listening');
            micIconStatus.className = 'fa-solid fa-microphone-lines';
            if (!isSpeaking) {
                statusMessage.textContent = 'मायक्रोफोन बंद आहे. बोलण्यासाठी पुन्हा क्लिक करा.';
            }
            setTimeout(() => {
                if (typeof resumeWakeWordIfNeeded === 'function') resumeWakeWordIfNeeded();
            }, 300);
        };

        micBtn.addEventListener('click', () => {
            unlockAudio();
            if (isListening) {
                recognition.stop();
            } else {
                safeStartListening();
            }
        });
    } else {
        micBtn.title = 'Speech recognition not supported in this browser. Use Chrome/Edge.';
        statusMessage.textContent = 'मायक्रोफोनसाठी कृपया Chrome किंवा Edge ब्राउझर वापरा.';
    }

    // -------------------------------------------------------------
    // 🗣️ Fail-Safe Voice Playback (Edge-TTS MP3 + Web Speech Fallback)
    // -------------------------------------------------------------
    function cleanTextForBrowserTTS(text) {
        if (!text) return '';
        return text
            .replace(/[#*`_~[\]()]/g, '')
            .replace(/https?:\/\/\S+/g, '')
            .replace(/[\U00010000-\U0010ffff]/g, '')
            .replace(/[\u2600-\u27bf]/g, '')
            .substring(0, 350)
            .trim();
    }

    function speakWithBrowserSynthesis(text, lang) {
        if (!window.speechSynthesis) return;
        try {
            window.speechSynthesis.cancel();
            const clean = cleanTextForBrowserTTS(text);
            const utterance = new SpeechSynthesisUtterance(clean);
            utterance.lang = lang === 'hi' ? 'hi-IN' : (lang === 'en' ? 'en-US' : 'mr-IN');
            utterance.rate = 1.0;
            utterance.pitch = 1.0;

            isSpeaking = true;
            statusMessage.textContent = 'जार्व्हिस बोलत आहे... // JARVIS SPEAKING';

            utterance.onend = () => {
                isSpeaking = false;
                statusMessage.textContent = 'मायक्रोफोनवर क्लिक करा किंवा बोला';
                if (typeof resumeWakeWordIfNeeded === 'function') {
                    resumeWakeWordIfNeeded();
                }
            };
            utterance.onerror = () => {
                isSpeaking = false;
                if (typeof resumeWakeWordIfNeeded === 'function') {
                    resumeWakeWordIfNeeded();
                }
            };

            window.speechSynthesis.speak(utterance);
        } catch (e) {
            console.error('Browser SpeechSynthesis error:', e);
            isSpeaking = false;
            if (typeof resumeWakeWordIfNeeded === 'function') {
                resumeWakeWordIfNeeded();
            }
        }
    }

    function playAudio(audioUrl, fallbackText = '', lang = 'mr') {
        unlockAudio();

        if (audioUrl && (audioUrl.endsWith('.mp3') || audioUrl.endsWith('.webm') || audioUrl.includes('/static/audio/') || audioUrl.includes('/api/music/stream'))) {
            jarvisAudioPlayer.src = audioUrl;
            jarvisAudioPlayer.volume = 1.0;
            jarvisAudioPlayer.muted = false;
            isSpeaking = true;

            const isAartiTrack = audioUrl.includes('ganpati_aarti') || audioUrl.includes('shivraya_aarti') || audioUrl.includes('hanuman_chalisa');
            const isMusicTrack = audioUrl.includes('/api/music/stream');

            if (isMusicTrack) {
                statusMessage.textContent = '🎵 गाणे वाजत आहे... // NOW PLAYING (DIRECT AUDIO)';
                updateMusicUI(true);
            } else if (audioUrl.includes('hanuman_chalisa')) {
                statusMessage.textContent = '🚩 श्री हनुमान चालीसा सुरू आहे... // HANUMAN CHALISA PLAYING';
                updateAartiUI(true);
            } else if (audioUrl.includes('shivraya_aarti')) {
                statusMessage.textContent = '🚩 छत्रपती शिवाजी महाराजांची आरती (शिवशंकराचा तू अवतार) सुरू आहे... // SHIVRAYA AARTI';
                updateAartiUI(true);
            } else if (audioUrl.includes('ganpati_aarti')) {
                statusMessage.textContent = '🌺 गणपती बाप्पांची मूळ आरती सुरू आहे... // AARTI PLAYING';
                updateAartiUI(true);
            } else {
                statusMessage.textContent = 'जार्व्हिस बोलत आहे... // JARVIS SPEAKING';
            }

            // Reset handlers before each play to avoid stale handler bugs
            jarvisAudioPlayer.onerror = null;
            jarvisAudioPlayer.onended = null;

            jarvisAudioPlayer.onerror = (e) => {
                console.warn('Audio element error, falling back to SpeechSynthesis:', e);
                isSpeaking = false;
                if (!isAartiTrack && !isMusicTrack && fallbackText) {
                    speakWithBrowserSynthesis(fallbackText, lang);
                } else {
                    if (typeof resumeWakeWordIfNeeded === 'function') {
                        resumeWakeWordIfNeeded();
                    }
                }
            };

            jarvisAudioPlayer.onended = () => {
                isSpeaking = false;
                updateAartiUI(false);
                updateMusicUI(false);
                statusMessage.textContent = 'मायक्रोफोनवर क्लिक करा किंवा बोला';
                if (typeof resumeWakeWordIfNeeded === 'function') {
                    resumeWakeWordIfNeeded();
                }
            };

            // Resume AudioContext first, then play — bypasses browser autoplay policy
            const tryPlay = () => {
                const playPromise = jarvisAudioPlayer.play();
                if (playPromise !== undefined) {
                    playPromise.then(() => {
                        if (isAartiTrack) updateAartiUI(true);
                        if (isMusicTrack) updateMusicUI(true);
                    }).catch(err => {
                        console.warn('HTML5 Audio play blocked or failed:', err);
                        isSpeaking = false;
                        if (isAartiTrack) {
                            updateAartiUI(false);
                            statusMessage.textContent = 'आरती प्ले करण्यासाठी खालील Play बटणावर क्लिक करा.';
                        } else if (isMusicTrack) {
                            updateMusicUI(false);
                            statusMessage.textContent = 'गाणे प्ले करण्यासाठी खालील Play बटणावर क्लिक करा.';
                        } else {
                            speakWithBrowserSynthesis(fallbackText, lang);
                        }
                    });
                }
            };

            const actx = getAudioContext();
            if (actx.state === 'suspended') {
                actx.resume().then(tryPlay).catch(tryPlay);
            } else {
                tryPlay();
            }
        } else if (fallbackText) {
            speakWithBrowserSynthesis(fallbackText, lang);
        }
    }


    // -------------------------------------------------------------
    // 🌺 & 🚩 In-Page Interactive Aarti Controls (Ganpati & Shivraya)
    // -------------------------------------------------------------
    window.toggleAartiPlay = function(customSrc) {
        unlockAudio();
        let defaultSrc = '/static/audio/ganpati_aarti_original.mp3';
        if (customSrc) {
            defaultSrc = customSrc;
        } else if (jarvisAudioPlayer.src && jarvisAudioPlayer.src.includes('hanuman_chalisa')) {
            defaultSrc = '/static/audio/hanuman_chalisa.webm';
        } else if (jarvisAudioPlayer.src && jarvisAudioPlayer.src.includes('shivraya')) {
            defaultSrc = '/static/audio/shivraya_aarti.webm';
        }

        if (!jarvisAudioPlayer.src || (!jarvisAudioPlayer.src.includes('ganpati_aarti') && !jarvisAudioPlayer.src.includes('shivraya_aarti') && !jarvisAudioPlayer.src.includes('hanuman_chalisa'))) {
            jarvisAudioPlayer.src = defaultSrc;
        } else if (customSrc && !jarvisAudioPlayer.src.includes(customSrc.split('/').pop())) {
            jarvisAudioPlayer.src = customSrc;
        }
        if (jarvisAudioPlayer.paused) {
            jarvisAudioPlayer.play().then(() => {
                isSpeaking = true;
                updateAartiUI(true);
                if (jarvisAudioPlayer.src.includes('hanuman_chalisa')) {
                    statusMessage.textContent = '🚩 श्री हनुमान चालीसा सुरू आहे...';
                } else if (jarvisAudioPlayer.src.includes('shivraya')) {
                    statusMessage.textContent = '🚩 छत्रपती शिवाजी महाराजांची आरती सुरू आहे...';
                } else {
                    statusMessage.textContent = '🌺 गणपती बाप्पांची मूळ आरती सुरू आहे...';
                }
            }).catch(e => console.warn('Aarti play error:', e));
        } else {
            jarvisAudioPlayer.pause();
            isSpeaking = false;
            updateAartiUI(false);
            statusMessage.textContent = 'ऑडिओ पॉज केला आहे.';
        }
    };

    window.stopAllMedia = function() {
        // 1. Stop HTML5 audio player
        if (jarvisAudioPlayer) {
            jarvisAudioPlayer.pause();
            jarvisAudioPlayer.currentTime = 0;
            jarvisAudioPlayer.src = '';
        }
        if (window.speechSynthesis) {
            window.speechSynthesis.cancel();
        }
        isSpeaking = false;
        updateAartiUI(false);
        updateMusicUI(false);

        // 2. Stop all active YouTube iframes across music and aarti cards
        document.querySelectorAll('.music-video-accordion iframe, .music-frame-wrapper iframe, .inline-yt-frame-box iframe, .aarti-video-container iframe').forEach(iframe => {
            try {
                iframe.contentWindow.postMessage('{"event":"command","func":"stopVideo","args":""}', '*');
            } catch(e) {}
            iframe.src = '';
        });

        statusMessage.textContent = 'सर्व ऑडिओ / व्हिडिओ थांबवले आहेत.';
        if (typeof resumeWakeWordIfNeeded === 'function') {
            resumeWakeWordIfNeeded();
        }
    };

    window.stopAarti = function() {
        window.stopAllMedia();
    };

    window.updateMusicUI = function(isPlaying) {
        document.querySelectorAll('.music-play-pause-btn i').forEach(icon => {
            icon.className = isPlaying ? 'fa-solid fa-pause' : 'fa-solid fa-play';
        });
        document.querySelectorAll('.music-vinyl-disc').forEach(disc => {
            if (isPlaying) disc.classList.add('spinning');
            else disc.classList.remove('spinning');
        });
        document.querySelectorAll('.music-equalizer-bars').forEach(eq => {
            if (isPlaying) eq.style.opacity = '1';
            else eq.style.opacity = '0.35';
        });
    };

    window.toggleMusicPlay = function(playerId) {
        unlockAudio();
        if (!jarvisAudioPlayer) return;
        if (jarvisAudioPlayer.paused) {
            jarvisAudioPlayer.play().then(() => {
                window.updateMusicUI(true);
                statusMessage.textContent = '🎵 गाणे वाजत आहे... // PLAYING';
            }).catch(e => console.warn('Music play error:', e));
        } else {
            jarvisAudioPlayer.pause();
            window.updateMusicUI(false);
            statusMessage.textContent = 'गाणे पॉज केले आहे. // PAUSED';
        }
    };

    window.stopMusicTrack = function(playerId) {
        window.stopAllMedia();
        statusMessage.textContent = 'गाणे थांबवले आहे. // STOPPED';
    };

    window.seekMusic = function(percent) {
        if (jarvisAudioPlayer && jarvisAudioPlayer.duration) {
            jarvisAudioPlayer.currentTime = (percent / 100) * jarvisAudioPlayer.duration;
        }
    };

    window.setMusicVolume = function(percent) {
        if (jarvisAudioPlayer) {
            jarvisAudioPlayer.volume = Math.max(0, Math.min(1, percent / 100));
        }
    };

    window.switchMusicCandidate = function(playerId, nextVid, encTitle, encChannel, encThumb) {
        unlockAudio();
        const decodedTitle = decodeURIComponent(encTitle || 'Music Track');
        const decodedChannel = decodeURIComponent(encChannel || 'Artist');
        const decodedThumb = encThumb ? decodeURIComponent(encThumb) : `https://img.youtube.com/vi/${nextVid}/hqdefault.jpg`;

        const titleEl = document.getElementById(playerId + '_title');
        const mainTitleEl = document.getElementById(playerId + '_main_title');
        const chEl = document.getElementById(playerId + '_channel');
        const thumbEl = document.getElementById(playerId + '_thumb');
        const iframe = document.getElementById(playerId + '_iframe');

        if (titleEl) titleEl.textContent = decodedTitle;
        if (mainTitleEl) mainTitleEl.textContent = decodedTitle;
        if (chEl) chEl.innerHTML = `<i class="fa-solid fa-compact-disc"></i> ${escapeHtml(decodedChannel)}`;
        if (thumbEl) thumbEl.src = decodedThumb;
        if (iframe) iframe.setAttribute('data-src', `https://www.youtube-nocookie.com/embed/${nextVid}?autoplay=1&enablejsapi=1`);

        const streamUrl = `/api/music/stream?v=${nextVid}`;
        jarvisAudioPlayer.src = streamUrl;
        jarvisAudioPlayer.play().then(() => {
            window.updateMusicUI(true);
            statusMessage.textContent = `🎵 आता वाजत आहे: ${decodedTitle}`;
        }).catch(err => {
            console.warn('Switch track stream play error:', err);
        });
    };

    window.toggleMusicVideo = function(playerId) {
        const wrap = document.getElementById(playerId + '_video_wrap');
        const iframe = document.getElementById(playerId + '_iframe');
        if (!wrap) return;
        if (wrap.style.display === 'none' || !wrap.style.display) {
            wrap.style.display = 'block';
            if (iframe && !iframe.src && iframe.getAttribute('data-src')) {
                iframe.src = iframe.getAttribute('data-src');
            }
        } else {
            wrap.style.display = 'none';
            if (iframe) iframe.src = '';
        }
    };

    window.seekAarti = function(percent) {
        if (jarvisAudioPlayer && jarvisAudioPlayer.duration) {
            jarvisAudioPlayer.currentTime = (percent / 100) * jarvisAudioPlayer.duration;
        }
    };

    window.toggleAartiVideo = function(btn) {
        const parent = btn.closest('.aarti-video-section');
        if (!parent) return;
        const container = parent.querySelector('.aarti-video-container');
        if (!container) return;
        if (container.style.display === 'none' || !container.style.display) {
            container.style.display = 'block';
            btn.innerHTML = '<i class="fa-solid fa-chevron-up"></i> व्हिडिओ लपवा (Hide Video)';
        } else {
            container.style.display = 'none';
            btn.innerHTML = '<i class="fa-brands fa-youtube"></i> मूळ YouTube व्हिडिओ स्क्रीनवर पहा (Watch Video)';
        }
    };

    function updateAartiUI(isPlaying) {
        document.querySelectorAll('.aarti-play-btn i, .side-aarti-play-badge i').forEach(icon => {
            icon.className = isPlaying ? 'fa-solid fa-circle-pause' : 'fa-solid fa-circle-play';
        });
        document.querySelectorAll('.aarti-icon-disc, .side-aarti-disc').forEach(disc => {
            if (isPlaying) disc.classList.add('spinning');
            else disc.classList.remove('spinning');
        });
        const navTrigger = document.getElementById('navAartiTrigger');
        if (navTrigger) {
            if (isPlaying) navTrigger.classList.add('playing-pulse');
            else navTrigger.classList.remove('playing-pulse');
        }
        const stopPill = document.getElementById('navAartiPlayingStopBtn');
        if (stopPill) {
            stopPill.style.display = isPlaying ? 'inline-flex' : 'none';
        }
    }

    function formatTime(secs) {
        if (isNaN(secs) || secs < 0) return '0:00';
        const m = Math.floor(secs / 60);
        const s = Math.floor(secs % 60);
        return `${m}:${s < 10 ? '0' : ''}${s}`;
    }

    jarvisAudioPlayer.addEventListener('timeupdate', () => {
        if (jarvisAudioPlayer.duration) {
            const pct = (jarvisAudioPlayer.currentTime / jarvisAudioPlayer.duration) * 100;
            document.querySelectorAll('.aarti-slider, .music-slider').forEach(slider => {
                slider.value = pct;
            });
            document.querySelectorAll('.aarti-current-time, .music-current-time').forEach(el => {
                el.textContent = formatTime(jarvisAudioPlayer.currentTime);
            });
            document.querySelectorAll('.aarti-duration, .music-duration').forEach(el => {
                el.textContent = formatTime(jarvisAudioPlayer.duration);
            });
        }
    });

    jarvisAudioPlayer.addEventListener('play', () => {
        updateAartiUI(true);
        if (window.updateMusicUI) window.updateMusicUI(true);
    });
    jarvisAudioPlayer.addEventListener('pause', () => {
        updateAartiUI(false);
        if (window.updateMusicUI) window.updateMusicUI(false);
    });

    function appendMessage(sender, text, audioUrl = null, imageUrl = null) {
        const card = document.createElement('div');
        card.className = `message-card ${sender === 'user' ? 'user-card' : 'jarvis-card'}`;

        const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const icon = sender === 'user' ? 'fa-user' : 'fa-robot';
        const name = sender === 'user' ? 'YOU' : 'J.A.R.V.I.S.';

        let audioActionHtml = '';
        if (audioUrl && !audioUrl.includes('ganpati_aarti') && !audioUrl.includes('shivraya_aarti') && !audioUrl.includes('hanuman_chalisa')) {
            const safeText = encodeURIComponent(cleanTextForBrowserTTS(text));
            audioActionHtml = `
                <div class="msg-actions">
                    <button class="replay-btn" onclick="window.playCustomAudio('${audioUrl}', decodeURIComponent('${safeText}'))">
                        <i class="fa-solid fa-volume-high"></i> ऐका (Listen)
                    </button>
                </div>
            `;
        }

        let imageHtml = '';
        if (imageUrl) {
            imageHtml = `<img src="${imageUrl}" class="chat-msg-image" alt="User uploaded image">`;
        }

        card.innerHTML = `
            <div class="msg-header">
                <div class="speaker-tag">
                    <i class="fa-solid ${icon}"></i> ${name}
                </div>
                <span class="timestamp">${timeStr}</span>
            </div>
            ${imageHtml}
            <div class="msg-body">${formatMarkdown(text)}</div>
            ${audioActionHtml}
        `;

        chatLog.appendChild(card);
        chatLog.scrollTop = chatLog.scrollHeight;
    }

    window.playCustomAudio = function(url, text) {
        playAudio(url, text, langSelect.value);
    };

    function escapeHtml(unsafe) {
        return (unsafe || '').toString()
             .replace(/&/g, "&amp;")
             .replace(/</g, "&lt;")
             .replace(/>/g, "&gt;")
             .replace(/"/g, "&quot;")
             .replace(/'/g, "&#039;");
    }

    function formatMarkdown(text) {
        if (!text) return '';
        let escaped = text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
        
        // Ganpati Aarti In-Page Player Replacement
        const ganpatiPlayerHtml = `
            <div class="aarti-player-card">
                <div class="aarti-player-header">
                    <div class="aarti-icon-disc pulsating-disc">
                        <i class="fa-solid fa-om"></i>
                    </div>
                    <div class="aarti-info">
                        <div class="aarti-title">॥ श्री सुखकर्ता दुःखहर्ता आरती ॥</div>
                        <div class="aarti-subtitle">🌺 मूळ सुप्रसिद्ध स्वर: लता मंगेशकर आणि उषा मंगेशकर (Original HD)</div>
                    </div>
                    <span class="aarti-badge"><i class="fa-solid fa-music"></i> थेट स्क्रीनवर</span>
                </div>
                <div class="aarti-controls">
                    <button type="button" class="aarti-btn aarti-play-btn" onclick="window.toggleAartiPlay('/static/audio/ganpati_aarti_original.mp3')" title="चालू / थांबवा (Play/Pause)">
                        <i class="fa-solid fa-pause"></i>
                    </button>
                    <div class="aarti-progress-wrapper">
                        <span class="aarti-time aarti-current-time">0:00</span>
                        <input type="range" class="aarti-slider" min="0" max="100" value="0" oninput="window.seekAarti(this.value)">
                        <span class="aarti-time aarti-duration">--:--</span>
                    </div>
                    <button type="button" class="aarti-btn aarti-stop-btn" onclick="window.stopAarti()" title="पूर्ण थांबवा (Stop)">
                        <i class="fa-solid fa-stop"></i>
                    </button>
                </div>
                <div class="aarti-video-section">
                    <button type="button" class="aarti-yt-toggle-btn" onclick="window.toggleAartiVideo(this)">
                        <i class="fa-brands fa-youtube"></i> मूळ YouTube व्हिडिओ स्क्रीनवर पहा (Watch Video)
                    </button>
                    <div class="aarti-video-container" style="display: none;">
                        <iframe src="https://www.youtube.com/embed/pLkirAh4WLE?enablejsapi=1" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                    </div>
                </div>
            </div>
        `;

        // Chhatrapati Shivaji Maharaj "शिवशंकराचा तू अवतार" In-Page Aarti Player Replacement
        const shivrayaPlayerHtml = `
            <div class="aarti-player-card shivraya-aarti-card">
                <div class="aarti-player-header">
                    <div class="aarti-icon-disc shivraya-disc pulsating-disc">
                        <i class="fa-solid fa-crown"></i>
                    </div>
                    <div class="aarti-info">
                        <div class="aarti-title shivraya-title">🚩 ॥ श्री छत्रपती शिवाजी महाराज आरती ॥ 🚩</div>
                        <div class="aarti-subtitle">शिवशंकराचा तू अवतार | स्वर: आदर्श शिंदे | संगीत: अभिषेक-दत्ता</div>
                    </div>
                    <span class="aarti-badge shivraya-badge"><i class="fa-solid fa-shield-halved"></i> SWARAJYA HD</span>
                </div>
                <div class="aarti-controls shivraya-controls">
                    <button type="button" class="aarti-btn aarti-play-btn shivraya-play-btn" onclick="window.toggleAartiPlay('/static/audio/shivraya_aarti.webm')" title="चालू / थांबवा (Play/Pause)">
                        <i class="fa-solid fa-pause"></i>
                    </button>
                    <div class="aarti-progress-wrapper">
                        <span class="aarti-time aarti-current-time">0:00</span>
                        <input type="range" class="aarti-slider shivraya-slider" min="0" max="100" value="0" oninput="window.seekAarti(this.value)">
                        <span class="aarti-time aarti-duration">--:--</span>
                    </div>
                    <button type="button" class="aarti-btn aarti-stop-btn" onclick="window.stopAarti()" title="पूर्ण थांबवा (Stop)">
                        <i class="fa-solid fa-stop"></i>
                    </button>
                </div>
                <div class="aarti-video-section">
                    <button type="button" class="aarti-yt-toggle-btn shivraya-yt-btn" onclick="window.toggleAartiVideo(this)">
                        <i class="fa-brands fa-youtube"></i> मूळ YouTube व्हिडिओ स्क्रीनवर पहा (Watch Video)
                    </button>
                    <div class="aarti-video-container" style="display: none;">
                        <iframe src="https://www.youtube.com/embed/e0-SwM80bvI?enablejsapi=1" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                    </div>
                </div>
            </div>
        `;

        // Shri Hanuman Chalisa In-Page Player Replacement
        const hanumanPlayerHtml = `
            <div class="aarti-player-card hanuman-aarti-card">
                <div class="aarti-player-header">
                    <div class="aarti-icon-disc hanuman-disc pulsating-disc">
                        <i class="fa-solid fa-hands-praying"></i>
                    </div>
                    <div class="aarti-info">
                        <div class="aarti-title hanuman-title">🚩 ॥ श्री हनुमान चालीसा ॥ 🚩</div>
                        <div class="aarti-subtitle">मूळ स्वर: हरिहरन | निर्मिती: गुलशन कुमार (T-Series Original HD)</div>
                    </div>
                    <span class="aarti-badge hanuman-badge"><i class="fa-solid fa-om"></i> SANKAT MOCHAN</span>
                </div>
                <div class="aarti-controls hanuman-controls">
                    <button type="button" class="aarti-btn aarti-play-btn hanuman-play-btn" onclick="window.toggleAartiPlay('/static/audio/hanuman_chalisa.webm')" title="चालू / थांबवा (Play/Pause)">
                        <i class="fa-solid fa-pause"></i>
                    </button>
                    <div class="aarti-progress-wrapper">
                        <span class="aarti-time aarti-current-time">0:00</span>
                        <input type="range" class="aarti-slider hanuman-slider" min="0" max="100" value="0" oninput="window.seekAarti(this.value)">
                        <span class="aarti-time aarti-duration">--:--</span>
                    </div>
                    <button type="button" class="aarti-btn aarti-stop-btn" onclick="window.stopAarti()" title="पूर्ण थांबवा (Stop)">
                        <i class="fa-solid fa-stop"></i>
                    </button>
                </div>
                <div class="aarti-video-section">
                    <button type="button" class="aarti-yt-toggle-btn hanuman-yt-btn" onclick="window.toggleAartiVideo(this)">
                        <i class="fa-brands fa-youtube"></i> मूळ YouTube व्हिडिओ स्क्रीनवर पहा (Watch Video)
                    </button>
                    <div class="aarti-video-container" style="display: none;">
                        <iframe src="https://www.youtube.com/embed/17ZHT4WbSfw?enablejsapi=1" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                    </div>
                </div>
            </div>
        `;

        escaped = escaped.replace(/\[AARTI_PLAYER\]/g, ganpatiPlayerHtml);
        escaped = escaped.replace(/\[SHIVRAYA_AARTI_PLAYER\]/g, shivrayaPlayerHtml);
        escaped = escaped.replace(/\[HANUMAN_CHALISA_PLAYER\]/g, hanumanPlayerHtml);

        // 🎵 Holographic In-Page Music Player Card (100% Zero Redirect & Direct Audio)
        escaped = escaped.replace(/\[MUSIC_PLAYER:([a-zA-Z0-9_-]+)\|([^\]]+)\]/g, function(match, vid, b64) {
            let cardData = null;
            try {
                cardData = JSON.parse(decodeURIComponent(escape(atob(b64))));
            } catch(e) {
                try { cardData = JSON.parse(atob(b64)); } catch(e2) {}
            }
            if (!cardData) cardData = { primary: { id: vid, title: 'Music Track', channel: 'Official Music', duration: 'HD', thumbnail: '' }, alternates: [] };
            
            const primary = cardData.primary || { id: vid, title: 'Music Track', channel: 'Official Music', duration: 'HD', thumbnail: '' };
            const alternates = cardData.alternates || [];
            const playerId = 'music_' + Math.random().toString(36).substr(2, 9);
            const safeTitle = primary.title || 'Superhit Song';
            const safeChannel = primary.channel || 'Official Music';
            const thumbUrl = primary.thumbnail || `https://img.youtube.com/vi/${primary.id}/hqdefault.jpg`;

            let altButtonsHtml = '';
            if (alternates.length > 0) {
                altButtonsHtml = `
                    <div class="music-alternates-box">
                        <span class="music-alt-label"><i class="fa-solid fa-shuffle"></i> पर्यायी व्हर्जन्स (Alternate Versions / Lyrics):</span>
                        <div class="music-alt-buttons">
                            ${alternates.map((alt, idx) => `
                                <button type="button" class="music-alt-btn" onclick="window.switchMusicCandidate('${playerId}', '${alt.id}', '${encodeURIComponent(alt.title || '')}', '${encodeURIComponent(alt.channel || '')}', '${encodeURIComponent(alt.thumbnail || '')}')" title="${escapeHtml(alt.title || '')}">
                                    <i class="fa-solid fa-play"></i> व्हर्जन ${idx + 2} <span class="alt-dur">(${alt.duration || 'HD'})</span>
                                </button>
                            `).join('')}
                        </div>
                    </div>
                `;
            }

            return `
                <div class="hud-music-player-card" id="${playerId}">
                    <div class="music-card-header">
                        <div class="music-header-left">
                            <div class="music-equalizer-bars">
                                <span></span><span></span><span></span><span></span>
                            </div>
                            <div class="music-meta-titles">
                                <span class="music-now-playing">▶ आता वाजत आहे // DIRECT AUDIO STREAM</span>
                                <span class="music-track-title" id="${playerId}_title">${escapeHtml(safeTitle)}</span>
                            </div>
                        </div>
                        <div class="music-header-badges">
                            <span class="music-badge-artist" id="${playerId}_channel"><i class="fa-solid fa-compact-disc"></i> ${escapeHtml(safeChannel)}</span>
                            <span class="music-badge-hd"><i class="fa-solid fa-shield-halved"></i> थेट स्पीकरवर</span>
                        </div>
                    </div>

                    <div class="music-banner-row">
                        <div class="music-art-disc-wrap">
                            <img class="music-thumb-img" id="${playerId}_thumb" src="${thumbUrl}" alt="${escapeHtml(safeTitle)}" />
                            <div class="music-vinyl-disc spinning" id="${playerId}_disc">
                                <div class="disc-center"><i class="fa-solid fa-music"></i></div>
                            </div>
                        </div>
                        <div class="music-details-col">
                            <div class="music-track-main-title" id="${playerId}_main_title">${escapeHtml(safeTitle)}</div>
                            <div class="music-artist-sub"><i class="fa-solid fa-microphone-lines"></i> ${escapeHtml(safeChannel)}</div>
                            <div class="music-duration-pill"><i class="fa-regular fa-clock"></i> <span id="${playerId}_dur">${primary.duration || 'HD'}</span> • HD Audio Engine</div>
                        </div>
                    </div>

                    <div class="music-player-controls-row">
                        <button type="button" class="music-play-pause-btn" id="${playerId}_play_btn" onclick="window.toggleMusicPlay('${playerId}')" title="प्ले / पॉज (Play/Pause)">
                            <i class="fa-solid fa-pause"></i>
                        </button>
                        <div class="music-progress-wrapper">
                            <span class="music-time music-current-time" id="${playerId}_curr">0:00</span>
                            <input type="range" class="music-slider" id="${playerId}_slider" min="0" max="100" value="0" oninput="window.seekMusic(this.value)">
                            <span class="music-time music-duration" id="${playerId}_tot">--:--</span>
                        </div>
                        <button type="button" class="music-ctrl-btn music-stop-btn" onclick="window.stopMusicTrack('${playerId}')" title="गाणे पूर्ण थांबवा (Stop)">
                            <i class="fa-solid fa-stop"></i>
                        </button>
                    </div>

                    <div class="music-extra-row">
                        <div class="music-volume-box">
                            <i class="fa-solid fa-volume-high" style="color: var(--cyan-neon); font-size: 0.8rem;"></i>
                            <input type="range" class="music-vol-slider" min="0" max="100" value="100" oninput="window.setMusicVolume(this.value)" title="आवाज (Volume)">
                        </div>
                        <div class="music-status-pill">
                            <i class="fa-solid fa-circle-check" style="color: #00ffaa;"></i> Zero Redirect • Active
                        </div>
                        <button type="button" class="music-yt-toggle-btn" onclick="window.toggleMusicVideo('${playerId}')" title="अधिकृत YouTube व्हिडिओ पहा">
                            <i class="fa-brands fa-youtube"></i> व्हिडिओ पहा
                        </button>
                    </div>

                    <div class="music-video-accordion" id="${playerId}_video_wrap" style="display: none;">
                        <iframe id="${playerId}_iframe"
                            data-src="https://www.youtube-nocookie.com/embed/${primary.id}?autoplay=1&enablejsapi=1&origin=${encodeURIComponent(window.location.origin)}&playsinline=1&rel=0"
                            src=""
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                            allowfullscreen>
                        </iframe>
                    </div>

                    ${altButtonsHtml}
                </div>
            `;
        });
        
        // Inline YouTube Player Card (Legacy fallback)
        escaped = escaped.replace(/\[YOUTUBE_INLINE:([a-zA-Z0-9_-]+):([^\]]*)\]/g, function(match, vid, title) {
            return `
                <div class="hud-music-player-card">
                    <div class="music-card-header">
                        <div class="music-header-left">
                            <i class="fa-brands fa-youtube" style="color: #ff0033; font-size: 1.3rem;"></i>
                            <div class="music-meta-titles">
                                <span class="music-now-playing">▶ आता वाजत आहे</span>
                                <span class="music-track-title">${title || 'YouTube Video'}</span>
                            </div>
                        </div>
                        <span class="music-badge-hd"><i class="fa-solid fa-bolt"></i> HD INLINE</span>
                    </div>
                    <div class="music-frame-wrapper">
                        <iframe src="https://www.youtube-nocookie.com/embed/${vid}?autoplay=1&enablejsapi=1&origin=${encodeURIComponent(window.location.origin)}&playsinline=1&rel=0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                    </div>
                </div>
            `;
        });

        // Live Weather HUD Card
        escaped = escaped.replace(/\[WEATHER_CARD:([^|\]]+)\|([^|\]]+)\|([^|\]]+)\|([^|\]]+)\|([^|\]]+)\|([^|\]]+)\|([^|\]]+)\]/g, function(match, city, temp, feels, desc, hum, wind, rain) {
            const rainNum = parseInt(rain) || 0;
            const isRainy = rainNum >= 40 || desc.includes('पाऊस') || desc.toLowerCase().includes('rain');
            const weatherIcon = isRainy ? 'fa-cloud-showers-heavy' : (desc.includes('ढगाळ') || desc.toLowerCase().includes('cloud') ? 'fa-cloud' : 'fa-sun');
            const iconColor = isRainy ? '#00e5ff' : '#ffb703';
            return `
                <div class="hud-weather-card">
                    <div class="weather-card-header">
                        <div class="weather-city"><i class="fa-solid fa-location-dot"></i> ${city}</div>
                        <span class="weather-badge">${desc}</span>
                    </div>
                    <div class="weather-main-row">
                        <div class="weather-temp-block">
                            <i class="fa-solid ${weatherIcon}" style="color: ${iconColor}; font-size: 2.4rem;"></i>
                            <div class="weather-temp">${temp}°C</div>
                        </div>
                        <div class="weather-feels">जाणवते: <strong>${feels}°C</strong></div>
                    </div>
                    <div class="weather-details-grid">
                        <div class="w-stat"><i class="fa-solid fa-droplet"></i> दमटपणा: <strong>${hum}%</strong></div>
                        <div class="w-stat"><i class="fa-solid fa-wind"></i> वारा: <strong>${wind} km/h</strong></div>
                        <div class="w-stat"><i class="fa-solid fa-cloud-rain"></i> पाऊस: <strong>${rain}%</strong></div>
                    </div>
                    ${isRainy ? '<div class="weather-alert-box"><i class="fa-solid fa-umbrella"></i> आज घराबाहेर पडताना छत्री सोबत ठेवा!</div>' : ''}
                </div>
            `;
        });

        // Live News HUD Card
        escaped = escaped.replace(/\[LIVE_NEWS_CARD:([^|\]]+)\|([^|\]]+)\|([^|\]]+)\]/g, function(match, dateStr, timeStr, b64Data) {
            let items = [];
            try {
                const jsonStr = decodeURIComponent(escape(atob(b64Data)));
                items = JSON.parse(jsonStr);
            } catch (e) {
                try {
                    items = JSON.parse(atob(b64Data));
                } catch (e2) {
                    console.warn('News card parse error:', e2);
                }
            }

            let itemsHtml = '';
            if (Array.isArray(items)) {
                items.forEach(it => {
                    const isTop = it.idx === 1;
                    const badgeClass = isTop ? 'news-badge-breaking' : 'news-badge-top';
                    const badgeIcon = isTop ? 'fa-bolt' : 'fa-newspaper';
                    const linkHtml = it.link ? `<a href="${it.link}" target="_blank" class="news-read-link" title="सविस्तर बातमी वाचा"><i class="fa-solid fa-arrow-up-right-from-square"></i></a>` : '';

                    itemsHtml += `
                        <div class="news-card-item ${isTop ? 'news-item-highlight' : ''}">
                            <div class="news-item-left">
                                <span class="news-idx-badge ${badgeClass}"><i class="fa-solid ${badgeIcon}"></i> #${it.idx}</span>
                            </div>
                            <div class="news-item-content">
                                <div class="news-item-title">${it.title}</div>
                                <div class="news-item-meta">
                                    <span class="news-meta-source"><i class="fa-solid fa-tower-broadcast"></i> ${it.source}</span>
                                    <span class="news-meta-time"><i class="fa-regular fa-clock"></i> ${it.time_tag}</span>
                                    ${linkHtml}
                                </div>
                            </div>
                        </div>
                    `;
                });
            }

            return `
                <div class="hud-news-card">
                    <div class="news-card-header">
                        <div class="news-live-tag">
                            <span class="live-blinking-dot"></span>
                            <span>LIVE NEWS FEED</span>
                        </div>
                        <div class="news-updated-pill">
                            <i class="fa-solid fa-clock-rotate-left"></i> ${timeStr} थेट अपडेट
                        </div>
                        <button type="button" class="news-refresh-btn" onclick="window.refreshLiveNews()" title="आत्ताच ताज्या बातम्या पुन्हा रिफ्रेश करा">
                            <i class="fa-solid fa-rotate"></i> रिफ्रेश (Refresh)
                        </button>
                    </div>
                    <div class="news-card-subheader">
                        <i class="fa-regular fa-calendar-check"></i> ${dateStr}
                    </div>
                    <div class="news-card-list">
                        ${itemsHtml}
                    </div>
                </div>
            `;
        });

        // Holographic Dinvishesh HUD Card
        escaped = escaped.replace(/\[DINVISHESH_CARD:([^|\]]+)\|([^|\]]+)\|([^|\]]+)\]/g, function(match, dateStr, langCode, b64Data) {
            let activeLang = langCode || 'mr';
            let cardData = {};
            try {
                cardData = JSON.parse(decodeURIComponent(escape(atob(b64Data))));
            } catch(e) {
                try { cardData = JSON.parse(atob(b64Data)); } catch(ex) {}
            }
            let shortDate = cardData.short_date || "";
            let titleText = activeLang === 'hi' ? 'दैनिक दिनविशेष // इतिहास के झरोखे से' : (activeLang === 'en' ? 'TODAY IN HISTORY // CHRONICLES' : 'दैनिक दिनविशेष // आजचा इतिहास');
            let switchPromptMR = shortDate ? `${shortDate} चा दिनविशेष मराठीत सांगा` : "आजचा दिनविशेष मराठीत सांगा";
            let switchPromptHI = shortDate ? `${shortDate} का दिनविशेष हिंदी में बताओ` : "आज का दिनविशेष हिंदी में बताओ";
            let switchPromptEN = shortDate ? `Tell Dinvishesh for ${shortDate} in English` : "Tell today's Dinvishesh in English";


            return `
                <div class="hud-dinvishesh-card">
                    <div class="dinvishesh-card-header">
                        <div class="dinvishesh-badge">
                            <i class="fa-solid fa-scroll"></i>
                            <span>${titleText}</span>
                        </div>
                        <div class="dinvishesh-date-pill">
                            <i class="fa-regular fa-calendar-days"></i> ${dateStr}
                        </div>
                    </div>
                    <div class="dinvishesh-lang-bar">
                        <span class="dinvishesh-lang-label"><i class="fa-solid fa-language"></i> तिन्ही भाषांमध्ये उपलब्ध (Available in 3 Languages):</span>
                        <div class="dinvishesh-lang-btns">
                            <button type="button" class="d-lang-btn ${activeLang === 'mr' ? 'active' : ''}" onclick="window.switchDinvisheshLang('${switchPromptMR}')" title="मराठीत पहा">
                                🚩 मराठी
                            </button>
                            <button type="button" class="d-lang-btn ${activeLang === 'hi' ? 'active' : ''}" onclick="window.switchDinvisheshLang('${switchPromptHI}')" title="हिंदी में देखें">
                                🇮🇳 हिंदी
                            </button>
                            <button type="button" class="d-lang-btn ${activeLang === 'en' ? 'active' : ''}" onclick="window.switchDinvisheshLang('${switchPromptEN}')" title="View in English">
                                🌐 English
                            </button>
                        </div>
                    </div>
                </div>
            `;
        });

        // Remove theme change token from message display
        escaped = escaped.replace(/\[CHANGE_THEME:[a-zA-Z0-9_-]+\]/g, '');

        escaped = escaped.replace(/\[YOUTUBE:([a-zA-Z0-9_-]+)\]/g, '<div class="video-embed-container"><iframe src="https://www.youtube.com/embed/$1?autoplay=1" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>');
        escaped = escaped.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
        escaped = escaped.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" class="chat-link"><i class="fa-solid fa-arrow-up-right-from-square"></i> $1</a>');
        escaped = escaped.replace(/^[•*]\s*(.+)$/gm, '• $1');
        escaped = escaped.replace(/\n/g, '<br>');
        return escaped;
    }

    let pendingImageBase64 = null;

    async function submitQuery(query) {
        if (!query.trim() && !pendingImageBase64) return;

        // Default query if only image is provided
        if (!query.trim() && pendingImageBase64) {
            if (langSelect.value === 'mr') query = "या फोटोबद्दल सविस्तर माहिती सांगा";
            else if (langSelect.value === 'hi') query = "इस फोटो के बारे में विस्तार से बताएं";
            else query = "Please tell me detailed information about this image";
        }

        unlockAudio();
        appendMessage('user', query, null, pendingImageBase64);
        
        const payloadImage = pendingImageBase64;
        clearImageSelection(); // Clear tray immediately
        
        textInput.value = '';
        statusMessage.textContent = 'जार्व्हिस विचार करत आहे... // PROCESSING';

        try {
            const currentPersona = document.getElementById('personaSelect') ? document.getElementById('personaSelect').value : 'ironman';
            let userName = localStorage.getItem('jarvis_user_name');
            if (!userName) {
                userName = await new Promise((resolve) => {
                    const modal = document.getElementById('nameModal');
                    const input = document.getElementById('nameInput');
                    const submitBtn = document.getElementById('submitNameBtn');
                    
                    if (modal && input && submitBtn) {
                        modal.classList.add('active');
                        input.focus();
                        
                        const cleanup = () => {
                            modal.classList.remove('active');
                            submitBtn.removeEventListener('click', onSubmit);
                        };
                        
                        const onSubmit = () => {
                            cleanup();
                            resolve(input.value || "Sir");
                        };
                        
                        submitBtn.addEventListener('click', onSubmit);
                    } else {
                        resolve("Sir");
                    }
                });

                if (userName && userName.trim()) {
                    userName = userName.trim();
                    localStorage.setItem('jarvis_user_name', userName);
                } else {
                    userName = "Sir";
                }
            }

            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: query,
                    lang: langSelect.value,
                    persona: currentPersona,
                    session_id: 'browser-user-session',
                    image: payloadImage,
                    user_name: userName
                })
            });

            const data = await res.json();
            if (data.status === 'success') {
                if (typeof playSfx === 'function') playSfx('success');
                if (data.is_stop) {
                    window.stopAllMedia();
                }

                // Check for dynamic theme change in Jarvis response
                if (data.response && data.response.includes('[CHANGE_THEME:')) {
                    const mTheme = data.response.match(/\[CHANGE_THEME:([a-zA-Z0-9_-]+)\]/);
                    if (mTheme && mTheme[1]) {
                        applyTheme(mTheme[1]);
                    }
                }

                appendMessage('jarvis', data.response, data.audio_url);


                if (data.is_aarti) {
                    if (data.aarti_type === 'hanuman_chalisa' || (data.audio_url && data.audio_url.includes('hanuman_chalisa'))) {
                        statusMessage.textContent = '🚩 श्री हनुमान चालीसा सुरू आहे... // HANUMAN CHALISA PLAYING';
                    } else if (data.aarti_type === 'shivraya' || (data.audio_url && data.audio_url.includes('shivraya'))) {
                        statusMessage.textContent = '🚩 छत्रपती शिवाजी महाराजांची आरती (शिवशंकराचा तू अवतार) सुरू आहे...';
                    } else {
                        statusMessage.textContent = '🌺 गणपती बाप्पांची मूळ आरती सुरू आहे... // AARTI PLAYING';
                    }
                    playAudio(data.audio_url || '/static/audio/ganpati_aarti_original.mp3', data.response, data.lang || langSelect.value);
                } else if (data.is_music && data.audio_url) {
                    statusMessage.textContent = '🎵 थेट गाणे सुरू होत आहे... // STARTING AUDIO STREAM';
                    playAudio(data.audio_url, '', data.lang || langSelect.value);
                } else if (!data.is_stop) {
                    playAudio(data.audio_url, data.response, data.lang || langSelect.value);
                }
            } else {
                if (typeof playSfx === 'function') playSfx('error');
                appendMessage('jarvis', 'क्षमस्व सर, विनंती पूर्ण करताना त्रुटी आली.');
                statusMessage.textContent = 'त्रुटी आली. कृपया पुन्हा प्रयत्न करा.';
                if (typeof resumeWakeWordIfNeeded === 'function') {
                    resumeWakeWordIfNeeded();
                }
            }
        } catch (err) {
            console.error('Fetch error:', err);
            if (typeof playSfx === 'function') playSfx('error');
            appendMessage('jarvis', 'सर्व्हरशी संपर्क होऊ शकला नाही. कृपया सर्व्हर चालू असल्याची खात्री करा.');
            if (typeof resumeWakeWordIfNeeded === 'function') {
                resumeWakeWordIfNeeded();
            }
        }
    }

    window.refreshLiveNews = function() {
        submitQuery('आजच्या ताज्या बातम्या काय आहेत?');
    };

    window.switchDinvisheshLang = function(promptText) {
        submitQuery(promptText);
    };

    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const query = textInput.value.trim();
        if (!query && !pendingImageBase64) return;
        textInput.value = '';   // ← लगेच clear करा
        textInput.focus();
        submitQuery(query);
    });


    // Quick Prompt Chips, Navbar Aarti Buttons & Modal Buttons
    document.querySelectorAll('.chip-btn, [data-prompt]').forEach(btn => {
        btn.addEventListener('click', () => {
            if (btn.id === 'quickVisionTipBtn' || btn.getAttribute('data-vision')) {
                const imageInput = document.getElementById('imageInput');
                if (imageInput) imageInput.click();
                return;
            }
            const prompt = btn.getAttribute('data-prompt');
            if (prompt) {
                textInput.value = prompt;
                submitQuery(prompt);
                // Also close navbar aarti dropdown and modal if opened
                const dropdownWrapper = document.getElementById('navAartiDropdownWrapper');
                if (dropdownWrapper) dropdownWrapper.classList.remove('active');
                const aartiModal = document.getElementById('aartiSangrahalayModal');
                if (aartiModal) aartiModal.classList.remove('active');
            }
        });
    });

    // -------------------------------------------------------------
    // 📷 Multimodal Image Upload Logic (Click, Paste, Drag&Drop)
    // -------------------------------------------------------------
    const imageUploadBtn = document.getElementById('imageUploadBtn');
    const imageInput = document.getElementById('imageInput');
    const imagePreviewTray = document.getElementById('imagePreviewTray');
    const imagePreviewImg = document.getElementById('imagePreviewImg');
    const clearImageBtn = document.getElementById('clearImageBtn');

    function clearImageSelection() {
        pendingImageBase64 = null;
        imagePreviewImg.src = '';
        imagePreviewTray.style.display = 'none';
        if (imageInput) imageInput.value = '';
    }

    if (clearImageBtn) {
        clearImageBtn.addEventListener('click', clearImageSelection);
    }

    if (imageUploadBtn && imageInput) {
        imageUploadBtn.addEventListener('click', () => {
            imageInput.click();
        });

        imageInput.addEventListener('change', (e) => {
            if (e.target.files && e.target.files[0]) {
                handleImageFile(e.target.files[0]);
            }
        });
    }

    function handleImageFile(file) {
        if (!file.type.startsWith('image/')) return;
        const reader = new FileReader();
        reader.onload = (e) => {
            pendingImageBase64 = e.target.result;
            imagePreviewImg.src = pendingImageBase64;
            imagePreviewTray.style.display = 'flex';
            textInput.focus();
        };
        reader.readAsDataURL(file);
    }

    // Paste Image from Clipboard (Ctrl+V)
    document.addEventListener('paste', (e) => {
        const items = (e.clipboardData || e.originalEvent.clipboardData).items;
        for (let item of items) {
            if (item.type.indexOf('image/') === 0) {
                const blob = item.getAsFile();
                if (blob) {
                    handleImageFile(blob);
                    e.preventDefault();
                }
            }
        }
    });

    // Drag and Drop support over the chat window
    const chatContainer = document.querySelector('.terminal-panel');
    if (chatContainer) {
        chatContainer.addEventListener('dragover', (e) => {
            e.preventDefault();
            chatContainer.style.boxShadow = 'inset 0 0 20px rgba(0, 238, 255, 0.4)';
        });
        chatContainer.addEventListener('dragleave', (e) => {
            e.preventDefault();
            chatContainer.style.boxShadow = 'none';
        });
        chatContainer.addEventListener('drop', (e) => {
            e.preventDefault();
            chatContainer.style.boxShadow = 'none';
            if (e.dataTransfer.files && e.dataTransfer.files[0]) {
                handleImageFile(e.dataTransfer.files[0]);
            }
        });
    }


    // 🌺 & 🚩 Dedicated Navbar Aarti Dropdown Toggle
    const navAartiDropdownWrapper = document.getElementById('navAartiDropdownWrapper');
    const navAartiTrigger = document.getElementById('navAartiTrigger');
    if (navAartiTrigger && navAartiDropdownWrapper) {
        navAartiTrigger.addEventListener('click', (e) => {
            e.stopPropagation();
            navAartiDropdownWrapper.classList.toggle('active');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!navAartiDropdownWrapper.contains(e.target)) {
                navAartiDropdownWrapper.classList.remove('active');
            }
        });
    }

    // 🌺 & 🚩 Aarti Sangrahalay Modal Open/Close
    const aartiSangrahalayModal = document.getElementById('aartiSangrahalayModal');
    const openAartiModalBtn = document.getElementById('openAartiModalBtn');
    const openAartiModalBtnSide = document.getElementById('openAartiModalBtnSide');
    const closeAartiModalBtn = document.getElementById('closeAartiModalBtn');
    const closeAartiModalFooterBtn = document.getElementById('closeAartiModalFooterBtn');

    function openAartiModal() {
        const dropdownWrapper = document.getElementById('navAartiDropdownWrapper');
        if (dropdownWrapper) dropdownWrapper.classList.remove('active');
        if (aartiSangrahalayModal) aartiSangrahalayModal.classList.add('active');
    }

    if (openAartiModalBtn) {
        openAartiModalBtn.addEventListener('click', openAartiModal);
    }
    if (openAartiModalBtnSide) {
        openAartiModalBtnSide.addEventListener('click', openAartiModal);
    }
    if (closeAartiModalBtn && aartiSangrahalayModal) {
        closeAartiModalBtn.addEventListener('click', () => aartiSangrahalayModal.classList.remove('active'));
    }
    if (closeAartiModalFooterBtn && aartiSangrahalayModal) {
        closeAartiModalFooterBtn.addEventListener('click', () => aartiSangrahalayModal.classList.remove('active'));
    }
    if (aartiSangrahalayModal) {
        aartiSangrahalayModal.addEventListener('click', (e) => {
            if (e.target === aartiSangrahalayModal) {
                aartiSangrahalayModal.classList.remove('active');
            }
        });
    }

    // Arc Core Click to Speak test
    arcCore.addEventListener('click', () => {
        const lang = langSelect.value;
        if (lang === 'hi') submitQuery('तुम कौन हो और क्या कर सकते हो?');
        else if (lang === 'en') submitQuery('Who are you and what are your capabilities?');
        else submitQuery('तू कोण आहेस आणि काय करू शकतोस?');
    });

    // Clear Log
    clearLogBtn.addEventListener('click', () => {
        chatLog.innerHTML = '';
        statusMessage.textContent = 'लॉग क्लिअर केला आहे.';
    });

    // Welcome Voice Replay
    if (welcomeVoiceBtn) {
        welcomeVoiceBtn.addEventListener('click', () => {
            const lang = langSelect.value;
            if (lang === 'hi') submitQuery('नमस्ते जार्विस');
            else if (lang === 'en') submitQuery('Hello Jarvis, introduce yourself');
            else submitQuery('नमस्कार जार्व्हिस');
        });
    }

    // Dynamic Language Selector Updates
    langSelect.addEventListener('change', () => {
        const lang = langSelect.value;
        if (lang === 'hi') {
            textInput.placeholder = "यहाँ टाइप करें या माइक्रोफ़ोन शुरू करें...";
            statusMessage.textContent = "हिंदी मोड सक्रिय // HINDI MODE ACTIVE";
            welcomeMsgBody.innerHTML = "नमस्ते सर! मैं <strong>जार्विस (J.A.R.V.I.S.)</strong> हूँ। सभी सिस्टम्स १००% सक्रिय हैं।<br><br>आप मुझसे हिंदी, मराठी या अंग्रेजी में कुछ भी पूछ सकते हैं। मैं आवाज और टेक्स्ट दोनों में तुरंत उत्तर दूंगा! 🚩";
        } else if (lang === 'en') {
            textInput.placeholder = "Type here or click microphone to speak...";
            statusMessage.textContent = "ENGLISH MODE ACTIVE // READY";
            welcomeMsgBody.innerHTML = "Greetings Sir! I am <strong>J.A.R.V.I.S.</strong> All systems are operational at 100% capacity.<br><br>You may ask me anything in English, Marathi, or Hindi. I will provide spoken audio and comprehensive textual answers immediately! 🌐";
        } else {
            textInput.placeholder = "येथे टाइप करा किंवा मायक्रोफोन चालू करा...";
            statusMessage.textContent = "मराठी मोड सक्रिय // MARATHI MODE ACTIVE";
            welcomeMsgBody.innerHTML = "नमस्कार सर! मी <strong>जार्व्हिस (J.A.R.V.I.S.)</strong> आहे. सर्व सिस्टीम्स १००% ऑनलाईन आहेत.<br><br>तुम्ही मला मराठी, हिंदी किंवा इंग्रजीमध्ये काहीही विचारू शकता. मी आवाज आणि मजकुराच्या स्वरूपात अचूक उत्तर देईन! 🚩";
        }
        try { if (wakeWordRecognition) wakeWordRecognition.stop(); } catch(e) {}
        setTimeout(() => { if (typeof ensureWakeWordActive === 'function') ensureWakeWordActive(); }, 300);
    });

    // -------------------------------------------------------------
    // ⏰ Background Reminders Checker Polling
    // -------------------------------------------------------------
    setInterval(async () => {
        try {
            const res = await fetch('/api/reminders/due');
            const data = await res.json();
            if (data.status === 'success' && data.due_reminders && data.due_reminders.length > 0) {
                data.due_reminders.forEach(r => {
                    playAlertSFX();
                    const alertMsg = `⏰ **अलर्ट / REMINDER:**\n${r.message}\n*(वेळ: ${r.target_time_str})*`;
                    appendMessage('jarvis', alertMsg, r.audio_url);
                    if (r.audio_url) {
                        playAudio(r.audio_url, r.message, 'mr');
                    }
                });
            }
        } catch (e) {}
    }, 6000);

    // -------------------------------------------------------------
    // 📝 Notes & Reminders Modal Operations
    // -------------------------------------------------------------
    async function loadNotesAndReminders() {
        try {
            const nRes = await fetch('/api/notes');
            const nData = await nRes.json();
            if (nData.status === 'success' && nData.notes.length > 0) {
                notesListContainer.innerHTML = nData.notes.map((n, i) => `
                    <div class="note-item">
                        <div class="note-text">${i + 1}. ${n.text}</div>
                        <div class="note-time"><i class="fa-regular fa-clock"></i> ${n.time}</div>
                    </div>
                `).join('');
            } else {
                notesListContainer.innerHTML = '<p class="empty-text">कोणतीही नोट उपलब्ध नाही.</p>';
            }

            const rRes = await fetch('/api/reminders');
            const rData = await rRes.json();
            if (rData.status === 'success' && rData.reminders.length > 0) {
                remindersListContainer.innerHTML = rData.reminders.map((r, i) => `
                    <div class="reminder-item ${r.triggered ? 'triggered' : 'active'}">
                        <div class="rem-msg">${i + 1}. ${r.message}</div>
                        <div class="rem-time"><i class="fa-solid fa-bell"></i> ${r.target_time_str} (${r.triggered ? 'पूर्ण / Done' : 'प्रलंबित / Pending'})</div>
                    </div>
                `).join('');
            } else {
                remindersListContainer.innerHTML = '<p class="empty-text">कोणताही रिमाइंड उपलब्ध नाही.</p>';
            }
        } catch (e) {
            console.error(e);
        }
    }

    if (notesModalBtn) {
        notesModalBtn.addEventListener('click', () => {
            loadNotesAndReminders();
            notesModal.classList.add('active');
        });
    }
    if (closeNotesBtn) {
        closeNotesBtn.addEventListener('click', () => notesModal.classList.remove('active'));
    }
    if (refreshNotesBtn) {
        refreshNotesBtn.addEventListener('click', loadNotesAndReminders);
    }
    if (clearAllNotesBtn) {
        clearAllNotesBtn.addEventListener('click', async () => {
            if (confirm('सर्व सेव्ह केलेल्या नोट्स पुसून टाकायच्या आहेत का?')) {
                await fetch('/api/notes', { method: 'DELETE' });
                await fetch('/api/reminders', { method: 'DELETE' });
                loadNotesAndReminders();
            }
        });
    }

    // -------------------------------------------------------------
    // ⚙️ Settings Modal
    // -------------------------------------------------------------
    settingsBtn.addEventListener('click', () => {
        settingsModal.classList.add('active');
    });
    closeSettingsBtn.addEventListener('click', () => {
        settingsModal.classList.remove('active');
    });
    cancelSettingsBtn.addEventListener('click', () => {
        settingsModal.classList.remove('active');
    });

    saveSettingsBtn.addEventListener('click', async () => {
        const key = apiKeyInput.value.trim();
        if (!key) return;

        try {
            const res = await fetch('/api/settings', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ gemini_api_key: key })
            });
            const data = await res.json();
            if (data.status === 'success') {
                playBeepSFX();
                alert('Gemini API Key यशस्वीरित्या सेव्ह केली!');
                settingsModal.classList.remove('active');
                document.getElementById('aiEngineLabel').textContent = 'GEMINI AI ACTIVE';
            } else {
                alert('त्रुटी: ' + data.message);
            }
        } catch (e) {
            alert('सेव्ह करताना अडचण आली: ' + e);
        }
    });

    // -------------------------------------------------------------
    // 🎨 Dynamic Sci-Fi Theme Manager
    // -------------------------------------------------------------
    function applyTheme(themeName) {
        const validThemes = ['saffron', 'matrix', 'purple', 'cyan'];
        const targetTheme = validThemes.includes(themeName) ? themeName : 'cyan';
        
        document.body.setAttribute('data-theme', targetTheme);
        localStorage.setItem('jarvis_theme', targetTheme);

        document.querySelectorAll('.theme-btn-dot').forEach(btn => {
            btn.classList.toggle('active', btn.getAttribute('data-theme') === targetTheme);
        });
    }

    document.querySelectorAll('.theme-btn-dot').forEach(btn => {
        btn.addEventListener('click', () => {
            const chosenTheme = btn.getAttribute('data-theme');
            if (chosenTheme) {
                applyTheme(chosenTheme);
                playBeepSFX();
            }
        });
    });

    // Initialize saved theme on load
    const savedTheme = localStorage.getItem('jarvis_theme') || 'cyan';
    applyTheme(savedTheme);

    // -------------------------------------------------------------
    // 🔋 Live Hardware Telemetry HUD (Battery & CPU)
    // -------------------------------------------------------------
    let warnedLowBattery = false;
    async function updateTelemetry() {
        try {
            const res = await fetch('/api/status');
            if (res.ok) {
                const data = await res.json();
                const tel = data.telemetry;
                if (tel) {
                    const batPct = document.getElementById('batteryPct');
                    const batIcon = document.getElementById('batteryIcon');
                    const cpuPct = document.getElementById('cpuPct');

                    if (batPct && tel.battery_percent !== null) {
                        batPct.textContent = `${tel.battery_percent}%`;
                        if (tel.power_plugged) {
                            batIcon.className = 'fa-solid fa-bolt-lightning';
                            batIcon.style.color = '#00ff88';
                        } else {
                            if (tel.battery_percent <= 20) {
                                batIcon.style.color = '#ff0055';
                                batIcon.className = 'fa-solid fa-battery-quarter';
                            } else if (tel.battery_percent <= 50) {
                                batIcon.style.color = '#ffaa00';
                                batIcon.className = 'fa-solid fa-battery-half';
                            } else {
                                batIcon.style.color = 'var(--cyan-bright)';
                                batIcon.className = 'fa-solid fa-battery-full';
                            }
                        }

                        // Voice / Audio Warning for low battery
                        if (!tel.power_plugged && tel.battery_percent <= 20 && !warnedLowBattery) {
                            warnedLowBattery = true;
                            playAlertSFX();
                            appendMessage('jarvis', '⚠️ **बॅटरी अलर्ट:** सर, लॅपटॉपची बॅटरी २०% पेक्षा कमी झाली आहे. कृपया चार्जर कनेक्ट करा!');
                        }
                    }

                    if (cpuPct && tel.cpu_percent !== null) {
                        cpuPct.textContent = `CPU ${tel.cpu_percent}%`;
                    }
                }
            }
        } catch (e) {
            // silent fail for telemetry
        }
    }

    setInterval(updateTelemetry, 15000);
    updateTelemetry();

    // -------------------------------------------------------------
    // 🔊 Futuristic Sci-Fi Sound FX Controller
    // -------------------------------------------------------------
    let sfxEnabled = localStorage.getItem('jarvis_sfx') !== 'false';
    const sfxToggleBtn = document.getElementById('sfxToggleBtn');
    if (sfxToggleBtn) {
        const updateSfxBtn = () => {
            sfxToggleBtn.classList.toggle('active', sfxEnabled);
            sfxToggleBtn.classList.toggle('muted', !sfxEnabled);
            sfxToggleBtn.innerHTML = sfxEnabled ? '<i class="fa-solid fa-volume-high"></i>' : '<i class="fa-solid fa-volume-xmark"></i>';
        };
        updateSfxBtn();
        sfxToggleBtn.addEventListener('click', () => {
            sfxEnabled = !sfxEnabled;
            localStorage.setItem('jarvis_sfx', sfxEnabled);
            updateSfxBtn();
            if (sfxEnabled) playSfx('listen');
        });
    }

    function playSfx(type) {
        if (!sfxEnabled) return;
        try {
            const ctx = getAudioContext();
            const now = ctx.currentTime;
            if (type === 'listen') {
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(987.77, now);
                osc.frequency.exponentialRampToValueAtTime(1318.51, now + 0.08);
                gain.gain.setValueAtTime(0.08, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.14);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(now);
                osc.stop(now + 0.15);
            } else if (type === 'success') {
                [523.25, 659.25, 783.99, 1046.50].forEach((freq, i) => {
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(freq, now + i * 0.06);
                    gain.gain.setValueAtTime(0.05, now + i * 0.06);
                    gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.06 + 0.2);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start(now + i * 0.06);
                    osc.stop(now + i * 0.06 + 0.25);
                });
            } else if (type === 'error') {
                [220, 164.81].forEach((freq, i) => {
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'sawtooth';
                    osc.frequency.setValueAtTime(freq, now + i * 0.1);
                    gain.gain.setValueAtTime(0.05, now + i * 0.1);
                    gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.1 + 0.15);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start(now + i * 0.1);
                    osc.stop(now + i * 0.1 + 0.2);
                });
            }
        } catch (e) {}
    }

    // -------------------------------------------------------------
    // 🎙️ "Hey Jarvis" Continuous Auto-Active Wake Word Engine (ALWAYS ON 24x7)
    // -------------------------------------------------------------
    let wakeWordEnabled = false; // Disabled by default to prevent continuous mic switching and audio blocking on mobile
    let wakeWordRecognition = null;
    let wakeWordActive = false;
    let wakeDebounceTimer = null;
    let lastDetectedInlineCmd = '';

    const wakeWordBtn = document.getElementById('wakeWordBtn');
    const wakeWordLabel = document.getElementById('wakeWordLabel');

    if (wakeWordBtn) {
        wakeWordBtn.classList.add('active');
    }
    if (wakeWordLabel) {
        wakeWordLabel.textContent = wakeWordEnabled ? "⚡ 'HEY JARVIS' २४x७ चालू (ALWAYS ACTIVE)" : "⚡ 'HEY JARVIS' बंद आहे (OFF)";
    }

    // Broad Multi-lingual Wake Word Pattern (English, Marathi, Hindi)
    const wakeRegex = /(?:^|.*?\b)(?:hey|hello|hi|ok|hai|hay|he|are|arre|aika|listen|हे|हाय|हॅलो|ऐका)?\s*(?:jarvis|जार्व्हिस|जारविस|जार्विस|jervis|zarvis|सर्व्हिस)\b\s*[,:]*\s*(.*)$/iu;

    if (SpeechRecognition) {
        wakeWordRecognition = new SpeechRecognition();
        wakeWordRecognition.continuous = true;
        wakeWordRecognition.interimResults = true;
        wakeWordRecognition.lang = getLangCode();

        wakeWordRecognition.onstart = () => {
            wakeWordActive = true;
            if (wakeWordBtn) wakeWordBtn.classList.add('active');
            if (wakeWordLabel) wakeWordLabel.textContent = "⚡ 'HEY JARVIS' २४x७ चालू (ALWAYS ACTIVE)";
        };

        wakeWordRecognition.onresult = (event) => {
            if (isSpeaking || isListening) return;
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                const phrase = event.results[i][0].transcript.trim();
                const isFinal = event.results[i].isFinal;
                console.log('[WAKE-WORD SCANNER]:', phrase, '| isFinal:', isFinal);

                const match = phrase.match(wakeRegex);
                if (match) {
                    const inlineCommand = match[1] ? match[1].trim() : '';
                    if (inlineCommand.length > 2) {
                        // User spoke wake word + direct command in ONE sentence! (e.g. "Hey Jarvis play aarti")
                        lastDetectedInlineCmd = inlineCommand;
                        statusMessage.textContent = `⚡ थेट आज्ञा: "${inlineCommand}"`;
                        if (wakeDebounceTimer) clearTimeout(wakeDebounceTimer);
                        wakeDebounceTimer = setTimeout(() => {
                            if (isSpeaking || isListening) return;
                            console.log('⚡ EXECUTING DIRECT ONE-SHOT COMMAND:', lastDetectedInlineCmd);
                            playSfx('listen');
                            try { wakeWordRecognition.stop(); } catch(e) {}
                            wakeWordActive = false;
                            submitQuery(lastDetectedInlineCmd);
                            lastDetectedInlineCmd = '';
                        }, isFinal ? 80 : 650);
                    } else {
                        // User just said "Hey Jarvis", waiting for confirmation
                        if (wakeDebounceTimer) clearTimeout(wakeDebounceTimer);
                        wakeDebounceTimer = setTimeout(() => {
                            if (isSpeaking || isListening) return;
                            console.log('⚡ WAKE WORD PROMPT TRIGGERED!');
                            playSfx('listen');
                            try { wakeWordRecognition.stop(); } catch(e) {}
                            wakeWordActive = false;
                            statusMessage.textContent = '⚡ होय सर, मी ऐकत आहे... // LISTENING...';
                            safeStartListening();
                        }, isFinal ? 60 : 450);
                    }
                    return;
                }
            }
        };

        wakeWordRecognition.onend = () => {
            wakeWordActive = false;
            if (wakeWordEnabled && !isListening && !isSpeaking) {
                setTimeout(ensureWakeWordActive, 200);
            }
        };

        wakeWordRecognition.onerror = (e) => {
            wakeWordActive = false;
            if (e.error !== 'no-speech') {
                console.warn('Wake word recognition status/error:', e.error);
            }
            if (wakeWordEnabled && !isListening && !isSpeaking) {
                setTimeout(ensureWakeWordActive, 600);
            }
        };
    }

    // Resilient Wake-Word Activator
    function ensureWakeWordActive() {
        if (!SpeechRecognition || !wakeWordRecognition) return;
        if (!wakeWordEnabled || isSpeaking || isListening) return;
        try {
            wakeWordRecognition.lang = getLangCode();
            wakeWordRecognition.start();
            wakeWordActive = true;
        } catch (e) {
            // Already started or transitioning
        }
    }
    window.ensureWakeWordActive = ensureWakeWordActive;
    window.resumeWakeWordIfNeeded = ensureWakeWordActive;

    // Auto-start wake word immediately on load
    ensureWakeWordActive();

    // Watchdog Heartbeat: Checks every 1.2 seconds so wake-word NEVER stays dead
    setInterval(() => {
        if (wakeWordEnabled && !isSpeaking && !isListening) {
            ensureWakeWordActive();
        }
    }, 1200);

    // Auto-resume on any user touch/click/key/focus to ensure browser security policies never block it
    ['click', 'keydown', 'touchstart', 'focus'].forEach(evt => {
        window.addEventListener(evt, () => {
            unlockAudio();
            ensureWakeWordActive();
        }, { passive: true });
    });

    document.addEventListener('visibilitychange', () => {
        if (!document.hidden) ensureWakeWordActive();
    });

    // Clicking the status badge toggles the wake word functionality
    if (wakeWordBtn) {
        if (!wakeWordEnabled) {
            wakeWordBtn.classList.remove('active');
        }
        wakeWordBtn.addEventListener('click', () => {
            unlockAudio();
            wakeWordEnabled = !wakeWordEnabled;
            if (wakeWordEnabled) {
                wakeWordBtn.classList.add('active');
                if (wakeWordLabel) wakeWordLabel.textContent = "⚡ 'HEY JARVIS' २४x७ चालू (ALWAYS ACTIVE)";
                statusMessage.textContent = '⚡ वेक-वर्ड चालू झाले आहे.';
                ensureWakeWordActive();
                playSfx('listen');
            } else {
                wakeWordBtn.classList.remove('active');
                if (wakeWordLabel) wakeWordLabel.textContent = "⚡ 'HEY JARVIS' बंद आहे (OFF)";
                statusMessage.textContent = '⚡ वेक-वर्ड बंद केले आहे.';
                try { if (wakeWordRecognition) wakeWordRecognition.stop(); } catch(e) {}
            }
        });
    }

    // -------------------------------------------------------------
    // 🎭 Personality Switcher Manager
    // -------------------------------------------------------------
    const personaSelect = document.getElementById('personaSelect');
    if (personaSelect) {
        const savedPersona = localStorage.getItem('jarvis_persona') || 'ironman';
        personaSelect.value = savedPersona;
        personaSelect.addEventListener('change', () => {
            localStorage.setItem('jarvis_persona', personaSelect.value);
            playSfx('listen');
            let welcome = "";
            if (personaSelect.value === 'mavala') {
                welcome = "🚩 जय भवानी! जय शिवाजी! स्वराज्य मावळा मोड सक्रिय झाला आहे. आज्ञा प्रमाणे तत्पर आहे!";
            } else if (personaSelect.value === 'casual') {
                welcome = "🤝 काय मग भावा! कॅज्युअल मित्र मोड चालू झाला आहे. बोल काय मदत करू?";
            } else {
                welcome = "🤖 At your service, Sir. Iron Man J.A.R.V.I.S. persona engaged.";
            }
            appendMessage('jarvis', welcome);
            speakWithBrowserSynthesis(welcome, langSelect.value);
        });
    }

    // -------------------------------------------------------------
    // 📱 Mobile Wi-Fi Remote Connect Manager
    // -------------------------------------------------------------
    const mobileRemoteBtn = document.getElementById('mobileRemoteBtn');
    const mobileModal = document.getElementById('mobileModal');
    const closeMobileBtn = document.getElementById('closeMobileBtn');
    const closeMobileModalBtn = document.getElementById('closeMobileModalBtn');
    const mobileIpDisplay = document.getElementById('mobileIpDisplay');
    const copyIpBtn = document.getElementById('copyIpBtn');

    async function loadMobileNetworkInfo() {
        try {
            if (mobileIpDisplay) mobileIpDisplay.textContent = 'तपासत आहे...';
            const res = await fetch('/api/local-ip');
            if (res.ok) {
                const data = await res.json();
                if (mobileIpDisplay && data.url) {
                    mobileIpDisplay.textContent = data.url;
                    mobileIpDisplay.dataset.url = data.url;
                }
            } else {
                if (mobileIpDisplay) mobileIpDisplay.textContent = `http://${window.location.hostname}:5000`;
            }
        } catch (e) {
            if (mobileIpDisplay) mobileIpDisplay.textContent = `http://${window.location.hostname}:5000`;
        }
    }

    if (mobileRemoteBtn && mobileModal) {
        mobileRemoteBtn.addEventListener('click', () => {
            mobileModal.classList.add('active');
            playSfx('listen');
            loadMobileNetworkInfo();
        });
    }
    if (closeMobileBtn && mobileModal) {
        closeMobileBtn.addEventListener('click', () => mobileModal.classList.remove('active'));
    }
    if (closeMobileModalBtn && mobileModal) {
        closeMobileModalBtn.addEventListener('click', () => mobileModal.classList.remove('active'));
    }
    if (copyIpBtn && mobileIpDisplay) {
        copyIpBtn.addEventListener('click', () => {
            const url = mobileIpDisplay.dataset.url || mobileIpDisplay.textContent;
            navigator.clipboard.writeText(url).then(() => {
                copyIpBtn.innerHTML = '<i class="fa-solid fa-check"></i> कॉपी केले!';
                setTimeout(() => {
                    copyIpBtn.innerHTML = '<i class="fa-solid fa-copy"></i> कॉपी';
                }, 2000);
            });
        });
    }

    // -------------------------------------------------------------
    // 🪐 Three.js 3D Holographic Arc Reactor Core
    // -------------------------------------------------------------
    let threeScene, threeCamera, threeRenderer, coreMesh, outerRing, innerRing, particleSystem;
    const threeContainer = document.getElementById('threeContainer');
    const threeCanvas = document.getElementById('threeCanvas');
    const btn2DReactor = document.getElementById('btn2DReactor');
    const btn3DReactor = document.getElementById('btn3DReactor');
    const reactorWrapper2D = document.getElementById('reactorWrapper2D');

    function initThreeJSHologram() {
        if (!window.THREE || !threeCanvas || !threeContainer || threeRenderer) return;

        const width = 280;
        const height = 280;

        threeScene = new THREE.Scene();
        threeCamera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
        threeCamera.position.z = 7;

        threeRenderer = new THREE.WebGLRenderer({ canvas: threeCanvas, alpha: true, antialias: true });
        threeRenderer.setSize(width, height);
        threeRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

        // Core Glowing Wireframe Icosahedron
        const coreGeo = new THREE.IcosahedronGeometry(1.2, 2);
        const coreMat = new THREE.MeshBasicMaterial({
            color: 0x00f2fe,
            wireframe: true,
            transparent: true,
            opacity: 0.85
        });
        coreMesh = new THREE.Mesh(coreGeo, coreMat);
        threeScene.add(coreMesh);

        // Inner Glowing Sphere
        const innerSolidGeo = new THREE.SphereGeometry(0.65, 16, 16);
        const innerSolidMat = new THREE.MeshBasicMaterial({
            color: 0x00f2fe,
            transparent: true,
            opacity: 0.45
        });
        const innerSolid = new THREE.Mesh(innerSolidGeo, innerSolidMat);
        coreMesh.add(innerSolid);

        // Outer Tech Ring Torus
        const outerTorusGeo = new THREE.TorusGeometry(2.1, 0.05, 16, 100);
        const outerTorusMat = new THREE.MeshBasicMaterial({
            color: 0x00a8ff,
            wireframe: true,
            transparent: true,
            opacity: 0.7
        });
        outerRing = new THREE.Mesh(outerTorusGeo, outerTorusMat);
        threeScene.add(outerRing);

        // Inner Rotating Torus
        const innerTorusGeo = new THREE.TorusGeometry(1.7, 0.04, 16, 80);
        const innerTorusMat = new THREE.MeshBasicMaterial({
            color: 0x00ff88,
            transparent: true,
            opacity: 0.75
        });
        innerRing = new THREE.Mesh(innerTorusGeo, innerTorusMat);
        innerRing.rotation.x = Math.PI / 3;
        threeScene.add(innerRing);

        // Floating Energy Particles
        const particleCount = 100;
        const particleGeo = new THREE.BufferGeometry();
        const posArray = new Float32Array(particleCount * 3);

        for (let i = 0; i < particleCount * 3; i += 3) {
            const r = 1.8 + Math.random() * 1.2;
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.acos(Math.random() * 2 - 1);
            posArray[i] = r * Math.sin(phi) * Math.cos(theta);
            posArray[i + 1] = r * Math.sin(phi) * Math.sin(theta);
            posArray[i + 2] = r * Math.cos(phi);
        }

        particleGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
        const particleMat = new THREE.PointsMaterial({
            size: 0.07,
            color: 0x00f2fe,
            transparent: true,
            opacity: 0.8
        });
        particleSystem = new THREE.Points(particleGeo, particleMat);
        threeScene.add(particleSystem);

        // Mouse Parallax Interaction
        let mouseX = 0, mouseY = 0;
        threeContainer.addEventListener('mousemove', (e) => {
            const rect = threeContainer.getBoundingClientRect();
            mouseX = ((e.clientX - rect.left) / rect.width - 0.5) * 2;
            mouseY = ((e.clientY - rect.top) / rect.height - 0.5) * 2;
        });
        threeContainer.addEventListener('mouseleave', () => {
            mouseX = 0;
            mouseY = 0;
        });

        // 3D Animation Loop
        let clock = 0;
        function animate3D() {
            requestAnimationFrame(animate3D);
            if (!threeContainer || threeContainer.style.display === 'none') return;

            clock += 0.015;
            const speedMultiplier = isSpeaking ? 3.0 : (isListening ? 2.0 : 1.0);

            coreMesh.rotation.y += 0.008 * speedMultiplier;
            coreMesh.rotation.x += 0.005 * speedMultiplier;

            outerRing.rotation.z += 0.012 * speedMultiplier;
            outerRing.rotation.y += 0.006 * speedMultiplier;

            innerRing.rotation.x -= 0.015 * speedMultiplier;
            innerRing.rotation.z += 0.008 * speedMultiplier;

            particleSystem.rotation.y += 0.004 * speedMultiplier;

            // Audio reaction pulsing
            const pulse = (Math.sin(clock * 3) * 0.05 + 1.0) * (isSpeaking ? 1.15 : (isListening ? 1.1 : 1.0));
            coreMesh.scale.set(pulse, pulse, pulse);

            // Mouse parallax tilt
            threeScene.rotation.y += (mouseX * 0.5 - threeScene.rotation.y) * 0.05;
            threeScene.rotation.x += (-mouseY * 0.5 - threeScene.rotation.x) * 0.05;

            threeRenderer.render(threeScene, threeCamera);
        }
        animate3D();
    }

    if (btn2DReactor && btn3DReactor && reactorWrapper2D && threeContainer) {
        btn2DReactor.addEventListener('click', () => {
            btn2DReactor.classList.add('active');
            btn3DReactor.classList.remove('active');
            reactorWrapper2D.style.display = 'flex';
            threeContainer.style.display = 'none';
            playSfx('listen');
        });

        btn3DReactor.addEventListener('click', () => {
            btn3DReactor.classList.add('active');
            btn2DReactor.classList.remove('active');
            reactorWrapper2D.style.display = 'none';
            threeContainer.style.display = 'flex';
            playSfx('listen');
            initThreeJSHologram();
        });
    }
});

