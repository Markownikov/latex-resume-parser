import re
import json

def parse_resume(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        resume_content = f.read()

    # Define regular expressions for parsing
    name_regex = r'\\newcommand{\\name}{(.*?)}'
    email_regex = r'\\newcommand{\\emaila}{(.*?)}'
    phone_regex = r'\\newcommand{\\phone}{(.*?)}'

    education_regex = r'\\section{\\textbf{Education}}(.*?)\\section{\\textbf{Projects}}'
    projects_regex = r'\\section{\\textbf{Projects}}(.*?)\\section{\\textbf{Coding Profiles}}'

    # Extract information using regex
    name = re.search(name_regex, resume_content, re.DOTALL).group(1).strip()
    email = re.search(email_regex, resume_content, re.DOTALL).group(1).strip()
    phone = re.search(phone_regex, resume_content, re.DOTALL).group(1).strip()

    education_section = re.search(education_regex, resume_content, re.DOTALL).group(1).strip()
    projects_section = re.search(projects_regex, resume_content, re.DOTALL).group(1).strip()

    # Further parse education details
    education_items = re.findall(r'\\resumeSubheading{(.*?)}{(.*?)}{(.*?)}{(.*?)}', education_section, re.DOTALL)
    education_list = []
    for item in education_items:
        education_list.append({
            'institution': item[0],
            'degree': item[1],
            'details': item[2],
            'duration': item[3]
        })

    # Further parse project details
    project_items = re.findall(r'\\resumeProject{(.*?)}{(.*?)}{(.*?)}{(.*?)}', projects_section, re.DOTALL)
    project_list = []
    for item in project_items:
        project_list.append({
            'name': item[0],
            'description': item[1],
            'link': item[2],
            'tools_technologies': item[3]
        })

    # Create JSON object
    resume_data = {
        'name': name,
        'email': email,
        'phone': phone,
        'education': education_list,
        'projects': project_list
    }

    # Convert to JSON and save to file
    output_json_file = 'resume_data.json'
    with open(output_json_file, 'w', encoding='utf-8') as json_file:
        json.dump(resume_data, json_file, indent=4)

    print(f'Resume parsed successfully. JSON data saved to {output_json_file}')

if __name__ == '__main__':
    resume_file = 'resume.tex'  # Replace with your LaTeX resume file path
    parse_resume(resume_file)
