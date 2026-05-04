// Reservoice Panel — backend bağlantı katmanı
// Aynı origin'de servis edildiği için relative path yeterli.
(function () {
  const BASE = '';

  async function request(path, opts = {}) {
    const res = await fetch(BASE + path, {
      headers: { 'Content-Type': 'application/json', 'X-User-Role': window.__role || 'staff' },
      ...opts,
      body: opts.body ? JSON.stringify(opts.body) : undefined,
    });
    if (!res.ok) {
      const text = await res.text().catch(() => '');
      throw new Error(`${res.status} ${res.statusText} — ${text}`);
    }
    if (res.status === 204) return null;
    return res.json();
  }

  const api = {
    health: () => request('/api/health'),

    conversations: {
      list: (q = '') => request('/api/conversations' + (q ? `?${q}` : '')),
      stats: () => request('/api/conversations/stats'),
      get: (id) => request(`/api/conversations/${id}`),
      create: (body) => request('/api/conversations', { method: 'POST', body }),
      update: (id, body) => request(`/api/conversations/${id}`, { method: 'PATCH', body }),
      takeover: (id) => request(`/api/conversations/${id}/takeover`, { method: 'POST' }),
      remove: (id) => request(`/api/conversations/${id}`, { method: 'DELETE' }),
      messages: (id) => request(`/api/conversations/${id}/messages`),
      sendMessage: (id, body) => request(`/api/conversations/${id}/messages`, { method: 'POST', body }),
    },

    reservations: {
      list: (q = '') => request('/api/reservations' + (q ? `?${q}` : '')),
      stats: () => request('/api/reservations/stats'),
      create: (body) => request('/api/reservations', { method: 'POST', body }),
      approve: (id) => request(`/api/reservations/${id}/approve`, { method: 'POST' }),
      reject: (id) => request(`/api/reservations/${id}/reject`, { method: 'POST' }),
      remove: (id) => request(`/api/reservations/${id}`, { method: 'DELETE' }),
    },

    tickets: {
      list: (q = '') => request('/api/tickets' + (q ? `?${q}` : '')),
      stats: () => request('/api/tickets/stats'),
      create: (body) => request('/api/tickets', { method: 'POST', body }),
      update: (id, body) => request(`/api/tickets/${id}`, { method: 'PATCH', body }),
      resolve: (id) => request(`/api/tickets/${id}/resolve`, { method: 'POST' }),
      remove: (id) => request(`/api/tickets/${id}`, { method: 'DELETE' }),
    },

    hotelInfo: {
      list: () => request('/api/hotel-info'),
      get: (section) => request(`/api/hotel-info/${section}`),
      save: (section, data) => request(`/api/hotel-info/${section}`, {
        method: 'PUT', body: { section, data },
      }),
    },

    rooms: {
      list: () => request('/api/rooms'),
      create: (body) => request('/api/rooms', { method: 'POST', body }),
      remove: (id) => request(`/api/rooms/${id}`, { method: 'DELETE' }),
    },

    restaurants: {
      list: () => request('/api/restaurants'),
      create: (body) => request('/api/restaurants', { method: 'POST', body }),
      remove: (id) => request(`/api/restaurants/${id}`, { method: 'DELETE' }),
    },

    aiRules: {
      list: () => request('/api/ai-rules'),
      create: (body) => request('/api/ai-rules', { method: 'POST', body }),
      update: (id, body) => request(`/api/ai-rules/${id}`, { method: 'PATCH', body }),
      remove: (id) => request(`/api/ai-rules/${id}`, { method: 'DELETE' }),
    },

    templates: {
      list: (q = '') => request('/api/templates' + (q ? `?${q}` : '')),
      create: (body) => request('/api/templates', { method: 'POST', body }),
      remove: (id) => request(`/api/templates/${id}`, { method: 'DELETE' }),
    },

    integrations: {
      list: (q = '') => request('/api/integrations' + (q ? `?${q}` : '')),
      get: (key) => request(`/api/integrations/${key}`),
      update: (key, body) => request(`/api/integrations/${key}`, { method: 'PATCH', body }),
      test: (key) => request(`/api/integrations/${key}/test`, { method: 'POST' }),
    },

    upsell: {
      list: (q = '') => request('/api/upsell' + (q ? `?${q}` : '')),
      create: (body) => request('/api/upsell', { method: 'POST', body }),
      update: (id, body) => request(`/api/upsell/${id}`, { method: 'PATCH', body }),
      send: (id) => request(`/api/upsell/${id}/send`, { method: 'POST' }),
      dismiss: (id) => request(`/api/upsell/${id}/dismiss`, { method: 'POST' }),
      remove: (id) => request(`/api/upsell/${id}`, { method: 'DELETE' }),
    },

    campaigns: {
      list: (q = '') => request('/api/campaigns' + (q ? `?${q}` : '')),
      create: (body) => request('/api/campaigns', { method: 'POST', body }),
      publish: (id) => request(`/api/campaigns/${id}/publish`, { method: 'POST' }),
      remove: (id) => request(`/api/campaigns/${id}`, { method: 'DELETE' }),
    },

    kvkk: {
      list: () => request('/api/kvkk'),
      create: (body) => request('/api/kvkk', { method: 'POST', body }),
      remove: (id) => request(`/api/kvkk/${id}`, { method: 'DELETE' }),
    },

    aiPerformance: {
      list: () => request('/api/ai-performance'),
      summary: () => request('/api/ai-performance/summary'),
    },

    users: {
      list: () => request('/api/users'),
      create: (body) => request('/api/users', { method: 'POST', body }),
      remove: (id) => request(`/api/users/${id}`, { method: 'DELETE' }),
    },
  };

  window.api = api;

  // ── Toast yardımcıları ──
  function toast(msg, type = 'success') {
    const colors = { success: '#10b981', error: '#ef4444', info: '#3b82f6' };
    const el = document.createElement('div');
    el.style.cssText = `position:fixed;top:72px;right:24px;background:${colors[type]};color:#fff;padding:12px 20px;border-radius:10px;font-size:13px;font-weight:700;box-shadow:0 4px 16px rgba(0,0,0,0.15);z-index:9999;max-width:420px`;
    el.textContent = msg;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 3500);
  }
  window.toast = toast;

  // ── Bağlantı kontrolü ──
  api.health()
    .then((r) => console.log('[Reservoice] backend hazır:', r))
    .catch((err) => {
      console.error('[Reservoice] backend bağlanamadı:', err);
      toast('Backend bağlantısı yok — uvicorn çalışıyor mu?', 'error');
    });

  // ── Sayfa açıldığında ilgili veriyi yükle ──
  function escapeHtml(s) {
    return String(s ?? '').replace(/[&<>"']/g, (c) => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
    })[c]);
  }

  function channelBadge(ch) {
    const map = {
      whatsapp: ['ch-wa', 'WhatsApp'],
      chat: ['ch-chat', 'Web Chat'],
      phone: ['ch-phone', 'Telefon'],
      telegram: ['ch-tg', 'Telegram'],
    };
    const [cls, label] = map[ch] || ['ch-chat', ch];
    return `<span class="ch-icon ${cls}">${label}</span>`;
  }

  function statusBadge(s) {
    const map = {
      active: ['badge-green', 'Aktif — AI'],
      takeover: ['', '👋 Devralma Bekliyor'],
      done: ['badge-gray', 'Tamamlandı'],
      pending: ['badge-yellow', 'Onay Bekliyor'],
      auto_approved: ['badge-blue', 'Otomatik Onaylandı'],
      approved: ['badge-green', 'Onaylandı'],
      rejected: ['badge-red', 'Reddedildi'],
      open: ['badge-red', 'Açık'],
      in_progress: ['badge-yellow', 'İşlemde'],
      resolved: ['badge-green', 'Çözüldü'],
    };
    const [cls, label] = map[s] || ['badge-gray', s];
    const extra = s === 'takeover' ? 'style="background:#ede9fe;color:#6d28d9"' : '';
    return `<span class="badge ${cls}" ${extra}>${label}</span>`;
  }

  async function loadConversations() {
    try {
      const [list, stats] = await Promise.all([api.conversations.list(), api.conversations.stats()]);
      // Update stat cards on conversations page
      const page = document.getElementById('page-conversations');
      if (!page) return;
      const cards = page.querySelectorAll('.stat-card .svalue');
      if (cards.length >= 4) {
        cards[0].textContent = stats.total;
        cards[1].textContent = stats.automation_pct + '%';
        cards[2].textContent = stats.takeover;
        cards[3].textContent = stats.done;
      }
      const tbody = page.querySelector('#conv-tab-all tbody');
      if (!tbody) return;
      tbody.innerHTML = list.map((c) => {
        const isTakeover = c.status === 'takeover';
        const rowStyle = isTakeover ? 'cursor:pointer;background:#faf5ff' : 'cursor:pointer';
        const wait = c.waiting_minutes
          ? `<span style="font-size:12px;font-weight:700;color:${c.waiting_minutes >= 7 ? '#ef4444' : c.waiting_minutes >= 3 ? '#f59e0b' : '#10b981'}">${c.waiting_minutes} dk${c.waiting_minutes >= 7 ? ' ⚠️' : ''}</span>`
          : '<span style="font-size:12px;color:#9ca3af">—</span>';
        return `
          <tr style="${rowStyle}" data-id="${c.id}">
            <td>
              <div class="gname">${escapeHtml(c.guest_name)}</div>
              <div class="groom">${escapeHtml(c.room_type || '')} ${c.stay_dates ? '· ' + escapeHtml(c.stay_dates) : ''}</div>
            </td>
            <td>${channelBadge(c.channel)}</td>
            <td style="max-width:160px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;${isTakeover ? 'color:#7c3aed;font-weight:600' : 'color:#6b7280'}">${escapeHtml(c.last_message || '')}</td>
            <td><span style="background:${isTakeover ? '#ede9fe' : '#dbeafe'};color:${isTakeover ? '#6d28d9' : '#1e40af'};padding:2px 7px;border-radius:10px;font-size:11px;font-weight:600">${escapeHtml(c.tag || '')}</span></td>
            <td>${statusBadge(c.status)}</td>
            <td>${wait}</td>
            <td><button class="btn ${isTakeover ? '' : 'btn-secondary'} btn-sm" ${isTakeover ? 'style="background:#7c3aed;color:#fff"' : ''} onclick="event.stopPropagation();nav('${isTakeover ? 'conv-detail-takeover' : 'conv-detail'}',null)">${isTakeover ? 'Devral' : 'Aç'}</button></td>
          </tr>`;
      }).join('');
    } catch (e) {
      console.error('loadConversations:', e);
    }
  }

  async function loadReservations() {
    try {
      const list = await api.reservations.list();
      const page = document.getElementById('page-reservations');
      if (!page) return;
      const pendingTab = page.querySelector('#resv-tab-pending');
      const autoTab = page.querySelector('#resv-tab-auto');
      if (!pendingTab) return;

      const pending = list.filter((r) => r.status === 'pending');
      const auto = list.filter((r) => r.status === 'auto_approved');

      // Update tab counts
      const tabs = page.querySelectorAll('.tabs .tab .tc');
      if (tabs[0]) tabs[0].textContent = pending.length;
      if (tabs[1]) tabs[1].textContent = auto.length;

      const renderCard = (r, isPending) => `
        <div class="resv-card ${isPending ? 'review' : ''}" data-id="${r.id}">
          <div class="resv-head">
            ${channelBadge(r.channel || 'whatsapp')}
            <div>
              <div class="resv-guest">${escapeHtml(r.guest_name)}</div>
              <div class="resv-id">${escapeHtml(r.code || '')}</div>
            </div>
            <span class="badge ${isPending ? 'badge-yellow' : 'badge-blue'}" style="margin-left:auto">${isPending ? (r.review_reason ? 'Manuel Onay' : 'Onay Bekliyor') : 'Otomatik Onaylandı'}</span>
          </div>
          <div class="resv-body">
            <div><div class="rf-label">Check-in</div><div class="rf-val">${escapeHtml(r.check_in || '—')}</div></div>
            <div><div class="rf-label">Check-out</div><div class="rf-val">${escapeHtml(r.check_out || '—')}</div></div>
            <div><div class="rf-label">Oda</div><div class="rf-val">${escapeHtml(r.room_type || '—')}</div></div>
            <div><div class="rf-label">Toplam</div><div class="rf-val">₺${r.total ?? '—'}</div></div>
          </div>
          ${isPending && r.review_reason ? `<div class="alert alert-warn" style="margin:0 0 10px;padding:8px 12px;font-size:12px">${escapeHtml(r.review_reason)}</div>` : ''}
          <div class="resv-actions">
            ${isPending
              ? `<button class="btn btn-success" onclick="window.api.reservations.approve(${r.id}).then(()=>{toast('Rezervasyon onaylandı');loadReservations()})">✓ Onayla</button>
                 <button class="btn btn-danger" onclick="window.api.reservations.reject(${r.id}).then(()=>{toast('Rezervasyon reddedildi','info');loadReservations()})">✕ Reddet</button>`
              : ''}
            <button class="btn btn-secondary" onclick="nav('conv-detail',null)">Konuşmayı Gör</button>
          </div>
        </div>`;

      // Pending tab — keep alert + render cards
      pendingTab.innerHTML = `
        <div class="alert alert-warn">
          <svg width="15" height="15" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.268 16.5c-.77.833.192 2.5 1.732 2.5z"/></svg>
          <span>${pending.length} rezervasyon AI tarafından oluşturuldu, manuel onayınızı bekliyor.</span>
        </div>
        ${pending.map((r) => renderCard(r, true)).join('') || '<div class="card"><div class="card-body" style="padding:40px;text-align:center;color:#9ca3af">Bekleyen rezervasyon yok.</div></div>'}
      `;
      autoTab.innerHTML = `
        <div class="alert alert-info">
          <svg width="15" height="15" fill="none" stroke="currentColor" viewBox="0 0 24 24" style="flex-shrink:0"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          <span>Bu rezervasyonlar AI tarafından otomatik onaylandı. Bilgi amaçlı listelenmektedir.</span>
        </div>
        ${auto.map((r) => renderCard(r, false)).join('') || '<div class="card"><div class="card-body" style="padding:40px;text-align:center;color:#9ca3af">Otomatik onaylı rezervasyon yok.</div></div>'}
      `;
    } catch (e) {
      console.error('loadReservations:', e);
    }
  }

  async function loadTickets() {
    try {
      const [list, stats] = await Promise.all([api.tickets.list(), api.tickets.stats()]);
      const page = document.getElementById('page-tickets');
      if (!page) return;

      const cards = page.querySelectorAll('.stat-card .svalue');
      if (cards.length >= 4) {
        cards[0].textContent = stats.open;
        cards[1].textContent = stats.in_progress;
        cards[2].textContent = stats.resolved;
        cards[3].textContent = stats.total;
      }

      const container = page.querySelector('div[style*="flex-direction:column;gap:10px"]');
      if (!container) return;

      const priorityColor = {
        urgent: ['#fca5a5', '#ef4444', '#fee2e2'],
        high: ['#fcd34d', '#f59e0b', '#fef3c7'],
        normal: ['#e5e7eb', '#6b7280', '#f3f4f6'],
        low: ['#d1fae5', '#10b981', '#d1fae5'],
      };
      const catIcon = {
        housekeeping: '🛏️', technical: '🔧', food: '🍽️',
        climate: '❄️', noise: '🔊', internet: '🌐', other: '📦',
      };
      const priorityLabel = { urgent: 'Acil', high: 'Yüksek', normal: 'Normal', low: 'Düşük' };
      const statusLabel = { open: 'Açık', in_progress: 'İşlemde', resolved: 'Çözüldü' };

      container.innerHTML = list.map((t) => {
        const [border, accent, iconBg] = priorityColor[t.priority] || priorityColor.normal;
        const icon = catIcon[t.category] || '📦';
        return `
          <div class="ticket-card" style="background:#fff;border:1px solid ${border};border-left:4px solid ${accent};border-radius:12px;padding:16px 18px" data-id="${t.id}">
            <div class="flex items-center gap-3 mb-3">
              <div style="width:36px;height:36px;background:${iconBg};border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:17px;flex-shrink:0">${icon}</div>
              <div class="flex-1">
                <div class="flex items-center gap-2">
                  <span class="font-bold" style="font-size:14px">${escapeHtml(t.title)}</span>
                  <span class="badge badge-${t.priority === 'urgent' ? 'red' : t.priority === 'high' ? 'yellow' : 'gray'}">${priorityLabel[t.priority] || t.priority}</span>
                  <span class="badge" style="background:#fef3c7;color:#92400e">${statusLabel[t.status] || t.status}</span>
                </div>
                <div class="text-sm text-muted mt-1">${icon} ${escapeHtml(t.category || '')} · Oda ${escapeHtml(t.room || '')} · ${escapeHtml(t.guest_name || '')}</div>
              </div>
            </div>
            <div style="background:#fafafa;border-radius:8px;padding:10px 12px;font-size:13px;color:#374151;margin-bottom:12px;border:1px solid #f3f4f6">${escapeHtml(t.description || '')}</div>
            <div class="flex items-center gap-2">
              ${t.status !== 'resolved' ? `<button class="btn btn-success btn-sm" onclick="window.api.tickets.resolve(${t.id}).then(()=>{toast('Şikayet çözüldü');loadTickets()})">✓ Çözüldü</button>` : ''}
              <button class="btn btn-secondary btn-sm" onclick="nav('conv-detail',null)">Konuşmaya Git</button>
              <div class="flex-1"></div>
              <span class="text-sm text-muted">#${escapeHtml(t.code || '')}</span>
            </div>
          </div>`;
      }).join('') || '<div class="card"><div class="card-body" style="padding:40px;text-align:center;color:#9ca3af">Şikayet bulunamadı.</div></div>';
    } catch (e) {
      console.error('loadTickets:', e);
    }
  }

  async function loadAIRules() {
    try {
      const list = await api.aiRules.list();
      const page = document.getElementById('page-ai-rules');
      if (!page) return;
      const wrap = page.querySelector('.card .card-body') || page;
      const html = list.map((r) => `
        <div style="border:1px solid #e5e7eb;border-radius:10px;padding:12px 14px;margin-bottom:10px;display:flex;gap:12px;align-items:start">
          <div class="flex-1">
            <div style="font-weight:700;font-size:13px;color:#0f1629">${escapeHtml(r.name)}</div>
            <div style="font-size:12px;color:#6b7280;margin-top:4px"><strong>Tetik:</strong> ${escapeHtml(r.trigger || '')}</div>
            <div style="font-size:12px;color:#6b7280"><strong>Aksiyon:</strong> ${escapeHtml(r.action || '')}</div>
          </div>
          <label class="toggle ${r.enabled ? 'on' : ''}" onclick="window.api.aiRules.update(${r.id},{enabled:${!r.enabled}}).then(loadAIRules)"></label>
          <button class="btn btn-danger btn-sm" onclick="if(confirm('Sil?'))window.api.aiRules.remove(${r.id}).then(loadAIRules)">Sil</button>
        </div>`).join('');
      const target = page.querySelector('[data-rules-list]') ||
        (() => {
          const card = document.createElement('div');
          card.className = 'card';
          card.innerHTML = `<div class="card-body" data-rules-list></div>`;
          page.appendChild(card);
          return card.querySelector('[data-rules-list]');
        })();
      target.innerHTML = html || '<div style="padding:24px;text-align:center;color:#9ca3af">Henüz kural yok.</div>';
    } catch (e) {
      console.error('loadAIRules:', e);
    }
  }

  async function loadIntegrations() {
    try {
      const list = await api.integrations.list();
      const page = document.getElementById('page-integrations');
      if (!page) return;
      // Just update enabled toggles where data-int-key matches
      list.forEach((it) => {
        const card = page.querySelector(`[data-int-key="${it.key}"]`);
        if (card) {
          const tog = card.querySelector('.toggle');
          if (tog) tog.classList.toggle('on', it.enabled);
        }
      });
    } catch (e) {
      console.error('loadIntegrations:', e);
    }
  }

  async function loadUpsell() {
    try {
      const list = await api.upsell.list();
      const page = document.getElementById('page-upsell');
      if (!page) return;
      const stats = page.querySelectorAll('.stat-card .svalue');
      if (stats[0]) stats[0].textContent = list.length;
      const totalSent = list.reduce((s, o) => s + (o.sent_count || 0), 0);
      const totalAcc = list.reduce((s, o) => s + (o.accepted_count || 0), 0);
      const rate = totalSent ? Math.round((totalAcc / totalSent) * 100) : 0;
      if (stats[1]) stats[1].textContent = totalSent;
      if (stats[2]) stats[2].textContent = totalAcc;
      if (stats[3]) stats[3].textContent = rate + '%';
    } catch (e) {
      console.error('loadUpsell:', e);
    }
  }

  async function loadAIPerformance() {
    try {
      const summary = await api.aiPerformance.summary();
      const page = document.getElementById('page-evaluation');
      if (!page) return;
      const cards = page.querySelectorAll('.stat-card .svalue');
      if (cards[0]) cards[0].textContent = summary.automation_pct + '%';
      if (cards[1]) cards[1].textContent = summary.csat;
      if (cards[2]) cards[2].textContent = summary.handled;
      if (cards[3]) cards[3].textContent = summary.escalated;
    } catch (e) {
      console.error('loadAIPerformance:', e);
    }
  }

  // Hook into nav() to load data when page changes
  const _origNav = window.nav;
  window.nav = function (id, el) {
    if (typeof _origNav === 'function') _origNav(id, el);
    const loaders = {
      conversations: loadConversations,
      reservations: loadReservations,
      tickets: loadTickets,
      'ai-rules': loadAIRules,
      integrations: loadIntegrations,
      upsell: loadUpsell,
      evaluation: loadAIPerformance,
    };
    const fn = loaders[id];
    if (fn) fn();
  };

  // Expose for inline buttons
  window.loadConversations = loadConversations;
  window.loadReservations = loadReservations;
  window.loadTickets = loadTickets;
  window.loadAIRules = loadAIRules;
  window.loadIntegrations = loadIntegrations;
  window.loadUpsell = loadUpsell;
  window.loadAIPerformance = loadAIPerformance;

  // Initial load: conversations is the active page on boot
  document.addEventListener('DOMContentLoaded', () => {
    loadConversations();
  });
})();
