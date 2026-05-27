from utilities import get_context

ai_prompts = {
"quiz": 
"""You are generating a simple html webpage with a quiz based on the context above. And chat interactions (if they exist).

Task:
- Create a standalone HTML document.
- Amount of questions depends on the context size.
- Don't go above 15 questions.
- Each question is either True/False or 1 correct answer out of 4.
- 1 question = 1 HTML radio type input.

Rules:
- Use only facts supported by the provided context.
- Do not invent details not present in the source material.
- Return a complete HTML document only.
- Do not add markdown fences, explanations, or extra commentary.
- Keep the HTML self-contained and simple enough to save as a file and open directly in a browser. You may add CSS for readability.
- If the information is limited on a certain subject, keep output about that subject minimal rather than fabricating content.

Output:
- Return only the final HTML.""",

"flashcard":
"""You are generating a simple flashcards webpage for studying based on the context above. And chat interactions (if they exist).

Task:
- Create a standalone HTML document.
- Amount of flashcards depends on the context size.
- Don't go above 20 flashcards.
- One flashcard is displayed on the screen at a time.
- Flashcards have to sides: word and it's definition.
- Click on a flashcard to flip it (switch between term and definition).
- Flashcard displayed on top, navigation arrows at the bottom.

Rules:
- Use only facts supported by the provided context.
- Do not invent details not present in the source material.
- Return a complete HTML document only.
- Do not add markdown fences, explanations, or extra commentary.
- Keep the HTML self-contained and simple enough to save as a file and open directly in a browser. You may add CSS for readability.
- If the information is limited on a certain subject, keep output about that subject minimal rather than fabricating content.

Output:
- Return only the final HTML.""",

"visualization":
"""You are generating a simple html page with a mermaid diagram using the provided context. 
The goal is to represent the relationships visually.

Task:
- Create a standalone HTML document.
- Strictly follow mermaid javascript library syntax.
- Wrap labels that contain special characters in double quotes. Avoid raw HTML (<...>) in labels. Escape quotes by using alternate quoting or remove them.
- Keep diagrams small: not more than 30 nodes and 60 chars per label; avoid huge graphs that may not render or exceed prompt/context budgets.
- If the provided context is computer code, use sequence diagram. Else, use flowchart. 
- Import via CDN: <script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
- Enclose mermaid syntax in <pre class="mermaid"></pre> tags.
- Besides script and pre tags, the document may contain basic HTML syntax (doctype, html, head and body tags) and minimalistic CSS
- In body, after pre tag with the chart, include a short text explanation of the chart.

Rules:
- Use only facts supported by the provided files.
- Do not invent details not present in the source material.
- Return a complete HTML document only.
- Do not add markdown fences, explanations, or extra commentary.
- Keep the HTML self-contained and simple enough to save as a file and open directly in a browser.
- If the information is limited on a certain subject, keep output about that subject minimal rather than fabricating content.

Output:
- Return only the final HTML."""
}

chromadb_queries = {
    "quiz": "Select key facts, terminology and definitions for a quiz.",
    "flashcard": "Select most important information for making studying flashcards.",
    "vizualization": "Select key data and relationships for building a chart."
}

def form_prompt(content_type, collection_names):
    content_type = content_type.lower()
    chromadb_query = chromadb_queries[content_type]
    ai_prompt = ai_prompts[content_type]

    if collection_names:
            context = "Context: \n"
            for collection_name in collection_names:
                context += get_context(chromadb_query, collection_name, n_results=15)
    else:
         raise ValueError("No collection names given")
    
    prompt = context + "\n" + ai_prompt
    return prompt