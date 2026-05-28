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

-This is was also done in parallel with our other RLA project in which Yuchen had started ahead of time, since he didnt have much work here-
Artem - backend, Success - frontend, Yuchen - docs and debugging.
* Document how responsibilities possibly evolved over time.

Artem - ended up also participating in frontend development too (chat.html outline, settings.html)
Success - did all of the Javascript and some backend (ensuring Flask-Javascript communication)
Yuchen - remained close to his original goal, also made us a presentation

---

#### AI Collaboration

Document how AI tools were used.

* What tools were used for what purposes?

Copilot - we mostly used ask mode, because we like having control over our development process. Chromadb chatbot - Artem had a little interaction on the website, which made him realise we need a parsing/chunking function. Gemini - Success used it for CSS styles (that's mainly for cosmetic purpose, a lot of essential CSS was written manually)
* How did AI influence design and implementation decisions?

We consulted ask mode about best solutions for our case. That's how we found out about "unstructured" library. Our tactic was to lead AI, not the other way around (i.e. we tried asking AI technical questions, not just asking for help). It's a good tool to look up a library for your project
* How did AI impact your learning and development process?

When something didn't work or confused us - we asked. It often saved us time. As much as we appreciate community help online, it might take a long time to find an answer.
* How did you evaluate AI-generated suggestions?

Mostly by their complexity and how do they compare to our knowledge level. We didn't try to shoot for the stars, so we always prioritezed functional and simple.
* How did you detect and handle AI errors or limitations?

Best way to handle is not to do anything blindly. Reading, understanding and only then implementing AI's suggestions was the key. Also staying away from overusing the agent mode

---

#### Failures and Iterations

Document:

* what failed?

We didn't initally understand that unstructured requires "unstructured local-inference" for PDF parsing to work.
During initial rag setups we were trying to pass the filename with the extension to chromaDB which led to an error, because chromaDB does not accept .
* what surprised you?

Gemini takes fairly little time to respond.
* what required redesign?

Initially, model.py was not a class. Success later refactored it to prevent creating the chat object repeatedly (and instead storing it as a property)

---

#### “When AI Failed or Was Wrong”

Document cases where AI-generated advice, code, or explanations were:

* incomplete

Of course AI can't read minds (yet), so some responses didn't answer all our questions. That's a call for us to be more precise with prompts.
* misleading

Similarly to "inefficient" section, we believe AI wasn't always as elaborate as it should have been. In those cases, we would go to the internet or ask a follow up question.
* incorrect

Originally, quiz & flashcards prompts said "Return a complete HTML document only," which confused AI into thinking it can't add JS (meaning the website wasn't functioning as intended).
* inefficient

Oftentimes we received explanations which were too broad. For a person new to a topic (e.g. to JS polling) it's difficult to make any use of advice like that. Whether it was socratic mode or "don't write code" part of the prompt, sometimes the prompts where not specific enough.

#### Explain how you detected the issue and how you resolved it.

For the aforementioned quiz & flashcards prompts, we had to restructure them a bit. "Use only HTML with simplistic CSS and Javascript (e.g. for quiz score calculation)" proved to work well.

---

#### Lessons Learned

Reflect on:

* technical growth

A lot of concepts learned: JS polling, flask endpoints (more advanced), RAG and everything that pertains to it, web API interaction, prompt engineering, error handling...
* workflow improvements

Asking AI to create a "separation of concerns" plan worked well. In particular, Artem asked AI to explain how to do file uploads and how to separate it between python and javascript. And that was of great help, because we could share the plan and do our own parts.
* Strengths and limitations of AI-assisted development

AI can speed up the process a lot (especially by eliminating the need for long web searching sessions) and helps you understand everything. It being context-driven makes it superior than simple web search. Moreover, it's very easy to find bugs using it.
Limitation - it's easy to lose control if you're not coding consciously and relying on AI. That's something we avoided during this project. Moreover, the AI may trained on old data, which means it can't use modern syntax/libraries. It's a big downside in a rapid programming environment