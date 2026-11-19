/* =========================================================
   audio.js — WebAudio 로 만드는 배경음과 효과음 (로파이 · 사무실 · 노을)
   외부 음원 파일 없이 코드로만 합성합니다.
   ========================================================= */
(function (global) {
  'use strict';

  var ctx = null;
  var master = null;
  var bgmBus = null;
  var sfxBus = null;
  var delay = null;
  var filter = null;
  var timer = null;
  var moodName = 'silent';
  var enabled = true;
  var bgmOn = true;
  var started = false;
  var nextTime = 0;
  var step = 0;
  var current = null;

  /* 음계: 각 무드의 코드 진행과 멜로디 패턴 */
  var MOODS = {
    title: {
      bpm: 68, wave: 'sine', pad: 0.05, pluck: 0.05, bass: 0.045,
      chords: [[50, 57, 62, 66], [47, 54, 59, 62], [43, 50, 55, 59], [45, 52, 57, 61]],
      bells: [[74, 78, 81, 78], [71, 74, 78, 74], [67, 71, 74, 71], [69, 73, 76, 73]],
      every: 8
    },
    day: {
      bpm: 84, wave: 'triangle', pad: 0.042, pluck: 0.05, bass: 0.04,
      chords: [[53, 60, 65, 69], [55, 62, 67, 71], [48, 55, 60, 64], [50, 57, 62, 66]],
      bells: [[77, 81, 84, 81], [79, 83, 86, 83], [72, 76, 79, 76], [74, 77, 81, 77]],
      every: 8
    },
    night: {
      bpm: 60, wave: 'sine', pad: 0.05, pluck: 0.042, bass: 0.05,
      chords: [[45, 52, 57, 60], [41, 48, 53, 57], [43, 50, 55, 58], [40, 47, 52, 55]],
      bells: [[69, 72, 76, 72], [65, 69, 72, 69], [67, 71, 74, 71], [64, 67, 71, 67]],
      every: 10
    },
    dusk: {
      bpm: 74, wave: 'triangle', pad: 0.046, pluck: 0.05, bass: 0.044,
      chords: [[48, 55, 60, 64], [50, 57, 62, 65], [45, 52, 57, 60], [47, 54, 59, 62]],
      bells: [[72, 76, 79, 84], [74, 78, 81, 86], [69, 72, 76, 81], [71, 74, 78, 83]],
      every: 8
    },
    jazz: {
      bpm: 92, wave: 'triangle', pad: 0.038, pluck: 0.05, bass: 0.042,
      chords: [[53, 60, 64, 67], [51, 58, 62, 65], [48, 55, 59, 62], [50, 57, 61, 64]],
      bells: [[77, 81, 84, 88], [75, 79, 82, 86], [72, 76, 79, 84], [74, 77, 81, 85]],
      every: 6
    },
    lofi: {
      bpm: 66, wave: 'sine', pad: 0.05, pluck: 0.036, bass: 0.048,
      chords: [[48, 55, 59, 62], [45, 52, 55, 59], [43, 50, 54, 57], [45, 52, 57, 60]],
      bells: [[72, 76, 79, 76], [69, 72, 76, 72], [67, 71, 74, 71], [69, 74, 77, 74]],
      every: 12
    },
    warm: {
      bpm: 72, wave: 'triangle', pad: 0.048, pluck: 0.055, bass: 0.045,
      chords: [[50, 57, 62, 65], [48, 55, 60, 64], [45, 52, 57, 60], [47, 54, 59, 62]],
      bells: [[74, 77, 81, 84], [72, 76, 79, 84], [69, 72, 76, 81], [71, 74, 78, 83]],
      every: 8
    },
    tense: {
      bpm: 96, wave: 'sawtooth', pad: 0.028, pluck: 0.028, bass: 0.045,
      chords: [[38, 45, 50], [38, 44, 51], [36, 43, 48], [38, 45, 50]],
      bells: [[62], [63], [60], [62]],
      every: 16
    }
  };

  function freq(m) { return 440 * Math.pow(2, (m - 69) / 12); }

  var rainSrc = null, rainGain = null, rainOn = false;

  function makeRain() {
    if (rainSrc) return;
    var len = Math.floor(ctx.sampleRate * 2);
    var buf = ctx.createBuffer(1, len, ctx.sampleRate);
    var d = buf.getChannelData(0);
    var last = 0;
    for (var i = 0; i < len; i++) {
      var w = Math.random() * 2 - 1;
      last = (last + 0.02 * w) / 1.02;   // 살짝 갈색 잡음
      d[i] = (w * 0.32 + last * 2.4) * 0.5;
    }
    rainSrc = ctx.createBufferSource();
    rainSrc.buffer = buf;
    rainSrc.loop = true;
    var hp = ctx.createBiquadFilter();
    hp.type = 'highpass'; hp.frequency.value = 700;
    var lp = ctx.createBiquadFilter();
    lp.type = 'lowpass'; lp.frequency.value = 5200;
    rainGain = ctx.createGain();
    rainGain.gain.value = 0;
    rainSrc.connect(hp); hp.connect(lp); lp.connect(rainGain);
    rainGain.connect(master);
    rainSrc.start(0);
  }

  function setRain(on) {
    rainOn = !!on;
    if (!ctx) {
      if (!on) return;
      init();
    }
    if (!ctx || !started) return;
    makeRain();
    rainGain.gain.setTargetAtTime(rainOn && enabled ? 0.5 : 0, ctx.currentTime, 0.9);
  }

  function init() {
    if (ctx) return ctx;
    var C = global.AudioContext || global.webkitAudioContext;
    if (!C) return null;
    ctx = new C();

    master = ctx.createGain();
    master.gain.value = 0.9;
    master.connect(ctx.destination);

    filter = ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.value = 2400;
    filter.Q.value = 0.6;
    filter.connect(master);

    delay = ctx.createDelay(1.2);
    delay.delayTime.value = 0.36;
    var fb = ctx.createGain();
    fb.gain.value = 0.26;
    var wet = ctx.createGain();
    wet.gain.value = 0.3;
    delay.connect(fb); fb.connect(delay);
    delay.connect(wet); wet.connect(filter);

    bgmBus = ctx.createGain();
    bgmBus.gain.value = 0;
    bgmBus.connect(filter);
    bgmBus.connect(delay);

    sfxBus = ctx.createGain();
    sfxBus.gain.value = 0.9;
    sfxBus.connect(master);
    return ctx;
  }

  /* 첫 사용자 조작에서 호출 — 브라우저 정책상 이때 열어야 합니다. */
  function unlock() {
    var c = init();
    if (!c) return;
    if (c.state === 'suspended') c.resume();
    started = true;
    if (bgmOn && moodName !== 'silent') startLoop();
    if (rainOn) setRain(true);
  }

  function startLoop() {
    if (timer || !ctx) return;
    nextTime = ctx.currentTime + 0.06;
    step = 0;
    timer = setInterval(schedule, 140);
  }

  function stopLoop() {
    if (timer) { clearInterval(timer); timer = null; }
  }

  function schedule() {
    if (!ctx || !current) return;
    var m = current;
    var beat = 60 / m.bpm;
    while (nextTime < ctx.currentTime + 0.9) {
      playStep(m, step, nextTime, beat);
      nextTime += beat;
      step++;
    }
  }

  function playStep(m, i, t, beat) {
    var bar = Math.floor(i / 4) % m.chords.length;
    if (i % 4 === 0) {
      var chord = m.chords[bar];
      for (var k = 0; k < chord.length; k++) {
        pad(freq(chord[k]), beat * 3.9, m.pad * (k === 0 ? 1.15 : 0.8), t + k * 0.012);
      }
      bass(freq(chord[0] - 12), beat * 3.6, m.bass, t);
    }
    // 멜로디: 2박마다, every 주기로 한 음
    if (i % 2 === 0) {
      var scale = m.bells[bar];
      var n = scale[(Math.floor(i / 2)) % scale.length];
      if ((i / 2) % m.every !== 0 || m.every < 8) {
        pluck(freq(n), beat * 2.4, m.pluck, t + 0.02);
      }
    }
    if (m === MOODS.tense && i % 4 === 2) {
      thump(t, 0.9);
    }
  }

  function pad(f, dur, vol, t) {
    var o = ctx.createOscillator();
    var o2 = ctx.createOscillator();
    var g = ctx.createGain();
    o.type = current.wave;
    o2.type = 'sine';
    o.frequency.value = f;
    o2.frequency.value = f * 1.004;
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(vol, t + Math.min(1.2, dur * 0.4));
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    o.connect(g); o2.connect(g); g.connect(bgmBus);
    o.start(t); o2.start(t);
    o.stop(t + dur + 0.05); o2.stop(t + dur + 0.05);
  }

  function pluck(f, dur, vol, t) {
    var o = ctx.createOscillator();
    var g = ctx.createGain();
    o.type = 'triangle';
    o.frequency.setValueAtTime(f, t);
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(vol, t + 0.02);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    o.connect(g); g.connect(bgmBus);
    o.start(t); o.stop(t + dur + 0.03);
  }

  function bass(f, dur, vol, t) {
    var o = ctx.createOscillator();
    var g = ctx.createGain();
    o.type = 'sine';
    o.frequency.setValueAtTime(f, t);
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(vol, t + 0.12);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    o.connect(g); g.connect(bgmBus);
    o.start(t); o.stop(t + dur + 0.05);
  }

  function thump(t, vol) {
    var o = ctx.createOscillator();
    var g = ctx.createGain();
    o.type = 'sine';
    o.frequency.setValueAtTime(72, t);
    o.frequency.exponentialRampToValueAtTime(42, t + 0.22);
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(vol * 0.09, t + 0.01);
    g.gain.exponentialRampToValueAtTime(0.0001, t + 0.32);
    o.connect(g); g.connect(bgmBus);
    o.start(t); o.stop(t + 0.36);
  }

  /* ---------------- public ---------------- */
  function setMood(name) {
    if (name === moodName) return;
    moodName = name;
    if (!ctx) { if (name !== 'silent') init(); }
    if (!ctx) return;
    var target = MOODS[name];
    if (!target) {
      bgmBus.gain.cancelScheduledValues(ctx.currentTime);
      bgmBus.gain.setTargetAtTime(0, ctx.currentTime, 0.4);
      current = null;
      stopLoop();
      return;
    }
    current = target;
    step = 0;
    nextTime = ctx.currentTime + 0.1;
    if (started && bgmOn) {
      bgmBus.gain.cancelScheduledValues(ctx.currentTime);
      bgmBus.gain.setTargetAtTime(0.9, ctx.currentTime, 0.8);
      startLoop();
    }
  }

  function setBgm(on) {
    bgmOn = on;
    if (!ctx) return;
    if (!on) {
      bgmBus.gain.setTargetAtTime(0, ctx.currentTime, 0.3);
      stopLoop();
    } else if (started && moodName !== 'silent') {
      bgmBus.gain.setTargetAtTime(0.9, ctx.currentTime, 0.6);
      startLoop();
    }
  }

  function sfx(kind) {
    if (!enabled) return;
    var c = init();
    if (!c || c.state === 'suspended') return;
    var t = c.currentTime;
    if (kind === 'blip') {
      tone(1180 + Math.random() * 110, 0.018, 'sine', 0.012, t);
    } else if (kind === 'advance') {
      tone(520, 0.06, 'triangle', 0.028, t);
    } else if (kind === 'select') {
      tone(659, 0.07, 'triangle', 0.045, t);
      tone(988, 0.1, 'sine', 0.034, t + 0.06);
    } else if (kind === 'open') {
      tone(880, 0.06, 'sine', 0.03, t);
      tone(1175, 0.09, 'sine', 0.024, t + 0.05);
    } else if (kind === 'chime') {
      [523.25, 659.25, 783.99, 1046.5].forEach(function (f, i) {
        tone(f, 0.6, 'sine', 0.05, t + i * 0.13);
      });
    } else if (kind === 'heart') {
      tone(740, 0.09, 'sine', 0.035, t);
      tone(988, 0.12, 'sine', 0.03, t + 0.07);
    }
  }

  function tone(f, dur, type, vol, t) {
    var o = ctx.createOscillator();
    var g = ctx.createGain();
    o.type = type || 'sine';
    o.frequency.setValueAtTime(f, t);
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(vol || 0.04, t + 0.008);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    o.connect(g); g.connect(sfxBus);
    o.start(t); o.stop(t + dur + 0.02);
  }

  global.VNAudio = {
    unlock: unlock,
    setRain: setRain,
    setMood: setMood,
    setBgm: setBgm,
    sfx: sfx,
    setSfx: function (on) {
      enabled = on;
      if (ctx && rainGain && rainOn) {
        rainGain.gain.setTargetAtTime(on ? 0.5 : 0, ctx.currentTime, 0.4);
      }
    },
    isReady: function () { return !!ctx; },
    debug: function () {
      return { state: ctx ? ctx.state : 'none', mood: moodName, bgmGain: bgmBus ? bgmBus.gain.value : 0 };
    }
  };
})(window);
