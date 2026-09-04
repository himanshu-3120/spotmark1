import base64
import json
import streamlit as st

from utils import (
    ResumeData, WorkExperience, Education, Project, Certification, get_sample_resume
)
from ai_engine import AIEngine
from pdf_generator import PDFResumeGenerator

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="AI Resumix Pro | Professional CV & Resume Builder",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Injected CSS for Glassmorphism & High Aesthetic Visuals
CUSTOM_CSS = """
<style>
    /* Dark glassmorphism & gradient themes */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        color: #f8fafc;
    }
    
    /* Header Container */
    .header-box {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    .header-title {
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: 8px;
    }
    
    .header-subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
    }
    
    /* Card Container */
    .glass-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* Custom Metric Badges */
    .metric-badge {
        display: inline-block;
        background: rgba(99, 102, 241, 0.2);
        border: 1px solid rgba(99, 102, 241, 0.4);
        color: #a5b4fc;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 4px;
    }
    
    .missing-badge {
        display: inline-block;
        background: rgba(239, 68, 68, 0.2);
        border: 1px solid rgba(239, 68, 68, 0.4);
        color: #fca5a5;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 4px;
    }
    
    /* Streamlit Buttons Styling */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Initialize Session State
if "resume" not in st.session_state:
    st.session_state.resume = get_sample_resume()

# Header Banner
st.markdown("""
<div class="header-box">
    <div class="header-title">📄 AI Resumix Pro</div>
    <div class="header-subtitle">Build, Enhance & Tailor Professional CVs Powered by Generative AI</div>
</div>
""", unsafe_allow_html=True)

# Sidebar - Settings & Actions
with st.sidebar:
    st.image("https://img.icons8.com/isometric/96/resume.png", width=70)
    st.title("⚙️ AI & Layout Settings")
    
    provider = st.selectbox(
        "AI Intelligence Mode",
        ["Smart Offline (No Key Needed)", "Google Gemini", "OpenAI"],
        help="Smart Offline mode works immediately without an API key using built-in heuristic algorithms."
    )
    
    api_key = ""
    if provider in ["Google Gemini", "OpenAI"]:
        api_key = st.text_input(
            f"Enter {provider} API Key",
            type="password",
            help="Your API key stays strictly in memory for this session."
        )
    
    st.divider()
    st.subheader("🎨 PDF Visual Theme")
    pdf_theme = st.selectbox(
        "Select Resume Theme",
        ["Modern Executive", "Creative Tech", "Minimalist Classic"]
    )
    
    st.divider()
    st.subheader("⚡ Quick Actions")
    col_s1, col_s2 = st.columns(2)
    if col_s1.button("📋 Load Sample", use_container_width=True):
        st.session_state.resume = get_sample_resume()
        st.rerun()
    if col_s2.button("🗑️ Clear Form", use_container_width=True):
        st.session_state.resume = ResumeData()
        st.rerun()

    st.markdown("---")
    st.caption("🚀 Created for LinkedIn Portfolio Showcase")

# Initialize AI Engine
ai_engine = AIEngine(provider=provider, api_key=api_key)

# Main Navigation Tabs
tab_editor, tab_ai, tab_ats, tab_export = st.tabs([
    "📝 Interactive Resume Editor",
    "✨ AI Enhancement Studio",
    "🎯 ATS Keyword & Score Analyzer",
    "📄 PDF Download & JSON Sync"
])

# ---------------------------------------------------------
# TAB 1: INTERACTIVE RESUME EDITOR
# ---------------------------------------------------------
with tab_editor:
    res = st.session_state.resume
    
    st.markdown("### 👤 Personal Details")
    c1, c2, c3 = st.columns(3)
    res.full_name = c1.text_input("Full Name", value=res.full_name)
    res.job_title = c2.text_input("Target Job Title", value=res.job_title)
    res.email = c3.text_input("Email Address", value=res.email)
    
    c4, c5, c6 = st.columns(3)
    res.phone = c4.text_input("Phone Number", value=res.phone)
    res.location = c5.text_input("Location", value=res.location)
    res.linkedin = c6.text_input("LinkedIn Profile URL", value=res.linkedin)
    
    c7, c8 = st.columns(2)
    res.github = c7.text_input("GitHub Profile URL", value=res.github)
    res.portfolio = c8.text_input("Portfolio Website URL", value=res.portfolio)
    
    st.markdown("---")
    st.markdown("### 📝 Professional Summary")
    res.summary = st.text_area("Executive Summary", value=res.summary, height=110)
    
    st.markdown("---")
    st.markdown("### 🛠️ Core Competencies & Skills")
    skills_text = st.text_input("Skills (comma-separated)", value=", ".join(res.skills))
    res.skills = [s.strip() for s in skills_text.split(",") if s.strip()]
    
    st.markdown("---")
    st.markdown("### 💼 Work Experience")
    
    # Add new experience button
    if st.button("➕ Add Work Experience"):
        res.experiences.append(WorkExperience(company="New Company", role="Role Title"))
        st.rerun()

    exp_to_remove = None
    for idx, exp in enumerate(res.experiences):
        with st.expander(f"🏢 {exp.role or 'Position'} at {exp.company or 'Company'}", expanded=(idx == 0)):
            cx1, cx2, cx3 = st.columns(3)
            exp.company = cx1.text_input(f"Company", value=exp.company, key=f"exp_comp_{idx}")
            exp.role = cx2.text_input(f"Role Title", value=exp.role, key=f"exp_role_{idx}")
            exp.location = cx3.text_input(f"Location", value=exp.location, key=f"exp_loc_{idx}")
            
            cd1, cd2 = st.columns(2)
            exp.start_date = cd1.text_input(f"Start Date", value=exp.start_date, key=f"exp_start_{idx}")
            exp.end_date = cd2.text_input(f"End Date", value=exp.end_date, key=f"exp_end_{idx}")
            
            bullets_str = "\n".join(exp.bullets)
            updated_bullets = st.text_area(
                "Accomplishment Bullets (one per line)",
                value=bullets_str,
                height=100,
                key=f"exp_bullets_{idx}"
            )
            exp.bullets = [b.strip() for b in updated_bullets.split("\n") if b.strip()]
            
            if st.button(f"🗑️ Delete Item", key=f"del_exp_{idx}"):
                exp_to_remove = idx
                
    if exp_to_remove is not None:
        res.experiences.pop(exp_to_remove)
        st.rerun()

    st.markdown("---")
    st.markdown("### 🎓 Education & Certifications")
    
    col_edu, col_cert = st.columns(2)
    with col_edu:
        st.subheader("Education")
        if st.button("➕ Add Education"):
            res.education.append(Education(institution="University Name", degree="Degree"))
            st.rerun()
            
        edu_to_remove = None
        for idx, edu in enumerate(res.education):
            with st.expander(f"🎓 {edu.degree} - {edu.institution}", expanded=(idx == 0)):
                edu.institution = st.text_input("Institution", value=edu.institution, key=f"edu_inst_{idx}")
                edu.degree = st.text_input("Degree", value=edu.degree, key=f"edu_deg_{idx}")
                edu.field_of_study = st.text_input("Field of Study", value=edu.field_of_study, key=f"edu_field_{idx}")
                c_e1, c_e2 = st.columns(2)
                edu.start_date = c_e1.text_input("Start Date", value=edu.start_date, key=f"edu_s_{idx}")
                edu.end_date = c_e2.text_input("End Date", value=edu.end_date, key=f"edu_e_{idx}")
                edu.gpa = st.text_input("GPA", value=edu.gpa, key=f"edu_gpa_{idx}")
                if st.button("Delete Education", key=f"del_edu_{idx}"):
                    edu_to_remove = idx
        if edu_to_remove is not None:
            res.education.pop(edu_to_remove)
            st.rerun()

    with col_cert:
        st.subheader("Certifications")
        if st.button("➕ Add Certification"):
            res.certifications.append(Certification(name="Certification Title"))
            st.rerun()
            
        cert_to_remove = None
        for idx, cert in enumerate(res.certifications):
            with st.expander(f"📜 {cert.name}", expanded=False):
                cert.name = st.text_input("Certification Name", value=cert.name, key=f"cert_n_{idx}")
                cert.issuer = st.text_input("Issuer", value=cert.issuer, key=f"cert_i_{idx}")
                cert.year = st.text_input("Year", value=cert.year, key=f"cert_y_{idx}")
                if st.button("Delete Certification", key=f"del_cert_{idx}"):
                    cert_to_remove = idx
        if cert_to_remove is not None:
            res.certifications.pop(cert_to_remove)
            st.rerun()

# ---------------------------------------------------------
# TAB 2: AI ENHANCEMENT STUDIO
# ---------------------------------------------------------
with tab_ai:
    st.markdown("## ✨ AI Enhancement Studio")
    st.info(f"Currently active AI Engine: **{provider}**")
    
    col_ai1, col_ai2 = st.columns(2)
    
    with col_ai1:
        st.subheader("1. AI Executive Summary Generator")
        st.write("Generate a high-impact, tailored executive summary based on your profile.")
        if st.button("🚀 Generate AI Summary", use_container_width=True):
            exp_text = "; ".join([f"{e.role} at {e.company}" for e in res.experiences])
            with st.spinner("AI is crafting your summary..."):
                gen_summary = ai_engine.generate_summary(
                    name=res.full_name,
                    job_title=res.job_title,
                    skills=res.skills,
                    experience_summary=exp_text
                )
                st.session_state["gen_summary_temp"] = gen_summary
        
        if "gen_summary_temp" in st.session_state:
            st.success("Generated Summary:")
            st.write(st.session_state["gen_summary_temp"])
            if st.button("✅ Apply to Resume Summary"):
                res.summary = st.session_state["gen_summary_temp"]
                st.success("Summary updated!")
                st.rerun()

    with col_ai2:
        st.subheader("2. AI Bullet Point Rewriter")
        st.write("Transform weak bullet points into metric-driven STAR accomplishment statements.")
        
        raw_bullet = st.text_area(
            "Paste bullet point to enhance",
            placeholder="e.g. Responsible for managing the company database and building APIs."
        )
        if st.button("✨ Polish & Enhance Bullet", use_container_width=True):
            if raw_bullet.strip():
                with st.spinner("Rewriting with active verbs & metrics..."):
                    enhanced = ai_engine.enhance_bullet_point(raw_bullet, target_role=res.job_title)
                    st.session_state["enhanced_bullet_temp"] = enhanced
            else:
                st.warning("Please enter a bullet point to enhance.")
                
        if "enhanced_bullet_temp" in st.session_state:
            st.success("High-Impact Result:")
            st.code(st.session_state["enhanced_bullet_temp"], language="text")

    st.markdown("---")
    st.subheader("3. AI Skill Recommender")
    st.write("Get instant skill suggestions tailored to your target job title.")
    if st.button("💡 Recommend Industry Skills"):
        with st.spinner("Searching skill taxonomies..."):
            suggested = ai_engine.suggest_skills(res.job_title)
            st.session_state["suggested_skills"] = suggested

    if "suggested_skills" in st.session_state:
        st.write("**Recommended Skills:**")
        badges_html = "".join([f'<span class="metric-badge">{s}</span>' for s in st.session_state["suggested_skills"]])
        st.markdown(badges_html, unsafe_allow_html=True)
        if st.button("➕ Merge Suggested Skills into Resume"):
            new_skills = list(set(res.skills + st.session_state["suggested_skills"]))
            res.skills = new_skills
            st.success("Skills merged successfully!")
            st.rerun()

# ---------------------------------------------------------
# TAB 3: ATS KEYWORD & SCORE ANALYZER
# ---------------------------------------------------------
with tab_ats:
    st.markdown("## 🎯 ATS Keyword & Match Analyzer")
    st.write("Paste a target job posting description to evaluate ATS match percentage and identify missing keywords.")
    
    job_desc = st.text_area("Paste Target Job Description (JD)", height=160, placeholder="Paste the job advertisement responsibilities and requirements here...")
    
    if st.button("🔍 Run ATS Match Analysis", use_container_width=True):
        # Build composite resume text
        exp_text = " ".join([" ".join(e.bullets) for e in res.experiences])
        full_res_text = f"{res.job_title} {res.summary} {' '.join(res.skills)} {exp_text}"
        
        with st.spinner("Analyzing keyword frequency & semantic density..."):
            ats_res = ai_engine.analyze_ats(full_res_text, job_desc)
            st.session_state["ats_result"] = ats_res

    if "ats_result" in st.session_state:
        ats = st.session_state["ats_result"]
        
        col_m1, col_m2 = st.columns([1, 2])
        with col_m1:
            st.metric("ATS Compatibility Score", f"{ats['score']}%")
            st.progress(ats['score'] / 100.0)
        with col_m2:
            st.markdown(f"**Analysis Summary**: {ats['summary']}")

        st.markdown("### 🟢 Matched Keywords")
        if ats["matched_keywords"]:
            matched_html = "".join([f'<span class="metric-badge">{w}</span>' for w in ats["matched_keywords"]])
            st.markdown(matched_html, unsafe_allow_html=True)
        else:
            st.write("No exact key terms matched yet.")

        st.markdown("### 🔴 Missing Keywords (Recommended to Add)")
        if ats["missing_keywords"]:
            missing_html = "".join([f'<span class="missing-badge">{w}</span>' for w in ats["missing_keywords"]])
            st.markdown(missing_html, unsafe_allow_html=True)
            if st.button("➕ Auto-Add Missing Keywords to Skills"):
                res.skills = list(set(res.skills + ats["missing_keywords"]))
                st.success("Added missing keywords to your skill list!")
                st.rerun()

        st.markdown("### 💡 Optimization Tips")
        for tip in ats["tips"]:
            st.write(f"- {tip}")

# ---------------------------------------------------------
# TAB 4: PDF DOWNLOAD & JSON SYNC
# ---------------------------------------------------------
with tab_export:
    st.markdown("## 📄 Export & Sync Studio")
    
    col_p1, col_p2 = st.columns([1, 1])
    
    pdf_gen = PDFResumeGenerator(theme_name=pdf_theme)
    pdf_bytes = pdf_gen.generate(st.session_state.resume)
    
    with col_p1:
        st.subheader("📥 Download Vector PDF")
        st.write(f"Theme Selected: **{pdf_theme}**")
        
        file_name = f"Resume_{st.session_state.resume.full_name.replace(' ', '_')}.pdf"
        st.download_button(
            label="⬇️ Download Professional Resume PDF",
            data=pdf_bytes,
            file_name=file_name,
            mime="application/pdf",
            use_container_width=True
        )
        
        st.markdown("---")
        st.subheader("💾 Backup & Sync Resume Data")
        
        # Save JSON
        json_str = json.dumps(st.session_state.resume.to_dict(), indent=2)
        st.download_button(
            label="💾 Export Resume Profile (JSON)",
            data=json_str,
            file_name="resume_profile.json",
            mime="application/json",
            use_container_width=True
        )
        
        # Load JSON
        uploaded_file = st.file_uploader("📂 Import Saved Resume Profile (JSON)", type=["json"])
        if uploaded_file is not None:
            try:
                data_dict = json.load(uploaded_file)
                st.session_state.resume = ResumeData.from_dict(data_dict)
                st.success("Resume data imported successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error loading JSON: {e}")

    with col_p2:
        st.subheader("👁️ Live PDF Preview")
        base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="550" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
