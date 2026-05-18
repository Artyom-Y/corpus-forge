# This Journal gets updated automatically by the Journal Logger Agent

### **New Interaction**
- **Hook Version**: 1.02
- **Date**: 17-05-2026 13:58
- **Prompt**: I'm creating a simple web app with RAG functionality. I want to explore two points (prioritize teaching me to just giving answers). One: what's a better way to dynamically update the page with AI's responses? Maybe I should disable streaming to make it easier? But even then, I doubt just using HTTP methods would be enough. Two: for RAG, should I use chromadb or gemini-embedding-2, considering I'm already planning to use google's genai module for AI interaction? I need the embeddings to be free and persistent

### **New Interaction**
- **Hook Version**: 1.02
- **Date**: 17-05-2026 14:56
- **Prompt**: Could you recommend me a python library for extracting text from PDFs, markdowns and source code files? I need it to create embeddings

### **New Interaction**
- **Hook Version**: 1.02
- **Date**: 18-05-2026 20:47
- **Prompt**: earlier i asked about methods of making the page update with AI's response. now i want to add a question on top: what are our options for saving the chat history? does google gemini api have a solution for that? JSON could work. we update the JSON file with AI's response and then update the webpage with new JSON. But that would mean we have to pass a larger file each time. maybe there are alternatives I'm not aware of like some python library? also the solution should work well with the web page updating. optimization isn't the biggest concern, we need something that's both understandable for a first year and quick to implement

### **New Interaction**
- **Hook Version**: 1.02
- **Date**: 18-05-2026 21:14
- **Prompt**: i like your suggestion, but first i need to understand how will that work (i need to write google gemini API functions to work with this setup). please explain step by step how are the functions related (less emphasis on helper functions, more on polling and what does "messages" page do). also, could we use document.getElementById("demo").innerHTML = <something inside fetchMessages to update our chatbox?
