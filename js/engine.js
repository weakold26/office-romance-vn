/* =========================================================
   engine.js — 퇴근 삼십 분 전
   비주얼 노벨 엔진: 무대, 타자기, 분기, 호감도, 세이브, 자동/스킵
   ========================================================= */
(function () {
  'use strict';

  var KEY = {
    auto: 'orbitvn.auto',
    slot: 'orbitvn.slot.',
    endings: 'orbitvn.endings',
    settings: 'orbitvn.settings'
  };

  var ASSETS = {
    bg: {
      office_day: 'assets/img/office_day.webp?v=3',
      rooftop_sunset: 'assets/img/rooftop_sunset.webp?v=3',
      office_night: 'assets/img/office_night.webp?v=3',
      store_night: 'assets/img/store_night.webp?v=3'
    },
    char: {
      seoyun: {
        base: 'assets/img/seoyun_base.webp?v=3',
        blush: 'assets/img/seoyun_blush.webp?v=3',
        surprised: 'assets/img/seoyun_surprised.webp?v=3',
        serious: 'assets/img/seoyun_serious.webp?v=3'
      },
      haram: {
        base: 'assets/img/haram_base.webp?v=3',
        blush: 'assets/img/haram_blush.webp?v=3',
        surprised: 'assets/img/haram_surprised.webp?v=3',
        serious: 'assets/img/haram_serious.webp?v=3'
      }
    }
  };

  /* ---------------- state ---------------- */
  var meta = null, nodes = null;
  var state = newState();
  var history = [];
  var typingTimer = null, fullText = '', charIndex = 0, afterTyping = null;
  var choiceOpen = false, modalOpen = false, ended = false;
  var bgFront = 'A';
  var settings = { sound: true, bgm: true, speed: 24 };
  var autoTimer = null, autoOn = false, skipOn = false;
  var rainState = false;

  function newState() {
    return { node: null, aff: { seoyun: 0, haram: 0 }, flags: {}, chapter: '' };
  }

  function $(id) { return document.getElementById(id); }

  /* ---------------- boot ---------------- */
  function init() {
    loadSettings();
    buildDust();
    bindGlobal();
    fetch('src/data/scenario.json', { cache: 'no-cache' })
      .then(function (r) { return r.json(); })
      .then(function (json) {
        meta = json.meta;
        nodes = json.nodes;
        preload().then(function () {
          document.body.classList.remove('loading');
          showTitle();
        });
      })
      .catch(function (e) {
        document.body.classList.remove('loading');
        var box = $('title-menu');
        if (box) box.innerHTML = '<p class="err">시나리오를 불러오지 못했습니다. 새로고침해 주세요.</p>';
        console.error(e);
      });
  }

  function preload() {
    var urls = [];
    Object.keys(ASSETS.bg).forEach(function (k) { urls.push(ASSETS.bg[k]); });
    Object.keys(ASSETS.char).forEach(function (k) {
      Object.keys(ASSETS.char[k]).forEach(function (e) { urls.push(ASSETS.char[k][e]); });
    });
    var uniq = urls.filter(function (v, i) { return urls.indexOf(v) === i; });
    var done = 0;
    return Promise.all(uniq.map(function (u) {
      return new Promise(function (res) {
        var img = new Image();
        var finish = function () {
          done++;
          var bar = $('loader-bar');
          if (bar) bar.style.width = Math.round(done / uniq.length * 100) + '%';
          res();
        };
        img.onload = finish;
        img.onerror = finish;
        img.src = u;
      });
    }));
  }

  function loadSettings() {
    try {
      var s = JSON.parse(localStorage.getItem(KEY.settings) || 'null');
      if (s) {
        settings.sound = s.sound !== false;
        settings.bgm = s.bgm !== false;
        settings.speed = (typeof s.speed === 'number' ? s.speed : 24);
      }
    } catch (e) { /* ignore */ }
    syncSoundButton();
  }

  function saveSettings() {
    try { localStorage.setItem(KEY.settings, JSON.stringify(settings)); } catch (e) {}
    syncSoundButton();
  }

  function syncSoundButton() {
    var b = $('btn-bgm');
    var on = settings.bgm || settings.sound;
    if (b) {
      b.textContent = on ? '♪' : '✕';
      b.classList.toggle('off', !on);
      b.setAttribute('aria-label', on ? '소리 끄기' : '소리 켜기');
    }
    var t = $('title-sound');
    if (t) t.textContent = on ? '소리 · 켜짐' : '소리 · 꺼짐';
  }

  /* ---------------- dust ---------------- */
  function buildDust() {
    var box = $('dust');
    if (!box) return;
    for (var i = 0; i < 16; i++) {
      var s = document.createElement('span');
      s.className = 'mote';
      s.style.left = (Math.random() * 100).toFixed(1) + '%';
      s.style.top = (Math.random() * 100).toFixed(1) + '%';
      s.style.animationDuration = (14 + Math.random() * 16).toFixed(1) + 's';
      s.style.animationDelay = (-Math.random() * 24).toFixed(1) + 's';
      s.style.opacity = (0.12 + Math.random() * 0.42).toFixed(2);
      box.appendChild(s);
    }
  }

  /* ---------------- title ---------------- */
  function readyTitle() {
    var cont = $('btn-continue');
    if (cont) cont.disabled = !hasAnySave();
    updateGalleryCount();
  }

  function hasAnySave() {
    try {
      if (localStorage.getItem(KEY.auto)) return true;
      for (var i = 1; i <= 3; i++) if (localStorage.getItem(KEY.slot + i)) return true;
    } catch (e) {}
    return false;
  }

  function showTitle() {
    ended = false;
    if (window.VNAudio) VNAudio.setRain(false);
    document.body.classList.remove('is-ending');
    stopAuto();
    setSkip(false);
    document.body.classList.add('is-title');
    $('title-screen').classList.add('on');
    $('ending-screen').classList.remove('on');
    closeModal();
    VNAudio.setMood('title');
    readyTitle();
  }

  function startNew() {
    VNAudio.unlock();
    VNAudio.setRain(false);
    rainState = false;
    document.body.classList.remove('is-ending');
    document.body.classList.remove('is-title');
    $('title-screen').classList.remove('on');
    $('ending-screen').classList.remove('on');
    history = [];
    state = newState();
    ended = false;
    hideChar(true);
    updateHud();
    goNode(meta.start);
  }

  function continueGame() {
    VNAudio.unlock();
    document.body.classList.remove('is-ending');
    var raw = localStorage.getItem(KEY.auto);
    if (!raw) {
      var best = null, bestTs = 0;
      for (var i = 1; i <= 3; i++) {
        var s = readSlot(KEY.slot + i);
        if (s && s.ts > bestTs) { best = s; bestTs = s.ts; }
      }
      if (!best) return;
      raw = JSON.stringify(best);
    }
    var data;
    try { data = JSON.parse(raw); } catch (e) { return; }
    if (!data || !nodes[data.node]) return;
    document.body.classList.remove('is-title');
    $('title-screen').classList.remove('on');
    $('ending-screen').classList.remove('on');
    loadData(data);
  }

  /* ---------------- stage ---------------- */
  function setBg(key) {
    if (!key || !ASSETS.bg[key]) return;
    document.body.dataset.bg = key;
    var frontEl = $(bgFront === 'A' ? 'bgA' : 'bgB');
    var backEl = $(bgFront === 'A' ? 'bgB' : 'bgA');
    if (frontEl.dataset.key === key) return;
    backEl.style.backgroundImage = 'url("' + ASSETS.bg[key] + '")';
    backEl.dataset.key = key;
    backEl.classList.add('on');
    frontEl.classList.remove('on');
    bgFront = bgFront === 'A' ? 'B' : 'A';
  }

  var chars = { main: null, side: null };

  function setChar(slot, id, expr) {
    var set = ASSETS.char[id];
    if (!set) return;
    var use = set[expr] ? expr : 'base';
    var el = slot === 'main' ? $('charMain') : $('charSide');
    chars[slot] = { id: id, expr: use };
    if (el.getAttribute('src') !== set[use]) {
      el.src = set[use];
      el.alt = meta.heroines[id] ? meta.heroines[id].name : '';
    }
    el.dataset.who = id;
    el.classList.add('on');
    syncLayer();
  }

  function clearChar(slot) {
    var el = slot === 'main' ? $('charMain') : $('charSide');
    chars[slot] = null;
    el.classList.remove('on');
    el.classList.remove('dim');
    syncLayer();
  }

  function syncLayer() {
    var layer = $('char-layer');
    if (!layer) return;
    var both = !!(chars.main && chars.side);
    layer.classList.toggle('two', both);
    $('stage').classList.toggle('has-char', !!(chars.main || chars.side));
  }

  function markSpeaker(spk) {
    [['main', $('charMain')], ['side', $('charSide')]].forEach(function (pair) {
      var slot = chars[pair[0]];
      if (!slot) return;
      pair[1].classList.toggle('dim', !!spk && slot.id !== spk);
    });
  }

  /* 노드의 캐릭터 지시를 적용한다. 화자가 무대에 없으면 주역으로 세운다. */
  function applyChars(n, spk) {
    if (n.hide) { clearChar('main'); clearChar('side'); }
    if (n.hide2) clearChar('side');
    if (n.show) {
      if (chars.side && chars.side.id === n.show.id) clearChar('side');
      setChar('main', n.show.id, n.show.expr);
    }
    if (n.show2 && !(chars.main && chars.main.id === n.show2.id)) {
      setChar('side', n.show2.id, n.show2.expr);
    }

    if (spk && n.e) {
      if (chars.main && chars.main.id === spk) setChar('main', spk, n.e);
      else if (chars.side && chars.side.id === spk) setChar('side', spk, n.e);
    }
    if (spk && !(chars.main && chars.main.id === spk) && !(chars.side && chars.side.id === spk)) {
      setChar('main', spk, n.e || 'base');
    }
    markSpeaker(spk);
  }

  function hideChar(instant) {
    ['charMain', 'charSide'].forEach(function (id) {
      var el = $(id);
      el.classList.remove('on');
      el.classList.remove('dim');
      if (instant) el.removeAttribute('src');
    });
    chars = { main: null, side: null };
    syncLayer();
  }

  function showChapterCard(text) {
    var card = $('chapter-card');
    if (!card) return;
    card.textContent = text;
    card.classList.remove('on');
    void card.offsetWidth;
    card.classList.add('on');
    VNAudio.sfx('open');
  }

  /* ---------------- flow ---------------- */
  function goNode(id, restore) {
    var guard = 0;
    while (true) {
      if (guard++ > 600) { console.warn('node chain too long at', id); return; }
      var n = nodes[id];
      if (!n) {
        console.warn('missing node', id);
        return;
      }
      state.node = id;

      if (!restore) {
        if (n.ch && n.ch !== state.chapter) {
          state.chapter = n.ch;
          updateHud();
          showChapterCard(n.ch);
        }
        if (n.bg) setBg(n.bg);
        if (n.bgm) VNAudio.setMood(n.bgm);
        if (typeof n.rain !== 'undefined') { rainState = !!n.rain; VNAudio.setRain(rainState); }
        if (n.hide) hideChar();
        else {
          if (n.hide2) clearChar('side');
          if (n.show) setChar('main', n.show.id, n.show.expr);
          if (n.show2) setChar('side', n.show2.id, n.show2.expr);
        }
      }

      if (n.branch) { id = resolveBranch(n); continue; }
      if (n.ending && !n.text) { return showEnding(n.ending); }
      if (!n.text && !n.choices && n.next) { id = n.next; continue; }

      autosave();
      render(n);
      return;
    }
  }

  function applyEff(eff) {
    if (!eff) return;
    var toast = [];
    if (eff.seoyun) { state.aff.seoyun += eff.seoyun; toast.push(['seoyun', eff.seoyun]); }
    if (eff.haram) { state.aff.haram += eff.haram; toast.push(['haram', eff.haram]); }
    if (eff.flag) state.flags[eff.flag] = true;
    if (toast.length) {
      updateHud();
      toast.forEach(function (t) { floatAff(t[0], t[1]); });
      VNAudio.sfx('heart');
    }
  }

  function resolveBranch(n) {
    for (var i = 0; i < n.branch.length; i++) {
      var b = n.branch[i];
      if (!b.if || testCond(b.if)) return b.next;
    }
    return n.branch[n.branch.length - 1].next;
  }

  function testCond(c) {
    if (!c) return true;
    if (c.flag && !state.flags[c.flag]) return false;
    if (c.noflag && state.flags[c.noflag]) return false;
    if (c.flag2 && !state.flags[c.flag2]) return false;
    if (c.affMin) {
      for (var k in c.affMin) if ((state.aff[k] || 0) < c.affMin[k]) return false;
    }
    if (c.affMax) {
      for (var k2 in c.affMax) if ((state.aff[k2] || 0) > c.affMax[k2]) return false;
    }
    return true;
  }

  function whoKey(who) {
    if (!who) return null;
    if (who.indexOf('서윤') >= 0) return 'seoyun';
    if (who.indexOf('하람') >= 0) return 'haram';
    if (who === '나') return 'me';
    return 'other';
  }

  function render(n) {
    choiceOpen = false;
    var box = $('choices');
    box.innerHTML = '';
    box.classList.remove('on');

    var nameEl = $('namebox');
    var key = whoKey(n.who);
    if (n.who) {
      nameEl.classList.add('on');
      $('name').textContent = n.who;
      nameEl.dataset.who = key || 'other';
    } else {
      nameEl.classList.remove('on');
      $('name').textContent = '';
    }

    $('dialogue').classList.toggle('narration', !n.who);

    applyChars(n, key === 'seoyun' || key === 'haram' ? key : null);

    if (n.text) {
      history.push({ who: n.who || '', text: n.text });
      if (history.length > 500) history.shift();
      autosave();
    }

    typeText(n.text || '', function () {
      if (n.choices) showChoices(n.choices);
      else if (n.ending) $('next-ind').classList.add('hot');
      if (autoOn) scheduleAuto(n);
    });

    $('next-ind').classList.remove('hot');
    $('next-ind').classList.remove('done');
  }

  function typeText(text, done) {
    clearInterval(typingTimer);
    typingTimer = null;
    fullText = text;
    charIndex = 0;
    afterTyping = done;
    var el = $('text');

    if (settings.speed <= 0 || skipOn) {
      el.textContent = text;
      charIndex = text.length;
      afterTyping = null;
      $('next-ind').classList.add('done');
      if (done) done();
      return;
    }
    el.textContent = '';
    typingTimer = setInterval(function () {
      charIndex++;
      if (charIndex % 3 === 0 && charIndex % 9 !== 0) VNAudio.sfx('blip');
      el.textContent = fullText.slice(0, charIndex);
      if (charIndex >= fullText.length) finishTyping();
    }, settings.speed);
  }

  function finishTyping() {
    clearInterval(typingTimer);
    typingTimer = null;
    $('text').textContent = fullText;
    charIndex = fullText.length;
    $('next-ind').classList.add('done');
    var cb = afterTyping;
    afterTyping = null;
    if (cb) cb();
  }

  function showChoices(list) {
    choiceOpen = true;
    stopAuto();
    var box = $('choices');
    box.innerHTML = '';
    var shown = 0;
    list.forEach(function (c) {
      if (c.when && !testCond(c.when)) return;
      var i = shown++;
      var b = document.createElement('button');
      b.className = 'choice';
      b.type = 'button';
      b.style.animationDelay = (i * 70) + 'ms';
      b.innerHTML = '<span class="num">' + (i + 1) + '</span><span class="txt"></span>';
      b.querySelector('.txt').textContent = c.t;
      b.addEventListener('click', function (ev) {
        ev.stopPropagation();
        if (!choiceOpen) return;
        choiceOpen = false;
        VNAudio.sfx('select');
        box.classList.remove('on');
        if (c.eff) applyEff(c.eff);
        if (c.flag) state.flags[c.flag] = true;
        box.innerHTML = '';
        goNode(c.next);
      });
      box.appendChild(b);
    });
    box.classList.add('on');
  }

  function advance() {
    if (modalOpen || ended) return;
    if (document.body.classList.contains('is-title')) return;
    if (typingTimer) { finishTyping(); return; }
    if (choiceOpen) return;
    var n = nodes[state.node];
    if (!n) return;
    if (n.ending) { showEnding(n.ending); return; }
    if (n.next) { VNAudio.sfx('advance'); goNode(n.next); }
  }

  /* ---------------- auto / skip ---------------- */
  function scheduleAuto(n) {
    stopAuto();
    if (!autoOn || choiceOpen || ended || n.ending) return;
    var delay = 1200 + Math.min(2200, (fullText.length || 0) * 42);
    autoTimer = setTimeout(function () {
      if (autoOn && !modalOpen && !choiceOpen) advance();
    }, delay);
  }

  function stopAuto() {
    if (autoTimer) { clearTimeout(autoTimer); autoTimer = null; }
  }

  function setAuto(on) {
    autoOn = on;
    var b = $('btn-auto');
    if (b) b.classList.toggle('on', on);
    if (on) {
      if (skipOn) setSkip(false);
      if (!typingTimer && !choiceOpen) {
        var n = nodes[state.node];
        if (n && n.next) advance();
        else scheduleAuto(n || {});
      }
    } else {
      stopAuto();
    }
  }

  var skipTimer = null;

  function setSkip(on) {
    skipOn = on;
    var b = $('btn-skip');
    if (b) b.classList.toggle('on', on);
    if (skipTimer) { clearTimeout(skipTimer); skipTimer = null; }
    if (on) {
      if (autoOn) setAuto(false);
      tickSkip();
    }
  }

  function tickSkip() {
    if (!skipOn) return;
    var n = nodes[state.node];
    if (modalOpen || ended) { setSkip(false); return; }
    if (n && n.choices) { setSkip(false); return; }
    if (typingTimer) { finishTyping(); }
    if (n && n.ending) { setSkip(false); return; }
    advance();
    skipTimer = setTimeout(tickSkip, 70);
  }

  /* ---------------- HUD ---------------- */
  function updateHud() {
    var chip = $('chapter-chip');
    if (chip) {
      var ch = state.chapter || '프롤로그';
      chip.textContent = window.innerWidth < 520 ? ch.split(' · ')[0] : ch;
    }
    ['seoyun', 'haram'].forEach(function (k) {
      var host = document.querySelector('.aff[data-k="' + k + '"]');
      if (!host) return;
      var bar = host.querySelector('.bar > i');
      var num = host.querySelector('.num');
      var v = state.aff[k] || 0;
      var max = meta ? meta.affMax || 18 : 18;
      if (bar) bar.style.width = Math.min(100, Math.round(v / max * 100)) + '%';
      if (num) num.textContent = v;
    });
  }

  function floatAff(who, delta) {
    var host = document.querySelector('.aff[data-k="' + who + '"]');
    if (!host) return;
    var s = document.createElement('span');
    s.className = 'float';
    s.textContent = '+' + delta;
    host.appendChild(s);
    setTimeout(function () { s.remove(); }, 1000);
  }

  /* ---------------- save / load ---------------- */
  function snapshot() {
    return {
      v: 1,
      node: state.node,
      aff: state.aff,
      flags: state.flags,
      chapter: state.chapter,
      bg: document.body.dataset.bg || 'office_day',
      rain: rainState,
      chars: { main: chars.main, side: chars.side },
      history: history.slice(-60),
      ts: Date.now()
    };
  }

  function autosave() {
    try { localStorage.setItem(KEY.auto, JSON.stringify(snapshot())); } catch (e) {}
  }

  function readSlot(k) {
    try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch (e) { return null; }
  }

  function loadData(data) {
    if (!data || !nodes[data.node]) return;
    state = newState();
    state.node = data.node;
    state.aff = {
      seoyun: (data.aff && data.aff.seoyun) || 0,
      haram: (data.aff && data.aff.haram) || 0
    };
    state.flags = data.flags || {};
    state.chapter = data.chapter || '';
    history = data.history || [];
    ended = false;
    hideChar(true);
    if (data.bg) setBg(data.bg);
    if (data.rain) VNAudio.setRain(true);
    if (data.chars) {
      if (data.chars.main) setChar('main', data.chars.main.id, data.chars.main.expr);
      if (data.chars.side) setChar('side', data.chars.side.id, data.chars.side.expr);
    }
    updateHud();
    closeModal();
    var n = nodes[data.node];
    if (n.ending && !n.text) { showEnding(n.ending); return; }
    goNode(data.node, true);
  }

  function slotLabel(i) { return i === 0 ? '자동 저장' : 'SLOT ' + i; }

  function renderSlots(mode) {
    var html = '<div class="slots">';
    for (var i = 0; i <= 3; i++) {
      var key = i === 0 ? KEY.auto : KEY.slot + i;
      var d = readSlot(key);
      html += '<div class="slot" data-i="' + i + '">';
      html += '<div class="slot-head"><b>' + slotLabel(i) + '</b>';
      html += '<span class="slot-time">' + (d ? fmtDate(d.ts) : '비어 있음') + '</span></div>';
      html += '<div class="slot-body">' + (d ? esc(d.chapter || '') + ' · ' + esc(preview(d)) : '—') + '</div>';
      html += '<div class="slot-btns">';
      if (mode === 'save' && i > 0) html += '<button class="mini" data-act="save">저장</button>';
      if (d) html += '<button class="mini" data-act="load">불러오기</button>';
      if (d && mode === 'save' && i > 0) html += '<button class="mini ghost" data-act="del">삭제</button>';
      html += '</div></div>';
    }
    html += '</div>';
    return html;
  }

  function preview(d) {
    var h = (d.history || []).slice().reverse();
    for (var i = 0; i < h.length; i++) {
      if (h[i].text) {
        var t = h[i].text.replace(/\n/g, ' ');
        return t.length > 40 ? t.slice(0, 40) + '…' : t;
      }
    }
    return '—';
  }

  function fmtDate(ts) {
    var d = new Date(ts);
    var p = function (n) { return n < 10 ? '0' + n : '' + n; };
    return (d.getMonth() + 1) + '/' + d.getDate() + ' ' + p(d.getHours()) + ':' + p(d.getMinutes());
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  function openSave(mode) {
    if (ended) return;
    modalOpen = true;
    stopAuto();
    VNAudio.sfx('open');
    $('modal-title').textContent = mode === 'save' ? '저장' : '불러오기';
    $('modal-body').innerHTML = renderSlots(mode);
    $('modal').classList.add('on');
    $('modal-body').querySelectorAll('.slot').forEach(function (row) {
      row.addEventListener('click', function (ev) {
        var act = ev.target.getAttribute && ev.target.getAttribute('data-act');
        if (!act) return;
        var idx = parseInt(row.getAttribute('data-i'), 10);
        var key = idx === 0 ? KEY.auto : KEY.slot + idx;
        if (act === 'save') {
          try { localStorage.setItem(key, JSON.stringify(snapshot())); } catch (e) {}
          VNAudio.sfx('select');
          openSave(mode);
        } else if (act === 'load') {
          var d = readSlot(key);
          if (d) { VNAudio.sfx('select'); modalOpen = false; $('modal').classList.remove('on'); loadData(d); }
        } else if (act === 'del') {
          try { localStorage.removeItem(key); } catch (e) {}
          openSave(mode);
        }
      });
    });
  }

  function openLog() {
    modalOpen = true;
    stopAuto();
    VNAudio.sfx('open');
    var rows = history.slice(-160).map(function (h) {
      return '<div class="log-row' + (h.who ? '' : ' nar') + '">' +
        (h.who ? '<span class="log-who" data-who="' + (whoKey(h.who) || '') + '">' + esc(h.who) + '</span>' : '') +
        '<span class="log-txt">' + esc(h.text) + '</span></div>';
    }).join('');
    $('modal-title').textContent = '백로그';
    $('modal-body').innerHTML = '<div class="log">' + (rows || '<p class="muted">아직 대사가 없습니다.</p>') + '</div>';
    $('modal').classList.add('on');
    var log = $('modal-body').querySelector('.log');
    if (log) log.scrollTop = log.scrollHeight;
  }

  function openSettings() {
    modalOpen = true;
    stopAuto();
    VNAudio.sfx('open');
    var speeds = [[44, '느리게'], [24, '보통'], [10, '빠르게'], [0, '즉시']];
    var html = '<div class="setting"><span>글자 속도</span><div class="seg">';
    speeds.forEach(function (s) {
      html += '<button class="seg-btn' + (settings.speed === s[0] ? ' on' : '') + '" data-speed="' + s[0] + '">' + s[1] + '</button>';
    });
    html += '</div></div>';
    html += '<div class="setting"><span>배경음</span><div class="seg"><button class="seg-btn' +
      (settings.bgm ? ' on' : '') + '" data-bgm="on">켜짐</button><button class="seg-btn' +
      (!settings.bgm ? ' on' : '') + '" data-bgm="off">꺼짐</button></div></div>';
    html += '<div class="setting"><span>효과음</span><div class="seg"><button class="seg-btn' +
      (settings.sound ? ' on' : '') + '" data-sound="on">켜짐</button><button class="seg-btn' +
      (!settings.sound ? ' on' : '') + '" data-sound="off">꺼짐</button></div></div>';
    html += '<p class="muted small">진행은 자동으로 저장됩니다. 선택지에서 멈추고, 엔딩까지 갈 수 있어요.</p>';
    html += '<div class="row"><button class="mini ghost" data-act="load">불러오기</button><button class="mini ghost" data-act="title">타이틀로 돌아가기</button></div>';
    $('modal-title').textContent = '설정';
    $('modal-body').innerHTML = html;
    $('modal').classList.add('on');
  }

  function closeModal() {
    modalOpen = false;
    $('modal').classList.remove('on');
  }

  /* ---------------- endings ---------------- */
  function unlocked() {
    try { return JSON.parse(localStorage.getItem(KEY.endings) || '{}'); } catch (e) { return {}; }
  }

  function showEnding(id) {
    ended = true;
    document.body.classList.add('is-ending');
    stopAuto();
    setSkip(false);
    var e = meta.endings[id];
    if (!e) { console.warn('unknown ending', id); return; }
    var u = unlocked();
    var isNew = !u[id];
    u[id] = u[id] || new Date().toISOString();
    try { localStorage.setItem(KEY.endings, JSON.stringify(u)); } catch (err) {}
    VNAudio.setMood('warm');
    VNAudio.sfx('chime');

    var total = Object.keys(meta.endings).length;
    var got = Object.keys(unlocked()).length;
    var screen = $('ending-screen');
    screen.innerHTML =
      '<div class="ending-inner">' +
      '<div class="ending-label">' + e.label + (isNew ? ' · NEW' : '') + '</div>' +
      '<div class="ending-no">ENDING ' + e.no + '</div>' +
      '<h2>' + esc(e.title) + '</h2>' +
      '<p class="ending-desc">' + esc(e.desc) + '</p>' +
      '<p class="ending-progress">엔딩 도감 ' + got + ' / ' + total + '</p>' +
      '<div class="ending-btns">' +
      '<button class="btn" data-act="gallery">엔딩 도감</button>' +
      '<button class="btn ghost" data-act="title">타이틀로</button>' +
      '</div></div>';
    screen.classList.add('on');
    screen.querySelector('[data-act="gallery"]').addEventListener('click', function () { openGallery(); });
    screen.querySelector('[data-act="title"]').addEventListener('click', function () {
      screen.classList.remove('on');
      showTitle();
    });
    try { localStorage.removeItem(KEY.auto); } catch (e2) {}
  }

  function openGallery() {
    modalOpen = true;
    VNAudio.sfx('open');
    var u = unlocked();
    var html = '<div class="gallery">';
    Object.keys(meta.endings).forEach(function (k) {
      var e = meta.endings[k];
      var has = !!u[k];
      html += '<div class="g-card' + (has ? ' got' : ' locked') + '">' +
        '<div class="g-no">' + e.no + '</div>' +
        '<div class="g-label">' + (has ? e.label : 'LOCKED') + '</div>' +
        '<h4>' + (has ? esc(e.title) : '？？？') + '</h4>' +
        '<p>' + (has ? esc(e.desc) : '아직 만나지 못한 결말입니다.') + '</p>' +
        '</div>';
    });
    html += '</div>';
    $('modal-title').textContent = '엔딩 도감 ' + Object.keys(u).length + ' / ' + Object.keys(meta.endings).length;
    $('modal-body').innerHTML = html;
    $('modal').classList.add('on');
  }

  function updateGalleryCount() {
    var el = $('gallery-count');
    if (!el || !meta) return;
    el.textContent = Object.keys(unlocked()).length + ' / ' + Object.keys(meta.endings).length;
  }

  /* ---------------- input ---------------- */
  function bindGlobal() {
    $('stage').addEventListener('click', function (ev) {
      if (ev.target.closest('#topbar, #hud, #choices, #modal, #title-screen, #ending-screen')) return;
      if (ev.target.closest('button')) return;
      advance();
    });

    document.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape') { closeModal(); return; }
      if (modalOpen) return;
      if (choiceOpen && /^[1-9]$/.test(ev.key)) {
        var cbtns = document.querySelectorAll('#choices .choice');
        var cb = cbtns[parseInt(ev.key, 10) - 1];
        if (cb) { cb.click(); return; }
      }
      if (document.body.classList.contains('is-title')) {
        if (ev.key === 'Enter') startNew();
        return;
      }
      if (ev.key === ' ' || ev.key === 'Enter' || ev.key === 'ArrowRight') {
        ev.preventDefault();
        advance();
      } else if (ev.key === 'l' || ev.key === 'L') {
        openLog();
      } else if (ev.key === 'a' || ev.key === 'A') {
        setAuto(!autoOn);
      } else if (ev.key === 's' || ev.key === 'S') {
        setSkip(!skipOn);
      }
    });

    $('btn-log').addEventListener('click', function (e) { e.stopPropagation(); openLog(); });
    $('btn-save').addEventListener('click', function (e) { e.stopPropagation(); openSave('save'); });
    $('btn-load').addEventListener('click', function (e) { e.stopPropagation(); openSave('load'); });
    $('btn-menu').addEventListener('click', function (e) { e.stopPropagation(); openSettings(); });
    $('btn-auto').addEventListener('click', function (e) { e.stopPropagation(); VNAudio.unlock(); setAuto(!autoOn); });
    $('btn-skip').addEventListener('click', function (e) { e.stopPropagation(); VNAudio.unlock(); setSkip(!skipOn); });
    $('btn-bgm').addEventListener('click', function (e) {
      e.stopPropagation();
      var on = !(settings.bgm || settings.sound);
      settings.bgm = on && settings.bgm ? true : on;
      settings.sound = on;
      if (!on) settings.bgm = false;
      saveSettings();
      VNAudio.setBgm(settings.bgm);
      VNAudio.setSfx(settings.sound);
      if (on) VNAudio.sfx('select');
    });

    $('modal-body').addEventListener('click', function (ev) {
      var t = ev.target.closest('[data-speed],[data-sound],[data-bgm],[data-act]');
      if (!t) return;
      if (t.dataset.speed !== undefined && t.dataset.speed !== '') {
        settings.speed = parseInt(t.dataset.speed, 10);
        saveSettings();
        openSettings();
      } else if (t.dataset.bgm) {
        settings.bgm = t.dataset.bgm === 'on';
        saveSettings();
        VNAudio.setBgm(settings.bgm);
        openSettings();
      } else if (t.dataset.sound) {
        settings.sound = t.dataset.sound === 'on';
        saveSettings();
        VNAudio.setSfx(settings.sound);
        if (settings.sound) VNAudio.sfx('select');
        openSettings();
      } else if (t.dataset.act === 'title') {
        modalOpen = false;
        $('modal').classList.remove('on');
        autosave();
        showTitle();
      } else if (t.dataset.act === 'load') {
        $('modal').classList.remove('on');
        openSave('load');
      }
    });

    $('modal-close').addEventListener('click', closeModal);
    $('modal').addEventListener('click', function (e) {
      if (e.target === $('modal')) closeModal();
    });

    $('btn-start').addEventListener('click', function (e) {
      e.stopPropagation();
      startNew();
    });
    $('btn-continue').addEventListener('click', function (e) {
      e.stopPropagation();
      continueGame();
    });
    $('btn-gallery').addEventListener('click', function (e) {
      e.stopPropagation();
      VNAudio.sfx('open');
      openGallery();
    });
    $('title-sound').addEventListener('click', function (e) {
      e.stopPropagation();
      var on = !(settings.bgm || settings.sound);
      settings.bgm = on;
      settings.sound = on;
      saveSettings();
      VNAudio.unlock();
      VNAudio.setBgm(on);
      VNAudio.setSfx(on);
      if (on) VNAudio.sfx('select');
    });

    document.addEventListener('gesturestart', function (e) { e.preventDefault(); });
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) stopAuto();
    });
  }

  document.addEventListener('DOMContentLoaded', init);
})();
