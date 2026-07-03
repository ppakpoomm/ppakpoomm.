const DATA_BASE = '../data';

async function loadData() {
  const [submissions, status, issues] = await Promise.all([
    fetch(`${DATA_BASE}/submissions_standard_2569.json`).then(r => r.json()),
    fetch(`${DATA_BASE}/status_standard_2569.json`).then(r => r.json()),
    fetch(`${DATA_BASE}/quality_issues.json`).then(r => r.json()),
  ]);
  return { submissions, status, issues };
}

function renderMetrics(status, submissions) {
  const m = status.metrics;
  const el = document.getElementById('metrics');
  el.innerHTML = `
    <div class="metric-card"><div class="metric-value">${submissions.length}</div><div class="metric-label">รายการส่งฟอร์ม</div></div>
    <div class="metric-card success"><div class="metric-value">${m.provinces_complete_both}</div><div class="metric-label">จังหวัดครบถ้วน ✅</div></div>
    <div class="metric-card warning"><div class="metric-value">${m.provinces_letter_only}</div><div class="metric-label">มีหนังสือ ไม่กรอกฟอร์ม</div></div>
    <div class="metric-card danger"><div class="metric-value">${m.provinces_form_only}</div><div class="metric-label">กรอกฟอร์ม ไม่ส่งหนังสือ</div></div>
    <div class="metric-card warning"><div class="metric-value">${m.data_quality_issues}</div><div class="metric-label">ปัญหาคุณภาพข้อมูล</div></div>
  `;
}

function renderCharts(submissions, status) {
  const m = status.metrics;
  new Chart(document.getElementById('statusChart'), {
    type: 'doughnut',
    data: {
      labels: ['ครบถ้วน', 'มีหนังสืออย่างเดียว', 'มีฟอร์มอย่างเดียว'],
      datasets: [{
        data: [m.provinces_complete_both, m.provinces_letter_only, m.provinces_form_only],
        backgroundColor: ['#27ae60', '#f39c12', '#e74c3c'],
      }],
    },
    options: { plugins: { legend: { position: 'bottom' } } },
  });

  const unitCounts = {};
  submissions.forEach(s => { unitCounts[s.unit_type] = (unitCounts[s.unit_type] || 0) + 1; });

  new Chart(document.getElementById('unitChart'), {
    type: 'bar',
    data: {
      labels: Object.keys(unitCounts),
      datasets: [{
        label: 'จำนวน',
        data: Object.values(unitCounts),
        backgroundColor: ['#27ae60', '#2980b9', '#f39c12'],
      }],
    },
    options: { plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } },
  });
}

function renderAlerts(issues) {
  const el = document.getElementById('alerts');
  el.innerHTML = '<h2 style="margin-bottom:0.8rem;color:#1a5276">⚠️ ปัญหาคุณภาพข้อมูล</h2>' +
    issues.map(i => `<div class="alert"><strong>${i.province}</strong> — ${i.org_name}: ${i.issue}</div>`).join('');
}

function unitBadge(type) {
  const cls = type === 'ระดับพื้นฐาน' ? 'badge-basic' : type === 'ระดับสูง' ? 'badge-high' : 'badge-admin';
  return `<span class="badge ${cls}">${type}</span>`;
}

function renderTable(submissions) {
  const tbody = document.querySelector('#submissionsTable tbody');
  const searchInput = document.getElementById('searchInput');
  const unitFilter = document.getElementById('unitFilter');
  const issueFilter = document.getElementById('issueFilter');

  function filter() {
    const q = searchInput.value.toLowerCase();
    const unit = unitFilter.value;
    const issueOnly = issueFilter.value === 'issue';

    tbody.innerHTML = submissions
      .filter(s => {
        if (unit && s.unit_type !== unit) return false;
        if (issueOnly && !s.has_issue && !s.notes) return false;
        if (q && !(`${s.province} ${s.org_name} ${s.coordinator}`.toLowerCase().includes(q))) return false;
        return true;
      })
      .map(s => `
        <tr class="${s.has_issue ? 'has-issue' : ''}">
          <td>${s.id}</td>
          <td>${s.province}</td>
          <td>${unitBadge(s.unit_type)}</td>
          <td>${s.org_name}</td>
          <td>${s.coordinator}</td>
          <td>${s.score ?? '—'}</td>
          <td>${s.notes ?? ''}</td>
        </tr>
      `).join('');
  }

  searchInput.addEventListener('input', filter);
  unitFilter.addEventListener('change', filter);
  issueFilter.addEventListener('change', filter);
  filter();
}

function renderFollowup(status) {
  const el = document.getElementById('followupGrid');
  const letterCards = status.provinces_letter_only.map(p =>
    `<div class="followup-card letter-only">📄 ${p}<br><small>มีหนังสือ ยังไม่กรอกฟอร์ม</small></div>`
  ).join('');
  const formCards = status.provinces_form_only.map(p =>
    `<div class="followup-card form-only">📝 ${p}<br><small>กรอกฟอร์มแล้ว ยังไม่ส่งหนังสือ</small></div>`
  ).join('');
  el.innerHTML = letterCards + formCards;
}

async function init() {
  try {
    const { submissions, status, issues } = await loadData();
    renderMetrics(status, submissions);
    renderCharts(submissions, status);
    renderAlerts(issues);
    renderTable(submissions);
    renderFollowup(status);
  } catch (err) {
    document.querySelector('main').innerHTML = `<p style="color:red;padding:2rem">ไม่สามารถโหลดข้อมูลได้: ${err.message}<br>กรุณารันผ่าน local server: <code>python -m http.server 8080</code></p>`;
  }
}

init();
