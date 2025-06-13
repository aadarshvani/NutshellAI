"""
Simple AI summarization using LangChain and Groq
"""
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain

def get_prompt_template(format_type, word_limit):
    """Get prompt template based on format"""
    
    templates = {
        "structured": f"""
        Summarize the following content in {word_limit} words with this structure:
        
        **Crux:** [Main point]
        **Key Takeaways:** [Important points]
        **Instructions:** [Action items if any]
        **Conclusion:** [Final summary]
        
        Content: {{text}}
        """,
        
        "bullet_points": f"""
        Summarize the following content in {word_limit} words using bullet points:
        
        Content: {{text}}
        
        Format as clear bullet points (•) with the most important information.
        """,
        
        "paragraph": f"""
        Write a flowing {word_limit}-word summary of the following content:
        
        Content: {{text}}
        
        Create a natural, readable paragraph that captures the main ideas.
        """,
        
        "executive": f"""
        Create an executive summary of the following content in {word_limit} words:
        
        Content: {{text}}
        
        Focus on key findings, recommendations, and business implications.
        """
    }
    
    template = templates.get(format_type, templates["structured"])
    return PromptTemplate(input_variables=['text'], template=template)

def create_summarizer(api_key, model_name):
    """Create summarizer instance"""
    try:
        llm = ChatGroq(
            api_key=api_key,
            model=model_name,
            temperature=0.3
        )
        return llm
    except Exception as e:
        raise Exception(f"Failed to create summarizer: {str(e)}")

def summarize_content(documents, api_key, model_name, format_type, word_limit):
    """Summarize documents"""
    try:
        # Create LLM
        llm = create_summarizer(api_key, model_name)
        
        # Get prompt template
        prompt = get_prompt_template(format_type, word_limit)
        
        # Create chain
        chain = load_summarize_chain(
            llm=llm,
            chain_type="stuff",
            prompt=prompt
        )
        
        # Generate summary using invoke (not deprecated run)
        result = chain.invoke({"input_documents": documents})
        summary = result["output_text"]
        
        if not summary.strip():
            raise Exception("Empty summary generated")
        
        return {
            "summary": summary.strip(),
            "word_count": len(summary.split()),
            "model_used": model_name,
            "format_type": format_type
        }
        
    except Exception as e:
        if "rate limit" in str(e).lower():
            raise Exception("Rate limit exceeded. Please try again in a few moments.")
        elif "api key" in str(e).lower():
            raise Exception("Invalid API key. Please check your Groq API key.")
        else:
            raise Exception(f"Summarization failed: {str(e)}")