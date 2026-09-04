import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any

@dataclass
class WorkExperience:
    company: str = ""
    role: str = ""
    location: str = ""
    start_date: str = ""
    end_date: str = ""
    bullets: List[str] = field(default_factory=list)

@dataclass
class Education:
    institution: str = ""
    degree: str = ""
    field_of_study: str = ""
    start_date: str = ""
    end_date: str = ""
    gpa: str = ""

@dataclass
class Project:
    title: str = ""
    description: str = ""
    tech_stack: str = ""
    link: str = ""
    bullets: List[str] = field(default_factory=list)

@dataclass
class Certification:
    name: str = ""
    issuer: str = ""
    year: str = ""

@dataclass
class ResumeData:
    full_name: str = ""
    job_title: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    linkedin: str = ""
    github: str = ""
    portfolio: str = ""
    summary: str = ""
    skills: List[str] = field(default_factory=list)
    experiences: List[WorkExperience] = field(default_factory=list)
    education: List[Education] = field(default_factory=list)
    projects: List[Project] = field(default_factory=list)
    certifications: List[Certification] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ResumeData':
        exp_list = [WorkExperience(**exp) for exp in data.get("experiences", [])]
        edu_list = [Education(**edu) for edu in data.get("education", [])]
        proj_list = [Project(**proj) for proj in data.get("projects", [])]
        cert_list = [Certification(**cert) for cert in data.get("certifications", [])]

        return cls(
            full_name=data.get("full_name", ""),
            job_title=data.get("job_title", ""),
            email=data.get("email", ""),
            phone=data.get("phone", ""),
            location=data.get("location", ""),
            linkedin=data.get("linkedin", ""),
            github=data.get("github", ""),
            portfolio=data.get("portfolio", ""),
            summary=data.get("summary", ""),
            skills=data.get("skills", []),
            experiences=exp_list,
            education=edu_list,
            projects=proj_list,
            certifications=cert_list
        )

def get_sample_resume() -> ResumeData:
    """Returns a rich, professional sample resume profile for quick testing and demos."""
    return ResumeData(
        full_name="Alex R. Vance",
        job_title="Senior AI & Full Stack Software Engineer",
        email="alex.vance@techstudio.io",
        phone="+1 (555) 382-9102",
        location="San Francisco, CA (Open to Remote)",
        linkedin="linkedin.com/in/alexvance-ai",
        github="github.com/alexvance-dev",
        portfolio="alexvance.dev",
        summary="Results-driven Senior AI & Full-Stack Engineer with 6+ years of experience architecting high-throughput distributed systems, LLM-powered applications, and scalable microservices. Proven track record of boosting platform performance by 40% and deploying generative AI workflows serving 500k+ monthly active users.",
        skills=[
            "Python", "TypeScript", "PyTorch", "OpenAI API", "LangChain", "FastAPI", 
            "React.js", "Next.js", "Docker", "Kubernetes", "AWS (EC2, Lambda, S3)", 
            "PostgreSQL", "Redis", "Vector DBs (Pinecone, Qdrant)", "CI/CD", "Git"
        ],
        experiences=[
            WorkExperience(
                company="Nexus AI Innovations",
                role="Senior AI Solutions Engineer",
                location="San Francisco, CA",
                start_date="Jan 2023",
                end_date="Present",
                bullets=[
                    "Engineered enterprise LLM orchestration pipeline using Python, LangChain, and Qdrant vector database, reducing customer support resolution latency by 45%.",
                    "Architected scalable microservices handling 2M+ daily requests on AWS EKS with 99.99% uptime.",
                    "Mentored a team of 5 junior/mid-level engineers in clean code practices, unit testing, and prompt engineering patterns."
                ]
            ),
            WorkExperience(
                company="Apex Cloud Systems",
                role="Full Stack Software Engineer",
                location="Austin, TX",
                start_date="Jun 2020",
                end_date="Dec 2022",
                bullets=[
                    "Developed high-converting React/TypeScript analytics dashboard, driving a 30% increase in enterprise customer retention.",
                    "Designed RESTful & GraphQL APIs in FastAPI and PostgreSQL, optimizing query speeds by 3.5x using custom indexing strategies.",
                    "Implemented automated CI/CD deployment pipelines via GitHub Actions, reducing release cycle time from 3 days to 25 minutes."
                ]
            )
        ],
        education=[
            Education(
                institution="University of California, Berkeley",
                degree="Bachelor of Science",
                field_of_study="Computer Science & Data Science",
                start_date="Sep 2016",
                end_date="May 2020",
                gpa="3.88 / 4.0"
            )
        ],
        projects=[
            Project(
                title="AI Knowledge Graph Synthesizer",
                description="An open-source tool that converts raw unstructured documents into interactive semantic knowledge graphs using LLMs and PyTorch.",
                tech_stack="Python, PyTorch, Streamlit, NetworkX, Neo4j",
                link="github.com/alexvance-dev/graph-synthesizer",
                bullets=[
                    "Starred 1.2k+ times on GitHub and featured in PyTorch Weekly.",
                    "Implemented semantic chunking algorithms that improved graph entity extraction accuracy by 28%."
                ]
            )
        ],
        certifications=[
            Certification(
                name="AWS Certified Solutions Architect – Associate",
                issuer="Amazon Web Services",
                year="2023"
            ),
            Certification(
                name="Deep Learning Specialization",
                issuer="DeepLearning.AI (Coursera)",
                year="2022"
            )
        ]
    )
