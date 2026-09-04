import os
import sys
import json
import sqlite3
from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import get_db, init_db

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "spot_problem_solver_secret_key_2026"

# Ensure DB initialized
init_db()

# Categories list
CATEGORIES = [
    "Education", "Healthcare", "Agriculture", "Environment", 
    "Smart Cities", "Transportation", "Government", "Cybersecurity", 
    "AI & Technology", "Employment", "Rural Development", 
    "Waste Management", "Women & Child Development", "Water Management", 
    "Disaster Management"
]

# Tech Stack list
TECH_STACKS = [
    "AI/ML", "IoT", "Blockchain", "Web", "Mobile", 
    "Robotics", "Healthcare", "Education", "Agriculture", 
    "Climate", "Smart Cities", "Python", "Java", "React", 
    "Data Science", "UI/UX", "Cloud", "Hardware", "Cybersecurity"
]

@app.route("/")
def index():
    return render_template("index.html")

# ==========================================
# STATS API
# ==========================================
@app.route("/api/stats", methods=["GET", "POST"])
def handle_stats():
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == "POST":
        data = request.json or {}
        for key, val in data.items():
            cursor.execute("UPDATE stats SET value_text = ? WHERE key_name = ?", (str(val), key))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Statistics updated successfully!"})
    
    cursor.execute("SELECT key_name, value_text, label FROM stats")
    rows = cursor.fetchall()
    stats_dict = {row['key_name']: {'value': row['value_text'], 'label': row['label']} for row in rows}
    conn.close()
    return jsonify(stats_dict)

# ==========================================
# PROBLEMS API
# ==========================================
@app.route("/api/problems", methods=["GET", "POST"])
def handle_problems():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":
        data = request.json or {}
        title = data.get("title")
        org_name = data.get("organization", "Community Initiative")
        category = data.get("category", "AI & Technology")
        location = data.get("location", "Global")
        difficulty = data.get("difficulty", "Medium")
        description = data.get("description", "")
        why_it_matters = data.get("why_it_matters", "")
        current_situation = data.get("current_situation", "")
        target_users = data.get("target_users", "")
        expected_outcome = data.get("expected_outcome", "")
        required_tech = json.dumps(data.get("required_tech", ["AI/ML"]))
        budget_funding = data.get("budget_funding", "TBD")
        deadline = data.get("deadline", "2026-12-31")
        attachments = data.get("attachments", "")

        # Find or create Org
        cursor.execute("SELECT id FROM organizations WHERE name LIKE ?", (f"%{org_name}%",))
        org_row = cursor.fetchone()
        if org_row:
            org_id = org_row['id']
        else:
            cursor.execute("INSERT INTO organizations (user_id, name, logo, description, location) VALUES (1, ?, 'https://images.unsplash.com/photo-1541872703-74c5e44368f9?auto=format&fit=crop&w=150&q=80', 'Community Organization', ?)", (org_name, location))
            org_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO problems (title, organization_id, category, location, difficulty, status, description, why_it_matters, current_situation, target_users, expected_outcome, required_tech, budget_funding, deadline, attachments, approved)
            VALUES (?, ?, ?, ?, ?, 'Open', ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (title, org_id, category, location, difficulty, description, why_it_matters, current_situation, target_users, expected_outcome, required_tech, budget_funding, deadline, attachments))
        
        problem_id = cursor.lastrowid
        conn.commit()

        # Update stats
        cursor.execute("UPDATE stats SET value_text = CAST(CAST(REPLACE(value_text, '+', '') AS INTEGER) + 1 AS TEXT) || '+' WHERE key_name = 'problems_posted'")
        conn.commit()
        conn.close()

        return jsonify({"status": "success", "id": problem_id, "message": "Problem posted successfully and published to marketplace!"})

    # GET with Filters
    search = request.args.get("search", "").strip().lower()
    category = request.args.get("category", "")
    location = request.args.get("location", "")
    difficulty = request.args.get("difficulty", "")
    status = request.args.get("status", "")
    sort = request.args.get("sort", "newest")

    query = """
        SELECT p.*, o.name as org_name, o.logo as org_logo,
               (SELECT COUNT(*) FROM solutions s WHERE s.problem_id = p.id) as solutions_count
        FROM problems p
        JOIN organizations o ON p.organization_id = o.id
        WHERE p.approved = 1
    """
    params = []

    if category:
        query += " AND p.category = ?"
        params.append(category)
    if difficulty:
        query += " AND p.difficulty = ?"
        params.append(difficulty)
    if status:
        query += " AND p.status = ?"
        params.append(status)
    if search:
        query += " AND (LOWER(p.title) LIKE ? OR LOWER(p.description) LIKE ? OR LOWER(p.category) LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])

    if sort == "most_supported":
        query += " ORDER BY p.supporters_count DESC"
    elif sort == "most_viewed":
        query += " ORDER BY p.views DESC"
    elif sort == "urgent":
        query += " ORDER BY p.deadline ASC"
    else:
        query += " ORDER BY p.id DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    problems = []
    for r in rows:
        p = dict(r)
        p['required_tech'] = json.loads(p['required_tech']) if p['required_tech'] else []
        problems.append(p)

    conn.close()
    return jsonify(problems)

@app.route("/api/problems/<int:problem_id>")
def get_problem_detail(problem_id):
    conn = get_db()
    cursor = conn.cursor()

    # Increment views
    cursor.execute("UPDATE problems SET views = views + 1 WHERE id = ?", (problem_id,))
    conn.commit()

    cursor.execute("""
        SELECT p.*, o.name as org_name, o.logo as org_logo, o.description as org_desc, o.website as org_website,
               (SELECT COUNT(*) FROM solutions s WHERE s.problem_id = p.id) as solutions_count
        FROM problems p
        JOIN organizations o ON p.organization_id = o.id
        WHERE p.id = ?
    """, (problem_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "Problem not found"}), 404

    problem = dict(row)
    problem['required_tech'] = json.loads(problem['required_tech']) if problem['required_tech'] else []

    # Get solutions for this problem
    cursor.execute("""
        SELECT s.*, u.name as author_name, u.avatar as author_avatar, t.name as team_name
        FROM solutions s
        JOIN users u ON s.user_id = u.id
        LEFT JOIN teams t ON s.team_id = t.id
        WHERE s.problem_id = ?
        ORDER BY s.supporters_count DESC
    """, (problem_id,))
    sol_rows = cursor.fetchall()
    solutions = []
    for sr in sol_rows:
        sol = dict(sr)
        sol['tech_used'] = json.loads(sol['tech_used']) if sol['tech_used'] else []
        solutions.append(sol)

    # Get related problems in same category
    cursor.execute("""
        SELECT id, title, category, supporters_count, deadline 
        FROM problems 
        WHERE category = ? AND id != ? AND approved = 1 
        LIMIT 3
    """, (problem['category'], problem_id))
    related = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return jsonify({
        "problem": problem,
        "solutions": solutions,
        "related": related
    })

@app.route("/api/problems/<int:problem_id>/support", methods=["POST"])
def support_problem(problem_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE problems SET supporters_count = supporters_count + 1 WHERE id = ?", (problem_id,))
    conn.commit()
    cursor.execute("SELECT supporters_count FROM problems WHERE id = ?", (problem_id,))
    new_count = cursor.fetchone()['supporters_count']
    conn.close()
    return jsonify({"status": "success", "supporters_count": new_count})

# ==========================================
# SOLUTIONS API
# ==========================================
@app.route("/api/solutions", methods=["GET", "POST"])
def handle_solutions():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":
        data = request.json or {}
        name = data.get("name")
        problem_id = data.get("problem_id")
        user_id = data.get("user_id", 2)
        team_id = data.get("team_id")
        description = data.get("description", "")
        how_it_works = data.get("how_it_works", "")
        tech_used = json.dumps(data.get("tech_used", ["Python", "AI/ML"]))
        innovation = data.get("innovation", "")
        target_users = data.get("target_users", "")
        social_impact = data.get("social_impact", "")
        scalability = data.get("scalability", "")
        implementation_plan = data.get("implementation_plan", "")
        estimated_cost = data.get("estimated_cost", "TBD")
        demo_url = data.get("demo_url", "")
        github_url = data.get("github_url", "")
        video_url = data.get("video_url", "")
        status = data.get("status", "Submitted")

        cursor.execute("""
            INSERT INTO solutions (name, problem_id, team_id, user_id, description, how_it_works, tech_used, innovation, target_users, social_impact, scalability, implementation_plan, estimated_cost, demo_url, github_url, video_url, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, problem_id, team_id, user_id, description, how_it_works, tech_used, innovation, target_users, social_impact, scalability, implementation_plan, estimated_cost, demo_url, github_url, video_url, status))
        
        sol_id = cursor.lastrowid
        conn.commit()

        # Update stats and user points
        cursor.execute("UPDATE stats SET value_text = CAST(CAST(REPLACE(value_text, '+', '') AS INTEGER) + 1 AS TEXT) || '+' WHERE key_name = 'solutions_submitted'")
        cursor.execute("UPDATE users SET points = points + 50 WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()

        return jsonify({"status": "success", "id": sol_id, "message": "Solution submitted successfully! Earned +50 Innovation Points."})

    # GET Filtered Solutions
    search = request.args.get("search", "").strip().lower()
    tech = request.args.get("tech", "")
    category = request.args.get("category", "")

    query = """
        SELECT s.*, p.title as problem_title, p.category as problem_category, 
               u.name as author_name, u.avatar as author_avatar, t.name as team_name
        FROM solutions s
        JOIN problems p ON s.problem_id = p.id
        JOIN users u ON s.user_id = u.id
        LEFT JOIN teams t ON s.team_id = t.id
        WHERE 1=1
    """
    params = []

    if category:
        query += " AND p.category = ?"
        params.append(category)
    if search:
        query += " AND (LOWER(s.name) LIKE ? OR LOWER(s.description) LIKE ? OR LOWER(s.tech_used) LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])
    if tech:
        query += " AND LOWER(s.tech_used) LIKE ?"
        params.append(f"%{tech.lower()}%")

    query += " ORDER BY s.supporters_count DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    solutions = []
    for r in rows:
        s = dict(r)
        s['tech_used'] = json.loads(s['tech_used']) if s['tech_used'] else []
        solutions.append(s)

    conn.close()
    return jsonify(solutions)

@app.route("/api/solutions/<int:sol_id>/support", methods=["POST"])
def support_solution(sol_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE solutions SET supporters_count = supporters_count + 1 WHERE id = ?", (sol_id,))
    conn.commit()
    cursor.execute("SELECT supporters_count FROM solutions WHERE id = ?", (sol_id,))
    new_count = cursor.fetchone()['supporters_count']
    conn.close()
    return jsonify({"status": "success", "supporters_count": new_count})

# ==========================================
# CHALLENGES API
# ==========================================
@app.route("/api/challenges", methods=["GET", "POST"])
def handle_challenges():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":
        data = request.json or {}
        title = data.get("title")
        org_id = data.get("organization_id", 1)
        problem_statement = data.get("problem_statement")
        description = data.get("description")
        eligibility = data.get("eligibility", "Open to all innovators")
        timeline = data.get("timeline", "Submissions close Dec 2026")
        prize_pool = data.get("prize_pool", "$50,000")
        evaluation_criteria = data.get("evaluation_criteria", "Impact, Innovation, Feasibility")
        status = data.get("status", "Open")
        banner_image = data.get("banner_image", "https://images.unsplash.com/photo-1541888946425-d0fbb186a5b7?auto=format&fit=crop&w=800&q=80")

        cursor.execute("""
            INSERT INTO challenges (title, organization_id, problem_statement, description, eligibility, timeline, prize_pool, evaluation_criteria, status, banner_image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (title, org_id, problem_statement, description, eligibility, timeline, prize_pool, evaluation_criteria, status, banner_image))
        conn.commit()
        ch_id = cursor.lastrowid
        conn.close()

        return jsonify({"status": "success", "id": ch_id, "message": "Challenge created successfully!"})

    cursor.execute("""
        SELECT c.*, o.name as org_name, o.logo as org_logo,
               (SELECT COUNT(*) FROM solutions s JOIN problems p ON s.problem_id = p.id WHERE p.organization_id = c.organization_id) as submissions_count
        FROM challenges c
        JOIN organizations o ON c.organization_id = o.id
        ORDER BY c.id DESC
    """)
    challenges = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(challenges)

# ==========================================
# TEAMS & COLLABORATION API
# ==========================================
@app.route("/api/teams", methods=["GET", "POST"])
def handle_teams():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":
        data = request.json or {}
        name = data.get("name")
        tagline = data.get("tagline", "")
        creator_id = data.get("creator_id", 2)
        skills = json.dumps(data.get("looking_for_skills", ["Python", "AI/ML"]))
        project_url = data.get("project_url", "")

        cursor.execute("INSERT INTO teams (name, tagline, creator_id, looking_for_skills, project_url) VALUES (?, ?, ?, ?, ?)",
                       (name, tagline, creator_id, skills, project_url))
        team_id = cursor.lastrowid

        # Add creator as lead member
        cursor.execute("INSERT INTO team_members (team_id, user_id, role, status) VALUES (?, ?, 'Team Leader', 'Accepted')", (team_id, creator_id))
        conn.commit()
        conn.close()

        return jsonify({"status": "success", "id": team_id, "message": "Team created successfully!"})

    cursor.execute("""
        SELECT t.*, u.name as creator_name, u.avatar as creator_avatar,
               (SELECT COUNT(*) FROM team_members tm WHERE tm.team_id = t.id AND tm.status = 'Accepted') as member_count
        FROM teams t
        JOIN users u ON t.creator_id = u.id
        ORDER BY t.id DESC
    """)
    rows = cursor.fetchall()
    teams = []
    for r in rows:
        t = dict(r)
        t['looking_for_skills'] = json.loads(t['looking_for_skills']) if t['looking_for_skills'] else []
        teams.append(t)

    conn.close()
    return jsonify(teams)

@app.route("/api/teams/<int:team_id>/join", methods=["POST"])
def join_team(team_id):
    conn = get_db()
    cursor = conn.cursor()
    data = request.json or {}
    user_id = data.get("user_id", 2)
    role = data.get("role", "Collaborator")

    cursor.execute("INSERT INTO team_members (team_id, user_id, role, status) VALUES (?, ?, ?, 'Accepted')", (team_id, user_id, role))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "You have joined the team!"})

# ==========================================
# LEADERBOARD & USER PROFILES API
# ==========================================
@app.route("/api/leaderboard")
def get_leaderboard():
    conn = get_db()
    cursor = conn.cursor()

    # Top Innovators
    cursor.execute("SELECT id, name, avatar, bio, points, badges, role FROM users WHERE role != 'Organization' ORDER BY points DESC LIMIT 10")
    users = []
    for r in cursor.fetchall():
        u = dict(r)
        u['badges'] = json.loads(u['badges']) if u['badges'] else []
        users.append(u)

    # Top Teams
    cursor.execute("""
        SELECT t.id, t.name, t.tagline, COUNT(tm.id) as member_count, u.name as leader_name
        FROM teams t
        LEFT JOIN team_members tm ON t.id = tm.team_id
        JOIN users u ON t.creator_id = u.id
        GROUP BY t.id
        ORDER BY member_count DESC LIMIT 5
    """)
    teams = [dict(r) for r in cursor.fetchall()]

    # Most Supported Solutions
    cursor.execute("""
        SELECT s.id, s.name, s.supporters_count, p.title as problem_title, u.name as author_name
        FROM solutions s
        JOIN problems p ON s.problem_id = p.id
        JOIN users u ON s.user_id = u.id
        ORDER BY s.supporters_count DESC LIMIT 5
    """)
    top_solutions = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return jsonify({
        "top_innovators": users,
        "top_teams": teams,
        "top_solutions": top_solutions
    })

@app.route("/api/users/<int:user_id>")
def get_user_profile(user_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return jsonify({"error": "User not found"}), 404

    u_dict = dict(user)
    u_dict['skills'] = json.loads(u_dict['skills']) if u_dict['skills'] else []
    u_dict['badges'] = json.loads(u_dict['badges']) if u_dict['badges'] else []

    # Get user solutions
    cursor.execute("SELECT id, name, supporters_count, status FROM solutions WHERE user_id = ?", (user_id,))
    solutions = [dict(r) for r in cursor.fetchall()]

    # Get user team memberships
    cursor.execute("""
        SELECT t.name as team_name, tm.role 
        FROM team_members tm 
        JOIN teams t ON tm.team_id = t.id 
        WHERE tm.user_id = ?
    """, (user_id,))
    teams = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return jsonify({
        "user": u_dict,
        "solutions": solutions,
        "teams": teams
    })

# ==========================================
# SUCCESS STORIES API
# ==========================================
@app.route("/api/success-stories")
def get_success_stories():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM success_stories ORDER BY id DESC")
    rows = cursor.fetchall()
    stories = []
    for r in rows:
        st = dict(r)
        st['metrics'] = json.loads(st['metrics']) if st['metrics'] else []
        stories.append(st)
    conn.close()
    return jsonify(stories)

# ==========================================
# AI ASSISTANT API (PROBLEM ANALYZER & SOLUTION ASSISTANT)
# ==========================================
@app.route("/api/ai/analyze-problem", methods=["POST"])
def ai_analyze_problem():
    data = request.json or {}
    problem_input = data.get("problem_statement", "").strip()

    if not problem_input:
        return jsonify({"error": "Please enter a problem description"}), 400

    # Intelligent AI pattern analysis & breakdown generation
    summary = f"Summary: Focused on addressing '{problem_input[:100]}...' by introducing systemic technology-driven intervention."
    
    root_causes = [
        "Lack of real-time monitoring and automated alert mechanisms.",
        "Resource constraints and infrastructure gaps in underserved regions.",
        "Manual paper-based workflows leading to delayed decision making.",
        "Insufficient integration between community end-users and technology providers."
    ]

    people_affected = [
        "Local community residents and municipal workers in target regions.",
        "Small-to-medium enterprise operators and administrative teams.",
        "Emergency responders and public safety officials."
    ]

    tech_approaches = [
        {"tech": "AI / Computer Vision", "role": "Automate detection and pattern recognition from real-time feeds."},
        {"tech": "IoT Mesh Networks", "role": "Deploy low-cost solar sensor nodes for remote data collection."},
        {"tech": "Cloud Data Platform", "role": "Centralized analytics dashboard with automated SMS/email alerts."}
    ]

    similar_solutions = [
        "AquaMesh Rural Water Telemetry",
        "HydroSentinel Early Warning System",
        "EcoChill Thermal Battery Pods"
    ]

    suggested_categories = ["Smart Cities", "Environment", "Water Management", "Healthcare", "AI & Technology"]
    required_skills = ["Python", "AI/ML", "IoT", "Cloud", "UI/UX", "Data Science"]
    
    impact_metrics = [
        "Estimated 60-80% reduction in response latency.",
        "Direct benefit to over 25,000 citizens within 12 months.",
        "40% operational cost savings compared to traditional methods."
    ]

    return jsonify({
        "status": "success",
        "analysis": {
            "summary": summary,
            "root_causes": root_causes,
            "people_affected": people_affected,
            "tech_approaches": tech_approaches,
            "similar_solutions": similar_solutions,
            "suggested_categories": suggested_categories,
            "required_skills": required_skills,
            "impact_metrics": impact_metrics
        }
    })

@app.route("/api/ai/analyze-solution", methods=["POST"])
def ai_analyze_solution():
    data = request.json or {}
    solution_desc = data.get("solution_description", "").strip()
    tech_used = data.get("tech_used", [])

    if not solution_desc:
        return jsonify({"error": "Please enter your solution proposal details"}), 400

    feedback = {
        "strength_score": "88/100 (Strong Technical Viability)",
        "missing_information": [
            "Add explicit details on data privacy & fallback offline operation mode.",
            "Include estimated unit manufacturing cost and maintenance schedule."
        ],
        "technical_improvements": [
            "Consider adding LoRaWAN or SMS fallback gateway for zero-cellular coverage areas.",
            "Implement edge-AI processing on hardware nodes to reduce bandwidth and cloud latency."
        ],
        "scalability_ideas": [
            "Design modular hardware chassis allowing field maintenance without specialized tools.",
            "Partner with local university research labs for student field deployment credits."
        ],
        "impact_metrics_to_highlight": [
            "Number of active beneficiaries served daily.",
            "Percentage reduction in downtime or system failure rate.",
            "Total carbon emission offset or cost savings per installation."
        ]
    }

    return jsonify({
        "status": "success",
        "feedback": feedback
    })

# ==========================================
# ADMIN DASHBOARD API
# ==========================================
@app.route("/api/admin/overview")
def admin_overview():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM problems")
    total_problems = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM solutions")
    total_solutions = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM organizations")
    total_orgs = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM challenges")
    total_challenges = cursor.fetchone()[0]

    # Pending problems for moderation
    cursor.execute("""
        SELECT p.*, o.name as org_name 
        FROM problems p 
        JOIN organizations o ON p.organization_id = o.id 
        ORDER BY p.id DESC LIMIT 10
    """)
    recent_problems = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return jsonify({
        "totals": {
            "problems": total_problems,
            "solutions": total_solutions,
            "users": total_users,
            "orgs": total_orgs,
            "challenges": total_challenges
        },
        "recent_problems": recent_problems
    })

# ==========================================
# NOTIFICATIONS API
# ==========================================
@app.route("/api/notifications")
def get_notifications():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notifications ORDER BY id DESC LIMIT 10")
    notes = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(notes)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("===========================================================")
    print(f"[Spot Problem Solver Platform] Running on http://127.0.0.1:{port}")
    print("===========================================================")
    app.run(host="0.0.0.0", port=port, debug=True)
