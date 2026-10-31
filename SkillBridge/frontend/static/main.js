// Main UI interactions for premium frontend
function toast(message, type = 'info', timeout = 3500) {
  const root = document.getElementById('toast-root');
  if (!root) return;
  const el = document.createElement('div');
  el.className = 'toast text-sm mb-3 flex items-start gap-3';
  el.innerHTML = `<div class="w-2 h-8 rounded-full ${type==='success'?'bg-emerald-400':type==='warn'?'bg-amber-400':'bg-sb-primaryFrom'}"></div><div class="flex-1">${message}</div>`;
  root.appendChild(el);
  setTimeout(()=>{ el.style.opacity=0; el.style.transform='translateY(-6px)'; setTimeout(()=>el.remove(),400)}, timeout);
}

function persistTheme(isDark){
  if(isDark) document.documentElement.classList.add('dark'); else document.documentElement.classList.remove('dark');
  localStorage.setItem('sb-theme', isDark ? 'dark' : 'light');
}

function initTheme(){
  const stored = localStorage.getItem('sb-theme');
  if(stored) persistTheme(stored==='dark');
  else persistTheme(true);
}

function initHamburger(){
  const hb = document.getElementById('hamburger');
  if(!hb) return;
  hb.addEventListener('click', ()=>{
    const sidebar = document.getElementById('sidebar');
    if(sidebar.style.display==='block') sidebar.style.display='none'; else sidebar.style.display='block';
  });
}

function initModeToggle(){
  const btn = document.getElementById('modeToggle');
  if(!btn) return;
  btn.addEventListener('click', ()=>{
    const isDark = document.documentElement.classList.toggle('dark');
    persistTheme(isDark);
    toast(`Switched to ${isDark?'Dark':'Light'} mode`, 'success');
  });
}

function initMatchCards(){
  document.querySelectorAll('.match-card').forEach(card=>{
    card.addEventListener('click', (e)=>{
      if(e.target.closest('.invite-btn')) return;
      card.classList.toggle('match-expanded');
      card.classList.toggle('match-collapsed');
    })
  });
  document.querySelectorAll('.invite-btn').forEach(b=>b.addEventListener('click', (e)=>{ e.stopPropagation(); toast('Invite sent', 'success'); }));
}

function initSkillTags(){
  document.querySelectorAll('.skill-chip').forEach(chip=>{
    chip.addEventListener('click', ()=>chip.classList.toggle('tag-selected'));
  });
}

function initCharts(){
  // Radar chart placeholder
  const radar = document.getElementById('radarChart');
  if(radar){
    new Chart(radar.getContext('2d'), {
      type: 'radar',
      data: {
        labels: ['UI','Backend','ML','Data','Product','Research'],
        datasets: [{label:'Your Skills', data:[6,4,7,5,6,4], backgroundColor:'rgba(79,70,229,0.25)', borderColor:'#4f46e5', pointBackgroundColor:'#7c3aed'}]
      }, options:{plugins:{legend:{display:false}}}
    });
  }

  const trend = document.getElementById('trendChart');
  if(trend){ new Chart(trend.getContext('2d'), {type:'line', data:{labels:['Jan','Feb','Mar','Apr','May','Jun'], datasets:[{label:'Demand',data:[20,30,45,40,60,80], borderColor:'#06b6d4', backgroundColor:'rgba(6,182,212,0.12)'}]}}); }

  const trust = document.getElementById('trustChart');
  if(trust){ new Chart(trust.getContext('2d'), {type:'bar', data:{labels:['Dec','Jan','Feb','Mar','Apr'], datasets:[{label:'Trust Score',data:[60,65,70,72,78], backgroundColor:'#7c3aed'}]}}); }
}

function escapeHtml(value) {
  const node = document.createElement('div');
  node.textContent = value;
  return node.innerHTML;
}

function careerList(items, emptyText) {
  return items.length ? items.map(item => `<span class="chip">${escapeHtml(item)}</span>`).join(' ') : `<span class="text-sm text-emerald-300">${emptyText}</span>`;
}

function initCareerForm() {
  const form = document.getElementById('careerForm');
  if (!form) return;
  const results = document.getElementById('careerResults');
  const empty = document.getElementById('careerEmpty');
  const button = document.getElementById('careerSubmit');
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    button.disabled = true; button.textContent = 'Finding your options...';
    try {
      const response = await fetch('/api/career-recommendations', { method: 'POST', body: new FormData(form) });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || 'Unable to generate recommendations.');
      results.innerHTML = data.recommendations.map((role, index) => `
        <article class="card-glass p-5 career-card">
          <div class="flex justify-between gap-4"><div><p class="text-xs uppercase tracking-wider text-cyan-300">#${index + 1} career target</p><h2 class="mt-1 text-xl font-bold">${escapeHtml(role.title)}</h2></div><span class="h-fit chip text-cyan-200">${role.match_score}% fit</span></div>
          <p class="mt-3 text-sm text-gray-300">${escapeHtml(role.description)}</p>
          <div class="mt-4"><h3 class="text-sm font-semibold">Skills needed</h3><div class="mt-2 flex flex-wrap gap-2">${careerList(role.skills_needed, '')}</div></div>
          <div class="mt-4"><h3 class="text-sm font-semibold text-amber-300">Learn next</h3><div class="mt-2 flex flex-wrap gap-2">${careerList(role.learn, 'You already cover the core listed skills.')}</div></div>
        </article>`).join('');
      empty.classList.add('hidden'); results.classList.remove('hidden');
    } catch (error) { toast(error.message, 'warn'); }
    finally { button.disabled = false; button.textContent = 'Find my career options'; }
  });
}

async function fetchSkills(){
  try{ const res = await fetch('/skills'); if(!res.ok) return []; return await res.json(); }catch(e){ return []; }
}

document.addEventListener('DOMContentLoaded', async ()=>{
  initTheme(); initHamburger(); initModeToggle(); initCharts(); initMatchCards(); initSkillTags();
  initCareerForm();

  // wire profile and project forms with graceful UI
  const skills = await fetchSkills();
  const skillsList = document.getElementById('skillsList');
  if(skillsList){ skills.slice(0,20).forEach(s=>{ const el = document.createElement('button'); el.type='button'; el.className='skill-chip chip mr-2 mb-2 btn-animate'; el.textContent=s.name; el.dataset.id=s.id; skillsList.appendChild(el); }); }

  const projectSkillContainer = document.getElementById('projectSkills');
  if(projectSkillContainer){ skills.slice(0,20).forEach(s=>{ const el = document.createElement('button'); el.type='button'; el.className='skill-chip chip mr-2 mb-2 btn-animate'; el.textContent=s.name; el.dataset.id=s.id; projectSkillContainer.appendChild(el); }); }

  const profileForm = document.getElementById('profileForm');
  if(profileForm){ profileForm.addEventListener('submit', async (e)=>{ e.preventDefault(); toast('Profile saved', 'success'); }); }

  const projectForm = document.getElementById('projectForm');
  if(projectForm){ projectForm.addEventListener('submit', async (e)=>{ e.preventDefault(); toast('Project created', 'success'); }); }

});

// expose for debugging
window.SB = { toast };
