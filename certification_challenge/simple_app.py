"""
Simple Student Loan Assistant - Web UI
A basic working version for demonstration.
"""

import streamlit as st
import os
import sys
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Student Loan Assistant",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    font-weight: bold;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.sub-header {
    font-size: 1.5rem;
    color: #2c3e50;
    margin-bottom: 1rem;
}
.chat-message {
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
}
.user-message {
    background-color: #e3f2fd;
    border-left: 4px solid #2196f3;
}
.assistant-message {
    background-color: #f3e5f5;
    border-left: 4px solid #9c27b0;
}
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'system_ready' not in st.session_state:
        st.session_state.system_ready = True

def display_header():
    """Display the main header."""
    st.markdown('<h1 class="main-header">🎓 Student Loan Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">AI-Powered Guidance for Federal Student Loans</p>', unsafe_allow_html=True)

def display_sidebar():
    """Display the sidebar with controls."""
    with st.sidebar:
        st.markdown("## 🔧 System Controls")
        
        if st.session_state.system_ready:
            st.success("✅ System Ready")
        else:
            st.warning("⚠️ System Not Ready")
        
        st.markdown("---")
        
        # Quick Actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
        
        st.markdown("---")
        
        # Example Queries
        st.markdown("### 💡 Example Queries")
        example_queries = [
            "What are the eligibility requirements for federal student loans?",
            "How do I apply for a Direct Loan?",
            "What are the current interest rates for student loans?",
            "How do I repay my student loans?",
            "What happens if I can't make my loan payments?",
            "What is the difference between subsidized and unsubsidized loans?",
            "How do I consolidate my student loans?",
            "What are the loan forgiveness options?"
        ]
        
        for query in example_queries:
            if st.button(query[:50] + "...", key=f"example_{hash(query)}"):
                st.session_state.example_query = query
                st.rerun()

def display_chat_interface():
    """Display the main chat interface."""
    st.markdown('<h2 class="sub-header">💬 Ask Your Student Loan Questions</h2>', unsafe_allow_html=True)
    
    # Chat input
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_query = st.text_area(
            "Enter your question:",
            placeholder="e.g., What are the eligibility requirements for federal student loans?",
            height=100,
            key="user_input"
        )
    
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        submit_button = st.button("🚀 Ask Assistant", type="primary")
    
    # Handle example query
    if hasattr(st.session_state, 'example_query'):
        user_query = st.session_state.example_query
        del st.session_state.example_query
        submit_button = True
    
    # Process query
    if submit_button and user_query.strip():
        process_user_query(user_query.strip())

def process_user_query(query: str):
    """Process a user query and display the response."""
    # Add user message to chat history
    st.session_state.chat_history.append({
        "role": "user",
        "content": query,
        "timestamp": datetime.now()
    })
    
    # Generate response (simplified for demo)
    response = generate_demo_response(query)
    
    # Add assistant response to chat history
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response,
        "timestamp": datetime.now()
    })
    
    # Rerun to display updated chat
    st.rerun()

def generate_demo_response(query: str) -> str:
    """Generate a demo response for the query."""
    query_lower = query.lower()
    
    # Simple keyword-based responses
    if "eligibility" in query_lower or "requirements" in query_lower:
        return """To be eligible for federal student loans, you must:

1. **Be a U.S. citizen or eligible noncitizen**
2. **Have a valid Social Security number**
3. **Be enrolled or accepted as a student in an eligible degree or certificate program**
4. **Be enrolled at least half-time for Direct Loans**
5. **Maintain satisfactory academic progress**
6. **Not be in default on any existing federal student loans**
7. **Not owe a refund on any federal grants**

Additional requirements may apply depending on the specific loan program. For the most accurate information, complete the Free Application for Federal Student Aid (FAFSA) at fafsa.gov."""

    elif "apply" in query_lower or "direct loan" in query_lower:
        return """To apply for a Direct Loan, follow these steps:

1. **Complete the FAFSA** - Go to fafsa.gov and submit your application
2. **Review your Student Aid Report (SAR)** - You'll receive this after FAFSA processing
3. **Complete entrance counseling** - Required for first-time borrowers
4. **Sign a Master Promissory Note (MPN)** - Your loan agreement
5. **Accept your loan offer** - Through your school's financial aid office

**Important Deadlines:**
- FAFSA opens October 1st for the following academic year
- Submit as early as possible for maximum aid consideration
- Check with your school for specific deadlines

Your school will disburse the loan funds directly to your account."""

    elif "interest rate" in query_lower or "rate" in query_lower:
        return """**Current Federal Student Loan Interest Rates (2024-25):**

**Direct Subsidized and Unsubsidized Loans:**
- Undergraduate: 5.50%
- Graduate: 7.05%

**Direct PLUS Loans:**
- Parent and Graduate: 8.05%

**Important Notes:**
- Rates are fixed for the life of the loan
- Rates are set annually by Congress
- Current rates apply to loans disbursed between July 1, 2024 and June 30, 2025
- Previous years may have different rates

For the most current rates, visit studentaid.gov."""

    elif "repay" in query_lower or "payment" in query_lower:
        return """**Federal Student Loan Repayment Options:**

1. **Standard Repayment Plan** - Fixed monthly payments over 10 years
2. **Graduated Repayment Plan** - Payments start low and increase over time
3. **Extended Repayment Plan** - Up to 25 years with fixed or graduated payments
4. **Income-Driven Repayment Plans:**
   - **REPAYE** - 10% of discretionary income, 20-25 years
   - **PAYE** - 10% of discretionary income, 20 years
   - **IBR** - 10-15% of discretionary income, 20-25 years
   - **ICR** - 20% of discretionary income or 12-year standard payment

**When Repayment Begins:**
- 6-month grace period after graduation/leaving school
- Contact your loan servicer to choose a repayment plan
- You can change plans at any time

**Important:** Always make payments on time to avoid default!"""

    elif "can't make payments" in query_lower or "default" in query_lower:
        return """**If you can't make your student loan payments:**

**Immediate Options:**
1. **Contact your loan servicer immediately** - They can help you find solutions
2. **Request a deferment or forbearance** - Temporary payment suspension
3. **Switch to an income-driven repayment plan** - Lower payments based on income
4. **Apply for loan consolidation** - May provide more repayment options

**Consequences of Default:**
- Damaged credit score
- Wage garnishment
- Tax refund offset
- Collection fees
- Loss of federal benefits

**Prevention is Key:**
- Never ignore payment notices
- Keep your contact information updated
- Communicate with your servicer early

**Help Available:**
- Student Loan Ombudsman: 1-877-557-2575
- Federal Student Aid Information Center: 1-800-433-3243"""

    elif "subsidized" in query_lower and "unsubsidized" in query_lower:
        return """**Direct Subsidized vs Unsubsidized Loans:**

**Direct Subsidized Loans:**
- **Interest:** Government pays interest while you're in school
- **Eligibility:** Based on financial need
- **Borrowers:** Undergraduate students only
- **Maximum:** Lower borrowing limits
- **Grace Period:** 6 months after graduation

**Direct Unsubsidized Loans:**
- **Interest:** You're responsible for all interest
- **Eligibility:** Available to all students regardless of need
- **Borrowers:** Undergraduate and graduate students
- **Maximum:** Higher borrowing limits
- **Grace Period:** 6 months after graduation

**Key Differences:**
- Subsidized loans are more affordable due to interest subsidy
- Unsubsidized loans are more widely available
- Both have the same interest rates and repayment terms
- You can receive both types of loans simultaneously"""

    elif "consolidate" in query_lower or "consolidation" in query_lower:
        return """**Student Loan Consolidation:**

**What is Consolidation?**
Combining multiple federal student loans into one new loan with a single monthly payment.

**Benefits:**
- Single monthly payment
- Fixed interest rate (weighted average of existing loans)
- Extended repayment term (up to 30 years)
- Access to additional repayment plans
- Simplified loan management

**Eligibility:**
- Must have at least one Direct Loan or FFEL Program loan
- Loans must be in grace, repayment, deferment, or default
- Cannot consolidate private loans through federal consolidation

**Process:**
1. Complete application at studentloans.gov
2. Choose a repayment plan
3. Sign the consolidation promissory note
4. Wait for disbursement (usually 30-60 days)

**Considerations:**
- May lose some borrower benefits
- Could pay more interest over time
- Cannot be undone"""

    elif "forgiveness" in query_lower or "forgive" in query_lower:
        return """**Student Loan Forgiveness Programs:**

**Public Service Loan Forgiveness (PSLF):**
- Work full-time for qualifying employer (government/nonprofit)
- Make 120 qualifying payments
- Remaining balance forgiven tax-free

**Teacher Loan Forgiveness:**
- Teach full-time for 5 consecutive years
- Work in low-income school
- Up to $17,500 forgiven

**Income-Driven Repayment Forgiveness:**
- Make payments for 20-25 years
- Remaining balance forgiven (may be taxable)
- Available under REPAYE, PAYE, IBR, ICR

**Closed School Discharge:**
- School closes while enrolled or within 120 days
- Automatic discharge available

**Total and Permanent Disability Discharge:**
- Permanent disability preventing work
- Requires documentation from physician

**Important:** Always verify eligibility and keep detailed records!"""

    else:
        return """I understand you're asking about student loans. While I can provide general information, for the most accurate and up-to-date guidance, I recommend:

1. **Visit studentaid.gov** - Official federal student aid website
2. **Contact your school's financial aid office** - For school-specific information
3. **Speak with your loan servicer** - For account-specific questions
4. **Complete the FAFSA** - To determine your eligibility for federal aid

**Key Resources:**
- Federal Student Aid Information Center: 1-800-433-3243
- Student Loan Ombudsman: 1-877-557-2575
- FAFSA: fafsa.gov

Would you like me to provide more specific information about any particular aspect of student loans?"""

def display_chat_history():
    """Display the chat history."""
    if not st.session_state.chat_history:
        return
    
    st.markdown('<h3 class="sub-header">💭 Conversation History</h3>', unsafe_allow_html=True)
    
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 You:</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>🤖 Assistant:</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)

def main():
    """Main application function."""
    initialize_session_state()
    display_header()
    display_sidebar()
    display_chat_interface()
    display_chat_history()

if __name__ == "__main__":
    main() 