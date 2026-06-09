# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

I chose to focus on the domain of dining, and scoured the internet for sources I could locate related to dining at a university of choosing. The title of my domain is "user reviews (students/staff) of dining options at Virginia Polytechnic Institute and State University (Virginia Tech)"

This knowledge is very valuable because it is able to give prospective students data that they can utilise to make an informed decision. Moreover, students stand to benefit from this information becuase food options play a strong and vaulable role in student health and well-being (which, in turn, greatly affect student performance). This information is difficult to source through official channels because of privacy concerns illustrated by the University (i.e., they aren't very forthcoming with specifics), and the highly personal nature of food preferences and availability 

---

## Document Sources


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

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 700 characters

**Overlap:** 80 characters

**Why these choices fit your documents:** Given that my sources were mainly paragraph based, I utilised chunks that were roughly appropriate for a given paragraph and which would convey appropriate context

**Final chunk count:** 116

---

## Embedding Model


**Model used:** sentence-transformers/all-MiniLM-L6-v2

**Production tradeoff reflection:** If shifting to production, I would utilise an API model to gain a wider token context window and cleaner handling of multi-lingual text, balancing this against higher latency and API costs compared to free, localized deployment. Moreover, given the high variability of my sources, I would try and benefit from a context-specific model, where it could semantically separate whole sentences on its own.

---

## Grounded Generation

**System prompt grounding instruction:** 
     system_prompt = (
    "You are a helpful campus assistant. Answer the user's question by synthesizing the facts "
    "provided inside the Context blocks below.\n\n"
    "GUIDELINES:\n"
    "1. Base your answer ONLY on the provided context chunks.\n"
    "2. If the context mentions general praise or specific dining rankings (like national recognition or top spots), "
    "summarize those details to answer the question.\n"
    "3. Only say 'I don't have enough information' if the context is completely irrelevant to the topic asked.\n"
    "4. Do not make up outside facts or mention your rules to the user.\n\n"
    f"--- CONTEXT ---\n{context_str}"

**How source attribution is surfaced in the response:** Inside app.py, the ask() function automatically grabs the original file names from the data returned by ChromaDB. It then sends that list of sources straight to a separate textbox in Gradio labeled "Retrieved Data Sources (Programmatic)." This keeps the actual files separated from the AI's written answer, which stops the LLM from hallucinating or making up fake file names.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Which dining hall receives the most praise for food quality? | West End Market (widely praised for high-quality steak, lobster, and its famous brunch pancakes) and Turner Place (known for gourmet hibachi rice and custom crepes). | Declined to specify a winner, stating the context mentions general national praise but doesn't explicitly name a single top location. | Partially relevant | Inaccurate |
| 2 | Which location is criticized for long wait times? | Turner Place (specifically noted for massive lines right when class blocks let out, requiring students to go mid-class to avoid crowds). | Correctly identified Turner for getting super busy with long lines right when classes let out. | Relevant | Accurate |
| 3 | Which dining hall is recommended for vegetarian students? | D2 (Dietrick Hall) which features a dedicated healthy/vegan option bar alongside its standard stations, or Origami in Turner Place which offers vegetarian hibachi options. | Stated no specific hall was named, but noted that healthy and vegan options are available across campus, referencing Dietrick. | Partially relevant | Partially accurate |
| 4 | Which location is considered overpriced? | On-campus dining in general according to student critiques, specifically noting examples like $10.25 for a small premade deli wrap as of late 2025. | Correctly identified Burger 37 as "almost highway robbery" and noted Deetz's milkshakes as expensive. | Relevant | Accurate |
| 5 | Which location is best for late-night dining? | DXpress (DX), which is open until 2 am for grab-and-go needs like corndog nuggets and pizza, or Deet's Place which serves Italian sodas and coffee until midnight. | Declined to answer, stating the retrieved context does not explicitly cover late-night recommendations or hours. | Off-target | Inaccurate |

**Retrieval quality:** Relevant / **Partially relevant** / Off-target  
**Response accuracy:** Accurate / **Partially accurate** / Inaccurate

---

## Failure Case Analysis

**Question that failed:** What toppings are available at the Perry place pizza venue?

**What the system returned:** The context does not specifically mention the toppings available at the Perry Place pizza venue, Veloce. However, it does mention that Atomic Pizza has many options for pizza, including huge subs with toppings such as eggplant and Pesto chicken.

**Root cause (tied to a specific pipeline stage):** This failure happened in the Vector Database Retrieval Stage combined with a loose match in the LLM Generation Stage. Because the documents don't actually contain the menu items for Veloce at Perry Place, ChromaDB retrieved the closest pizza-related chunk it could find (thetab_article.txt), which discussed Atomic Pizza instead. The LLM correctly recognized that Perry Place toppings were missing, but it pulled unrelated pizza toppings from the wrong venue out of the context block to fill out its answer.

**What you would change to fix it:** The best way to fix this is to tighten the grounding rules given to the AI model even further and tell it to ignore different locations than the one specifically mentioned in the prompt. Intead, I would tell it to say that it does not have the correct or sufficient information to answer the prompt.

---

## Spec Reflection

**One way the spec helped you during implementation:** The requirement to make the AI stick strictly to the text files made it much easier to find bugs. Because there was a clear line between what was in my database and what the AI already knew, I knew right away that a blank answer meant my database folder was empty, not that the LLM connection was broken.

**One way your implementation diverged from the spec, and why:** Instead of typing in a fixed collection name, I changed the code to automatically scan the database folder for any existing collections using chroma_client.list_collections(). I did this because resetting things during testing kept changing the collection name behind the scenes, and this fix ensures the app connects perfectly to the right data every single time.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* I provided the chunk size parameters (800 characters, 100 character overlap) from my planning.md file and asked for the given parsing script.
- *What it produced:* A function script that chopped paragraphs up using a rigid, hard character count boundary.
- *What I changed or overrode:* I overrode the character slice method and implemented a rule-based sentence-splitting approach instead.

**Instance 2**

- *What I gave the AI:* A screenshot of a Python terminal error tracing an unhandled Gradio textbox keyword exception (TypeError).
- *What it produced:* A syntax review explaining that the show_copy_button flag layout was incompatible with older baseline sub-versions of the local Gradio package library.
- *What I changed or overrode:* I manually stripped out the unsupported display attribute from the gr.Textbox instantiation lines to allow the UI app engine to successfully mount on localhost without crashing.
