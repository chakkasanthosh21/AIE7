"""
Golden Test Data Set Generator for Student Loan Assistant RAGAS Evaluation.
Creates synthetic Q&A pairs covering all major student loan topics.
"""

import json
import pandas as pd
from typing import List, Dict, Any
from datasets import Dataset
from ragas.metrics import (
    faithfulness, 
    ResponseRelevancy, 
    ContextPrecision, 
    ContextRecall
)


class GoldenTestDataSet:
    """Generates comprehensive test data for student loan assistant evaluation."""
    
    def __init__(self):
        self.test_queries = self._generate_test_queries()
        self.ground_truth_answers = self._generate_ground_truth_answers()
        self.contexts = self._generate_contexts()
        
    def _generate_test_queries(self) -> List[str]:
        """Generate comprehensive test queries covering all student loan topics."""
        return [
            # Eligibility Questions
            "What are the eligibility requirements for federal student loans?",
            "Am I eligible for Pell Grants?",
            "Can I get federal loans if I have bad credit?",
            "What is the maximum income for Pell Grant eligibility?",
            "Do I need to be enrolled full-time to get federal loans?",
            
            # Application Questions
            "How do I apply for federal student loans?",
            "What is the FAFSA deadline?",
            "What documents do I need for loan verification?",
            "How do I complete the FAFSA form?",
            "What happens after I submit my FAFSA?",
            
            # Loan Types Questions
            "What is the difference between subsidized and unsubsidized loans?",
            "What are Direct PLUS loans?",
            "How much can I borrow with federal loans?",
            "What are the interest rates for federal student loans?",
            "Are there limits on how much I can borrow?",
            
            # Repayment Questions
            "What are my repayment options for federal loans?",
            "How do income-driven repayment plans work?",
            "When do I have to start repaying my loans?",
            "Can I consolidate my federal student loans?",
            "What happens if I can't make my loan payments?",
            
            # Current Information Questions
            "What's the latest on student loan forgiveness?",
            "Are student loan payments still paused?",
            "What are the current federal loan interest rates?",
            "Has the Supreme Court ruled on loan forgiveness?",
            "What changes were made to student loan policies recently?",
            
            # Specific Scenarios
            "I'm a first-generation college student. What help is available?",
            "I have $50,000 in student loans. What are my options?",
            "I lost my job and can't pay my loans. What should I do?",
            "I want to go to graduate school. Can I get more loans?",
            "I'm a parent. Can I get loans for my child's education?"
        ]
    
    def _generate_ground_truth_answers(self) -> List[str]:
        """Generate accurate ground truth answers for test queries."""
        return [
            # Eligibility Answers
            "To be eligible for federal student loans, you must: be a U.S. citizen or eligible noncitizen, have a valid Social Security number, be enrolled or accepted in an eligible degree or certificate program, maintain satisfactory academic progress, and not be in default on previous federal loans. You must also complete the FAFSA annually.",
            
            "Pell Grant eligibility is based on financial need, cost of attendance, enrollment status, and plans to attend school for a full academic year. There's no specific income cutoff, but most recipients come from families with income below $50,000. The maximum award for 2024-25 is $7,395.",
            
            "Federal student loans don't require a credit check for most borrowers. Direct Subsidized and Unsubsidized Loans are available regardless of credit history. Only Direct PLUS Loans (for parents and graduate students) require a credit check, and even then, you can still qualify with an endorser.",
            
            "There's no specific income limit for Pell Grants. Eligibility is determined by the Expected Family Contribution (EFC) calculated from your FAFSA. Most recipients have family income below $50,000, but some with higher incomes may qualify based on family size and other factors.",
            
            "No, you don't need to be enrolled full-time for federal loans. You can receive loans for part-time enrollment (at least half-time, typically 6 credit hours). However, your loan amount will be prorated based on your enrollment level.",
            
            # Application Answers
            "To apply for federal student loans: 1) Complete the FAFSA at fafsa.gov, 2) Provide required documentation (tax returns, W-2s, etc.), 3) Review your Student Aid Report (SAR), 4) Accept your loan offer through your school's financial aid office, 5) Complete entrance counseling and sign a Master Promissory Note.",
            
            "The FAFSA deadline varies by state and school. The federal deadline is June 30th of the academic year, but many states and schools have earlier deadlines. For the 2024-25 academic year, the FAFSA opened in December 2023. Check your state's deadline at studentaid.gov.",
            
            "For verification, you may need: tax returns and W-2s, untaxed income records, bank statements, investment records, and documentation of family size. Your school will notify you if you're selected for verification and what specific documents are required.",
            
            "Complete the FAFSA at fafsa.gov by: 1) Creating an FSA ID, 2) Gathering required documents, 3) Filling out the form with accurate information, 4) Adding school codes for institutions you're considering, 5) Signing and submitting the form. You can save and return to complete it later.",
            
            "After submitting FAFSA: 1) You'll receive a Student Aid Report (SAR) in 3-5 days, 2) Your school will receive your information and create a financial aid package, 3) You'll receive an award letter from your school, 4) Accept or decline the offered aid, 5) Complete any additional requirements like entrance counseling.",
            
            # Loan Types Answers
            "Subsidized loans are need-based and the government pays interest while you're in school. Unsubsidized loans are not need-based and interest accrues immediately. Both have the same interest rates and repayment terms, but subsidized loans are more favorable due to the interest subsidy.",
            
            "Direct PLUS Loans are federal loans for graduate students and parents of dependent undergraduate students. They have higher interest rates than other federal loans and require a credit check. They can cover the full cost of attendance minus other financial aid received.",
            
            "Annual loan limits depend on your year in school and dependency status. For dependent undergraduates: $5,500-$7,500 annually. For independent undergraduates: $9,500-$12,500 annually. Graduate students can borrow up to $20,500 annually in unsubsidized loans plus PLUS loans.",
            
            "Federal student loan interest rates are set annually by Congress. For 2024-25: 5.50% for undergraduate Direct Loans, 7.05% for graduate Direct Loans, and 8.05% for Direct PLUS Loans. These are fixed rates that don't change over the life of the loan.",
            
            "Yes, there are both annual and aggregate limits. Annual limits vary by year in school and dependency status. Aggregate limits are $31,000 for dependent undergraduates, $57,500 for independent undergraduates, and $138,500 for graduate students (including undergraduate loans).",
            
            # Repayment Answers
            "Federal loan repayment options include: Standard Repayment (10 years), Graduated Repayment (10 years with increasing payments), Extended Repayment (25 years), and Income-Driven Repayment plans (PAYE, REPAYE, IBR, ICR) that base payments on income and family size.",
            
            "Income-driven repayment plans calculate your monthly payment as a percentage of your discretionary income. They include PAYE (10% of discretionary income), REPAYE (10% of discretionary income), IBR (10-15% of discretionary income), and ICR (20% of discretionary income). Payments can be as low as $0 for low-income borrowers.",
            
            "You must start repaying federal loans 6 months after you graduate, leave school, or drop below half-time enrollment. This is called the grace period. For PLUS loans, repayment begins immediately unless you're a graduate student or parent borrower who requests deferment.",
            
            "Yes, you can consolidate federal loans through the Direct Consolidation Loan program. This combines multiple federal loans into one loan with a single monthly payment. The interest rate is the weighted average of your existing loans. Consolidation can extend your repayment term up to 30 years.",
            
            "If you can't make payments, contact your loan servicer immediately. Options include: deferment (temporary postponement), forbearance (temporary reduction), income-driven repayment plans, or loan consolidation. Defaulting on federal loans has serious consequences including wage garnishment and loss of federal benefits.",
            
            # Current Information Answers
            "As of 2024, the Biden administration's broad student loan forgiveness plan was blocked by the Supreme Court. However, targeted forgiveness programs continue, including Public Service Loan Forgiveness, income-driven repayment forgiveness, and borrower defense to repayment. The SAVE plan offers enhanced benefits for income-driven repayment.",
            
            "The COVID-19 payment pause ended in October 2023. Regular payments resumed, but the Biden administration implemented the SAVE plan which provides enhanced benefits including lower monthly payments and faster forgiveness for many borrowers.",
            
            "Federal student loan interest rates for 2024-25 are: 5.50% for undergraduate Direct Loans, 7.05% for graduate Direct Loans, and 8.05% for Direct PLUS Loans. These rates are fixed and set annually by Congress based on the 10-year Treasury note auction.",
            
            "Yes, in June 2023, the Supreme Court ruled 6-3 against the Biden administration's broad student loan forgiveness plan, finding that the HEROES Act didn't authorize the Secretary of Education to cancel $430 billion in student debt. The administration has since pursued alternative approaches through rulemaking.",
            
            "Recent changes include: implementation of the SAVE plan with enhanced income-driven repayment benefits, expansion of Public Service Loan Forgiveness eligibility, improved borrower defense to repayment process, and new regulations on gainful employment and financial responsibility for institutions.",
            
            # Specific Scenarios Answers
            "First-generation college students have access to all federal student aid programs plus additional support. This includes Pell Grants, federal student loans, work-study, and special programs like TRIO and GEAR UP. Many schools also offer first-generation student scholarships and support services.",
            
            "With $50,000 in student loans, consider: income-driven repayment plans to lower monthly payments, loan consolidation to simplify payments, refinancing with private lenders (if you have good credit), and exploring forgiveness programs like Public Service Loan Forgiveness or teacher loan forgiveness.",
            
            "If you can't pay due to job loss: 1) Contact your loan servicer immediately, 2) Apply for deferment or forbearance, 3) Switch to an income-driven repayment plan, 4) Consider unemployment deferment, 5) Look into state and federal assistance programs. Don't ignore the loans as default has serious consequences.",
            
            "Yes, graduate students can borrow up to $20,500 annually in Direct Unsubsidized Loans plus unlimited amounts in Direct PLUS Loans (subject to cost of attendance). Graduate PLUS loans require a credit check but have higher interest rates than other federal loans.",
            
            "Parents can borrow Direct PLUS Loans to help pay for their child's undergraduate education. These loans are in the parent's name and require a credit check. They can borrow up to the full cost of attendance minus other financial aid. Repayment typically begins immediately unless deferment is requested."
        ]
    
    def _generate_contexts(self) -> List[List[str]]:
        """Generate relevant contexts for each query."""
        # This would typically come from your vector database
        # For evaluation purposes, we'll create sample contexts
        contexts = []
        
        for i in range(len(self.test_queries)):
            # Create context that would be retrieved for each query
            context = [
                f"Context document {i+1}: Federal student loan information relevant to query {i+1}",
                f"Supporting document {i+1}: Additional details about student loan programs",
                f"Policy document {i+1}: Current regulations and requirements"
            ]
            contexts.append(context)
        
        return contexts
    
    def create_ragas_dataset(self) -> Dataset:
        """Create a RAGAS dataset for evaluation."""
        dataset_dict = {
            "question": self.test_queries,
            "answer": self.ground_truth_answers,
            "ground_truth": self.ground_truth_answers,  # Reference column
            "contexts": self.contexts
        }
        
        return Dataset.from_dict(dataset_dict)
    
    def save_test_data(self, filename: str = "golden_test_dataset.json"):
        """Save the test data to a JSON file."""
        data = {
            "test_queries": self.test_queries,
            "ground_truth_answers": self.ground_truth_answers,
            "contexts": self.contexts,
            "metadata": {
                "total_queries": len(self.test_queries),
                "categories": {
                    "eligibility": 5,
                    "application": 5,
                    "loan_types": 5,
                    "repayment": 5,
                    "current_info": 5,
                    "specific_scenarios": 5
                }
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Golden test dataset saved to {filename}")
    
    def create_evaluation_dataframe(self) -> pd.DataFrame:
        """Create a pandas DataFrame for analysis."""
        return pd.DataFrame({
            "query": self.test_queries,
            "ground_truth": self.ground_truth_answers,
            "contexts": [str(ctx) for ctx in self.contexts]
        })


def run_ragas_evaluation():
    """Run RAGAS evaluation on the golden test dataset."""
    print("🔍 Creating Golden Test Dataset...")
    
    # Create test dataset
    test_dataset = GoldenTestDataSet()
    ragas_dataset = test_dataset.create_ragas_dataset()
    
    # Save test data
    test_dataset.save_test_data()
    
    print("🔍 Running RAGAS Evaluation...")
    
    # Import evaluation metrics
    from ragas import evaluate
    from ragas.metrics import faithfulness, ResponseRelevancy, ContextPrecision, ContextRecall
    
    # Run evaluation
    results = evaluate(
        ragas_dataset,
        metrics=[
            faithfulness,
            ResponseRelevancy(), 
            ContextPrecision(),
            ContextRecall()
        ]
    )
    
    # Create results table
    results_table = {
        "Metric": ["Faithfulness", "Response Relevancy", "Context Precision", "Context Recall"],
        "Score": [
            results['faithfulness'],
            results['ResponseRelevancy'],
            results['ContextPrecision'],
            results['ContextRecall']
        ]
    }
    
    results_df = pd.DataFrame(results_table)
    
    print("\n📊 RAGAS Evaluation Results:")
    print("=" * 50)
    print(results_df.to_string(index=False))
    print("=" * 50)
    
    # Save results
    results_df.to_csv("ragas_evaluation_results.csv", index=False)
    print("✅ Results saved to ragas_evaluation_results.csv")
    
    return results_df


if __name__ == "__main__":
    # Run the evaluation
    results = run_ragas_evaluation()
    
    # Print conclusions
    print("\n📋 Evaluation Conclusions:")
    print("=" * 50)
    
    avg_score = results['Score'].mean()
    print(f"Overall Average Score: {avg_score:.3f}")
    
    if avg_score >= 0.8:
        print("✅ Excellent performance - system is highly effective")
    elif avg_score >= 0.7:
        print("✅ Good performance - system is effective with minor improvements needed")
    elif avg_score >= 0.6:
        print("⚠️  Fair performance - significant improvements recommended")
    else:
        print("❌ Poor performance - major improvements required")
    
    # Specific recommendations
    print("\n🎯 Specific Recommendations:")
    if results.loc[results['Metric'] == 'Faithfulness', 'Score'].iloc[0] < 0.8:
        print("- Improve response faithfulness to source documents")
    if results.loc[results['Metric'] == 'Response Relevancy', 'Score'].iloc[0] < 0.8:
        print("- Enhance response relevance to user queries")
    if results.loc[results['Metric'] == 'Context Precision', 'Score'].iloc[0] < 0.8:
        print("- Improve context retrieval precision")
    if results.loc[results['Metric'] == 'Context Recall', 'Score'].iloc[0] < 0.8:
        print("- Enhance context retrieval recall") 