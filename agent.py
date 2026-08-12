import os
import sys
import requests
import base64
from datetime import datetime

import requests
from anthropic import Anthropic
from openai import OpenAI

# --- Configuration -----------------------------------------------------

MODEL = "claude-sonnet-5"
IMAGE_MODEL = "gpt-image-1"

# Fill this in with a short summary of your background so Claude can write
# comments that sound like you. A few sentences is plenty — you don't need
# your full resume here.
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
Senior Executive Chef / Multi-Unit Market Leader — Operational Excellence PMO  |  P.F. Chang's  |  NC |  Dec 2010 – Feb 2022
12-year progressive operational excellence leadership across 7 NC locations with full P&L accountability for $35M+ annual portfolio.
•	Led two full greenfield restaurant launches (~$14M combined scale) with end-to-end project management: coordinated vendors and contractors, managed project timelines, allocated resources, directed staffing and training, and validated operational readiness — both delivered on time and within budget.
•	Ranked #3 in profitability among 210+ national PF Chang's units through operational excellence discipline; managed $5M–$7M annual revenue per location across a 7-location NC portfolio.
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

EXAMPLES = """ Example 1: Culture always wins long-term. Relying on one talented chef isn't sustainable — he can't work seven days a week forever, and if he tries, he'll burn out. Whatever his attitude is, it spreads: the team either gets too afraid to speak up, or starts mirroring his behavior back. And there's no version of unhappy, nervous staff delivering a genuinely happy guest experience. It shows, every time. I wouldn't terminate him — his talent is real and hard to replace. But coaching the behavior is non-negotiable. The key is understanding the why behind it first. Is it stress, insecurity, unclear expectations, burnout, something from outside work bleeding in? That root cause is what tells you how to actually approach him, instead of just reacting to the symptom. 16 years in operations taught me this: the food or product might be what customers notice first, but the culture is what determines whether you still have a great team a year from now.

Example 2: I'd actually push back a little here. Titles matter more than we'd like to admit, especially in a world where most resumes go through an ATS before a human ever sees them. If the keyword the system is scanning for is 'Manager' and your title says 'Lead,' you may never even surface in the search, regardless of your actual scope of responsibility. On top of that, your title on paper has to match what your employer verifies in a background check — you can't just tailor it after the fact to sound bigger than what's official. So candidates aren't just being precious about a label. They're thinking ahead to their next move, and the next one after that. Tailoring your resume bullet points to describe real scope and impact can only do so much when the title field itself is what's filtering you in or out before anyone reads those bullet points. In a perfect world, employers would judge based on substance alone — but candidates have to operate in the system that actually exists today, not the one we wish existed.

Example 3: Really appreciate you sharing this — insider stories on how someone like Jeff Bezos actually operates day-to-day at that level are far more valuable than the polished leadership advice most people put out. The 'decode the humans' point stands out most to me. In my own experience, the technical or financial case rarely fails on its own merit — it fails because the person presenting it didn't anticipate what the decision-maker actually cared about going in. Preparation isn't just knowing your numbers; it's knowing your audience well enough to speak in the terms that matter to them. Thanks for breaking this down with real specifics instead of vague theory. """.strip()


SYSTEM_PROMPT = f"""You are helping an Operations Leader draft comments and create posts on LinkedIn. Here is their background:

{RESUME_SUMMARY}
Here are examples of their writing style and perspective:

{EXAMPLES}

When given a topic, write ONE LinkedIn comment that:
- Sounds warm, genuine, and professional (not salesy or generic)
- Draws a light, credible connection to the person's PMO/Operations background
  where it naturally fits — don't force it
- Is 2-4 sentences long, conversational in tone
- Avoids corporate buzzword overload and avoids hashtags
- Does not use emojis unless the topic clearly calls for a light touch
- Reads like something a real person typed, not an AI-generated blurb

Return ONLY the comment text, with no preamble, quotation marks, or labels.
""".strip()


def generate_comment(client: Anthropic, topic: str) -> str:
    """Call Claude to draft a LinkedIn comment for the given topic."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"The LinkedIn post topic is: {topic}\n\nDraft the comment now.",
            }
        ],
    )

    # response.content is a list of content blocks; join any text blocks
    return "".join(block.text for block in response.content if block.type == "text").strip()


def generate_image_prompt(client: Anthropic, topic: str, post_text: str) -> str:
    """Ask Claude to write a detailed, professional gpt-image-1 prompt matching the post."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        system=(
            "You write image-generation prompts for gpt-image-1 to accompany LinkedIn posts. "
            "Given a post topic and the drafted post text, write ONE highly descriptive, "
            "professional prompt for a realistic, photographic image that would work well "
            "as a LinkedIn header image for this post. Favor a realistic corporate/operations "
            "photography style (e.g. warehouse, office, retail floor, team meeting, leadership "
            "scene) over anything cartoonish, abstract, or text-heavy. Do not include any text, "
            "logos, or words in the image itself. Return ONLY the image prompt, with no preamble "
            "or labels."
        ),
        messages=[
            {
                "role": "user",
                "content": f"Post topic: {topic}\n\nPost text:\n{post_text}\n\nWrite the gpt-image-1 prompt now.",
            }
        ],
    )
    return "".join(block.text for block in response.content if block.type == "text").strip()


def generate_post_image(openai_client: OpenAI, image_prompt: str) -> str:
    """Call gpt-image-1 to generate an image, download it, and save it as a PNG.

    Returns the local file path of the saved image.
    """
    result = openai_client.images.generate(
        model=IMAGE_MODEL,
        prompt=image_prompt,
        size="1024x1024",
        quality="high",
        n=1,
    )

    image_data = result.data[0]

    # The API can return either a direct URL or base64-encoded image data
    # depending on account/response settings — handle both.
    if getattr(image_data, "url", None):
        img_response = requests.get(image_data.url, timeout=60)
        img_response.raise_for_status()
        image_bytes = img_response.content
    elif getattr(image_data, "b64_json", None):
        image_bytes = base64.b64decode(image_data.b64_json)
    else:
        raise RuntimeError("DALL-E response did not include a URL or base64 image data.")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"linkedin_post_image_{timestamp}.png"
    output_dir = r"c:\Users\tahnh\OneDrive\Desktop\LinkedIn Agent\LinkedIn_post_image"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "wb") as f:
        f.write(image_bytes)

    return filepath


def generate_post(client: Anthropic, openai_client: OpenAI, topic: str):
    """Draft a full LinkedIn post, then generate and save a matching image.

    Returns a tuple: (post_text, image_prompt, saved_image_path)
    """
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
                "content": f"Create a LinkedIn post about: {topic}",
            }
        ],
    )
    post_text = "".join(
        block.text for block in response.content if block.type == "text"
    ).strip()

    image_prompt = generate_image_prompt(client, topic, post_text)
    saved_image_path = generate_post_image(openai_client, image_prompt)

    return post_text, image_prompt, saved_image_path

def schedule_post_to_buffer(text: str, save_to_draft: bool) -> dict:
    """Create (and optionally queue) a post on Buffer for the configured channel."""
    api_key = os.environ.get("BUFFER_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    query = """
    mutation CreatePost($text: String!, $channelId: ChannelId!, $saveToDraft: Boolean) {
      createPost(input: {
        text: $text,
        channelId: $channelId,
        schedulingType: automatic,
        mode: addToQueue,
        saveToDraft: $saveToDraft
      }) {
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

    response = requests.post("https://api.buffer.com", headers=headers, json=payload)
    return response.json()

def refine_draft(client: Anthropic, original_text: str, feedback: str, is_comment: bool) -> str:
    """Revise a previously drafted comment or post based on user feedback."""
    prompt_type = "comment" if is_comment else "post"
    max_tokens = 300 if is_comment else 600

    system_instruction = SYSTEM_PROMPT + (
        f"\n\nYou are revising a draft {prompt_type} based on the user's feedback."
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system_instruction,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Original draft:\n{original_text}\n\n"
                    f"User feedback:\n{feedback}\n\n"
                    "Generate the revised draft."
                ),
            }
        ],
    )

    return "".join(block.text for block in response.content if block.type == "text").strip()

def refine_image_prompt(client: Anthropic, post_text: str, current_prompt: str, feedback: str) -> str:
    system_instruction = SYSTEM_PROMPT + "\n\nYou are an expert at writing highly detailed prompts for DALL-E 3."
    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        system=system_instruction,
        messages=[
            {
                "role": "user",
                "content": f"Finalized post text:\n{post_text}\n\nCurrent image prompt:\n{current_prompt}\n\nUser feedback for the image:\n{feedback}\n\nWrite a revised, highly descriptive DALL-E 3 image prompt based on this feedback. Return only the prompt.",
            }
        ],
    )
    return "".join(block.text for block in response.content if block.type == "text").strip()

def save_idea(idea: str) -> None:
    """Append a content idea to ideas.txt."""
    with open("ideas.txt", "a") as f:
        f.write(idea + "\n")

def get_ideas() -> list:
    """Read saved content ideas from ideas.txt, one per line."""
    if not os.path.exists("ideas.txt"):
        return []

    with open("ideas.txt", "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable is not set.")
        sys.exit(1)
    if not openai_key:
        print("Error: OPENAI_API_KEY environment variable is not set.")
        sys.exit(1)

    client = Anthropic(api_key=api_key)
    openai_client = OpenAI(api_key=openai_key)

    print("1. Draft a Comment")
    print("2. Write a Post")
    print("3. Save a Content Idea")
    choice = input("Choose 1, 2, or 3: ").strip()

    # --- Option 3: save an idea and exit early ---
    if choice == "3":
        idea = input("Enter your content idea to save: ").strip()
        if idea:
            save_idea(idea)
            print("\nIdea saved to ideas.txt!")
        sys.exit(0)

    # --- Determine the topic (option 2 can pull from saved ideas) ---
    topic = ""
    if choice == "2":
        saved_ideas = get_ideas()
        if saved_ideas:
            print("\nSaved Ideas:")
            for idx, idea in enumerate(saved_ideas, 1):
                print(f"{idx}. {idea}")
            print(f"{len(saved_ideas) + 1}. Write about a new topic")

            idea_choice = input("Choose an idea number: ").strip()
            try:
                selected_idx = int(idea_choice) - 1
                if 0 <= selected_idx < len(saved_ideas):
                    topic = saved_ideas[selected_idx]
            except ValueError:
                pass

    if not topic:
        topic = input("Enter the topic: ").strip()
    if not topic:
        sys.exit(1)

    print("\nDrafting initial version...\n")

    try:
        # --- Option 1: comment flow ---
        if choice == "1":
            comment = generate_comment(client, topic)

            while True:
                print("--- Draft comment ---")
                print(comment)
                print("---------------------")

                feedback = input("\nType your feedback to revise, or press Enter to accept: ").strip()
                if not feedback:
                    break

                print("\nRevising...\n")
                comment = refine_draft(client, comment, feedback, is_comment=True)

            final_text = comment

        # --- Option 2: post + image flow ---
        else:
            post_text, image_prompt, saved_image_path = generate_post(client, openai_client, topic)

            while True:
                print("--- Draft post ---")
                print(post_text)
                print("---------------------")

                text_feedback = input("\nType text feedback to revise, or press Enter to accept text: ").strip()
                if not text_feedback:
                    break

                print("\nRevising text...\n")
                post_text = refine_draft(client, post_text, text_feedback, is_comment=False)

            final_text = post_text

            while True:
                print(f"\nImage saved at: {saved_image_path}")
                print(f"Current Image Prompt: {image_prompt}")

                image_feedback = input("\nType image feedback to revise, or press Enter to accept image: ").strip()
                if not image_feedback:
                    break

                print("\nRevising image prompt...\n")
                image_prompt = refine_image_prompt(client, final_text, image_prompt, image_feedback)

                print("\nGenerating new image...\n")
                saved_image_path = generate_post_image(openai_client, image_prompt)

            # --- Optionally send the finished post to Buffer ---
            send_to_buffer = input("\nWould you like to send this to Buffer? (y/n): ").strip().lower()
            if send_to_buffer == "y":
                print("\n1. Schedule to queue")
                print("2. Save as draft")
                buffer_choice = input("Choose 1 or 2: ").strip()
                save_to_draft = (buffer_choice == "2")

                print("\nSending to Buffer...")
                result = schedule_post_to_buffer(final_text, save_to_draft)

                if "errors" in result:
                    print(f"Error: {result['errors']}")
                elif "data" in result and result["data"].get("createPost", {}).get("message"):
                    print(f"Buffer Error: {result['data']['createPost']['message']}")
                else:
                    if save_to_draft:
                        print("\nSuccess! Post is saved as a draft in Buffer.")
                    else:
                        print("\nSuccess! Post is scheduled in your Buffer queue.")

    except Exception as e:
        print(f"Something went wrong: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
