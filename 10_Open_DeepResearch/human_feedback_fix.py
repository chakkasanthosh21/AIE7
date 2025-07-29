# Copy this function and replace the human_feedback function in your notebook

def human_feedback(state: ReportState, config: RunnableConfig) -> Command[Literal["generate_report_plan","build_section_with_web_research"]]:
    """Get feedback on the report plan - simplified to avoid interrupt issues"""
    sections = state['sections']
    
    # For demo purposes, automatically approve the plan
    # In a real implementation, you would handle user input here
    user_approval = True  # This would come from user input
    
    if user_approval:
        # Approve and kick off section writing
        return Command(goto=[
            Send("build_section_with_web_research", {"topic": state["topic"], "section": s, "search_iterations": 0}) 
            for s in sections 
            if s.research
        ])
    else:
        # Regenerate the report plan with feedback
        feedback = "Please improve the report structure"  # This would come from user input
        return Command(goto="generate_report_plan", 
                       update={"feedback_on_report_plan": feedback}) 