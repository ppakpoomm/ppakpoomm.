const DATA_BASE = '../data';

const STATUS_LABELS = {
  pending: 'ยังไม่ตอบรับ',
  responded: 'ตอบรับแล้ว',
  declined: 'ไม่เข้าร่วม',
  unknown: 'ไม่ระบุ',
};

const PARTICIPATION_LABELS = {
  trophy_and_exhibition: 'โล่ + นิทรรศการ',
  trophy_only: 'โล่เท่านั้น',
};

async function loadData() {
  const [awardees, pending, responded, summary, plan] = await Promise.all([
    fetch(`${DATA_BASE}/awardees.json`).then(r => r.json()),
    fetch(`${DATA_BASE}/pending_followup.json`).then(r => r.json()),
    fetch(`${DATA_BASE}/responded.json`).then(r => r.json()),
    fetch(`${DATA_BASE}/summary.json`).then(r => r.json()),
    fetch(`${DATA_BASE}/tracking_plan.json`).then(r => r.json()),
  ]);
  return { awardees, pending, responded, summary, plan };
}

function renderAlert(summary) {
  const el = document.getElementById('alertBanner');
  el.innerHTML = `
    <strong>⚠️ ต้องติดตามด่วน:</strong>
    อปท. ได้รับรางวัล <strong>${summary.total_awardees}</strong> แห่ง — ตอบรับแล้ว <strong>${summary.responded_count}</strong> แห่ง
    (${summary.response_rate_pct}%) · ยังไม่ตอบรับ <strong>${summary.pending_count}</strong> แห่ง
  `;
}

function renderMetrics(summary) {
  const el = document.getElementById('metrics');
  el.innerHTML = `
    <div class="metric-card gold"><div class="metric-value">${summary.total_awardees}</div><div class="metric-label">อปท. ได้รับรางวัล</div></div>
    <div class="metric-card success"><div class="metric-value">${summary.responded_count}</div><div class="metric-label">ตอบรับแล้ว</div></div>
    <div class="metric-card danger"><div class="metric-value">${summary.pending_count}</div><div class="metric-label">ยังไม่ตอบรับ</div></div>
    <div class="metric-card warning"><div class="metric-value">${summary.declined_count}</div><div class="metric-label">ไม่เข้าร่วม</div></div>
    <div class="metric-card"><div class="metric-value">${summary.with_phone}</div><div class="metric-label">มีเบอร์โทร</div></div>
    <div class="metric-card"><div class="metric-value">${summary.with_email}</div><div class="metric-label">มีอีเมล</div></div>
  `;
}

function renderCharts(summary) {
  const statusData = summary.by_form_status_label || {};
  const pending = summary.pending_count || 0;
  const responded = summary.responded_count || 0;
  const declined = summary.declined_count || 0;

  new Chart(document.getElementById('statusChart'), {
    type: 'doughnut',
    data: {
      labels: ['ตอบรับแล้ว', 'ยังไม่ตอบรับ', 'ไม่เข้าร่วม'],
      datasets: [{
        data: [responded, pending, declined],
        backgroundColor: ['#27ae60', '#e74c3c', '#95a5a6'],
      }],
    },
    options: { plugins: { legend: { position: 'bottom' } } },
  });

  const partData = summary.by_participation_mode || {};
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

  const awardData = summary.by_award_type || {};
  new Chart(document.getElementById('travelChart'), {
    type: 'bar',
    data: {
      labels: ['พื้นฐาน', 'อำนวยการดีเด่น', 'ระดับสูง'],
      datasets: [{
        label: 'จำนวน',
        data: [
          awardData['ประเภทหน่วยปฏิบัติการแพทย์ ระดับพื้นฐาน'] || 0,
          awardData['ประเภทหน่วยปฏิบัติการอำนวยการดีเด่น'] || 0,
          awardData['ประเภทหน่วยปฏิบัติการแพทย์ ระดับสูง (นอกโรงพยาบาล)'] || 0,
        ],
        backgroundColor: '#2980b9',
      }],
    },
    options: {
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true } },
    },
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

function statusBadge(status, label) {
  const cls = status === 'responded' ? 'badge-winner'
    : status === 'declined' ? 'badge-declined'
    : status === 'pending' ? 'badge-declined' : 'badge-exhibitor';
  return `<span class="badge ${cls}">${label || STATUS_LABELS[status] || status}</span>`;
}

function participationBadge(mode) {
  if (!mode) return '—';
  const cls = mode === 'trophy_and_exhibition' ? 'badge-exhibit' : 'badge-trophy';
  return `<span class="badge ${cls}">${PARTICIPATION_LABELS[mode] || mode}</span>`;
}

function renderTable(awardees) {
  const tbody = document.querySelector('#rsvpTable tbody');
  const searchInput = document.getElementById('searchInput');
  const statusFilter = document.getElementById('statusFilter');
  const participationFilter = document.getElementById('participationFilter');

  function filter() {
    const q = searchInput.value.toLowerCase();
    const status = statusFilter.value;
    const participation = participationFilter.value;

    tbody.innerHTML = awardees
      .filter(r => {
        if (status && r.form_status !== status) return false;
        if (participation && r.participation_mode !== participation) return false;
        if (q && !(`${r.province || ''} ${r.org_name || ''} ${r.coordinator || ''}`.toLowerCase().includes(q))) return false;
        return true;
      })
      .map(r => `
        <tr>
          <td>${r.code || '—'}</td>
          <td>${statusBadge(r.form_status, r.form_status_label)}</td>
          <td>${r.province || '—'}</td>
          <td>${r.org_name || '—'}</td>
          <td><small>${(r.award_type || '—').replace('ประเภทหน่วยปฏิบัติการ', '')}</small></td>
          <td>${participationBadge(r.participation_mode)}</td>
          <td>${r.coordinator || '—'}<br><small>${r.phone || ''}</small></td>
          <td><small>${r.follow_up_by || '—'}</small></td>
          <td>${r.email ? `<small>${r.email}</small>` : '—'}</td>
        </tr>
      `).join('');
  }

  searchInput.addEventListener('input', filter);
  statusFilter.addEventListener('change', filter);
  participationFilter.addEventListener('change', filter);
  filter();
}

function renderPending(summary, pending) {
  document.getElementById('totalCount').textContent = summary.total_awardees;
  document.getElementById('respondedCount').textContent = summary.responded_count;
  document.getElementById('pendingCount').textContent = summary.pending_count;

  const byProvince = summary.by_province_pending || {};
  const provinceList = Object.entries(byProvince)
    .sort((a, b) => a[0].localeCompare(b[0], 'th'))
    .map(([p, c]) => `<li>${p} (${c})</li>`)
    .join('');

  const urgent = pending.filter(p => !p.email).slice(0, 8);
  const urgentList = urgent.map(p =>
    `<li>#${p.code} ${p.org_name} — ${p.phone || 'ไม่มีโทร'}</li>`
  ).join('');

  const box = document.getElementById('pendingBox');
  box.innerHTML = `
    <p><strong>อัตราตอบรับ:</strong> ${summary.response_rate_pct}% (${summary.responded_count}/${summary.total_awardees})</p>
    <p><strong>จังหวัดที่ยังไม่ตอบรับ (${Object.keys(byProvince).length} จังหวัด):</strong></p>
    <ul class="province-list">${provinceList}</ul>
    <p><strong>เร่งด่วน — ไม่มีอีเมล (${pending.filter(p => !p.email).length} แห่ง):</strong></p>
    <ul>${urgentList || '<li>—</li>'}</ul>
    <p><strong>แนวทางติดตาม:</strong></p>
    <ol>
      <li>โทรผู้ประสานงานในรายการด้านล่าง (${summary.pending_count} แห่ง)</li>
      <li>ส่งอีเมล saraban / ผู้ประสานงานที่มีในระบบ</li>
      <li>ประสาน สสจ. ทุกจังหวัดผ่านหนังสือเชิญ (01-05 ใน Drive)</li>
      <li>อัปเดต Spreadsheet หลังได้รับคำตอบ — รัน <code>make sync</code></li>
    </ol>
    <div class="table-wrap">
      <table id="pendingTable">
        <thead>
          <tr>
            <th>#</th><th>จังหวัด</th><th>ชื่อ อปท.</th><th>ผู้ประสานงาน</th><th>โทร</th><th>อีเมล</th>
          </tr>
        </thead>
        <tbody>
          ${pending.map(p => `
            <tr>
              <td>${p.code || '—'}</td>
              <td>${p.province || '—'}</td>
              <td>${p.org_name || '—'}</td>
              <td>${p.coordinator || '—'}</td>
              <td>${p.phone || '—'}</td>
              <td>${p.email || '<span class="badge badge-declined">ไม่มี</span>'}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    </div>
  `;
}

async function init() {
  try {
    const { awardees, pending, summary, plan } = await loadData();
    renderAlert(summary);
    renderMetrics(summary);
    renderCharts(summary);
    renderPhases(plan);
    renderTable(awardees);
    renderPending(summary, pending);
  } catch (err) {
    document.querySelector('main').innerHTML =
      `<p style="color:red;padding:2rem">ไม่สามารถโหลดข้อมูลได้: ${err.message}<br>รัน <code>python3 -m http.server 8080</code> จาก root โปรเจกต์</p>`;
  }
}

init();
