import os
import re
import random
from typing import Dict, List, Any, Tuple

# Try importing AI SDKs gracefully
try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

class AIEngine:
    def __init__(self, provider: str = "Smart Offline", api_key: str = ""):
        self.provider = provider
        self.api_key = api_key.strip()
        
        if self.provider == "Google Gemini" and self.api_key and HAS_GEMINI:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        elif self.provider == "OpenAI" and self.api_key and HAS_OPENAI:
            self.client = openai.OpenAI(api_key=self.api_key)

    def generate_summary(self, name: str, job_title: str, skills: List[str], experience_summary: str) -> str:
        """Generates a professional executive summary."""
        prompt = f"""
        Write a high-impact, professional executive summary (3-4 sentences, ~60-80 words) for a CV/Resume.
        Candidate Name: {name}
        Target Job Title: {job_title}
        Key Skills: {', '.join(skills[:8])}
        Brief Experience background: {experience_summary}

        Requirements:
        - Use strong action verbs and industry-standard keywords.
        - Highlight value delivered, leadership/collaboration, and technical mastery.
        - Do NOT use filler words or generic fluff.
        - Write in third-person professional tone or first-person implied (no "I am a...").
        """
        
        if self.provider == "Google Gemini" and self.api_key and HAS_GEMINI:
            try:
                response = self.model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                pass # fallback to smart engine

        elif self.provider == "OpenAI" and self.api_key and HAS_OPENAI:
            try:
                res = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=200,
                    temperature=0.7
                )
                return res.choices[0].message.content.strip()
            except Exception as e:
                pass # fallback to smart engine

        # Smart Fallback Engine
        top_skills = ", ".join(skills[:4]) if skills else "modern technical stacks"
        return (
            f"Results-oriented {job_title or 'Professional'} with proven expertise in {top_skills}. "
            f"Demonstrated history of driving technical innovation, optimizing system performance, and scaling operational workflows. "
            f"Adept at collaborating across cross-functional teams to deliver scalable, high-business-impact solutions."
        )

    def enhance_bullet_point(self, raw_bullet: str, target_role: str = "") -> str:
        """Transforms a weak or simple bullet point into a high-impact action statement with metrics."""
        if not raw_bullet.strip():
            return raw_bullet

        prompt = f"""
        Rewrite the following resume bullet point into a high-impact, STAR-formatted (Situation, Task, Action, Result) accomplishment statement.
        Target Job Role: {target_role}
        Original Bullet Point: "{raw_bullet}"

        Rules:
        - Start with a strong active power verb (e.g. Architected, Spearheaded, Optimized, Orchestrated).
        - Include realistic quantifiable metrics or impact (e.g. %, speed improvement, revenue, time saved).
        - Keep it concise (15-25 words).
        - Output ONLY the rewritten bullet point without quotation marks or bullet symbols.
        """

        if self.provider == "Google Gemini" and self.api_key and HAS_GEMINI:
            try:
                response = self.model.generate_content(prompt)
                return response.text.strip().lstrip("•- ").strip()
            except Exception:
                pass

        elif self.provider == "OpenAI" and self.api_key and HAS_OPENAI:
            try:
                res = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=100,
                    temperature=0.7
                )
                return res.choices[0].message.content.strip().lstrip("•- ").strip()
            except Exception:
                pass

        # Smart Heuristic Rewriter (Offline)
        power_verbs = ["Spearheaded", "Architected", "Optimized", "Streamlined", "Orchestrated", "Engineered"]
        metrics = ["by 35%", "reducing processing time by 40%", "saving 15+ engineering hours weekly", "boosting platform performance by 3x"]
        
        verb = random.choice(power_verbs)
        metric = random.choice(metrics)
        clean_raw = raw_bullet.strip().rstrip(".")
        
        # Remove weak leading words if any
        clean_raw = re.sub(r'^(worked on|helped with|responsible for|did|made|built|created)\s+', '', clean_raw, flags=re.IGNORECASE)
        
        return f"{verb} {clean_raw[0].lower() + clean_raw[1:] if clean_raw else 'key initiatives'}, {metric}."

    def analyze_ats(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """Analyzes resume text against a target job description for ATS compatibility."""
        if not job_description.strip():
            return {
                "score": 85,
                "summary": "Please provide a target Job Description to run detailed ATS comparison.",
                "matched_keywords": ["Python", "Engineering", "Architecture", "API", "Optimization"],
                "missing_keywords": ["CI/CD", "Cloud Architecture", "Agile Methodologies"],
                "tips": [
                    "Include quantifiable metrics in every bullet point.",
                    "Tailor your skill section keywords to match job posting titles directly."
                ]
            }

        # Extract words for heuristic matching
        def extract_keywords(text: str) -> set:
            words = re.findall(r'\b[A-Za-z0-9+#.-]{3,}\b', text)
            stopwords = {"and", "the", "for", "with", "that", "this", "from", "have", "you", "your", "are", "will", "our", "work"}
            return {w.strip().lower() for w in words if w.lower() not in stopwords and len(w) > 2}

        jd_words = extract_keywords(job_description)
        resume_words = extract_keywords(resume_text)

        matched = jd_words.intersection(resume_words)
        missing = jd_words.difference(resume_words)

        match_ratio = len(matched) / (len(jd_words) if jd_words else 1)
        calculated_score = min(98, max(45, int(match_ratio * 100 + 20)))

        # Convert back to readable sample words
        display_matched = sorted([w.capitalize() for w in list(matched)[:10]])
        display_missing = sorted([w.capitalize() for w in list(missing)[:8]])

        return {
            "score": calculated_score,
            "summary": f"Your resume has a **{calculated_score}% ATS keyword alignment** with the targeted job description.",
            "matched_keywords": display_matched,
            "missing_keywords": display_missing,
            "tips": [
                f"Add these missing key terms into your skills or bullet points: {', '.join(display_missing[:4])}.",
                "Ensure your job titles match standard industry naming conventions.",
                "Use bulleted list formatting over dense multi-line paragraphs for better ATS parser readability."
            ]
        }

    def suggest_skills(self, job_title: str) -> List[str]:
        """Suggests relevant technical and soft skills based on job title."""
        title_lower = job_title.lower()
        if "data" in title_lower or "ai" in title_lower or "machine learning" in title_lower:
            return ["Python", "PyTorch", "TensorFlow", "Pandas", "Scikit-Learn", "SQL", "LLMs", "LangChain", "Vector DBs", "MLOps", "Git"]
        elif "frontend" in title_lower or "web" in title_lower or "react" in title_lower:
            return ["React.js", "Next.js", "TypeScript", "JavaScript", "HTML5/CSS3", "Tailwind CSS", "Redux", "REST APIs", "GraphQL", "Web Analytics"]
        elif "backend" in title_lower or "cloud" in title_lower or "devops" in title_lower:
            return ["Python", "Go", "Java", "Docker", "Kubernetes", "AWS", "FastAPI", "PostgreSQL", "Redis", "Kafka", "CI/CD", "Terraform"]
        else:
            return ["Python", "Strategic Planning", "Project Management", "Agile/Scrum", "Data Analysis", "System Design", "Cross-functional Leadership"]
