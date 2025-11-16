# Warning control
import warnings
warnings.filterwarnings('ignore')

import os
import yaml
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

load_dotenv()
os.environ['OPENAI_MODEL_NAME'] = 'gpt-4o-mini'

# Loading agents and tasks from config - START - 
files = {
    'agents': 'config/agents.yaml',
    'tasks': 'config/tasks.yaml'}

configs = {}
for config_type, file_path in files.items():
    with open(file_path, 'r') as file:
        configs[config_type] = yaml.safe_load(file)

agents_config = configs['agents']
tasks_config = configs['tasks']

# Loading agents and tasks from config - END -

# Setting up content validation using pydantic - START - 
from typing import List
from pydantic import BaseModel, Field

class TaskEstimate(BaseModel):
    task_name: str = Field(..., description="Name of the task")
    estimated_time_hours: float = Field(..., description="Estimated time to complete the task in hours")
    required_resources: List[str] = Field(..., description="List of resources required to complete the task")

class Milestone(BaseModel):
    milestone_name: str = Field(..., description="Name of the milestone")
    tasks: List[str] = Field(..., description="List of task IDs associated with this milestone")

class ProjectPlan(BaseModel):
    tasks: List[TaskEstimate] = Field(..., description="List of tasks with their estimates")
    milestones: List[Milestone] = Field(..., description="List of project milestones")

# Setting up content validation using pydantic - END - 

# Creating Agents - START - 
project_planning_agent = Agent(
  config=agents_config['project_planning_agent']
)

estimation_agent = Agent(
  config=agents_config['estimation_agent']
)

resource_allocation_agent = Agent(
  config=agents_config['resource_allocation_agent']
)
# Creating Agents - END - 

# Creating Tasks - START - 
task_breakdown = Task(
  config=tasks_config['task_breakdown'],
  agent=project_planning_agent
)

time_resource_estimation = Task(
  config=tasks_config['time_resource_estimation'],
  agent=estimation_agent
)

resource_allocation = Task(
  config=tasks_config['resource_allocation'],
  agent=resource_allocation_agent,
  output_pydantic=ProjectPlan # This is the structured output we want
)
# Creating Tasks - END - 

# Creating Crew - START - 
crew = Crew(
  agents=[
    project_planning_agent,
    estimation_agent,
    resource_allocation_agent
  ],
  tasks=[
    task_breakdown,
    time_resource_estimation,
    resource_allocation
  ],
  verbose=True
)
# Creating Crew - END - 

# Setting up input to feed to the crew - START - 
from IPython.display import display, Markdown

project = 'Website'
industry = 'Technology'
project_objectives = 'Create a website for a small business'
team_members = """
- John Doe (Project Manager)
- Jane Doe (Software Engineer)
- Bob Smith (Designer)
- Alice Johnson (QA Engineer)
- Tom Brown (QA Engineer)
"""
project_requirements = """
- Create a responsive design that works well on desktop and mobile devices
- Implement a modern, visually appealing user interface with a clean look
- Develop a user-friendly navigation system with intuitive menu structure
- Include an "About Us" page highlighting the company's history and values
- Design a "Services" page showcasing the business's offerings with descriptions
- Create a "Contact Us" page with a form and integrated map for communication
- Implement a blog section for sharing industry news and company updates
- Ensure fast loading times and optimize for search engines (SEO)
- Integrate social media links and sharing capabilities
- Include a testimonials section to showcase customer feedback and build trust
"""


formatted_output = f"""
**Project Type:** {project}

**Project Objectives:** {project_objectives}

**Industry:** {industry}

**Team Members:**
{team_members}
**Project Requirements:**
{project_requirements}
"""

# display(Markdown(formatted_output))

inputs = {
  'project_type': project,
  'project_objectives': project_objectives,
  'industry': industry,
  'team_members': team_members,
  'project_requirements': project_requirements
}

# Setting up input to feed to the crew - END - 

# Run the crew -- 
result = crew.kickoff(
  inputs=inputs
)
# -- 


result.pydantic.dict()

# tasks = result.pydantic.dict()['tasks']
# df_tasks = pd.DataFrame(tasks)

# # Display the DataFrame as an HTML table
# df_tasks.style.set_table_attributes('border="1"').set_caption("Task Details").set_table_styles(
#     [{'selector': 'th, td', 'props': [('font-size', '120%')]}]
# )


# milestones = result.pydantic.dict()['milestones']
# df_milestones = pd.DataFrame(milestones)

# # Display the DataFrame as an HTML table
# df_milestones.style.set_table_attributes('border="1"').set_caption("Task Details").set_table_styles(
#     [{'selector': 'th, td', 'props': [('font-size', '120%')]}]
# )