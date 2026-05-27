# Project Report

#### The Team members

* Names, epita email addresses, and GitHub usernames of all team members.
- Artem Iavchunovskii - artem.iavchunovskii@epita.fr - Artyom-Y
- Success Aderibigbe - success.aderibigbe@epita.fr - pulse2106
- Yuchen Zheng - yuchen.zheng@epita.fr - Meaow-09

---

#### Initial Design

* initial architecture

We made a brainstorm file. Flask was an immediate choice for it's simplicity. Some tasks where straightforward, some required reading documentation and asking copilot (later on that). Gemini API and Chromadb where among instant picks as well - because using them would mean we could look at previous labs as a reference.
* assumptions

The quiz/flashcard generation assignment seemed difficult. We assumed we would have to implement agents at first. Also, we originally didn't consider how to parse/chunk files. Ultimately, the content generation part appeared to be the most challenging at first.
* technical choices

Flask - web API. All of us already had experience with it. We kept gemini API and chromaDB because the course has introduced us to them. After consulting copilot, we settled on "unstructured" as a file parser. It's local model for parsing PDFs adds complexity, but it's otherwise an elegant all-in-one solution. To prevent further complications, we tried to use only vanilla HTML/CSS/JS. Our does HTML has two CDN script imports, but those are for parsing AI's markdown output. 

---

#### Engineering Decisions

For each major decision:

* what alternatives were considered?

Quizzes and flashcards. Once again, originally we thought of using agents (https://ai.google.dev/gemini-api/docs/agents). But then Artem had an idea of simply pre-making prompts and then passing them to AI when needed. Using this in pair with mermaid graphs could prove dangerous: in case AI hallucinates something, nothing will work. JSON vs database was an easy for this project.
* why was this solution chosen?

Using agents would complicate the development, especially considering our limited time. We chose JSON because database would introduce a lot of dependencies and more code all for a single conversation. 

---

#### Who Did What?

* Document how the project was originally divided among each team member.
* Document how responsibilities possibly evolved over time.

---

#### AI Collaboration

Document how AI tools were used.

* What tools were used for what purposes?
* How did AI influence design and implementation decisions?

We consulted ask mode about best solutions for our case. That's how we found out about "unstructured" library. Our tactic was to lead AI, not the other way around (i.e. we tried asking AI technical questions, not just asking for help)
* How did AI impact your learning and development process?
* How did you evaluate AI-generated suggestions?
* How did you detect and handle AI errors or limitations?

---

#### Failures and Iterations

Document:

* what failed?

We didn't initally understand that unstructured requires "unstructured local-inference" for PDF parsing to work.
* what surprised you?
* what required redesign?

---

#### “When AI Failed or Was Wrong”

Document cases where AI-generated advice, code, or explanations were:

* incomplete
* misleading
* incorrect

Originally, quiz & flashcards prompts said "Return a complete HTML document only," which confused AI into thinking it can't add JS (meaning the website wasn't functioning as intended)
* inefficient

Explain how you detected the issue and how you resolved it.

---

#### Lessons Learned

Reflect on:

* technical growth
* workflow improvements
* Strengths and limitations of AI-assisted development
