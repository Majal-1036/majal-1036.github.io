from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "files" / "Arslan_Majal_CV.pdf"

PAGE_W, PAGE_H = letter
LEFT = RIGHT = 0.56 * inch
TOP = 0.52 * inch
BOTTOM = 0.48 * inch
CONTENT_W = PAGE_W - LEFT - RIGHT

NAVY = colors.HexColor("#071A33")
BLUE = colors.HexColor("#1759B3")
MUTED = colors.HexColor("#536073")
LINE = colors.HexColor("#D8E1EC")
PALE = colors.HexColor("#EAF2FF")
GREEN = colors.HexColor("#1E6B4F")


styles = getSampleStyleSheet()
name_style = ParagraphStyle(
    "Name",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=23,
    leading=25,
    textColor=NAVY,
    alignment=TA_CENTER,
    spaceAfter=3,
)
headline_style = ParagraphStyle(
    "Headline",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=9.5,
    leading=12,
    textColor=BLUE,
    alignment=TA_CENTER,
    spaceAfter=3,
)
contact_style = ParagraphStyle(
    "Contact",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.2,
    leading=11,
    textColor=MUTED,
    alignment=TA_CENTER,
    spaceAfter=5,
)
auth_style = ParagraphStyle(
    "Authorization",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=8.2,
    leading=10,
    textColor=GREEN,
    alignment=TA_CENTER,
)
section_style = ParagraphStyle(
    "Section",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=10.6,
    leading=13,
    textColor=NAVY,
    spaceBefore=2,
    spaceAfter=3,
)
role_style = ParagraphStyle(
    "Role",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=9.1,
    leading=11,
    textColor=NAVY,
)
org_style = ParagraphStyle(
    "Organization",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=8.4,
    leading=10,
    textColor=BLUE,
)
date_style = ParagraphStyle(
    "Date",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.1,
    leading=10,
    textColor=MUTED,
    alignment=TA_RIGHT,
)
body_style = ParagraphStyle(
    "Body",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.25,
    leading=10.7,
    textColor=colors.HexColor("#273548"),
    alignment=TA_LEFT,
    spaceAfter=2,
)
bullet_style = ParagraphStyle(
    "Bullet",
    parent=body_style,
    leftIndent=9,
    firstLineIndent=-7,
    bulletIndent=0,
    spaceAfter=1.4,
)
small_style = ParagraphStyle(
    "Small",
    parent=body_style,
    fontSize=7.8,
    leading=10,
)
pub_style = ParagraphStyle(
    "Publication",
    parent=body_style,
    leftIndent=10,
    firstLineIndent=-9,
    spaceAfter=3,
)


def section(title):
    table = Table([[Paragraph(title.upper(), section_style)]], colWidths=[CONTENT_W])
    table.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("LINEBELOW", (0, 0), (-1, -1), 0.8, BLUE),
            ]
        )
    )
    return [Spacer(1, 5), table, Spacer(1, 4)]


def role_block(role, organization, dates, bullets):
    header = Table(
        [
            [Paragraph(role, role_style), Paragraph(dates, date_style)],
            [Paragraph(organization, org_style), ""],
        ],
        colWidths=[CONTENT_W * 0.76, CONTENT_W * 0.24],
    )
    header.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ("SPAN", (1, 0), (1, 1)),
            ]
        )
    )
    items = [header, Spacer(1, 2)]
    for bullet in bullets:
        items.append(Paragraph(f"- {bullet}", bullet_style))
    items.append(Spacer(1, 4))
    return KeepTogether(items)


def education_block(degree, institution, dates, details):
    header = Table(
        [[Paragraph(degree, role_style), Paragraph(dates, date_style)]],
        colWidths=[CONTENT_W * 0.76, CONTENT_W * 0.24],
    )
    header.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return KeepTogether(
        [
            header,
            Paragraph(institution, org_style),
            Paragraph(details, body_style),
            Spacer(1, 4),
        ]
    )


def project_block(title, text):
    return KeepTogether(
        [
            Paragraph(title, role_style),
            Paragraph(text, body_style),
            Spacer(1, 4),
        ]
    )


def draw_page(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(LEFT, 0.37 * inch, PAGE_W - RIGHT, 0.37 * inch)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.4)
    canvas.drawString(LEFT, 0.23 * inch, "Arslan Majal - Public Academic CV")
    canvas.drawRightString(PAGE_W - RIGHT, 0.23 * inch, f"Page {doc.page}")
    canvas.restoreState()


class CVDocTemplate(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(
            filename,
            pagesize=letter,
            leftMargin=LEFT,
            rightMargin=RIGHT,
            topMargin=TOP,
            bottomMargin=BOTTOM,
            title="Arslan Majal - Academic CV",
            author="Arslan Majal",
            subject="Academic curriculum vitae",
        )
        frame = Frame(
            LEFT,
            BOTTOM,
            CONTENT_W,
            PAGE_H - TOP - BOTTOM,
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
            id="cv-frame",
        )
        self.addPageTemplates([PageTemplate(id="cv", frames=[frame], onPage=draw_page)])


def build_story():
    story = [
        Paragraph("ARSLAN MAJAL", name_style),
        Paragraph(
            "Machine Learning Researcher | Robust Estimation and Uncertainty-Aware Learning",
            headline_style,
        ),
        Paragraph(
            'Bronx, New York | <link href="mailto:majal.wisc@gmail.com">majal.wisc@gmail.com</link> | '
            '<link href="https://www.linkedin.com/in/arslan-majal-06828b2b1">LinkedIn</link> | '
            '<link href="https://github.com/Majal-1036">GitHub</link> | '
            '<link href="https://scholar.google.com/citations?hl=en&amp;user=iQ3lR7IAAAAJ">Google Scholar</link>',
            contact_style,
        ),
        Table(
            [[Paragraph("U.S. Work Authorization: STEM OPT through July 2028 - No Current Sponsorship Required", auth_style)]],
            colWidths=[CONTENT_W],
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EDF8F3")),
                    ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#BED8CE")),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            ),
        ),
    ]

    story += section("Professional Profile")
    story.append(
        Paragraph(
            "Research Engineer with graduate training in machine learning, applied mathematics, Bayesian inference, and statistical modeling. Develops reliable estimation and learning methods for systems affected by outliers, biased measurements, heteroscedastic noise, and imperfect data. Experienced with Python and MATLAB implementation, simulation design, quantitative benchmarking, uncertainty analysis, and academic writing, with applications in robotics, perception, localization, GNSS reliability, image processing, and sensor fusion.",
            body_style,
        )
    )

    story += section("Research Interests")
    interests = [
        "Robust Gaussian Process Regression",
        "Outlier-Robust Neural Network Training",
        "Uncertainty-Aware and Adaptive Bayesian Filtering",
        "Machine Learning under Heteroscedastic Noise",
        "Sensor Fusion and State Estimation",
        "Uncertainty Quantification for Perception and Control",
    ]
    interest_table = Table(
        [[Paragraph(item, small_style) for item in interests[:3]], [Paragraph(item, small_style) for item in interests[3:]]],
        colWidths=[CONTENT_W / 3] * 3,
    )
    interest_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PALE),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#C9DBF4")),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C9DBF4")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(interest_table)

    story += section("Education")
    story.append(
        education_block(
            "M.S. in Mechanical Engineering - GPA: 3.83",
            "University of Wisconsin-Madison",
            "Sep 2023 - May 2025",
            '<b>Thesis:</b> "Quantifying Estimation Errors in Robust Vision-Based Control: An Extreme Value Theory Approach." Relevant study included artificial neural networks, matrix methods for machine learning, computer vision, image processing, optimization, probability, and statistics.',
        )
    )
    story.append(
        education_block(
            "B.S. in Computer Engineering - GPA: 3.83",
            "University of Engineering and Technology, Lahore",
            "Sep 2016 - Aug 2020",
            '<b>Thesis:</b> "Received Signal Strength (RSS)-Based Neural Network for Localization." Graduated as Gold Medalist for best academic performance.',
        )
    )

    story += section("Professional and Research Experience")
    story.append(
        role_block(
            "Research Engineer",
            "Zunitech LLC",
            "Jul 2026 - Present",
            [
                "Conduct research and development in robust machine learning, Bayesian state estimation, and uncertainty-aware inference.",
                "Develop and evaluate Python and MATLAB algorithms for detecting and mitigating corrupted measurements, with applications in robotics, GNSS reliability, image processing, and sensor-based systems.",
            ],
        )
    )
    story.append(
        role_block(
            "Graduate Researcher",
            "ARC Lab, University of Wisconsin-Madison",
            "Sep 2023 - May 2025",
            [
                "Applied Extreme Value Theory to estimate local norm error bounds for learning-based and model-based perception algorithms near nominal control trajectories.",
                "Built Python and MATLAB pipelines for simulation, numerical analysis, uncertainty evaluation, and technical reporting in robust vision-based control.",
            ],
        )
    )
    story.append(
        role_block(
            "Research Assistant / Graduate Researcher",
            "Smart Data Systems and Applications Laboratory, LUMS",
            "Sep 2020 - Aug 2023",
            [
                "Developed variational Bayesian filtering and smoothing algorithms for nonlinear state estimation with outliers, measurement bias, and uncertain noise statistics.",
                "Led development and evaluation of selective outlier-rejection smoothers for multi-sensor trajectory reconstruction, preserving valid measurement dimensions while suppressing corrupted data.",
                "Contributed to deep-unfolding methods for low-rank decomposition and multi-degradation image restoration under noise, blur, and rain artifacts.",
            ],
        )
    )

    story.append(PageBreak())
    story += section("Teaching Experience")
    story.append(
        role_block(
            "Teaching Assistant - ME 340: Dynamic Systems",
            "University of Wisconsin-Madison",
            "Fall 2023 - Spring 2025",
            [
                "Served across four semesters for a course enrolling more than 150 students; led weekly problem-solving discussion sections, held office hours, graded assignments and examinations, and provided detailed technical feedback.",
            ],
        )
    )
    story.append(
        role_block(
            "Mathematics Teacher and AI Advisor",
            "Springfield Commonwealth Academy",
            "Sep 2025 - Jun 2026",
            [
                "Taught grades 6-12 across Pre-Algebra, Algebra I, Algebra II, Geometry, and Precalculus; designed lessons, assessments, and differentiated learning activities.",
                "Helped the school explore practical and responsible uses of artificial intelligence in teaching and academic workflows.",
            ],
        )
    )
    story.append(
        role_block(
            "Geometry Teacher",
            "Vertex Charter School",
            "May 2026 - Aug 2026",
            [
                "Worked with Vertex from May through August, including an intensive Geometry summer term from July through August; developed objectives, lessons, practice packets, quizzes, tests, study materials, and final examinations.",
                "Provided individualized one-on-one instruction to students with Individualized Education Programs (IEPs), adapting explanations, pacing, and practice to their learning needs.",
            ],
        )
    )

    story += section("Publications and Preprints")
    publications = [
        '<b>Dictionary-Based Contrastive Learning for GNSS Jamming Detection.</b> Z. Hussain, <b>A. Majal</b>, A. H. Chughtai, and T. Nadeem. arXiv:2512.07512, 2025. <link href="https://arxiv.org/abs/2512.07512">[arXiv]</link>',
        '<b>EMORF-II: Adaptive EM-Based Outlier-Robust Filtering with Correlated Measurement Noise.</b> <b>A. Majal</b>, A. H. Chughtai, and M. Tahir. IEEE MLSP, 2025. <link href="https://ieeexplore.ieee.org/document/11204236/">[IEEE]</link> <link href="https://arxiv.org/abs/2509.07415">[arXiv]</link>',
        '<b>Trajectory Reconstruction through a Gaussian Adaptive Selective Outlier Rejecting Smoother.</b> <b>A. Majal</b> and A. H. Chughtai. arXiv:2410.20411, 2024. <link href="https://arxiv.org/abs/2410.20411">[arXiv]</link>',
        '<b>Outlier-Robust Unscented RTS Smoothing for Independent Sensing Data.</b> <b>A. Majal</b> and A. H. Chughtai. IEEE Sensors Letters, vol. 8, no. 10, 2024. <link href="https://ieeexplore.ieee.org/document/10680401/">[IEEE]</link>',
        '<b>Variational-Based Nonlinear Bayesian Filtering with Biased Observations.</b> A. H. Chughtai, <b>A. Majal</b>, M. Tahir, and M. Uppal. IEEE Transactions on Signal Processing, vol. 70, pp. 5295-5307, 2022. <link href="https://ieeexplore.ieee.org/document/9931968/">[IEEE]</link>',
    ]
    for item in publications:
        story.append(Paragraph(f"- {item}", pub_style))

    story += section("Selected Technical Projects")
    story.append(
        project_block(
            "Deep Learning for Robust Kalman Filtering",
            "Developing a learning-augmented Extended Kalman Filter for outliers, sensor bias, and uncertain noise, with evaluation against classical EKF and learning-based filtering frameworks.",
        )
    )
    story.append(
        project_block(
            "Robust Gaussian Process Regression with Adaptive Noise Learning",
            "Integrating variational Bayesian and Expectation-Maximization updates to learn nominal noise and outlier behavior directly from corrupted regression data.",
        )
    )
    story.append(
        project_block(
            "Multi-Degradation Image Restoration via Deep Unfolding",
            "Combining Orthogonal Variational PCA, content-aware partitioning, adaptive rank estimation, and attention-based refinement for unknown noise, blur, and rain degradations.",
        )
    )
    story.append(
        project_block(
            "Outlier-Robust Neural Network Training",
            "Developing adaptive sample-weighting and robust cross-validation strategies for label noise and unknown data contamination.",
        )
    )

    story += section("Technical Skills")
    skills = [
        ("Programming", "Python, MATLAB, C++, SQL"),
        ("Machine Learning", "PyTorch, scikit-learn, NumPy, pandas, neural networks, Gaussian processes, regression, clustering"),
        ("Inference and Estimation", "Variational Bayes, Expectation-Maximization, nonlinear Kalman filtering, RTS smoothing, uncertainty quantification"),
        ("Tools", "Jupyter, LaTeX, Git, Excel, Google Sheets, simulation-based analysis, technical writing"),
    ]
    skills_table = Table(
        [[Paragraph(f"<b>{label}</b>", body_style), Paragraph(value, body_style)] for label, value in skills],
        colWidths=[1.35 * inch, CONTENT_W - 1.35 * inch],
    )
    skills_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    story.append(skills_table)

    story += section("Honors and Awards")
    story.append(Paragraph("- Fulbright Scholarship Selectee, 2021", bullet_style))
    story.append(Paragraph("- Gold Medalist for Best Academic Performance, UET Lahore, 2020", bullet_style))
    return story


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = CVDocTemplate(str(OUTPUT))
    doc.build(build_story())
    print(OUTPUT)


if __name__ == "__main__":
    main()
