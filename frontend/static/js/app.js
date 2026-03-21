const API = '/api';

// ─── Tab Navigation ───────────────────────────────────────────
document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    tab.classList.add('active');
    document.getElementById(`tab-${tab.dataset.tab}`).classList.add('active');
  });
});

// ─── Modal Helpers ────────────────────────────────────────────
function openModal(id) { document.getElementById(id).classList.remove('hidden'); }
function closeModal(id) { document.getElementById(id).classList.add('hidden'); }

document.querySelectorAll('.modal-overlay').forEach(overlay => {
  overlay.addEventListener('click', e => {
    if (e.target === overlay) overlay.classList.add('hidden');
  });
});

// ─── Toast ────────────────────────────────────────────────────
function showToast(msg, type = 'success') {
  const toast = document.getElementById('toast');
  toast.textContent = msg;
  toast.className = `toast ${type}`;
  setTimeout(() => toast.classList.add('hidden'), 3000);
}

// ─── API Helpers ──────────────────────────────────────────────
async function apiFetch(path, options = {}) {
  const res = await fetch(API + path, {
    headers: { 'Content-Type': 'application/json' },
    ...options
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Request failed');
  }
  return res.json();
}

// ─── APPOINTMENTS ─────────────────────────────────────────────
async function loadAppointments() {
  const list = document.getElementById('appointments-list');
  list.innerHTML = '<p class="empty-state">Loading...</p>';
  try {
    const data = await apiFetch('/appointments/');
    if (!data.length) {
      list.innerHTML = '<p class="empty-state">No appointments yet. Create one!</p>';
      return;
    }
    list.innerHTML = data.map(a => `
      <div class="card">
        <span class="status-badge status-${a.status}">${a.status}</span>
        <div class="card-title">
          ${a.patient.first_name} ${a.patient.last_name}
          <span style="font-size:0.8rem;color:var(--muted)"> → Dr. ${a.doctor.last_name}</span>
        </div>
        <div class="card-meta">
          📅 ${formatDate(a.appointment_date)}<br/>
          🩺 ${a.doctor.specialization}<br/>
          ${a.notes ? `📝 ${a.notes}` : ''}
        </div>
        <div class="card-actions">
          <select onchange="changeStatus(${a.id}, this.value)" style="font-size:0.8rem;padding:0.3rem 0.5rem;border-radius:6px;border:1px solid var(--border)">
            <option value="scheduled" ${a.status==='scheduled'?'selected':''}>Scheduled</option>
            <option value="completed" ${a.status==='completed'?'selected':''}>Completed</option>
            <option value="cancelled" ${a.status==='cancelled'?'selected':''}>Cancelled</option>
          </select>
          <button class="btn btn-danger" onclick="deleteAppointment(${a.id})">Delete</button>
        </div>
      </div>
    `).join('');
  } catch (e) {
    list.innerHTML = `<p class="empty-state">Error loading appointments: ${e.message}</p>`;
  }
}

async function createAppointment() {
  const body = {
    patient_id: parseInt(document.getElementById('appt-patient-id').value),
    doctor_id: parseInt(document.getElementById('appt-doctor-id').value),
    appointment_date: document.getElementById('appt-date').value,
    notes: document.getElementById('appt-notes').value || null
  };
  try {
    await apiFetch('/appointments/', { method: 'POST', body: JSON.stringify(body) });
    closeModal('modal-add-appointment');
    showToast('Appointment created!');
    loadAppointments();
  } catch (e) { showToast(e.message, 'error'); }
}

async function changeStatus(id, status) {
  try {
    await apiFetch(`/appointments/${id}`, { method: 'PUT', body: JSON.stringify({ status }) });
    showToast('Status updated!');
    loadAppointments();
  } catch (e) { showToast(e.message, 'error'); }
}

async function deleteAppointment(id) {
  if (!confirm('Delete this appointment?')) return;
  try {
    await apiFetch(`/appointments/${id}`, { method: 'DELETE' });
    showToast('Appointment deleted');
    loadAppointments();
  } catch (e) { showToast(e.message, 'error'); }
}

// ─── PATIENTS ─────────────────────────────────────────────────
async function loadPatients() {
  const list = document.getElementById('patients-list');
  list.innerHTML = '<p class="empty-state">Loading...</p>';
  try {
    const data = await apiFetch('/patients/');
    if (!data.length) {
      list.innerHTML = '<p class="empty-state">No patients yet.</p>';
      return;
    }
    list.innerHTML = data.map(p => `
      <div class="card">
        <div class="card-title">${p.first_name} ${p.last_name}</div>
        <div class="card-meta">
          ✉️ ${p.email}<br/>
          ${p.phone ? `📞 ${p.phone}<br/>` : ''}
          ${p.date_of_birth ? `🎂 ${p.date_of_birth}` : ''}
        </div>
        <div class="card-meta" style="margin-top:0.4rem;font-size:0.75rem;color:var(--muted)">ID: ${p.id}</div>
        <div class="card-actions">
          <button class="btn btn-danger" onclick="deletePatient(${p.id})">Delete</button>
        </div>
      </div>
    `).join('');
  } catch (e) {
    list.innerHTML = `<p class="empty-state">Error: ${e.message}</p>`;
  }
}

async function createPatient() {
  const body = {
    first_name: document.getElementById('pat-first').value,
    last_name: document.getElementById('pat-last').value,
    email: document.getElementById('pat-email').value,
    phone: document.getElementById('pat-phone').value || null,
    date_of_birth: document.getElementById('pat-dob').value || null,
  };
  try {
    await apiFetch('/patients/', { method: 'POST', body: JSON.stringify(body) });
    closeModal('modal-add-patient');
    showToast('Patient added!');
    loadPatients();
  } catch (e) { showToast(e.message, 'error'); }
}

async function deletePatient(id) {
  if (!confirm('Delete this patient?')) return;
  try {
    await apiFetch(`/patients/${id}`, { method: 'DELETE' });
    showToast('Patient deleted');
    loadPatients();
  } catch (e) { showToast(e.message, 'error'); }
}

// ─── DOCTORS ──────────────────────────────────────────────────
async function loadDoctors() {
  const list = document.getElementById('doctors-list');
  list.innerHTML = '<p class="empty-state">Loading...</p>';
  try {
    const data = await apiFetch('/doctors/');
    if (!data.length) {
      list.innerHTML = '<p class="empty-state">No doctors yet.</p>';
      return;
    }
    list.innerHTML = data.map(d => `
      <div class="card">
        <div class="card-title">Dr. ${d.first_name} ${d.last_name}</div>
        <div class="card-meta">
          🩺 ${d.specialization}<br/>
          ✉️ ${d.email}<br/>
          ${d.phone ? `📞 ${d.phone}` : ''}
        </div>
        <div class="card-meta" style="margin-top:0.4rem;font-size:0.75rem;color:var(--muted)">ID: ${d.id}</div>
        <div class="card-actions">
          <button class="btn btn-danger" onclick="deleteDoctor(${d.id})">Delete</button>
        </div>
      </div>
    `).join('');
  } catch (e) {
    list.innerHTML = `<p class="empty-state">Error: ${e.message}</p>`;
  }
}

async function createDoctor() {
  const body = {
    first_name: document.getElementById('doc-first').value,
    last_name: document.getElementById('doc-last').value,
    specialization: document.getElementById('doc-spec').value,
    email: document.getElementById('doc-email').value,
    phone: document.getElementById('doc-phone').value || null,
  };
  try {
    await apiFetch('/doctors/', { method: 'POST', body: JSON.stringify(body) });
    closeModal('modal-add-doctor');
    showToast('Doctor added!');
    loadDoctors();
  } catch (e) { showToast(e.message, 'error'); }
}

async function deleteDoctor(id) {
  if (!confirm('Delete this doctor?')) return;
  try {
    await apiFetch(`/doctors/${id}`, { method: 'DELETE' });
    showToast('Doctor deleted');
    loadDoctors();
  } catch (e) { showToast(e.message, 'error'); }
}

// ─── Utils ────────────────────────────────────────────────────
function formatDate(str) {
  if (!str) return '—';
  const d = new Date(str);
  return isNaN(d) ? str : d.toLocaleString('en-GB', { dateStyle: 'medium', timeStyle: 'short' });
}

// ─── Init ─────────────────────────────────────────────────────
loadAppointments();
loadPatients();
loadDoctors();
