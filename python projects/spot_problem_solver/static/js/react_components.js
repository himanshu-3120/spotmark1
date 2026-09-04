/* ==========================================================================
   SPOT PROBLEM SOLVER — React JS Animated Innovation Radar & Impact Matrix
   ========================================================================== */

const { useState, useEffect } = React;

// Custom Animated Counter Hook
function useAnimatedCounter(target, duration = 1500) {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let startTimestamp = null;
    const numericTarget = parseInt(String(target).replace(/[^0-9]/g, '')) || 0;

    const step = (timestamp) => {
      if (!startTimestamp) startTimestamp = timestamp;
      const progress = Math.min((timestamp - startTimestamp) / duration, 1);
      // Ease-out quad
      const currentVal = Math.floor(progress * (2 - progress) * numericTarget);
      setCount(currentVal);
      if (progress < 1) {
        window.requestAnimationFrame(step);
      }
    };

    window.requestAnimationFrame(step);
  }, [target, duration]);

  return count;
}

// React Stat Card Component
function AnimatedStatCard({ icon, value, label, subtitle, badgeColor, rawNum }) {
  const animatedValue = useAnimatedCounter(rawNum);
  const formattedVal = rawNum > 1000 ? animatedValue.toLocaleString() + '+' : animatedValue + '+';

  return (
    <div className="group relative bg-slate-800/80 hover:bg-slate-800 backdrop-blur-xl border border-slate-700/80 hover:border-brand-500/50 p-6 rounded-3xl transition-all duration-300 transform hover:-translate-y-1 shadow-xl hover:shadow-2xl hover:shadow-brand-500/10">
      <div className="flex items-center justify-between mb-3">
        <span className="text-2xl">{icon}</span>
        <span className={`text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-full ${badgeColor}`}>
          Live Sync
        </span>
      </div>
      <div className="space-y-1">
        <span className="font-heading text-3xl sm:text-4xl font-extrabold text-white tracking-tight block">
          {formattedVal}
        </span>
        <span className="text-xs font-bold text-slate-300 block">{label}</span>
        <span className="text-[11px] text-slate-400 block">{subtitle}</span>
      </div>
      
      {/* Animated Subtle Progress Glow */}
      <div className="mt-4 w-full bg-slate-700/50 h-1.5 rounded-full overflow-hidden">
        <div className="bg-gradient-to-r from-brand-500 to-impact-500 h-full rounded-full animate-pulse" style={{ width: '85%' }}></div>
      </div>
    </div>
  );
}

// Main React Innovation Radar Component
function InnovationRadarApp() {
  const [activeTab, setActiveTab] = useState('counters'); // 'counters', 'stream', 'radar'
  const [activityFeed, setActivityFeed] = useState([
    { id: 1, text: "⚡ Team AquaMesh submitted solution for Water Quality Monitoring", time: "2 seconds ago", tag: "Solution Submitted", color: "bg-emerald-500/20 text-emerald-300" },
    { id: 2, text: "🏆 $100,000 Grand Challenge launched by Ministry of Water Resources", time: "1 minute ago", tag: "New Challenge", color: "bg-amber-500/20 text-amber-300" },
    { id: 3, text: "❤️ HydroSentinel AI received 50+ community upvotes", time: "3 minutes ago", tag: "Popular Idea", color: "bg-rose-500/20 text-rose-300" },
    { id: 4, text: "👥 David Chen joined CyberDefenders Squad as Systems Lead", time: "8 minutes ago", tag: "Team Formed", color: "bg-purple-500/20 text-purple-300" }
  ]);

  const [techRadar] = useState([
    { tech: "AI / Machine Learning", pct: 35, count: "3,650 Solutions", color: "from-blue-500 to-indigo-600" },
    { tech: "IoT Mesh Sensors", pct: 25, count: "2,410 Solutions", color: "from-emerald-500 to-teal-600" },
    { tech: "Clean Water & AgTech", pct: 20, count: "1,980 Solutions", color: "from-amber-500 to-orange-600" },
    { tech: "Smart Cities Infrastructure", pct: 12, count: "1,150 Solutions", color: "from-purple-500 to-pink-600" },
    { tech: "Healthcare Cybersecurity", pct: 8, count: "780 Solutions", color: "from-rose-500 to-red-600" }
  ]);

  // Simulate Live Stream Updates
  useEffect(() => {
    const interval = setInterval(() => {
      const simulatedActions = [
        { text: "✨ New problem posted: Automated E-Waste Segregation Robot", tag: "New Problem", color: "bg-blue-500/20 text-blue-300" },
        { text: "🔥 EcoChill Thermal Pod reached 100+ supporters milestone!", tag: "Milestone", color: "bg-emerald-500/20 text-emerald-300" },
        { text: "⚡ Innovator Priya Sharma earned 'Solution Builder' badge", tag: "Badge Earned", color: "bg-amber-500/20 text-amber-300" }
      ];
      const randomAction = simulatedActions[Math.floor(Math.random() * simulatedActions.length)];
      const newEntry = {
        id: Date.now(),
        text: randomAction.text,
        time: "Just now",
        tag: randomAction.tag,
        color: randomAction.color
      };

      setActivityFeed(prev => [newEntry, ...prev.slice(0, 3)]);
    }, 6000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-8">
      
      <!-- React Animated Header Bar -->
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-500/10 border border-brand-500/20 text-brand-400 text-xs font-bold uppercase tracking-wider mb-2">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
            React JS Animated Platform Matrix
          </div>
          <h2 class="text-2xl sm:text-3xl font-extrabold tracking-tight text-white">
            Real-Time Innovation & Impact Hub
          </h2>
        </div>

        <!-- React Interactive Tab Switcher -->
        <div class="flex items-center gap-1.5 bg-slate-800/80 p-1.5 rounded-2xl border border-slate-700/80">
          <button 
            onClick={() => setActiveTab('counters')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              activeTab === 'counters' ? 'bg-brand-600 text-white shadow-lg' : 'text-slate-400 hover:text-white'
            }`}
          >
            📊 Animated Counters
          </button>

          <button 
            onClick={() => setActiveTab('stream')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              activeTab === 'stream' ? 'bg-brand-600 text-white shadow-lg' : 'text-slate-400 hover:text-white'
            }`}
          >
            ⚡ Live Activity Stream
          </button>

          <button 
            onClick={() => setActiveTab('radar')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              activeTab === 'radar' ? 'bg-brand-600 text-white shadow-lg' : 'text-slate-400 hover:text-white'
            }`}
          >
            🌐 Tech Impact Radar
          </button>
        </div>
      </div>

      {/* TAB CONTENT 1: ANIMATED COUNTER CARDS */}
      {activeTab === 'counters' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-5">
          <AnimatedStatCard icon="💡" rawNum={10480} label="Problems Posted" subtitle="Verified challenges" badgeColor="bg-blue-500/20 text-blue-300" />
          <AnimatedStatCard icon="🛠️" rawNum={25920} label="Solutions Submitted" subtitle="Hardware & Software" badgeColor="bg-emerald-500/20 text-emerald-300" />
          <AnimatedStatCard icon="👩‍💻" rawNum={5850} label="Global Innovators" subtitle="Developers & Scientists" badgeColor="bg-purple-500/20 text-purple-300" />
          <AnimatedStatCard icon="🏛️" rawNum={520} label="Organizations" subtitle="Gov, NGOs & Universities" badgeColor="bg-amber-500/20 text-amber-300" />
          <AnimatedStatCard icon="🌍" rawNum={140} label="Cities Reached" subtitle="Global Field Pilots" badgeColor="bg-teal-500/20 text-teal-300" />
          <AnimatedStatCard icon="🏆" rawNum={54} label="Active Challenges" subtitle="$500k+ Total Prize Pool" badgeColor="bg-rose-500/20 text-rose-300" />
        </div>
      )}

      {/* TAB CONTENT 2: LIVE ACTIVITY STREAM */}
      {activeTab === 'stream' && (
        <div className="bg-slate-800/60 border border-slate-700/80 rounded-3xl p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-700/60 pb-3">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Live Platform Stream</span>
            <span className="text-[11px] text-emerald-400 font-medium">● Auto-syncing every 6s</span>
          </div>

          <div className="space-y-3">
            {activityFeed.map(item => (
              <div key={item.id} className="p-4 rounded-2xl bg-slate-900/60 border border-slate-700/50 flex flex-col sm:flex-row sm:items-center justify-between gap-3 animate-fadeIn transition-all">
                <div className="flex items-center gap-3">
                  <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold ${item.color}`}>
                    {item.tag}
                  </span>
                  <span className="text-xs font-semibold text-white">{item.text}</span>
                </div>
                <span className="text-[11px] text-slate-400 font-medium">{item.time}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT 3: TECH IMPACT RADAR */}
      {activeTab === 'radar' && (
        <div className="bg-slate-800/60 border border-slate-700/80 rounded-3xl p-6 space-y-6">
          <div className="flex items-center justify-between border-b border-slate-700/60 pb-3">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Technology Distribution Radar</span>
            <span class="text-xs text-brand-400 font-semibold">100% Verified Submissions</span>
          </div>

          <div className="space-y-5">
            {techRadar.map(item => (
              <div key={item.tech} className="space-y-2">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-bold text-white">{item.tech}</span>
                  <div className="flex items-center gap-3">
                    <span className="text-slate-400 text-[11px]">{item.count}</span>
                    <strong className="text-brand-400 font-extrabold">{item.pct}%</strong>
                  </div>
                </div>
                <div className="w-full bg-slate-900 h-3 rounded-full overflow-hidden p-0.5 border border-slate-700">
                  <div 
                    className={`bg-gradient-to-r ${item.color} h-full rounded-full transition-all duration-1000 ease-out`}
                    style={{ width: `${item.pct}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

    </div>
  );
}

// Mount React Component
document.addEventListener('DOMContentLoaded', () => {
  const rootElement = document.getElementById('react-innovation-radar-root');
  if (rootElement && window.ReactDOM) {
    const root = ReactDOM.createRoot(rootElement);
    root.render(React.createElement(InnovationRadarApp));
  }
});
