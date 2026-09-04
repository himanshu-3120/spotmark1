import sqlite3
import os
import json
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "spot_solver.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Create Tables
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        role TEXT NOT NULL DEFAULT 'Innovator', -- User, Innovator, Organization, Reviewer, Admin
        avatar TEXT,
        bio TEXT,
        skills TEXT, -- JSON array
        education TEXT,
        github TEXT,
        linkedin TEXT,
        points INTEGER DEFAULT 120,
        badges TEXT, -- JSON array
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT NOT NULL,
        logo TEXT,
        description TEXT,
        location TEXT,
        website TEXT,
        verified INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS problems (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        organization_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        location TEXT NOT NULL,
        difficulty TEXT DEFAULT 'Medium', -- Easy, Medium, Hard, Expert
        status TEXT DEFAULT 'Open', -- Open, In Progress, Solved, Under Review
        description TEXT NOT NULL,
        why_it_matters TEXT,
        current_situation TEXT,
        target_users TEXT,
        expected_outcome TEXT,
        required_tech TEXT, -- JSON array
        budget_funding TEXT,
        deadline TEXT,
        attachments TEXT,
        views INTEGER DEFAULT 420,
        supporters_count INTEGER DEFAULT 35,
        featured INTEGER DEFAULT 0,
        approved INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (organization_id) REFERENCES organizations(id)
    );

    CREATE TABLE IF NOT EXISTS solutions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        problem_id INTEGER NOT NULL,
        team_id INTEGER,
        user_id INTEGER NOT NULL,
        description TEXT NOT NULL,
        how_it_works TEXT,
        tech_used TEXT, -- JSON array
        innovation TEXT,
        target_users TEXT,
        social_impact TEXT,
        scalability TEXT,
        implementation_plan TEXT,
        estimated_cost TEXT,
        demo_url TEXT,
        github_url TEXT,
        video_url TEXT,
        status TEXT DEFAULT 'Submitted', -- Draft, Submitted, Under Evaluation, Winner, Implemented
        supporters_count INTEGER DEFAULT 18,
        featured INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (problem_id) REFERENCES problems(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS challenges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        organization_id INTEGER NOT NULL,
        problem_statement TEXT NOT NULL,
        description TEXT NOT NULL,
        eligibility TEXT,
        timeline TEXT,
        prize_pool TEXT,
        evaluation_criteria TEXT,
        status TEXT DEFAULT 'Open', -- Coming Soon, Open, Closing Soon, Closed, Winners Announced
        banner_image TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (organization_id) REFERENCES organizations(id)
    );

    CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        tagline TEXT,
        creator_id INTEGER NOT NULL,
        looking_for_skills TEXT, -- JSON array
        project_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (creator_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS team_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        role TEXT NOT NULL,
        status TEXT DEFAULT 'Accepted', -- Pending, Accepted
        FOREIGN KEY (team_id) REFERENCES teams(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target_type TEXT NOT NULL, -- problem, solution, challenge, discussion
        target_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS votes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        target_type TEXT NOT NULL, -- problem, solution
        target_id INTEGER NOT NULL,
        UNIQUE(user_id, target_type, target_id)
    );

    CREATE TABLE IF NOT EXISTS bookmarks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        target_type TEXT NOT NULL, -- problem, solution
        target_id INTEGER NOT NULL,
        UNIQUE(user_id, target_type, target_id)
    );

    CREATE TABLE IF NOT EXISTS stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key_name TEXT UNIQUE NOT NULL,
        value_text TEXT NOT NULL,
        label TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS success_stories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        problem_title TEXT NOT NULL,
        solution_name TEXT NOT NULL,
        team_name TEXT NOT NULL,
        organization TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT NOT NULL,
        metrics TEXT NOT NULL, -- JSON array of string metrics
        impact_summary TEXT NOT NULL,
        image_url TEXT
    );

    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        type TEXT DEFAULT 'info', -- info, success, warning, challenge
        read INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()

    # Seed initial data if empty
    cursor.execute("SELECT COUNT(*) FROM problems")
    if cursor.fetchone()[0] == 0:
        seed_data(cursor, conn)

    conn.close()

def seed_data(cursor, conn):
    print("Seeding database with rich demo data...")

    # 1. Stats
    stats_data = [
        ('problems_posted', '10,480+', 'Problems Posted'),
        ('solutions_submitted', '25,920+', 'Solutions Submitted'),
        ('innovators', '5,850+', 'Innovators'),
        ('organizations', '520+', 'Organizations'),
        ('cities', '140+', 'Cities Reached'),
        ('active_challenges', '54', 'Active Challenges')
    ]
    cursor.executemany("INSERT INTO stats (key_name, value_text, label) VALUES (?, ?, ?)", stats_data)

    # 2. Users
    users_data = [
        ('Dr. Aris Thorne', 'admin@spotsolver.org', 'Admin', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80', 'Chief Platform Admin & Innovation Director', json.dumps(['AI/ML', 'Policy', 'Research']), 'PhD in Computer Science - MIT', 'https://github.com/aristhorne', 'https://linkedin.com/in/aristhorne', 850, json.dumps(['Problem Spotter', 'Innovation Leader', 'Impact Maker'])),
        ('Priya Sharma', 'priya@techforgood.io', 'Innovator', 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=200&q=80', 'AI & IoT Researcher working on clean water accessibility and smart sensors.', json.dumps(['Python', 'IoT', 'AI/ML', 'React']), 'B.Tech CS - IIT Delhi', 'https://github.com/priyasharma', 'https://linkedin.com/in/priyasharma', 640, json.dumps(['Solution Builder', 'Community Champion'])),
        ('Marcus Vance', 'marcus@ecohive.org', 'Innovator', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80', 'Full Stack Developer & Hardware Hacker. Passionate about AgTech.', json.dumps(['Java', 'Hardware', 'UI/UX', 'Cloud']), 'M.S. Robotics - Stanford', 'https://github.com/marcusvance', 'https://linkedin.com/in/marcusvance', 490, json.dumps(['Problem Spotter', 'Solution Builder'])),
        ('Elena Rostova', 'elena@smartcity.gov', 'Organization', 'https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=200&q=80', 'Urban Planning Commissioner at National Smart Cities Mission', json.dumps(['Urban Planning', 'Public Policy', 'GIS']), 'M.P.A. Harvard Kennedy School', '', 'https://linkedin.com/in/elenarostova', 320, json.dumps(['Impact Maker'])),
        ('David Chen', 'david@healthstack.co', 'Innovator', 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=200&q=80', 'Biomedical Engineer & Data Scientist building low-cost diagnostics.', json.dumps(['Python', 'Data Science', 'Healthcare', 'AI/ML']), 'M.D. / M.S. Johns Hopkins', 'https://github.com/davidchen', 'https://linkedin.com/in/davidchen', 530, json.dumps(['Innovation Leader']))
    ]
    cursor.executemany("INSERT INTO users (name, email, role, avatar, bio, skills, education, github, linkedin, points, badges) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", users_data)

    # 3. Organizations
    orgs_data = [
        (4, 'Ministry of Urban Development & Environment', 'https://images.unsplash.com/photo-1541872703-74c5e44368f9?auto=format&fit=crop&w=150&q=80', 'Government body dedicated to sustainable city infrastructure, clean air, and modern waste management.', 'New Delhi & Global', 'https://urbandevelopment.gov.in', 1),
        (1, 'Global Health Access NGO', 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=150&q=80', 'International non-profit expanding diagnostic healthcare to remote and rural areas.', 'Geneva / Boston', 'https://globalhealthaccess.org', 1),
        (1, 'AgriTech Future Foundation', 'https://images.unsplash.com/photo-1592982537447-7440770cbfc9?auto=format&fit=crop&w=150&q=80', 'Empowering smallholder farmers through modern IoT tools, drought prediction, and soil AI.', 'Nairobi / Bangalore', 'https://agritechfuture.org', 1),
        (4, 'CyberShield Alliance & University Network', 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=150&q=80', 'Collaborative consortium protecting critical civic infrastructure from ransomware and cyber threats.', 'San Francisco', 'https://cybershieldalliance.org', 1)
    ]
    cursor.executemany("INSERT INTO organizations (user_id, name, logo, description, location, website, verified) VALUES (?, ?, ?, ?, ?, ?, ?)", orgs_data)

    # 4. Problems
    problems_data = [
        (
            'Smart Water Quality Monitoring for Remote Villages',
            2,
            'Water Management',
            'Rural Communities (Global)',
            'Hard',
            'Open',
            'Over 400 rural communities lack real-time contamination detection in drinking water wells, leading to waterborne illness outbreaks.',
            'Unsafe water causes severe intestinal diseases and agricultural contamination. Manual water testing occurs only twice a year, leaving months of undetected chemical and bacterial hazards.',
            'Currently, village councils use manual paper strip testing which takes weeks to process in regional labs. Remote villages have poor cellular connectivity.',
            'Villagers, local health workers, and municipal water authorities across 120 rural districts.',
            'Solar-powered, low-cost water quality sensor nodes transmitting alerts over LoRaWAN mesh networks to a centralized dashboard.',
            json.dumps(['IoT', 'Python', 'Cloud', 'Hardware']),
            '$50,000 Innovation Grant',
            '2026-11-15',
            'water_specs_v1.pdf',
            1240, 89, 1, 1
        ),
        (
            'AI-Driven Early Warning System for Flash Floods & Landslides',
            1,
            'Disaster Management',
            'Himalayan & Coastal Regions',
            'Expert',
            'In Progress',
            'Flash floods triggered by cloudbursts cause catastrophic damage without sufficient evacuation notice for mountain towns.',
            'Topography limits traditional radar warning. High-risk zones need hyper-local river level prediction models integrated with emergency SMS sirens.',
            'Radar stations are spaced 150km apart. Small mountain streams surge in under 20 minutes without sensor coverage.',
            'Local residents, disaster management forces, first responders, and emergency transport services.',
            'Predictive AI system using satellite micro-imagery, rain gauge arrays, and hydrologic physics models to issue 45-minute advance warnings.',
            json.dumps(['AI/ML', 'Data Science', 'Python', 'Cloud']),
            '$75,000 Seed Fund + Computing Credits',
            '2026-10-30',
            'flood_risk_data.json',
            980, 114, 1, 1
        ),
        (
            'Automated E-Waste Segregation & Material Recovery Robot',
            1,
            'Waste Management',
            'Urban Municipal Hubs',
            'Medium',
            'Open',
            'Electronic waste is growing at 12% annually, yet 80% is manually handled under toxic conditions by informal workers.',
            'E-waste contains valuable metals like copper, gold, and lithium alongside toxic lead and mercury. Manual sorting poses severe health risks.',
            'Recycling centers rely on manual sorting belts where hazardous batteries are frequently missed, causing plant fires.',
            'Municipal recycling facilities, e-waste dismantlers, and environmental protection agencies.',
            'Computer vision-guided robotic sorter capable of identifying PCBs, lithium batteries, and casing plastics at 60 items/minute.',
            json.dumps(['Robotics', 'AI/ML', 'Hardware', 'UI/UX']),
            '$35,000 Pilot Deployment Support',
            '2026-12-01',
            'ewaste_recycling_schema.png',
            750, 62, 0, 1
        ),
        (
            'Solar-Powered Portable Cold Storage for Smallholder Farmers',
            3,
            'Agriculture',
            'Sub-Saharan Africa & South Asia',
            'Medium',
            'Open',
            'Up to 40% of fresh produce rots before reaching urban markets due to lack of refrigerated cold chain transport in rural farming belts.',
            'Farmers lose nearly half their potential income while food insecurity remains high. Grid electricity is unreliable or unavailable in farm clusters.',
            'Farmers sell produce at distressed prices immediately after harvest or use ice blocks that melt within hours.',
            'Smallholder horticulture farmers, cooperative societies, and regional distributors.',
            'Low-cost, modular, solar-thermal cold storage unit using thermal energy storage (phase change materials) providing 24/7 cooling at $0 grid energy cost.',
            json.dumps(['Hardware', 'Research', 'IoT']),
            '$60,000 Commercialization Prize',
            '2026-11-01',
            'agri_cold_storage.pdf',
            1430, 156, 1, 1
        ),
        (
            'Cybersecurity Defense for Municipal Hospital Networks',
            4,
            'Cybersecurity',
            'Metropolitan Cities',
            'Hard',
            'Open',
            'Public municipal hospitals are increasingly targeted by ransomware attacks, paralyzing ICU devices and electronic health records.',
            'Hospital shutdowns threaten patient lives directly. Public healthcare institutions lack dedicated SOC security budgets.',
            'Legacy Windows machines connected to patient monitors without network isolation or automated threat response.',
            'Hospital IT teams, doctors, nurses, and emergency medical personnel.',
            'Zero-trust light agent software that isolates compromised medical devices within seconds without interrupting life-critical telemetry.',
            json.dumps(['Cybersecurity', 'Cloud', 'Python', 'Java']),
            '$40,000 Deployment Grant',
            '2026-10-15',
            'hospital_sec_audit.pdf',
            610, 48, 0, 1
        ),
        (
            'Offline Interactive Digital Learning Pods for Rural Schools',
            1,
            'Education',
            'Tier 3 & Rural Districts',
            'Easy',
            'Solved',
            'Rural primary schools struggle with teacher shortages and zero internet connectivity, leaving children behind in STEM foundation skills.',
            'Digital divide prevents millions of kids from learning interactive math and science curriculum available online.',
            'Schools have limited electricity and no broadband access. Commercial tablets break easily and require internet updates.',
            'Rural school children aged 6-14 and village teachers.',
            'Solar-charged rugged mesh micro-servers loading compressed interactive lessons to ultra-low-cost e-ink tablets over local offline Wi-Fi.',
            json.dumps(['Web', 'UI/UX', 'Python', 'Hardware']),
            '$30,000 Implementation Award',
            '2026-08-20',
            'edu_pod_results.pdf',
            2100, 210, 1, 1
        )
    ]
    cursor.executemany("""
    INSERT INTO problems (title, organization_id, category, location, difficulty, status, description, why_it_matters, current_situation, target_users, expected_outcome, required_tech, budget_funding, deadline, attachments, views, supporters_count, featured, approved)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, problems_data)

    # 5. Solutions
    solutions_data = [
        (
            'AquaMesh: Solar LoRaWAN Water Quality Monitoring System',
            1, # Problem ID 1
            None,
            2, # User ID (Priya)
            'AquaMesh uses solar-powered sensor nodes deployed in village wells that communicate over long-range LoRaWAN frequencies to a central cloud alert dashboard.',
            'Sensors measure pH, turbidity, TDS, nitrate, and bacterial capacitance every 15 minutes. Data is relayed via a dual SIM micro-gateway with SMS fallback for instant contamination warnings.',
            json.dumps(['IoT', 'Python', 'Cloud', 'Hardware']),
            'Patented ultra-low power sensor coating preventing bio-fouling for up to 18 months without manual cleaning.',
            '450 rural households across 8 trial villages.',
            'Reduces waterborne outbreaks by an estimated 75% and alerts local health workers within 3 minutes of contamination.',
            'Modular hardware nodes manufactured at $45 per unit. Cloud backend supports 10,000 concurrent nodes.',
            'Phase 1: Pilot in 10 villages (Months 1-3). Phase 2: District-wide rollout (Months 4-6).',
            '$12,500 total deployment cost for 50 villages',
            'https://aquamesh.demo.app',
            'https://github.com/priyasharma/aquamesh-lora',
            'https://youtube.com/watch?v=aquamesh-demo',
            'Submitted', 42, 1
        ),
        (
            'HydroSentinel AI: Satellite & Hydrologic Sensor Fusion',
            2, # Problem ID 2
            None,
            3, # User ID (Marcus)
            'HydroSentinel combines Sentinel-1 SAR satellite imagery with ultrasonic stream level sensors to predict mountain flash floods up to 45 minutes prior.',
            'Deep learning model trained on 15 years of Himalayan monsoon hydrographs continuously analyzes rainfall rate and stream velocity to trigger village warning sirens.',
            json.dumps(['AI/ML', 'Python', 'Data Science', 'Cloud']),
            'Multi-modal neural network combining synthetic aperture radar with ground-level acoustic stream sensors.',
            'Emergency response teams and 85,000 mountain valley residents.',
            'Extends flash flood warning window from 5 minutes to 45 minutes, enabling timely evacuation.',
            'Cloud-native architecture on AWS/GCP processing 1,000 river points simultaneously.',
            '6-month field trial across 3 river basins in Uttarakhand.',
            '$28,000 compute and sensor deployment',
            'https://hydrosentinel.ai',
            'https://github.com/marcusvance/hydrosentinel-core',
            'https://youtube.com/watch?v=hydrosentinel',
            'Under Evaluation', 38, 1
        ),
        (
            'EcoChill Solar: Phase-Change Cold Pod for Farm Collectives',
            4, # Problem ID 4
            None,
            3, # User ID (Marcus)
            'EcoChill is a walk-in cold room powered by rooftop solar panels that freezes non-toxic Phase Change Material (PCM) thermal batteries during sunny hours, keeping produce at 4°C for 48 hours without grid power.',
            'Direct expansion solar chiller charges PCM thermal mass during daylight. At night, passive thermal convection maintains zero-carbon cooling.',
            json.dumps(['Hardware', 'Research', 'IoT']),
            'Salt-hydrate thermal battery system eliminating expensive lithium battery banks.',
            'Smallholder tomato, berry, and leafy green farmers.',
            'Extends produce shelf life from 2 days to 14 days; increases farmer income by 35%.',
            'Standardized 20ft container module servicing 40 farmers per hub.',
            'Deploy 5 prototype hubs in Kenya and Maharashtra.',
            '$8,500 per 20ft container unit',
            'https://ecochill.agri.org',
            'https://github.com/marcusvance/ecochill-hardware',
            'https://youtube.com/watch?v=ecochill-demo',
            'Winner', 95, 1
        ),
        (
            'EduNode E-Ink Tablet Mesh Network',
            6, # Problem ID 6
            None,
            5, # User ID (David)
            'Rugged e-ink tablet pods pre-loaded with interactive curriculum synced via offline local Wi-Fi hotspots powered by micro solar cells.',
            'Students interact with gamified math & science modules on low-power e-ink screens that last 2 weeks on a single charge.',
            json.dumps(['Web', 'UI/UX', 'Hardware']),
            'Local offline peer-to-peer sync engine using local micro-servers.',
            '1,200 primary school children in 15 offline villages.',
            'Increased STEM comprehension scores by 42% over a 6-month trial.',
            'E-ink tablet bill of materials at $22 per student device.',
            'Fully implemented in 15 pilot schools.',
            '$15,000 pilot budget',
            'https://edunode.org',
            'https://github.com/davidchen/edunode-tablet',
            'https://youtube.com/watch?v=edunode',
            'Implemented', 128, 1
        )
    ]
    cursor.executemany("""
    INSERT INTO solutions (name, problem_id, team_id, user_id, description, how_it_works, tech_used, innovation, target_users, social_impact, scalability, implementation_plan, estimated_cost, demo_url, github_url, video_url, status, supporters_count, featured)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, solutions_data)

    # 6. Challenges
    challenges_data = [
        (
            'National Clean Water Innovation Grand Challenge 2026',
            1,
            'Develop scalable sensor technology or filtration systems to bring safe drinking water to 10,000 rural villages.',
            'This global challenge invites startups, university teams, and independent engineers to pitch operational solutions for rural water security.',
            'Open to all innovators, teams, university students, startups, and research institutions worldwide.',
            'Phase 1 Proposals: Oct 15 | Prototype Review: Nov 20 | Finals: Dec 10',
            '$100,000 Total Prize Pool + $50k Deployment Grant',
            'Technical feasibility (30%), Cost per beneficiary (25%), Scalability (25%), Team expertise (20%)',
            'Open',
            'https://images.unsplash.com/photo-1541888946425-d0fbb186a5b7?auto=format&fit=crop&w=800&q=80'
        ),
        (
            'AI for Climate Resilience & Urban Disaster Mitigation',
            2,
            'Build predictive models and early warning infrastructure for urban heatwaves, floods, and landslides.',
            'Challenge seeking machine learning models using multi-spectral satellite imagery and sensor networks for climate adaptation.',
            'Developers, Data Scientists, AI Researchers, and Climate Tech Startups.',
            'Submissions close Nov 30, 2026',
            '$75,000 + Compute Credits from Cloud Partners',
            'Predictive accuracy (35%), Low latency (25%), Ease of civic deployment (20%), User experience (20%)',
            'Open',
            'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80'
        ),
        (
            'Zero Waste City Challenge: Autonomous E-Waste Sorters',
            1,
            'Create robotic or computer-vision hardware that automates sorting of electronic waste components.',
            'Looking for prototype hardware and vision models to automate recycling plant belts.',
            'Robotics engineers, hardware startups, research labs.',
            'Applications open until Dec 15, 2026',
            '$50,000 Incubator Seed Grant',
            'Sorting throughput (40%), Object classification precision (30%), Safety (30%)',
            'Coming Soon',
            'https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?auto=format&fit=crop&w=800&q=80'
        )
    ]
    cursor.executemany("""
    INSERT INTO challenges (title, organization_id, problem_statement, description, eligibility, timeline, prize_pool, evaluation_criteria, status, banner_image)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, challenges_data)

    # 7. Teams
    teams_data = [
        ('AquaMesh Collective', 'Smart LoRaWAN water sensors for sustainable communities', 2, json.dumps(['Hardware', 'Python', 'UI/UX', 'Cloud']), 'https://aquamesh.org'),
        ('EcoEngineers Lab', 'Clean energy thermal batteries & AgTech solutions', 3, json.dumps(['Research', 'Java', 'IoT', 'AI/ML']), 'https://ecoengineers.lab'),
        ('CyberDefenders Squad', 'Zero-trust security for healthcare systems', 5, json.dumps(['Cybersecurity', 'Cloud', 'Python']), 'https://cyberdefenders.dev')
    ]
    cursor.executemany("INSERT INTO teams (name, tagline, creator_id, looking_for_skills, project_url) VALUES (?, ?, ?, ?, ?)", teams_data)

    # 8. Team Members
    team_members_data = [
        (1, 2, 'Lead System Architect', 'Accepted'),
        (1, 3, 'Hardware Engineer', 'Accepted'),
        (2, 3, 'Founder & Thermal Lead', 'Accepted'),
        (2, 5, 'Software Integration', 'Accepted')
    ]
    cursor.executemany("INSERT INTO team_members (team_id, user_id, role, status) VALUES (?, ?, ?, ?)", team_members_data)

    # 9. Success Stories
    stories_data = [
        (
            'Solar Micro-Grids for Mountain Schools',
            'HelioPod Portable Mesh Solar Grid',
            'SunPower Collective',
            'Department of Rural Education',
            'Education & Energy',
            'Deployed 45 modular solar micro-grids to off-grid Himalayan school pods, giving 6,000+ students access to computer labs and night study lighting.',
            json.dumps(['6,000+ Students Benefited', '100% Carbon Free Power', '45 Mountain Villages Reached', '99.4% Uptime Recorded']),
            'Prior to installation, schools operated with zero electricity. Now students score 38% higher in standardized STEM examinations.',
            'https://images.unsplash.com/photo-1509099836639-18ba1795216d?auto=format&fit=crop&w=800&q=80'
        ),
        (
            'AI Agricultural Soil Health Diagnosis',
            'SoilVision Mobile NIR Spectrometer',
            'AgriTech Innovators',
            'National Farmers Federation',
            'Agriculture & AI',
            'Handheld near-infrared scanner linked to a mobile AI app providing instant soil nitrogen, phosphorus, and pH readings in under 30 seconds.',
            json.dumps(['18,000+ Soil Tests Conducted', '32% Reduction in Fertilizer Cost', '24% Crop Yield Increase', '120 Farm Cooperatives']),
            'Farmers saved an average of $240 per harvest by eliminating unnecessary chemical fertilizer overuse.',
            'https://images.unsplash.com/photo-1592982537447-7440770cbfc9?auto=format&fit=crop&w=800&q=80'
        )
    ]
    cursor.executemany("""
    INSERT INTO success_stories (problem_title, solution_name, team_name, organization, category, description, metrics, impact_summary, image_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, stories_data)

    # 10. Initial Notifications
    notifications_data = [
        (2, 'Solution Upvoted!', 'Your solution AquaMesh received 5 new supporters.', 'success', 0),
        (2, 'Challenge Launched', 'National Clean Water Grand Challenge 2026 is now accepting applications!', 'challenge', 0),
        (3, 'Team Invitation', 'You were invited to join CyberDefenders Squad as IoT Integration Specialist.', 'info', 0)
    ]
    cursor.executemany("INSERT INTO notifications (user_id, title, message, type, read) VALUES (?, ?, ?, ?, ?)", notifications_data)

    conn.commit()
    print("Database seeding completed successfully.")

if __name__ == "__main__":
    init_db()
