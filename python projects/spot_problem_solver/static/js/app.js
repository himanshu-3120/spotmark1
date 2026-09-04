/* ==========================================================================
   SPOT PROBLEM SOLVER — Main Application Engine (SPA Router & Client JS)
   ========================================================================== */

let currentState = {
  activePage: 'home',
  problems: [],
  solutions: [],
  challenges: [],
  teams: [],
  stats: {},
  currentStep: 1,
  selectedTechFilter: '',
  activeAIModalTab: 'analyzer'
};

// Lucide Icon Initializer
function refreshIcons() {
  if (window.lucide) {
    window.lucide.createIcons();
  }
}

// Toast System
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast-item border-l-4 ${
    type === 'success' ? 'border-emerald-500' : type === 'warning' ? 'border-amber-500' : 'border-brand-600'
  }`;

  toast.innerHTML = `
    <div class="w-8 h-8 rounded-full ${
      type === 'success' ? 'bg-emerald-100 text-emerald-600' : 'bg-brand-100 text-brand-600'
    } flex items-center justify-center font-bold text-sm">
      ${type === 'success' ? '✓' : 'i'}
    </div>
    <div class="flex-grow">
      <p class="font-bold text-slate-800 text-xs">${message}</p>
    </div>
  `;

  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// Router
function navigateTo(page, params = {}) {
  currentState.activePage = page;
  
  // Hide all page sections
  document.querySelectorAll('.page-view').forEach(sec => sec.classList.add('hidden'));

  // Show target page
  const target = document.getElementById(`page-${page}`);
  if (target) {
    target.classList.remove('hidden');
  }

  // Update Nav Button Active State
  document.querySelectorAll('.nav-btn').forEach(btn => {
    if (btn.getAttribute('data-page') === page) {
      btn.classList.add('text-brand-600', 'bg-brand-50', 'font-bold');
    } else {
      btn.classList.remove('text-brand-600', 'bg-brand-50', 'font-bold');
    }
  });

  window.scrollTo({ top: 0, behavior: 'smooth' });

  // Load specific page data
  if (page === 'home') loadHomePageData();
  else if (page === 'discover') loadDiscoverProblems();
  else if (page === 'solutions') loadSolutionsMarketplace();
  else if (page === 'challenges') loadChallenges();
  else if (page === 'teams') loadTeams();
  else if (page === 'leaderboard') loadLeaderboard();
  else if (page === 'success-stories') loadSuccessStories();
  else if (page === 'admin') loadAdminDashboard();
  else if (page === 'profile') loadUserProfile(params.userId || 2);
  else if (page === 'problem-detail') loadProblemDetail(params.problemId || 1);

  refreshIcons();
}

// Mobile Menu Toggle
function toggleMobileMenu() {
  const menu = document.getElementById('mobile-menu');
  menu.classList.toggle('hidden');
}

// Notification Dropdown Toggle
function toggleNotificationDropdown() {
  const dropdown = document.getElementById('notif-dropdown');
  dropdown.classList.toggle('hidden');
}

function loadNotifications() {
  fetch('/api/notifications')
    .then(r => r.json())
    .then(notes => {
      const container = document.getElementById('notif-list');
      if (!container) return;
      container.innerHTML = notes.map(n => `
        <div class="px-4 py-3 hover:bg-slate-50 cursor-pointer">
          <span class="font-bold text-slate-800">${n.title}</span>
          <p class="text-slate-500 mt-0.5">${n.message}</p>
        </div>
      `).join('');
    });
}

function markAllNotificationsRead() {
  document.getElementById('nav-notif-badge')?.classList.add('hidden');
  toggleNotificationDropdown();
  showToast('All notifications marked as read', 'success');
}

// ==========================================================================
// HOMEPAGE LOGIC
// ==========================================================================
function loadHomePageData() {
  // Fetch stats
  fetch('/api/stats')
    .then(r => r.json())
    .then(stats => {
      currentState.stats = stats;
      renderStatsGrid(stats);
    });

  // Fetch featured problems
  fetch('/api/problems?sort=most_supported')
    .then(r => r.json())
    .then(problems => {
      const grid = document.getElementById('home-featured-problems-grid');
      if (!grid) return;
      grid.innerHTML = problems.slice(0, 3).map(p => renderProblemCard(p)).join('');
      refreshIcons();
    });
}

function renderStatsGrid(stats) {
  const grid = document.getElementById('homepage-stats-grid');
  if (!grid) return;

  grid.innerHTML = Object.keys(stats).map(key => {
    const s = stats[key];
    return `
      <div class="p-4 rounded-2xl bg-slate-50 border border-slate-100 hover:border-brand-300 transition-colors">
        <span class="font-heading text-2xl sm:text-3xl font-extrabold text-brand-600 block">${s.value}</span>
        <span class="text-xs font-medium text-slate-600 mt-1 block">${s.label}</span>
      </div>
    `;
  }).join('');
}

// ==========================================================================
// DISCOVER PROBLEMS MARKETPLACE
// ==========================================================================
function loadDiscoverProblems() {
  filterProblems();
}

function filterProblems() {
  const search = document.getElementById('problem-search-input')?.value || '';
  const category = document.getElementById('filter-category')?.value || '';
  const difficulty = document.getElementById('filter-difficulty')?.value || '';
  const status = document.getElementById('filter-status')?.value || '';
  const sort = document.getElementById('filter-sort')?.value || 'newest';

  const params = new URLSearchParams({ search, category, difficulty, status, sort });

  fetch(`/api/problems?${params.toString()}`)
    .then(r => r.json())
    .then(problems => {
      currentState.problems = problems;
      const grid = document.getElementById('discover-problems-grid');
      if (!grid) return;

      if (problems.length === 0) {
        grid.innerHTML = `
          <div class="col-span-full py-16 text-center text-slate-500 space-y-3">
            <i data-lucide="search-x" class="w-12 h-12 mx-auto text-slate-400"></i>
            <h3 class="font-bold text-lg text-slate-700">No problems found</h3>
            <p class="text-xs">Try adjusting your category filters or search keywords.</p>
          </div>
        `;
      } else {
        grid.innerHTML = problems.map(p => renderProblemCard(p)).join('');
      }
      refreshIcons();
    });
}

function resetProblemFilters() {
  if (document.getElementById('problem-search-input')) document.getElementById('problem-search-input').value = '';
  if (document.getElementById('filter-category')) document.getElementById('filter-category').value = '';
  if (document.getElementById('filter-difficulty')) document.getElementById('filter-difficulty').value = '';
  if (document.getElementById('filter-status')) document.getElementById('filter-status').value = '';
  if (document.getElementById('filter-sort')) document.getElementById('filter-sort').value = 'newest';
  filterProblems();
}

function renderProblemCard(p) {
  const diffClass = p.difficulty === 'Easy' ? 'badge-difficulty-easy' :
                    p.difficulty === 'Medium' ? 'badge-difficulty-medium' :
                    p.difficulty === 'Hard' ? 'badge-difficulty-hard' : 'badge-difficulty-expert';

  return `
    <div class="glass-card rounded-3xl p-6 flex flex-col justify-between space-y-4 group">
      <div class="space-y-3">
        
        <!-- Category & Difficulty Header -->
        <div class="flex items-center justify-between gap-2 text-xs">
          <span class="px-2.5 py-1 rounded-full badge-category font-bold">${p.category}</span>
          <span class="px-2.5 py-1 rounded-full ${diffClass} font-semibold">${p.difficulty}</span>
        </div>

        <!-- Problem Title -->
        <h3 class="font-bold text-slate-900 text-lg group-hover:text-brand-600 transition-colors line-clamp-2">
          ${p.title}
        </h3>

        <!-- Organization & Location -->
        <div class="flex items-center gap-2 text-xs text-slate-500">
          <img src="${p.org_logo || 'https://images.unsplash.com/photo-1541872703-74c5e44368f9?auto=format&fit=crop&w=150&q=80'}" class="w-5 h-5 rounded-full object-cover" />
          <span class="font-medium text-slate-700 truncate">${p.org_name}</span>
          <span>•</span>
          <span class="truncate">${p.location}</span>
        </div>

        <!-- Description Excerpt -->
        <p class="text-xs text-slate-600 line-clamp-3 leading-relaxed">
          ${p.description}
        </p>

        <!-- Tech Tags -->
        <div class="flex flex-wrap gap-1.5 pt-1">
          ${(p.required_tech || []).slice(0, 3).map(t => `<span class="px-2 py-0.5 rounded-md bg-slate-100 text-slate-600 text-[10px] font-semibold">${t}</span>`).join('')}
        </div>

      </div>

      <!-- Card Footer -->
      <div class="pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
        <div class="flex items-center gap-3">
          <span class="flex items-center gap-1"><i data-lucide="lightbulb" class="w-3.5 h-3.5 text-amber-500"></i> ${p.solutions_count || 0} solutions</span>
          <span class="flex items-center gap-1"><i data-lucide="heart" class="w-3.5 h-3.5 text-rose-500"></i> ${p.supporters_count || 0}</span>
        </div>
        <button onclick="navigateTo('problem-detail', { problemId: ${p.id} })" class="font-bold text-brand-600 hover:text-brand-700 flex items-center gap-1">
          View Problem <i data-lucide="chevron-right" class="w-4 h-4"></i>
        </button>
      </div>

    </div>
  `;
}

// ==========================================================================
// PROBLEM DETAILS PAGE
// ==========================================================================
function loadProblemDetail(problemId) {
  fetch(`/api/problems/${problemId}`)
    .then(r => r.json())
    .then(data => {
      const p = data.problem;
      const solutions = data.solutions;
      const related = data.related;

      const container = document.getElementById('problem-detail-container');
      if (!container) return;

      container.innerHTML = `
        <div class="space-y-8">
          
          <!-- Back Link -->
          <button onclick="navigateTo('discover')" class="text-xs font-semibold text-slate-500 hover:text-brand-600 flex items-center gap-1">
            <i data-lucide="arrow-left" class="w-4 h-4"></i> Back to Marketplace
          </button>

          <!-- Problem Header Banner -->
          <div class="glass-card p-8 rounded-3xl space-y-6">
            <div class="flex flex-wrap items-center justify-between gap-4">
              <div class="flex items-center gap-3">
                <span class="px-3 py-1 rounded-full badge-category font-bold text-xs">${p.category}</span>
                <span class="px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 font-bold text-xs">Status: ${p.status}</span>
                <span class="px-3 py-1 rounded-full bg-slate-100 text-slate-700 font-medium text-xs">Difficulty: ${p.difficulty}</span>
              </div>
              <span class="text-xs text-slate-500 font-medium">Deadline: <strong class="text-slate-800">${p.deadline}</strong></span>
            </div>

            <h1 class="text-3xl font-extrabold text-slate-900 leading-tight">${p.title}</h1>

            <div class="flex flex-wrap items-center justify-between gap-6 pt-4 border-t border-slate-100">
              
              <!-- Organization Info -->
              <div class="flex items-center gap-3">
                <img src="${p.org_logo}" class="w-12 h-12 rounded-xl object-cover border border-slate-200" />
                <div>
                  <h4 class="font-bold text-slate-900 text-sm">${p.org_name}</h4>
                  <p class="text-xs text-slate-500">${p.location} • Verified Organization</p>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="flex flex-wrap items-center gap-3">
                <button onclick="supportProblemAction(${p.id})" class="px-5 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold text-xs flex items-center gap-2">
                  <i data-lucide="heart" class="w-4 h-4 text-rose-500"></i> Support Problem (<span id="p-detail-support-count">${p.supporters_count}</span>)
                </button>
                <button onclick="triggerSubmitSolutionForProblem(${p.id}, '${p.title.replace(/'/g, "\\'")}')" class="px-6 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-bold text-xs shadow-md flex items-center gap-2">
                  <i data-lucide="send" class="w-4 h-4"></i> Submit Solution
                </button>
              </div>

            </div>
          </div>

          <!-- Main Content Grid: Statement & Requirements -->
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            <div class="lg:col-span-2 space-y-6">
              
              <!-- Detailed Statement -->
              <div class="glass-card p-6 rounded-3xl space-y-3">
                <h3 class="font-bold text-slate-900 text-base border-b pb-2">Detailed Problem Statement</h3>
                <p class="text-sm text-slate-700 leading-relaxed">${p.description}</p>
              </div>

              <!-- Why It Matters -->
              <div class="glass-card p-6 rounded-3xl space-y-3">
                <h3 class="font-bold text-slate-900 text-base border-b pb-2">Why This Problem Matters</h3>
                <p class="text-sm text-slate-700 leading-relaxed">${p.why_it_matters || 'No additional notes provided.'}</p>
              </div>

              <!-- Current Situation & Target Users -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="glass-card p-6 rounded-3xl space-y-2">
                  <h4 class="font-bold text-slate-900 text-xs uppercase tracking-wider text-slate-500">Current Situation</h4>
                  <p class="text-xs text-slate-700">${p.current_situation || 'Manual strip testing.'}</p>
                </div>
                <div class="glass-card p-6 rounded-3xl space-y-2">
                  <h4 class="font-bold text-slate-900 text-xs uppercase tracking-wider text-slate-500">Target Community</h4>
                  <p class="text-xs text-slate-700">${p.target_users || 'Rural village councils.'}</p>
                </div>
              </div>

              <!-- Submitted Solutions List -->
              <div class="space-y-4 pt-4">
                <h3 class="font-bold text-slate-900 text-lg flex items-center justify-between">
                  <span>Submitted Solutions (${solutions.length})</span>
                  <button onclick="triggerSubmitSolutionForProblem(${p.id}, '${p.title.replace(/'/g, "\\'")}')" class="text-xs font-bold text-brand-600 hover:underline">+ Add Solution</button>
                </h3>

                <div class="space-y-4">
                  ${solutions.length === 0 ? '<p class="text-xs text-slate-500 py-4">No solutions submitted yet. Be the first innovator!</p>' :
                    solutions.map(s => `
                      <div class="glass-card p-6 rounded-2xl space-y-3">
                        <div class="flex items-center justify-between">
                          <h4 class="font-bold text-slate-900 text-base">${s.name}</h4>
                          <span class="px-2.5 py-1 rounded-full bg-purple-100 text-purple-800 text-[10px] font-bold">${s.status}</span>
                        </div>
                        <p class="text-xs text-slate-600 leading-relaxed">${s.description}</p>
                        <div class="flex items-center justify-between text-xs pt-2 text-slate-500">
                          <span>By ${s.author_name} ${s.team_name ? `(${s.team_name})` : ''}</span>
                          <button onclick="supportSolutionAction(${s.id})" class="font-semibold text-rose-600 flex items-center gap-1">
                            ❤️ ${s.supporters_count} Supporters
                          </button>
                        </div>
                      </div>
                    `).join('')
                  }
                </div>
              </div>

            </div>

            <!-- Sidebar Info -->
            <div class="space-y-6">
              
              <div class="glass-card p-6 rounded-3xl space-y-4">
                <h3 class="font-bold text-slate-900 text-sm border-b pb-2">Funding & Specs</h3>
                
                <div>
                  <span class="text-[10px] font-bold uppercase text-slate-400 block">Available Reward / Grant</span>
                  <span class="font-extrabold text-emerald-600 text-lg">${p.budget_funding}</span>
                </div>

                <div>
                  <span class="text-[10px] font-bold uppercase text-slate-400 block">Required Technology</span>
                  <div class="flex flex-wrap gap-1.5 mt-1">
                    ${p.required_tech.map(t => `<span class="px-2.5 py-1 rounded-lg bg-slate-100 text-slate-700 text-xs font-semibold">${t}</span>`).join('')}
                  </div>
                </div>

                <div>
                  <span class="text-[10px] font-bold uppercase text-slate-400 block">Expected Deliverables</span>
                  <p class="text-xs text-slate-700 mt-1">${p.expected_outcome || 'Working prototype & source code'}</p>
                </div>
              </div>

              <!-- Related Problems -->
              <div class="glass-card p-6 rounded-3xl space-y-3">
                <h3 class="font-bold text-slate-900 text-sm border-b pb-2">Related Problems</h3>
                <div class="divide-y divide-slate-100 text-xs space-y-2">
                  ${related.map(r => `
                    <div onclick="navigateTo('problem-detail', { problemId: ${r.id} })" class="pt-2 cursor-pointer hover:text-brand-600">
                      <p class="font-semibold text-slate-800 line-clamp-1">${r.title}</p>
                      <span class="text-[10px] text-slate-400">${r.category}</span>
                    </div>
                  `).join('')}
                </div>
              </div>

            </div>

          </div>

        </div>
      `;
      refreshIcons();
    });
}

function supportProblemAction(problemId) {
  fetch(`/api/problems/${problemId}/support`, { method: 'POST' })
    .then(r => r.json())
    .then(res => {
      const countEl = document.getElementById('p-detail-support-count');
      if (countEl) countEl.innerText = res.supporters_count;
      showToast('Problem upvoted successfully!', 'success');
    });
}

function triggerSubmitSolutionForProblem(problemId, problemTitle) {
  document.getElementById('sol-problem-id').value = problemId;
  document.getElementById('sol-problem-title-display').innerText = problemTitle;
  navigateTo('submit-solution');
}

// ==========================================================================
// MULTI-STEP PROBLEM SUBMISSION WIZARD
// ==========================================================================
function wizardNextStep() {
  if (currentState.currentStep < 4) {
    currentState.currentStep++;
    updateWizardUI();
  }
}

function wizardPrevStep() {
  if (currentState.currentStep > 1) {
    currentState.currentStep--;
    updateWizardUI();
  }
}

function updateWizardUI() {
  const step = currentState.currentStep;

  // Toggle step contents
  for (let i = 1; i <= 4; i++) {
    const el = document.getElementById(`submit-step-${i}`);
    const dot = document.getElementById(`step-dot-${i}`);
    if (el) el.classList.toggle('hidden', i !== step);
    if (dot) {
      dot.classList.toggle('active', i === step);
      dot.classList.toggle('completed', i < step);
    }
  }

  // Buttons
  const prevBtn = document.getElementById('sp-prev-btn');
  const nextBtn = document.getElementById('sp-next-btn');
  const submitBtn = document.getElementById('sp-submit-btn');

  if (prevBtn) prevBtn.classList.toggle('hidden', step === 1);
  if (nextBtn) nextBtn.classList.toggle('hidden', step === 4);
  if (submitBtn) submitBtn.classList.toggle('hidden', step !== 4);

  if (step === 4) {
    renderStep4Review();
  }
}

function renderStep4Review() {
  const summary = document.getElementById('submit-review-summary');
  if (!summary) return;

  const title = document.getElementById('sp-title')?.value || 'Untitled Problem';
  const org = document.getElementById('sp-org')?.value || 'N/A';
  const category = document.getElementById('sp-category')?.value || 'N/A';
  const location = document.getElementById('sp-location')?.value || 'Global';

  summary.innerHTML = `
    <h4 class="font-bold text-slate-900 text-base mb-2">${title}</h4>
    <p><strong>Organization:</strong> ${org} | <strong>Category:</strong> ${category}</p>
    <p><strong>Location:</strong> ${location}</p>
    <p class="text-xs text-slate-500 pt-2 border-t mt-2">Ready to publish! Your problem statement will be listed in the Discover Marketplace.</p>
  `;
}

function submitProblemForm() {
  const payload = {
    title: document.getElementById('sp-title')?.value,
    organization: document.getElementById('sp-org')?.value,
    category: document.getElementById('sp-category')?.value,
    location: document.getElementById('sp-location')?.value,
    difficulty: document.getElementById('sp-difficulty')?.value,
    description: document.getElementById('sp-description')?.value,
    target_users: document.getElementById('sp-target')?.value,
    why_it_matters: document.getElementById('sp-why')?.value,
    expected_outcome: document.getElementById('sp-outcome')?.value,
    required_tech: (document.getElementById('sp-tech')?.value || '').split(',').map(s => s.trim()),
    budget_funding: document.getElementById('sp-budget')?.value,
    deadline: document.getElementById('sp-deadline')?.value,
    attachments: document.getElementById('sp-attachments')?.value
  };

  fetch('/api/problems', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  .then(r => r.json())
  .then(res => {
    showToast(res.message, 'success');
    currentState.currentStep = 1;
    updateWizardUI();
    navigateTo('discover');
  });
}

// ==========================================================================
// SOLUTION SUBMISSION FORM
// ==========================================================================
function submitSolutionForm(isDraft = false) {
  const payload = {
    problem_id: document.getElementById('sol-problem-id')?.value,
    name: document.getElementById('sol-name')?.value,
    team_name: document.getElementById('sol-team-name')?.value,
    description: document.getElementById('sol-description')?.value,
    how_it_works: document.getElementById('sol-how-it-works')?.value,
    tech_used: (document.getElementById('sol-tech')?.value || '').split(',').map(s => s.trim()),
    estimated_cost: document.getElementById('sol-cost')?.value,
    demo_url: document.getElementById('sol-demo-url')?.value,
    github_url: document.getElementById('sol-github-url')?.value,
    video_url: document.getElementById('sol-video-url')?.value,
    status: isDraft ? 'Draft' : 'Submitted'
  };

  fetch('/api/solutions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  .then(r => r.json())
  .then(res => {
    showToast(res.message, 'success');
    navigateTo('solutions');
  });
}

function supportSolutionAction(solId) {
  fetch(`/api/solutions/${solId}/support`, { method: 'POST' })
    .then(r => r.json())
    .then(res => {
      showToast('Solution upvoted!', 'success');
      loadSolutionsMarketplace();
    });
}

// ==========================================================================
// SOLUTIONS MARKETPLACE
// ==========================================================================
function loadSolutionsMarketplace() {
  const techTags = ['All', 'AI/ML', 'IoT', 'Blockchain', 'Web', 'Mobile', 'Robotics', 'Hardware', 'Cloud'];
  const filterContainer = document.getElementById('solutions-tech-filters');
  if (filterContainer) {
    filterContainer.innerHTML = techTags.map(tag => `
      <button onclick="filterSolutionsByTech('${tag === 'All' ? '' : tag}')" 
              class="px-3.5 py-1.5 rounded-full text-xs font-semibold transition-colors ${
                (currentState.selectedTechFilter === tag || (tag === 'All' && !currentState.selectedTechFilter)) ?
                'bg-brand-600 text-white' : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
              }">
        ${tag}
      </button>
    `).join('');
  }

  const tech = currentState.selectedTechFilter;
  fetch(`/api/solutions?tech=${encodeURIComponent(tech)}`)
    .then(r => r.json())
    .then(solutions => {
      currentState.solutions = solutions;
      const grid = document.getElementById('solutions-grid');
      if (!grid) return;

      grid.innerHTML = solutions.map(s => `
        <div class="glass-card rounded-3xl p-6 flex flex-col justify-between space-y-4">
          <div class="space-y-3">
            <div class="flex items-center justify-between text-xs">
              <span class="px-2.5 py-1 rounded-full bg-purple-100 text-purple-800 font-bold">${s.status}</span>
              <span class="text-slate-400 font-medium">By ${s.author_name}</span>
            </div>
            <h3 class="font-bold text-slate-900 text-lg">${s.name}</h3>
            <p class="text-xs font-semibold text-brand-600">Problem Solved: ${s.problem_title}</p>
            <p class="text-xs text-slate-600 line-clamp-3 leading-relaxed">${s.description}</p>
            
            <div class="flex flex-wrap gap-1.5 pt-1">
              ${s.tech_used.map(t => `<span class="px-2 py-0.5 rounded-md bg-slate-100 text-slate-600 text-[10px] font-semibold">${t}</span>`).join('')}
            </div>
          </div>

          <div class="pt-4 border-t border-slate-100 flex items-center justify-between text-xs">
            <button onclick="supportSolutionAction(${s.id})" class="font-bold text-rose-600 flex items-center gap-1">
              ❤️ ${s.supporters_count} Upvotes
            </button>
            ${s.demo_url ? `<a href="${s.demo_url}" target="_blank" class="font-bold text-brand-600 hover:underline">Live Demo ↗</a>` : ''}
          </div>
        </div>
      `).join('');
      refreshIcons();
    });
}

function filterSolutionsByTech(tech) {
  currentState.selectedTechFilter = tech;
  loadSolutionsMarketplace();
}

// ==========================================================================
// ACTIVE CHALLENGES PAGE
// ==========================================================================
function loadChallenges() {
  fetch('/api/challenges')
    .then(r => r.json())
    .then(challenges => {
      currentState.challenges = challenges;
      const grid = document.getElementById('challenges-grid');
      if (!grid) return;

      grid.innerHTML = challenges.map(c => `
        <div class="glass-card rounded-3xl overflow-hidden flex flex-col justify-between">
          <div class="h-48 relative overflow-hidden">
            <img src="${c.banner_image}" class="w-full h-full object-cover" />
            <div class="absolute top-4 right-4">
              <span class="px-3 py-1 rounded-full bg-slate-900/80 backdrop-blur-md text-white font-bold text-xs">${c.status}</span>
            </div>
          </div>

          <div class="p-6 space-y-4">
            <div class="flex items-center gap-2 text-xs text-slate-500">
              <img src="${c.org_logo}" class="w-5 h-5 rounded-full object-cover" />
              <span class="font-semibold text-slate-800">${c.org_name}</span>
            </div>

            <h3 class="font-extrabold text-slate-900 text-xl">${c.title}</h3>
            <p class="text-xs text-slate-600 leading-relaxed">${c.description}</p>

            <div class="grid grid-cols-2 gap-4 p-4 rounded-2xl bg-slate-50 text-xs">
              <div>
                <span class="text-slate-400 block text-[10px] font-bold uppercase">Prize Pool</span>
                <strong class="text-emerald-600 text-sm font-extrabold">${c.prize_pool}</strong>
              </div>
              <div>
                <span class="text-slate-400 block text-[10px] font-bold uppercase">Timeline</span>
                <strong class="text-slate-800">${c.timeline}</strong>
              </div>
            </div>

            <div class="pt-2 flex items-center justify-between">
              <span class="text-xs text-slate-500 font-medium">${c.submissions_count || 0} Submissions</span>
              <button onclick="navigateTo('submit-solution')" class="px-5 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-bold text-xs shadow-md">
                Participate in Challenge
              </button>
            </div>
          </div>
        </div>
      `).join('');
      refreshIcons();
    });
}

// ==========================================================================
// TEAMS & COLLABORATION
// ==========================================================================
function loadTeams() {
  fetch('/api/teams')
    .then(r => r.json())
    .then(teams => {
      currentState.teams = teams;
      const grid = document.getElementById('teams-grid');
      if (!grid) return;

      grid.innerHTML = teams.map(t => `
        <div class="glass-card rounded-3xl p-6 flex flex-col justify-between space-y-4">
          <div class="space-y-3">
            <div class="flex items-center justify-between text-xs text-slate-500">
              <span class="font-semibold text-slate-700">Created by ${t.creator_name}</span>
              <span>${t.member_count} Members</span>
            </div>
            <h3 class="font-bold text-slate-900 text-lg">${t.name}</h3>
            <p class="text-xs text-slate-600 leading-relaxed">${t.tagline || 'Collaborative team working on high-impact projects.'}</p>
            
            <div>
              <span class="text-[10px] font-bold uppercase text-slate-400 block mb-1">Looking for Roles</span>
              <div class="flex flex-wrap gap-1.5">
                ${t.looking_for_skills.map(s => `<span class="px-2.5 py-1 rounded-lg bg-amber-50 text-amber-800 border border-amber-200 text-[10px] font-bold">${s}</span>`).join('')}
              </div>
            </div>
          </div>

          <div class="pt-4 border-t border-slate-100 flex items-center justify-between">
            ${t.project_url ? `<a href="${t.project_url}" target="_blank" class="text-xs font-semibold text-brand-600 hover:underline">Team Link ↗</a>` : '<span></span>'}
            <button onclick="requestJoinTeam(${t.id})" class="px-4 py-2 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-bold text-xs shadow-md">
              Join Team
            </button>
          </div>
        </div>
      `).join('');
      refreshIcons();
    });
}

function requestJoinTeam(teamId) {
  fetch(`/api/teams/${teamId}/join`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: 2, role: 'Collaborator' })
  })
  .then(r => r.json())
  .then(res => {
    showToast(res.message, 'success');
    loadTeams();
  });
}

function openCreateTeamModal() {
  document.getElementById('modal-create-team')?.classList.remove('hidden');
}

function closeCreateTeamModal() {
  document.getElementById('modal-create-team')?.classList.add('hidden');
}

function submitCreateTeam() {
  const payload = {
    name: document.getElementById('mt-name')?.value,
    tagline: document.getElementById('mt-tagline')?.value,
    looking_for_skills: (document.getElementById('mt-skills')?.value || '').split(',').map(s => s.trim())
  };

  fetch('/api/teams', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  .then(r => r.json())
  .then(res => {
    showToast(res.message, 'success');
    closeCreateTeamModal();
    loadTeams();
  });
}

// ==========================================================================
// LEADERBOARD & BADGES
// ==========================================================================
function loadLeaderboard() {
  fetch('/api/leaderboard')
    .then(r => r.json())
    .then(data => {
      const innovatorsList = document.getElementById('leaderboard-innovators-list');
      if (innovatorsList) {
        innovatorsList.innerHTML = data.top_innovators.map((u, i) => `
          <div class="py-3 flex items-center justify-between gap-4">
            <div class="flex items-center gap-3">
              <span class="font-extrabold text-sm w-6 text-center ${i === 0 ? 'text-amber-500' : i === 1 ? 'text-slate-400' : i === 2 ? 'text-amber-700' : 'text-slate-500'}">#${i + 1}</span>
              <img src="${u.avatar}" class="w-10 h-10 rounded-full object-cover border border-slate-200" />
              <div>
                <h4 class="font-bold text-slate-900 text-sm cursor-pointer hover:text-brand-600" onclick="navigateTo('profile', {userId: ${u.id}})">${u.name}</h4>
                <p class="text-[10px] text-slate-500 truncate max-w-xs">${u.bio}</p>
              </div>
            </div>

            <div class="flex items-center gap-3">
              <div class="hidden sm:flex gap-1">
                ${u.badges.map(b => `<span class="px-2 py-0.5 rounded bg-amber-100 text-amber-800 text-[10px] font-bold">${b}</span>`).join('')}
              </div>
              <span class="font-extrabold text-brand-600 text-sm">${u.points} pts</span>
            </div>
          </div>
        `).join('');
      }

      const teamsList = document.getElementById('leaderboard-teams-list');
      if (teamsList) {
        teamsList.innerHTML = data.top_teams.map(t => `
          <div class="p-3 rounded-xl bg-slate-50 flex items-center justify-between">
            <div>
              <h5 class="font-bold text-slate-900">${t.name}</h5>
              <span class="text-[10px] text-slate-500">Leader: ${t.leader_name}</span>
            </div>
            <span class="font-bold text-brand-600 text-xs">${t.member_count} members</span>
          </div>
        `).join('');
      }

      const solList = document.getElementById('leaderboard-solutions-list');
      if (solList) {
        solList.innerHTML = data.top_solutions.map(s => `
          <div class="p-3 rounded-xl bg-slate-50 flex items-center justify-between">
            <div>
              <h5 class="font-bold text-slate-900">${s.name}</h5>
              <span class="text-[10px] text-slate-500">By ${s.author_name}</span>
            </div>
            <span class="font-bold text-rose-600 text-xs">❤️ ${s.supporters_count}</span>
          </div>
        `).join('');
      }
    });
}

// ==========================================================================
// USER PROFILE
// ==========================================================================
function loadUserProfile(userId) {
  fetch(`/api/users/${userId}`)
    .then(r => r.json())
    .then(data => {
      const u = data.user;
      const solutions = data.solutions;
      const teams = data.teams;

      const container = document.getElementById('user-profile-container');
      if (!container) return;

      container.innerHTML = `
        <div class="glass-card p-8 rounded-3xl space-y-6">
          <div class="flex flex-col sm:flex-row items-center gap-6 text-center sm:text-left">
            <img src="${u.avatar}" class="w-24 h-24 rounded-2xl object-cover border-2 border-brand-500 shadow-lg" />
            <div class="space-y-2">
              <div class="flex items-center justify-center sm:justify-start gap-2">
                <h1 class="text-2xl font-extrabold text-slate-900">${u.name}</h1>
                <span class="px-2.5 py-0.5 rounded-full bg-brand-100 text-brand-700 text-xs font-bold">${u.role}</span>
              </div>
              <p class="text-xs text-slate-600 max-w-lg leading-relaxed">${u.bio}</p>
              <p class="text-xs text-slate-500">🎓 ${u.education || 'N/A'}</p>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4 border-t border-slate-100">
            <div>
              <h4 class="font-bold text-slate-900 text-xs uppercase tracking-wider mb-2">Skills & Expertise</h4>
              <div class="flex flex-wrap gap-1.5">
                ${u.skills.map(s => `<span class="px-2.5 py-1 rounded-lg bg-slate-100 text-slate-700 text-xs font-semibold">${s}</span>`).join('')}
              </div>
            </div>

            <div>
              <h4 class="font-bold text-slate-900 text-xs uppercase tracking-wider mb-2">Gamification Badges</h4>
              <div class="flex flex-wrap gap-1.5">
                ${u.badges.map(b => `<span class="px-3 py-1 rounded-full bg-amber-100 text-amber-800 text-xs font-bold">${b}</span>`).join('')}
              </div>
            </div>
          </div>

          <div class="pt-4 border-t border-slate-100 space-y-3">
            <h4 class="font-bold text-slate-900 text-sm">Submitted Solutions (${solutions.length})</h4>
            <div class="space-y-2 text-xs">
              ${solutions.map(s => `
                <div class="p-3 rounded-xl bg-slate-50 flex items-center justify-between">
                  <span class="font-semibold text-slate-800">${s.name}</span>
                  <span class="text-rose-600 font-bold">❤️ ${s.supporters_count} Supporters</span>
                </div>
              `).join('')}
            </div>
          </div>
        </div>
      `;
    });
}

// ==========================================================================
// SUCCESS STORIES
// ==========================================================================
function loadSuccessStories() {
  fetch('/api/success-stories')
    .then(r => r.json())
    .then(stories => {
      const grid = document.getElementById('success-stories-grid');
      if (!grid) return;

      grid.innerHTML = stories.map(st => `
        <div class="glass-card rounded-3xl overflow-hidden flex flex-col justify-between space-y-4">
          <img src="${st.image_url}" class="w-full h-52 object-cover" />
          <div class="p-6 space-y-3">
            <span class="px-3 py-1 rounded-full badge-category font-bold text-xs">${st.category}</span>
            <h3 class="font-extrabold text-slate-900 text-xl">${st.problem_title}</h3>
            <p class="text-xs font-bold text-emerald-600">Solution: ${st.solution_name} by ${st.team_name}</p>
            <p class="text-xs text-slate-600 leading-relaxed">${st.description}</p>
            
            <div class="grid grid-cols-2 gap-2 pt-2">
              ${st.metrics.map(m => `
                <div class="p-2.5 rounded-xl bg-emerald-50 border border-emerald-200 text-center">
                  <span class="text-[11px] font-extrabold text-emerald-800">${m}</span>
                </div>
              `).join('')}
            </div>
          </div>
        </div>
      `).join('');
    });
}

// ==========================================================================
// ADMIN DASHBOARD
// ==========================================================================
function loadAdminDashboard() {
  fetch('/api/admin/overview')
    .then(r => r.json())
    .then(data => {
      const totals = data.totals;
      const cardsContainer = document.getElementById('admin-summary-cards');
      if (cardsContainer) {
        cardsContainer.innerHTML = `
          <div class="p-4 rounded-2xl bg-white border text-center"><span class="font-bold text-2xl text-brand-600 block">${totals.problems}</span><span class="text-xs text-slate-500">Problems</span></div>
          <div class="p-4 rounded-2xl bg-white border text-center"><span class="font-bold text-2xl text-emerald-600 block">${totals.solutions}</span><span class="text-xs text-slate-500">Solutions</span></div>
          <div class="p-4 rounded-2xl bg-white border text-center"><span class="font-bold text-2xl text-purple-600 block">${totals.users}</span><span class="text-xs text-slate-500">Users</span></div>
          <div class="p-4 rounded-2xl bg-white border text-center"><span class="font-bold text-2xl text-amber-600 block">${totals.orgs}</span><span class="text-xs text-slate-500">Organizations</span></div>
          <div class="p-4 rounded-2xl bg-white border text-center"><span class="font-bold text-2xl text-rose-600 block">${totals.challenges}</span><span class="text-xs text-slate-500">Challenges</span></div>
        `;
      }

      // Moderation table
      const table = document.getElementById('admin-moderation-table');
      if (table) {
        table.innerHTML = data.recent_problems.map(p => `
          <tr>
            <td class="p-3 font-bold text-slate-900">${p.title}</td>
            <td class="p-3"><span class="px-2 py-0.5 rounded bg-slate-100 text-slate-700">${p.category}</span></td>
            <td class="p-3">${p.org_name}</td>
            <td class="p-3"><span class="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold">${p.status}</span></td>
            <td class="p-3 text-right">
              <button class="px-2.5 py-1 rounded bg-brand-600 text-white font-bold text-[10px]">Approve</button>
            </td>
          </tr>
        `).join('');
      }

      renderAdminStatsForm();
      initAdminCharts();
    });
}

function renderAdminStatsForm() {
  fetch('/api/stats')
    .then(r => r.json())
    .then(stats => {
      const form = document.getElementById('admin-editable-stats-form');
      if (!form) return;

      form.innerHTML = Object.keys(stats).map(k => `
        <div>
          <label class="block font-bold text-slate-700 mb-1">${stats[k].label}</label>
          <input type="text" id="admin-stat-${k}" value="${stats[k].value}" class="w-full p-2 rounded-lg border text-xs focus:ring-2 focus:ring-brand-500" />
        </div>
      `).join('');
    });
}

function saveAdminStats() {
  const payload = {
    problems_posted: document.getElementById('admin-stat-problems_posted')?.value,
    solutions_submitted: document.getElementById('admin-stat-solutions_submitted')?.value,
    innovators: document.getElementById('admin-stat-innovators')?.value,
    organizations: document.getElementById('admin-stat-organizations')?.value,
    cities: document.getElementById('admin-stat-cities')?.value,
    active_challenges: document.getElementById('admin-stat-active_challenges')?.value
  };

  fetch('/api/stats', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  .then(r => r.json())
  .then(res => {
    showToast(res.message, 'success');
  });
}

function initAdminCharts() {
  const ctx1 = document.getElementById('chart-growth')?.getContext('2d');
  if (ctx1 && !window.myChart1) {
    window.myChart1 = new Chart(ctx1, {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'],
        datasets: [
          { label: 'Problems Posted', data: [120, 240, 410, 680, 920, 1340, 1890, 2400], borderColor: '#3b82f6', tension: 0.4 },
          { label: 'Solutions Submitted', data: [310, 580, 1100, 1900, 2800, 3900, 4800, 5920], borderColor: '#10b981', tension: 0.4 }
        ]
      }
    });
  }

  const ctx2 = document.getElementById('chart-categories')?.getContext('2d');
  if (ctx2 && !window.myChart2) {
    window.myChart2 = new Chart(ctx2, {
      type: 'doughnut',
      data: {
        labels: ['Water', 'Disaster', 'Agriculture', 'Education', 'Smart Cities'],
        datasets: [{ data: [35, 25, 20, 12, 8], backgroundColor: ['#3b82f6', '#f59e0b', '#10b981', '#a855f7', '#f43f5e'] }]
      }
    });
  }
}

// ==========================================================================
// AI ASSISTANT MODAL
// ==========================================================================
function openAIAssistantModal() {
  document.getElementById('modal-ai-assistant')?.classList.remove('hidden');
}

function closeAIAssistantModal() {
  document.getElementById('modal-ai-assistant')?.classList.add('hidden');
}

function switchAITab(tab) {
  currentState.activeAIModalTab = tab;
  document.getElementById('ai-tab-analyzer').classList.toggle('hidden', tab !== 'analyzer');
  document.getElementById('ai-tab-solution').classList.toggle('hidden', tab !== 'solution');
}

function runAIProblemAnalysis() {
  const text = document.getElementById('ai-problem-input')?.value;
  if (!text) return showToast('Please enter a problem description', 'warning');

  fetch('/api/ai/analyze-problem', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ problem_statement: text })
  })
  .then(r => r.json())
  .then(res => {
    const out = document.getElementById('ai-problem-output');
    if (!out) return;
    out.classList.remove('hidden');
    const a = res.analysis;

    out.innerHTML = `
      <p class="font-bold text-slate-900">${a.summary}</p>
      
      <div>
        <strong class="block text-slate-800 font-bold mb-1">Identified Root Causes:</strong>
        <ul class="list-disc pl-4 space-y-1 text-slate-600">
          ${a.root_causes.map(rc => `<li>${rc}</li>`).join('')}
        </ul>
      </div>

      <div>
        <strong class="block text-slate-800 font-bold mb-1">Suggested Tech Approaches:</strong>
        <div class="flex flex-wrap gap-2">
          ${a.tech_approaches.map(t => `<span class="px-2.5 py-1 rounded bg-amber-100 text-amber-900 font-bold">${t.tech}: ${t.role}</span>`).join('')}
        </div>
      </div>
    `;
  });
}

function runAISolutionAnalysis() {
  const text = document.getElementById('ai-solution-input')?.value;
  if (!text) return showToast('Please paste your solution proposal', 'warning');

  fetch('/api/ai/analyze-solution', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ solution_description: text })
  })
  .then(r => r.json())
  .then(res => {
    const out = document.getElementById('ai-solution-output');
    if (!out) return;
    out.classList.remove('hidden');
    const f = res.feedback;

    out.innerHTML = `
      <div class="p-3 rounded-xl bg-brand-100 text-brand-900 font-bold">Score: ${f.strength_score}</div>
      <div>
        <strong class="block text-slate-800 font-bold mb-1">Technical Improvements:</strong>
        <ul class="list-disc pl-4 space-y-1 text-slate-600">
          ${f.technical_improvements.map(ti => `<li>${ti}</li>`).join('')}
        </ul>
      </div>
      <div>
        <strong class="block text-slate-800 font-bold mb-1">Scalability Advice:</strong>
        <ul class="list-disc pl-4 space-y-1 text-slate-600">
          ${f.scalability_ideas.map(si => `<li>${si}</li>`).join('')}
        </ul>
      </div>
    `;
  });
}

// Global Initialization
document.addEventListener('DOMContentLoaded', () => {
  loadNotifications();
  navigateTo('home');
});
