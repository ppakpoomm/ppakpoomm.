const DATA_BASE = '../data';

const STATUS_LABELS = {
  award_winner: 'ได้รางวัล — เข้าร่วม',
  declined: 'ไม่เข้าร่วม',
  exhibitor: 'ออกนิทรรศการ',
  unknown: 'ไม่ระบุ',
};

const PARTICIPATION_LABELS = {
  trophy_and_exhibition: 'โล่ + นิทรรศการ',
  trophy_only: 'โล่เท่านั้น',
};

async function loadData() {
  const [responses, summary, plan] = await Promise.all([
    fetch(`${DATA_BASE}/rsvp_responses.json`).then(r => r.json()),
    fetch(`${DATA_BASE}/summary.json`).then(r => r.json()),
    fetch(`${DATA_BASE}/tracking_plan.json`).then(r => r.json()),
  ]);
  return { responses, summary, plan };
}

function renderAlert(summary) {
  const el = document.getElementById('alertBanner');
  const pending = summary.pending_awardees;
  el.innerHTML = `
    <strong>⚠️ ต้องติดตามด่วน:</strong>
    อปท. ได้รับรางวัล 59 แห่ง — ตอบรับแล้ว <strong>${summary.awardees_responded}</strong> แห่ง
    (${summary.response_rate_pct}%) · ยังไม่ตอบรับ <strong>${pending}</strong> แห่ง
  `;
}

function renderMetrics(summary) {
  const el = document.getElementById('metrics');
  el.innerHTML = `
    <div class="metric-card gold"><div class="metric-value">59</div><div class="metric-label">อปท. ได้รับรางวัล</div></div>
    <div class="metric-card success"><div class="metric-value">${summary.awardees_responded}</div><div class="metric-label">ตอบรับแล้ว</div></div>
    <div class="metric-card danger"><div class="metric-value">${summary.pending_awardees}</div><div class="metric-label">ยังไม่ตอบรับ</div></div>
    <div class="metric-card warning"><div class="metric-value">${summary.by_status.declined || 0}</div><div class="metric-label">ไม่เข้าร่วม</div></div>
    <div class="metric-card"><div class="metric-value">${summary.by_status.exhibitor || 0}</div><div class="metric-label">ออกนิทรรศการ</div></div>
    <div class="metric-card"><div class="metric-value">${summary.accommodation_requests}</div><div class="metric-label">ขอที่พัก อบจ.กระบี่</div></div>
  `;
}

function renderCharts(summary) {
  const statusData = summary.by_status;
  new Chart(document.getElementById('statusChart'), {
    type: 'doughnut',
    data: {
      labels: ['เข้าร่วม (ได้รางวัล)', 'ไม่เข้าร่วม', 'ออกนิทรรศการ'],
      datasets: [{
        data: [statusData.award_winner || 0, statusData.declined || 0, statusData.exhibitor || 0],
        backgroundColor: ['#27ae60', '#e74c3c', '#2980b9'],
      }],
    },
    options: { plugins: { legend: { position: 'bottom' } } },
  });

  const partData = summary.by_participation;
  new Chart(document.getElementById('participationChart'), {
    type: 'pie',
    data: {
      labels: ['โล่ + นิทรรศการ', 'โล่เท่านั้น'],
      datasets: [{
        data: [partData.trophy_and_exhibition || 0, partData.trophy_only || 0],
        backgroundColor: ['#8e44ad', '#f39c12'],
      }],
    },
    options: { plugins: { legend: { position: 'bottom' } } },
  });

  const travelData = summary.by_travel_mode;
  new Chart(document.getElementById('travelChart'), {
    type: 'bar',
    data: {
      labels: Object.keys(travelData),
      datasets: [{
        label: 'จำนวน',
        data: Object.values(travelData),
        backgroundColor: '#2980b9',
      }],
    },
    options: { plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } },
  });
}

function renderPhases(plan) {
  const el = document.getElementById('trackingPhases');
  el.innerHTML = plan.phases.map(p => `
    <div class="phase-card">
      <h3>${p.priority}. ${p.name}</h3>
      <ul>${p.actions.map(a => `<li>${a}</li>`).join('')}</ul>
    </div>
  `).join('');
}

function statusBadge(status) {
  const cls = status === 'award_winner' ? 'badge-winner' : status === 'declined' ? 'badge-declined' : 'badge-exhibitor';
  return `<span class="badge ${cls}">${STATUS_LABELS[status] || status}</span>`;
}

function participationBadge(mode) {
  if (!mode) return '—';
  const cls = mode === 'trophy_and_exhibition' ? 'badge-exhibit' : 'badge-trophy';
  return `<span class="badge ${cls}">${PARTICIPATION_LABELS[mode] || mode}</span>`;
}

function renderTable(responses) {
  const tbody = document.querySelector('#rsvpTable tbody');
  const searchInput = document.getElementById('searchInput');
  const statusFilter = document.getElementById('statusFilter');
  const participationFilter = document.getElementById('participationFilter');

  function filter() {
    const q = searchInput.value.toLowerCase();
    const status = statusFilter.value;
    const participation = participationFilter.value;

    tbody.innerHTML = responses
      .filter(r => {
        if (status && r.status !== status) return false;
        if (participation && r.participation_mode !== participation) return false;
        if (q && !(`${r.province || ''} ${r.org_name || ''} ${r.coordinator || ''}`.toLowerCase().includes(q))) return false;
        return true;
      })
      .map(r => `
        <tr>
          <td>${r.id}</td>
          <td>${statusBadge(r.status)}</td>
          <td>${r.province || '—'}</td>
          <td>${r.org_name || r.declined_org || '—'}</td>
          <td>${r.unit_type || '—'}</td>
          <td>${participationBadge(r.participation_mode)}</td>
          <td>${r.coordinator || r.declined_contact || '—'}<br><small>${r.coordinator_phone || ''}</small></td>
          <td><small>${r.travel_mode || '—'}</small></td>
          <td>${r.accommodation_request ? '<span class="badge badge-yes">ขอที่พัก</span>' : '—'}</td>
        </tr>
      `).join('');
  }

  searchInput.addEventListener('input', filter);
  statusFilter.addEventListener('change', filter);
  participationFilter.addEventListener('change', filter);
  filter();
}

function renderPending(summary, responses) {
  document.getElementById('respondedCount').textContent = summary.awardees_responded;
  document.getElementById('pendingCount').textContent = summary.pending_awardees;

  const respondedCodes = new Set(
    responses.filter(r => r.status === 'award_winner' && r.org_code).map(r => r.org_code)
  );

  const box = document.getElementById('pendingBox');
  box.innerHTML = `
    <p><strong>อัตราตอบรับ:</strong> ${summary.response_rate_pct}% (${summary.awardees_responded}/59)</p>
    <p><strong>รหัส อปท. ที่ตอบรับแล้ว:</strong> ${[...respondedCodes].sort((a,b) => +a - +b).join(', ') || '—'}</p>
    <p><strong>แนวทางติดตาม:</strong></p>
    <ol>
      <li>โทร/Line ติดตาม อปท. ที่ยังไม่กรอกฟอร์มตอบรับ (${summary.pending_awardees} แห่ง)</li>
      <li>ประสาน สสจ. ทุกจังหวัดผ่านหนังสือเชิญ (01-05 ใน Drive)</li>
      <li>อัปเดต Spreadsheet หลังได้รับคำตอบ — รัน <code>make sync</code></li>
      <li>สรุปที่พักและเดินทางส่ง อบจ.กระบี่ ก่อนวันประชุม</li>
    </ol>
  `;
}

async function init() {
  try {
    const { responses, summary, plan } = await loadData();
    renderAlert(summary);
    renderMetrics(summary);
    renderCharts(summary);
    renderPhases(plan);
    renderTable(responses);
    renderPending(summary, responses);
  } catch (err) {
    document.querySelector('main').innerHTML =
      `<p style="color:red;padding:2rem">ไม่สามารถโหลดข้อมูลได้: ${err.message}<br>รัน <code>python3 -m http.server 8080</code> จาก root โปรเจกต์</p>`;
  }
}

init();
