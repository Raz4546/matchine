class Prompts:
    """
    A class to manage and provide prompts for various tasks.
    """

    @staticmethod
    def get_resume_to_json_prompt(resume_txt: str) -> str:
        return f"""
        Convert the following resume text into a JSON object.
        The JSON object should have the following top-level keys:
        - "name": (string) The full name of the person.
        - "mail": (string) The email address.
        - "location": (string) The location of the person.
        - "phone number": (string) The phone number.
        - "experience": (array of objects) Each object representing a work experience entry.
            Each experience object should have:
            - "company": (string) The company name.
            - "title": (string) The job title.
            - "dates": (string) The duration of the employment (e.g., "October 2016 - current").
            - "location": (string) The location of the company.
            - "responsibilities": (array of strings) A list of bullet points describing responsibilities and achievements.
        - "skills": (object) An object containing different categories of skills.
            Each skill category (e.g., "Languages", "Frameworks", "Tools", "Databases") should be a key,
            and its value should be an array of strings.
        - "education": (array of objects) Each object representing an education entry.
        - "certifications": (array of objects) Each object representing a certification entry (optional).
        - "summary_or_career_objective": (string) A brief summary of the person's professional background (optional).
        - "projects": (array of objects) Each object representing a project entry (optional).
            Each project object should have:
            - "name": (string) The name of the project.
            - "description": (string) A brief description of the project.
            - "technologies": (array of strings) Technologies used in the project.
            - "position": (string) The person's role in the project (optional).
            - "year": (string) The year the project was completed (optional).

        Extract the information strictly from the provided resume text.
        Ensure the output is ONLY a valid JSON object, without any additional text or markdown.

        Resume Text:
        ---
        {resume_txt}
        ---
        """
