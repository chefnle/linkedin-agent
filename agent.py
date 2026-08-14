print("LinkedIn agent starting up!")

"""
LinkedIn Content Agent
----------------------

Creates:
    1. LinkedIn comments
    2. LinkedIn posts
    3. AI-generated post images
    4. LinkedIn carousel PDFs
    5. Buffer scheduling/drafts

Setup:
    pip install anthropic openai fpdf2

Environment variables:
    ANTHROPIC_API_KEY
    OPENAI_API_KEY

Run:
    python agent.py
"""

# ============================================================
# IMPORTS
# ============================================================

import base64
import json
import os
import sys
from datetime import datetime

import requests

from anthropic import Anthropic
from openai import OpenAI
from fpdf import FPDF


# ============================================================
# CONFIGURATION
# ============================================================

MODEL = "claude-sonnet-5"


# ============================================================
# YOUR RESUME / PERSONAL BACKGROUND
# DO NOT MODIFY
# ============================================================

RESUME_SUMMARY = """NHAT (NATE) LE, PMP® | LSSGB
Operational Excellence & PMO Leader  •  Project Management   •  Change Management
chefnle@gmail.com  •  (336) 609-2281  •  Apex, NC  •  US Citizen
•  linkedin.com/in/nhat-le-pmp  •  credly.com/users/nhat-le.db8a10fd
PROFESSIONAL SUMMARY
Operational Excellence and PMO professional with 16 years of multi-site project management, process optimization, and organizational transformation across high-volume operational environments. PMP® and Lean Six Sigma Green Belt certified. Consistent record of delivering enterprise project execution on time and within budget, building high-performing teams, and driving measurable operational excellence through structured DMAIC methodology, disciplined change management, and rigorous stakeholder management. Brings full project lifecycle ownership (initiation through closure), P&L accountability, and AI-enabled process improvement to every engagement. Currently completing Microsoft Power BI PL-300 certification.
CORE COMPETENCIES
Project Management & Project Execution  •  Operational Excellence & PMO Governance  •  Process Optimization & Reengineering  •  Change Management & Adoption
Lean Six Sigma DMAIC  •  Project Lifecycle Management (Initiation → Closure)  •  Stakeholder Management  •  Risk Identification & Mitigation
KPI Design, Tracking & Executive Reporting  •  Budget & Resource Management  •  SOP Development  •  Vendor & Contractor Coordination  •  Agile/Scrum  •  AI Tools & IBM AI Fundamentals
PROFESSIONAL EXPERIENCE
Operations Manager — Operational Excellence & Project Execution Lead  |  Starbucks  |  Apex, NC  |  Oct 2025 – Present
Lead operational turnaround and project execution for high-volume $65K+ weekly revenue location with 30+ partners.
•	Serve as site-level PMO lead for all quarterly corporate initiative deployments: own full project management lifecycle from initiation through closure — define scope, build implementation plans, set milestones, coordinate readiness across HR, Operations, Training, and Supply Chain, manage risks, and report outcomes to district and regional leadership — 100% on-time project execution.
•	Drove complete operational excellence turnaround using DMAIC process optimization methodology: national ranking 2 → 4 shots | Customer complaints 18 → 7 | Partner Hours Met 80% → 98% | Items Unavailability 7 → 1.6 — all metrics improved within five months.
•	Redesigned onboarding lifecycle and performance accountability framework through structured change management planning; reduced team turnover from 75% to 25% within one year.
•	Manage full P&L including labor cost optimization, inventory control, waste reduction, and financial reporting to district leadership; consistently at-budget or better.
•	Maintain SOPs, compliance documentation, and regulatory standards; conduct and pass all external operational audits.
Associate Operations Manager — Process Optimization & Multi-Site PMO  |  Sheetz Inc.  |  Raleigh-Durham, NC  |  May 2024 – Oct 2025
District PMO resource deployed across 10 locations; led multi-site process optimization initiatives and operational excellence programs across the region.
•	Applied Lean Six Sigma DMAIC process optimization methodology across all 10 district locations simultaneously: Order Accuracy 75% → 90% | Service Speed 60% → 80% | Customer Friendliness 65% → 80% | Cleanliness 50% → 65% — all four operational excellence metrics improved within a single cycle.
•	Built district onboarding program from zero: defined learning objectives, developed curriculum, coordinated project execution across 10 locations, tracked participant milestones, and measured performance outcomes against pre-program baseline.
•	Led cross-functional project management across 10 sites simultaneously: gathered business requirements, developed work plans, managed dependencies and scheduling conflicts, documented decisions, and drove accountability through regular stakeholder management reporting.
•	Mentored 2 Assistant Managers to Store Manager through structured 6-month individual development programs with regular reviews and district leadership coordination.
•	Resolved escalated operational issues, managed vendor relationships, and ensured process optimization and compliance across all 10 locations as primary district escalation resource.
Operations Manager — Project Management & Operational Excellence  |  Starbucks  |  Cary, NC  |  Feb 2022 – May 2024
Full P&L ownership and operational excellence leadership; responsible for project execution, team performance, and district-level PMO initiatives.
•	Rebuilt team performance culture through structured change management and accountability framework; reduced turnover from 75% to 25% within 12 months.
•	Improved drive-through out-time from 50+ seconds to under 45 seconds through process optimization — ranked top 10 among 100+ NC locations.
•	Grew comparable sales 25% year-over-year, achieving 110% of budget target through operational excellence discipline and team execution.
•	Delivered all corporate program rollouts on schedule through disciplined project management; selected by regional leadership to pilot district-level initiatives.
Senior Executive Chef / Multi-Unit Market Leader — Operational Excellence PMO  |  P.F. Chang’s  |  NC |  Dec 2010 – Feb 2022
12-year progressive operational excellence leadership across 7 NC locations with full P&L accountability for $35M+ annual portfolio.
•	Led two full greenfield restaurant launches (~$14M combined scale) with end-to-end project management: coordinated vendors and contractors, managed project timelines, allocated resources, directed staffing and training, and validated operational readiness — both delivered on time and within budget.
•	Ranked #3 in profitability among 210+ national PF Chang’s units through operational excellence discipline; managed $5M–$7M annual revenue per location across a 7-location NC portfolio.
•	Drove process optimization across 7 locations simultaneously: seasonal programs, operational improvement initiatives, training rollouts, and regional leadership development — all executed through structured project management.
•	Developed 20+ team members into leadership roles through structured change management and individual development programs; built leadership pipeline contributing to regional talent depth.
•	Designed and implemented cross-location SOP standardization and process optimization programs; reduced quality variance and improved operational excellence consistency across all locations.
•	Earned Restaurant of the Year 2018 and Executive Chef of the Year 2020; recognized for operational excellence, project execution, and people development.
CERTIFICATIONS
PMP® — Project Management Professional (PMI)  •  Lean Six Sigma Green Belt (SSGI)
Professional Scrum Master I & II (PSM I / PSM II)  •  Professional Agile Leadership (PAL)  •  IBM AI Fundamentals
Google Project Management Certificate  •  Jira & Confluence Certified  •  Microsoft Power BI PL-300 (In Progress, August 2026)  •  Supply Chain Management Coursework (CSCP Concepts), YouAccel Training
EDUCATION
Bachelor of Business Administration  |  Ho Chi Minh City University of Industry  |  2007"""


# ============================================================
# YOUR WRITING EXAMPLES
# DO NOT MODIFY
# ============================================================

EXAMPLES = """ Example 1: Culture always wins long-term. Relying on one talented chef isn't sustainable — he can't work seven days a week forever, and if he tries, he'll burn out. Whatever his attitude is, it spreads: the team either gets too afraid to speak up, or starts mirroring his behavior back. And there's no version of unhappy, nervous staff delivering a genuinely happy guest experience. It shows, every time. I wouldn't terminate him — his talent is real and hard to replace. But coaching the behavior is non-negotiable. The key is understanding the why behind it first. Is it stress, insecurity, unclear expectations, burnout, something from outside work bleeding in? That root cause is what tells you how to actually approach him, instead of just reacting to the symptom. 16 years in operations taught me this: the food or product might be what customers notice first, but the culture is what determines whether you still have a great team a year from now.

Example 2: I'd actually push back a little here. Titles matter more than we'd like to admit, especially in a world where most resumes go through an ATS before a human ever sees them. If the keyword the system is scanning for is 'Manager' and your title says 'Lead,' you may never even surface in the search, regardless of your actual scope of responsibility. On top of that, your title on paper has to match what your employer verifies in a background check — you can't just tailor it after the fact to sound bigger than what's official. So candidates aren't just being precious about a label. They're thinking ahead to their next move, and the next one after that. Tailoring your resume bullet points to describe real scope and impact can only do so much when the title field itself is what's filtering you in or out before anyone reads those bullet points. In a perfect world, employers would judge based on substance alone — but candidates have to operate in the system that actually exists today, not the one we wish existed.

Example 3: Really appreciate you sharing this — insider stories on how someone like Jeff Bezos actually operates day-to-day at that level are far more valuable than the polished leadership advice most people put out. The 'decode the humans' point stands out most to me. In my own experience, the technical or financial case rarely fails on its own merit — it fails because the person presenting it didn't anticipate what the decision-maker actually cared about going in. Preparation isn't just knowing your numbers; it's knowing your audience well enough to speak in the terms that matter to them. Thanks for breaking this down with real specifics instead of vague theory. """.strip()


# ============================================================
# YOUR COMMENT SYSTEM PROMPT
# DO NOT MODIFY
# ============================================================

SYSTEM_PROMPT = f"""You are helping Operations Leaders draft comments on LinkedIn posts. Here is their background:

{RESUME_SUMMARY}

Here are examples of their writing style and perspective:

{EXAMPLES}

When given a topic, write ONE LinkedIn comment that:

Sounds warm, genuine, and professional (not salesy or generic)
Draws a light, credible connection to the person's PMO/Operations background where it naturally fits — don't force it
Is 2-4 sentences long, conversational in tone
Avoids corporate buzzword overload and avoids hashtags
Does not use emojis unless the topic clearly calls for a light touch
Reads like something a real person typed, not an AI-generated blurb
Return ONLY the comment text, with no preamble, quotation marks, or labels. """.strip()


# ============================================================
# CLIENT SETUP
# ============================================================

def get_clients():
    """Create Anthropic and OpenAI clients."""

    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")

    if not anthropic_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY environment variable is not set."
        )

    if not openai_key:
        raise RuntimeError(
            "OPENAI_API_KEY environment variable is not set."
        )

    anthropic_client = Anthropic(
        api_key=anthropic_key
    )

    openai_client = OpenAI(
        api_key=openai_key
    )

    return anthropic_client, openai_client


# ============================================================
# AI RESPONSE HELPER
# ============================================================

def extract_text(response) -> str:
    """Extract text blocks from an Anthropic response."""

    return "".join(
        block.text
        for block in response.content
        if block.type == "text"
    ).strip()


# ============================================================
# COMMENT GENERATION
# ============================================================

def generate_comment(
    client: Anthropic,
    topic: str
) -> str:
    """Generate a LinkedIn comment."""

    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    f"The LinkedIn post topic is: {topic}\n\n"
                    "Draft the comment now."
                ),
            }
        ],
    )

    return extract_text(response)


# ============================================================
# COMMENT / POST REFINEMENT
# ============================================================

def refine_draft(
    client: Anthropic,
    draft: str,
    feedback: str,
    is_comment: bool = False
) -> str:
    """Revise an existing comment or post based on feedback."""

    if is_comment:
        instruction = """
Revise this LinkedIn comment based on the user's feedback.

Keep the person's authentic voice and perspective.
Do not make it sound corporate, generic, or AI-generated.
Keep it conversational and natural.
Return ONLY the revised comment.
"""
    else:
        instruction = """
Revise this LinkedIn post based on the user's feedback.

Keep the person's authentic voice and operational leadership perspective.
Preserve strong ideas and useful specifics unless the feedback asks
you to remove them.
Use natural LinkedIn formatting with short paragraphs.
Return ONLY the revised post.
"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=800,
        system=instruction,
        messages=[
            {
                "role": "user",
                "content": (
                    f"CURRENT DRAFT:\n\n"
                    f"{draft}\n\n"
                    f"USER FEEDBACK:\n\n"
                    f"{feedback}\n\n"
                    f"Revise the draft now."
                ),
            }
        ],
    )

    return extract_text(response)


# ============================================================
# POST GENERATION
# ============================================================

def generate_post(
    client: Anthropic,
    openai_client: OpenAI,
    topic: str
):
    """Generate post text, image prompt, and image."""

    post_system_prompt = SYSTEM_PROMPT + (
        "\n\nInstead of a short comment, write a full LinkedIn post: "
        "a strong opening hook, a short body that draws on the person's "
        "background where relevant, and a clear closing takeaway. "
        "Use short paragraphs/line breaks as is typical for LinkedIn. "
        "Create relevant hashtags."
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens=600,
        system=post_system_prompt,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Create a LinkedIn post about: {topic}"
                ),
            }
        ],
    )

    post_text = extract_text(response)

    print("\nGenerating image concept...")

    image_prompt = generate_image_prompt(
        client,
        topic,
        post_text
    )

    print("Generating image...")

    saved_image_path = generate_post_image(
        openai_client,
        image_prompt
    )

    return (
        post_text,
        image_prompt,
        saved_image_path
    )


# ============================================================
# IMAGE PROMPT GENERATION
# ============================================================

def generate_image_prompt(
    client: Anthropic,
    topic: str,
    post_text: str
) -> str:
    """Generate an image prompt for the LinkedIn post."""

    system_prompt = """
You are an expert visual creative director for LinkedIn content.

Create a professional image-generation prompt based on the LinkedIn
post topic and post content.

The image should:
- Look professional and appropriate for LinkedIn
- Visually communicate the main idea of the post
- Feel authentic and human rather than overly corporate
- Avoid text, logos and watermarks that would be violating copyright
- Use a cartoon or animated style, with sense of humor if appropriate for the topic
- Be visually interesting, and attract attention in a LinkedIn feed.

Return ONLY the image-generation prompt.
"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=400,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Topic: {topic}\n\n"
                    f"LinkedIn post:\n{post_text}\n\n"
                    "Create the image prompt."
                ),
            }
        ],
    )

    return extract_text(response)


# ============================================================
# IMAGE GENERATION
# ============================================================

def generate_post_image(
    openai_client: OpenAI,
    image_prompt: str
) -> str:
    """Generate and save a LinkedIn image."""

    response = openai_client.images.generate(
        model="gpt-image-1",
        prompt=image_prompt,
        size="1536x1024",
    )

    image_data = response.data[0]

    output_dir = "output/images"

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = os.path.join(
        output_dir,
        f"linkedin_post_{timestamp}.png"
    )

    if hasattr(image_data, "b64_json") and image_data.b64_json:

        image_bytes = base64.b64decode(
            image_data.b64_json
        )

        with open(
            filename,
            "wb"
        ) as f:
            f.write(image_bytes)

    else:
        raise RuntimeError(
            "Image API did not return base64 image data."
        )

    return filename


# ============================================================
# IMAGE PROMPT REFINEMENT
# ============================================================

def refine_image_prompt(
    client: Anthropic,
    post_text: str,
    current_prompt: str,
    feedback: str
) -> str:
    """Revise an image prompt based on user feedback."""

    system_prompt = """
You are an expert visual creative director.

Revise the current image-generation prompt based on the user's feedback.

Keep the image:
- Professional enough for LinkedIn
- Visually interesting
- Human and authentic
- Cartoon or animated when appropriate
- Free of text, logos, and watermarks

Do not explain your changes.

Return ONLY the revised image-generation prompt.
"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=500,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": (
                    f"LINKEDIN POST:\n\n"
                    f"{post_text}\n\n"
                    f"CURRENT IMAGE PROMPT:\n\n"
                    f"{current_prompt}\n\n"
                    f"USER FEEDBACK:\n\n"
                    f"{feedback}\n\n"
                    "Create the revised image prompt."
                ),
            }
        ],
    )

    return extract_text(response)


# ============================================================
# CAROUSEL SLIDE GENERATION
# ============================================================

def generate_carousel_slides(
    client: Anthropic,
    topic: str
) -> list:
    """Generate carousel slide content as JSON."""

    system_prompt = """
You are an expert LinkedIn content strategist.

Create 3 highly engaging LinkedIn carousel slides for the given topic.

The carousel should:
- Tell a simple story
- Have a strong first slide
- Provide practical insight
- Feel authentic and human
- Avoid generic corporate language
- Be concise enough for a visual carousel

Return ONLY valid JSON.

Use exactly this structure:

[
    {
        "title": "Short title",
        "text": "Short supporting text."
    },
    {
        "title": "Short title",
        "text": "Short supporting text."
    },
    {
        "title": "Short title",
        "text": "Short supporting text."
    }
]

Rules:
- Each title must be 6 words or fewer.
- Each text must be 2 sentences or fewer.
- No markdown.
- No code blocks.
- No explanation outside the JSON.
"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=600,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Generate carousel slides for:\n\n"
                    f"{topic}"
                ),
            }
        ],
    )

    raw_text = extract_text(response)

    # Handle accidental markdown fences
    if raw_text.startswith("```"):
        raw_text = raw_text.replace(
            "```json",
            ""
        )

        raw_text = raw_text.replace(
            "```",
            ""
        )

        raw_text = raw_text.strip()

    try:
        slides = json.loads(raw_text)

    except json.JSONDecodeError as e:
        raise ValueError(
            "Claude returned invalid carousel JSON.\n\n"
            f"Response:\n{raw_text}\n\n"
            f"JSON error: {e}"
        )

    if not isinstance(slides, list):
        raise ValueError(
            "Carousel response must be a list."
        )

    for slide in slides:

        if not isinstance(slide, dict):
            raise ValueError(
                "Each carousel slide must be an object."
            )

        if "title" not in slide:
            raise ValueError(
                "Carousel slide is missing 'title'."
            )

        if "text" not in slide:
            raise ValueError(
                "Carousel slide is missing 'text'."
            )

    return slides


# ============================================================
# PDF TEXT CLEANING
# ============================================================

def clean_pdf_text(
    text: str
) -> str:
    """Convert unsupported Unicode into Helvetica-safe text."""

    replacements = {
        "—": "-",
        "–": "-",
        "−": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "…": "...",
        "•": "-",
        "™": "(TM)",
        "®": "(R)",
        "©": "(C)",
        "\u00a0": " ",
    }

    for old, new in replacements.items():
        text = text.replace(
            old,
            new
        )

    return (
        text
        .encode(
            "latin-1",
            errors="replace"
        )
        .decode("latin-1")
    )


# ============================================================
# CAROUSEL PDF CREATION
# ============================================================

def create_carousel(
    slides,
    filename="linkedin_carousel.pdf"
):
    """Create a square LinkedIn carousel PDF."""

    pdf = FPDF(
        orientation="L",
        unit="pt",
        format=(1080, 1080)
    )

    for idx, slide in enumerate(slides):

        pdf.add_page()

        title = clean_pdf_text(
            str(slide["title"])
        )

        text = clean_pdf_text(
            str(slide["text"])
        )

        # ----------------------------------------------------
        # TITLE SLIDE
        # ----------------------------------------------------

        if idx == 0:

            pdf.set_fill_color(
                30,
                58,
                138
            )

            pdf.rect(
                0,
                0,
                1080,
                1080,
                "F"
            )

            pdf.set_text_color(
                255,
                255,
                255
            )

            pdf.set_font(
                "helvetica",
                "B",
                size=54
            )

            pdf.set_xy(
                100,
                350
            )

            pdf.multi_cell(
                880,
                70,
                title,
                align="C"
            )

            pdf.set_font(
                "helvetica",
                "",
                size=28
            )

            pdf.set_xy(
                100,
                550
            )

            pdf.multi_cell(
                880,
                40,
                text,
                align="C"
            )

        # ----------------------------------------------------
        # CONTENT SLIDES
        # ----------------------------------------------------

        else:

            pdf.set_fill_color(
                255,
                255,
                255
            )

            pdf.rect(
                0,
                0,
                1080,
                1080,
                "F"
            )

            pdf.set_fill_color(
                30,
                58,
                138
            )

            pdf.rect(
                0,
                0,
                1080,
                20,
                "F"
            )

            # Title
            pdf.set_text_color(
                30,
                58,
                138
            )

            pdf.set_font(
                "helvetica",
                "B",
                size=44
            )

            pdf.set_xy(
                100,
                150
            )

            pdf.multi_cell(
                880,
                55,
                title,
                align="L"
            )

            # Body
            pdf.set_text_color(
                75,
                85,
                99
            )

            pdf.set_font(
                "helvetica",
                "",
                size=28
            )

            pdf.set_xy(
                100,
                350
            )

            pdf.multi_cell(
                880,
                45,
                text,
                align="L"
            )

            # Slide number
            pdf.set_text_color(
                156,
                163,
                175
            )

            pdf.set_font(
                "helvetica",
                "",
                size=20
            )

            pdf.set_xy(
                100,
                950
            )

            pdf.multi_cell(
                880,
                30,
                f"Slide {idx + 1} of {len(slides)}",
                align="R"
            )

    pdf.output(filename)

    return filename


# ============================================================
# CONTENT IDEAS
# ============================================================

def save_idea(
    idea: str
) -> None:
    """Save a content idea."""

    with open(
        "ideas.txt",
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            idea + "\n"
        )


def get_ideas() -> list:
    """Return saved content ideas."""

    if not os.path.exists(
        "ideas.txt"
    ):
        return []

    with open(
        "ideas.txt",
        "r",
        encoding="utf-8"
    ) as f:

        return [
            line.strip()
            for line in f.readlines()
            if line.strip()
        ]


def delete_idea(
    idea_to_delete: str
) -> None:
    """Delete a saved content idea."""

    ideas = get_ideas()

    if idea_to_delete not in ideas:
        return

    ideas.remove(
        idea_to_delete
    )

    with open(
        "ideas.txt",
        "w",
        encoding="utf-8"
    ) as f:

        for idea in ideas:
            f.write(
                idea + "\n"
            )


def handle_save_idea():
    """Ask user for and save a content idea."""

    idea = input(
        "Enter your content idea to save: "
    ).strip()

    if idea:
        save_idea(idea)

        print(
            "\nIdea saved to ideas.txt!"
        )


def select_topic_from_ideas():
    """Allow user to select an existing idea."""

    saved_ideas = get_ideas()

    if not saved_ideas:
        return None

    print("\nSaved Ideas:")

    for idx, idea in enumerate(
        saved_ideas,
        1
    ):
        print(
            f"{idx}. {idea}"
        )

    print(
        f"{len(saved_ideas) + 1}. "
        "Write about a new topic"
    )

    idea_choice = input(
        "Choose an idea number: "
    ).strip()

    try:

        selected_idx = (
            int(idea_choice) - 1
        )

        if 0 <= selected_idx < len(saved_ideas):
            return saved_ideas[selected_idx]

    except ValueError:
        pass

    return None


# ============================================================
# USER INPUT
# ============================================================

def show_menu():
    """Display the main menu."""

    print(
        "\nLinkedIn Content Assistant"
    )

    print(
        "=" * 30
    )

    print(
        "1. Draft a Comment"
    )

    print(
        "2. Write a Post"
    )

    print(
        "3. Save a Content Idea"
    )

    return input(
        "Choose 1, 2, or 3: "
    ).strip()


def get_topic(
    choice: str
):
    """Determine the topic."""

    if choice == "2":

        topic = select_topic_from_ideas()

        if topic:
            return topic

    return input(
        "\nEnter the topic: "
    ).strip()


# ============================================================
# COMMENT WORKFLOW
# ============================================================

def run_comment_workflow(
    client,
    topic
):
    """Generate and refine a LinkedIn comment."""

    print(
        "\nDrafting initial version...\n"
    )

    comment = generate_comment(
        client,
        topic
    )

    while True:

        print(
            "\n--- Draft comment ---"
        )

        print(comment)

        print(
            "---------------------"
        )

        feedback = input(
            "\nType your feedback to revise, "
            "or press Enter to accept: "
        ).strip()

        if not feedback:
            break

        print(
            "\nRevising...\n"
        )

        comment = refine_draft(
            client,
            comment,
            feedback,
            is_comment=True
        )

    return comment


# ============================================================
# POST WORKFLOW
# ============================================================

def run_post_workflow(
    client,
    openai_client,
    topic
):
    """Generate, refine, and optionally create carousel."""

    print(
        "\nDrafting initial version...\n"
    )

    (
        post_text,
        image_prompt,
        saved_image_path
    ) = generate_post(
        client,
        openai_client,
        topic
    )

    # --------------------------------------------------------
    # REFINE POST
    # --------------------------------------------------------

    while True:

        print(
            "\n--- Draft post ---"
        )

        print(post_text)

        print(
            "---------------------"
        )

        feedback = input(
            "\nType text feedback to revise, "
            "or press Enter to accept text: "
        ).strip()

        if not feedback:
            break

        print(
            "\nRevising text...\n"
        )

        post_text = refine_draft(
            client,
            post_text,
            feedback,
            is_comment=False
        )

    # --------------------------------------------------------
    # REFINE IMAGE
    # --------------------------------------------------------

    while True:

        print(
            f"\nImage saved at: "
            f"{saved_image_path}"
        )

        print(
            f"Current Image Prompt: "
            f"{image_prompt}"
        )

        image_feedback = input(
            "\nType image feedback to revise, "
            "or press Enter to accept image: "
        ).strip()

        if not image_feedback:
            break

        print(
            "\nRevising image prompt...\n"
        )

        image_prompt = refine_image_prompt(
            client,
            post_text,
            image_prompt,
            image_feedback
        )

        print(
            "\nGenerating new image...\n"
        )

        saved_image_path = generate_post_image(
            openai_client,
            image_prompt
        )

    # --------------------------------------------------------
    # CAROUSEL
    # --------------------------------------------------------

    make_carousel = input(
        "\nWould you like to also generate "
        "a PDF carousel? (y/n): "
    ).strip().lower()

    if make_carousel == "y":

        print(
            "\nGenerating carousel slides..."
        )

        slides = generate_carousel_slides(
            client,
            topic
        )

        carousel_path = create_carousel(
            slides,
            filename="linkedin_carousel.pdf"
        )

        print(
            "\nCarousel saved successfully:"
        )

        print(
            carousel_path
        )

    return post_text


# ============================================================
# BUFFER WORKFLOW
# ============================================================

def send_to_buffer_workflow(
    final_text
):
    """Send content to Buffer."""

    send_to_buffer = input(
        "\nWould you like to send this to Buffer? (y/n): "
    ).strip().lower()

    if send_to_buffer != "y":
        return

    print(
        "\n1. Schedule to queue"
    )

    print(
        "2. Save as draft"
    )

    buffer_choice = input(
        "Choose 1 or 2: "
    ).strip()

    save_to_draft = (
        buffer_choice == "2"
    )

    print(
        "\nSending to Buffer..."
    )

    try:

        result = schedule_post_to_buffer(
            final_text,
            save_to_draft
        )

    except NameError:

        print(
            "\nBuffer integration is not defined "
            "in this file."
        )

        print(
            "Your content was generated successfully, "
            "but it was not sent to Buffer."
        )

        return

    if "errors" in result:

        print(
            f"Error: {result['errors']}"
        )

    elif (
        "data" in result
        and result["data"].get(
            "createPost",
            {}
        ).get("message")
    ):

        print(
            "Buffer Error: "
            f"{result['data']['createPost']['message']}"
        )

    else:

        if save_to_draft:

            print(
                "\nSuccess! Post is saved "
                "as a draft in Buffer."
            )

        else:

            print(
                "\nSuccess! Post is scheduled "
                "in your Buffer queue."
            )

# ============================================================
# BUFFER — SCHEDULING / DRAFT
# ============================================================

def schedule_post_to_buffer(
    text: str,
    save_to_draft: bool
) -> dict:
    """Send LinkedIn content to Buffer as a queued post or draft."""

    api_key = os.environ.get("BUFFER_API_KEY")

    if not api_key:
        raise RuntimeError(
            "BUFFER_API_KEY environment variable is not set."
        )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    query = """
    mutation CreatePost(
        $text: String!,
        $channelId: ChannelId!,
        $saveToDraft: Boolean
    ) {
        createPost(
            input: {
                text: $text
                channelId: $channelId
                schedulingType: automatic
                mode: addToQueue
                saveToDraft: $saveToDraft
            }
        ) {
            ... on PostActionSuccess {
                post {
                    id
                }
            }

            ... on MutationError {
                message
            }
        }
    }
    """

    payload = {
        "query": query,
        "variables": {
            "text": text,
            "channelId": "6a710b9a99afb44349f6d28a",
            "saveToDraft": save_to_draft
        }
    }

    response = requests.post(
        "https://api.buffer.com",
        headers=headers,
        json=payload
    )

    response.raise_for_status()

    return response.json()

# ============================================================
# MAIN APPLICATION
# ============================================================

def main():

    try:

        # ----------------------------------------------------
        # Create API clients
        # ----------------------------------------------------

        client, openai_client = get_clients()

        # ----------------------------------------------------
        # Show menu
        # ----------------------------------------------------

        choice = show_menu()

        # ----------------------------------------------------
        # Save idea
        # ----------------------------------------------------

        if choice == "3":

            handle_save_idea()

            return

        # ----------------------------------------------------
        # Validate choice
        # ----------------------------------------------------

        if choice not in (
            "1",
            "2"
        ):

            print(
                "\nInvalid choice."
            )

            return

        # ----------------------------------------------------
        # Get topic
        # ----------------------------------------------------

        topic = get_topic(
            choice
        )

        if not topic:

            print(
                "\nNo topic provided."
            )

            return

        # ----------------------------------------------------
        # Generate content
        # ----------------------------------------------------

        if choice == "1":

            final_text = run_comment_workflow(
                client,
                topic
            )

        else:

            final_text = run_post_workflow(
                client,
                openai_client,
                topic
            )

        # ----------------------------------------------------
        # Buffer
        # ----------------------------------------------------

        send_to_buffer_workflow(
            final_text
        )

    except KeyboardInterrupt:

        print(
            "\n\nOperation cancelled."
        )

    except Exception as e:

        print(
            "\nSomething went wrong:"
        )

        print(
            f"{type(e).__name__}: {e}"
        )

        sys.exit(1)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()