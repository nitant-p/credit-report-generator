from groq import Groq

from creditrating.settings import GROQ_API_KEY

class GroqClient:
    _instance = None

    @staticmethod
    def get_instance():
        if GroqClient._instance is None:
            GroqClient()
        return GroqClient._instance

    def __init__(self):
        if GroqClient._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.client = Groq(api_key='dummy_key')
            GroqClient._instance = self

    def generate_report_text(self, company_name, data, model="llama-3.1-70b-versatile", earning_calls_transcript=None,
                             financial_ratios=None, ten_k_report=None):

        content = (
            f"Please assess this credit data for company: {company_name} and create a short credit rating report.\n"
            f"The data provided may or may not include financial ratios over various years, earning conference calls "
            f"transcripts and annual reports submitted to the SEC. If no data is provided, please use your knowledge "
            f"to fill the gaps.\n"
            f"General Company data: {data}.\n"
            f"Financial Ratios: {financial_ratios}.\n"
            f"Earning Calls Transcript: {earning_calls_transcript}.\n"
            f"Ten K Report: {ten_k_report}.\n"
        )

        chat_completion = self.client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": content
            }],
            model=model
        )
        return chat_completion.choices[0].message.content
