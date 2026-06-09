# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

I chose to focus on the domain of dining, and scoured the internet for sources I could locate related to dining at a university of choosing. The title of my domain is "user reviews (students/staff) of dining options at Virginia Polytechnic Institute and State University (Virginia Tech)"

This knowledge is very valuable because it is able to give prospective students data that they can utilise to make an informed decision. Moreover, students stand to benefit from this information becuase food options play a strong and vaulable role in student health and well-being (which, in turn, greatly affect student performance). This information is difficult to source through official channels because of privacy concerns illustrated by the University (i.e., they aren't very forthcoming with specifics), and the highly personal nature of food preferences and availability 

---

## Documents

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Business Insider | Business Insider article profiling Virginia Tech's award-winning dining centers, focusing on high-quality offerings like lobster, brisket, and campus chains. | https://www.businessinsider.com/virginia-tech-best-campus-dining-2014-10 |
| 2 | College Confidential | College Confidential forum thread discussing VT's flexible dining plans, meal cost structure, individual chef setups, and late-night recommendations. | https://talk.collegeconfidential.com/t/how-good-is-the-food-really/2074350/2 |
| 3 | Collegiate Times (Op-Ed) | Collegiate Times op-ed evaluating the required meal plan structure for first-years, discussing the repetitive nature of eating on campus, and comparing identical venue menus. | https://www.collegiatetimes.com/opinion/a-year-of-eating-at-virginia-tech/article_7a3c5ed9-b8d5-4498-9285-7aa2c30d0e12.html |
| 4 | Collegiate Times | Collegiate Times foodie guide offering recommendations on overlooked items like Turner's crepes, Deet's Italian sodas, and Owen's Fantastic Frank sandwich. | https://www.collegiatetimes.com/lifestyles/good-eats-a-foodies-guide-to-virginia-tech-dining/article_b946dbac-c4ea-11e9-97f8-cf607c6f136b.html |
| 5 | Her Campus | Her Campus forum review ranking top venues like Turners and West End from a freshman picky eater perspective, while identifying subpar options like Newman Library Cafe. | https://www.hercampus.com/life/summer-everything-bag-cvs/ |
| 6 | Journeyman Joe | Journeyman Joe blog post reviewing an all-you-can-eat student dinner experience at Dietrick Dining Hall (D2), detailing the architecture, pricing, and food variety. | https://journeymanjoe.com/dining-at-d2-a-vt-dining-hall-experience/ |
| 7 | Niche | Niche campus review critique highlighting high food prices, pricing discrepancies, and broader student observations regarding campus affordability. | https://www.niche.com/colleges/virginia-tech/reviews/?page=2 |
| 8 | Spoon University | Spoon University review praising VT's Princeton Review ranking, focusing on DXpress grab-and-go options, Qdoba value, and weekend West End/D2 brunches. | https://spoonuniversity.com/school/virginia-tech/virginia-tech-dining-beyonce-college-food/ |
| 9 | The Tab | The Tab comprehensive dining hall guide ranking options from worst to best, featuring specific dish reviews for Turners Place, D2, and tips to avoid crowds. | https://archive.thetab.com/us/virginiatech/2017/06/13/virginia-tech-dining-hall-guide-worst-to-best-2505 |
| 10 | Reddit | Reddit thread on r/VirginiaTech exploring an unpopular junior opinion stating that campus food options are unhealthy, overrated, and over-reliant on fast-food chains. | https://www.reddit.com/r/VirginiaTech/comments/1n155b2/unpopular_opinion_the_food_at_tech_is_so_overrated/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size: 800 characters**

**Overlap: 100 characters**

**Reasoning: Most of the included sources are reviews of some sort or posts on forums. While highly individual, the vast majority are split into paragraph form, which are well-suited to fit into approximately 00 character chunks**

---

## Retrieval Approach

**Embedding model: sentence-transformers/all-MiniLM-L6-v2**

**Top-k: 4**

**Production tradeoff reflection:**

---

## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Which dining hall receives the most praise for food quality? | West End Market (widely praised for high-quality steak, lobster, and its famous brunch pancakes) and Turner Place (known for gourmet hibachi rice and custom crepes). |
| 2 | Which location is criticized for long wait times? | Turner Place (specifically noted for massive lines right when class blocks let out, requiring students to go mid-class to avoid crowds). |
| 3 | Which dining hall is recommended for vegetarian students? | D2 (Dietrick Hall) which features a dedicated healthy/vegan option bar alongside its standard stations, or Origami in Turner Place which offers vegetarian hibachi options. |
| 4 | Which location is considered overpriced? | On-campus dining in general according to student critiques, specifically noting examples like $10.25 for a small premade deli wrap as of late 2025. |
| 5 | Which location is best for late-night dining? | DXpress (DX), which is open until 2 am for grab-and-go needs like corndog nuggets and pizza, or Deet's Place which serves Italian sodas and coffee until midnight. |

---

## Anticipated Challenges

1. Overfragmentation, i.e. a chunk does not split the text very well and we are left with adkward and lanky chunks that do not lead to a good query answer 

2. Hallucinations in the form of general advice when the ingested documents lack super-specific menu items

---

## Architecture

[Document Ingestion: txt files] ──> [Chunking: Paragraph-based Chunker] ──> [Embedding: all-MiniLM-L6-v2] ──> [Vector Store: ChromaDB] ──> [Retrieval: Top-k Query] ──> [Generation: Groq Llama-3.3-70b-versatile]

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
