from typing import Dict, Any, List, Optional

from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.candidate_bc.resume.domain.enums.resume_type import ResumeType
from src.candidate_bc.resume.domain.value_objects.general_data import GeneralData
from src.candidate_bc.resume.domain.value_objects.resume_content import ResumeContent, AIGeneratedContent
from src.candidate_bc.resume.domain.value_objects.variable_section import VariableSection


class ResumeGenerationService:
    """Servicio para generar contenido de resumes"""

    def generate_basic_content(
            self,
            candidate_id: CandidateId,
            resume_type: ResumeType,
            candidate_data: Optional[Dict[str, Any]] = None
    ) -> ResumeContent:
        """Generate basic content for resume using new hybrid structure"""
        # Simulate processing (synchronously)
        import time
        time.sleep(0.1)

        # Generate general data (fixed section)
        general_data = self._generate_general_data(candidate_data)

        # Generate variable sections with HTML content
        variable_sections = self._generate_variable_sections(candidate_data)

        # Create resume content with new structure
        content = ResumeContent(
            general_data=general_data,
            variable_sections=variable_sections
        )

        return content

    def generate_basic_content_legacy(
            self,
            candidate_id: CandidateId,
            resume_type: ResumeType,
            candidate_data: Optional[Dict[str, Any]] = None
    ) -> ResumeContent:
        """Legacy method - generates content using old markdown structure"""
        # Simular procesamiento (sincronamente)
        import time
        time.sleep(0.1)

        # Generar contenido según RESUME.md - solo secciones requeridas
        experiencia_profesional = self._generate_experiencia_profesional_markdown(candidate_data)
        educacion = self._generate_educacion_markdown(candidate_data)
        proyectos = self._generate_proyectos_markdown(candidate_data)
        habilidades = self._generate_habilidades_markdown(candidate_data)
        datos_personales = self._generate_datos_personales(candidate_data)

        # Convert to new structure for compatibility
        general_data = GeneralData.from_dict(datos_personales)

        # Create variable sections from legacy content
        variable_sections = []
        if experiencia_profesional:
            variable_sections.append(VariableSection(
                key='experience',
                title='Work Experience',
                content=self._markdown_to_html(experiencia_profesional),
                order=1
            ))
        if educacion:
            variable_sections.append(VariableSection(
                key='education',
                title='Education',
                content=self._markdown_to_html(educacion),
                order=2
            ))
        if habilidades:
            variable_sections.append(VariableSection(
                key='skills',
                title='Skills',
                content=self._markdown_to_html(habilidades),
                order=3
            ))
        if proyectos:
            variable_sections.append(VariableSection(
                key='projects',
                title='Projects',
                content=self._markdown_to_html(proyectos),
                order=4
            ))

        return ResumeContent(
            general_data=general_data,
            variable_sections=variable_sections
        )

    def generate_ai_enhanced_content(
            self,
            candidate_id: CandidateId,
            resume_type: ResumeType,
            basic_content: ResumeContent,
            candidate_data: Optional[Dict[str, Any]] = None
    ) -> AIGeneratedContent:
        """Genera contenido mejorado con IA - mantener simple por ahora"""
        # Simular procesamiento de IA (más lento, sincronamente)
        import time
        time.sleep(0.5)

        # No generar contenido AI automáticamente - solo usar datos reales
        return AIGeneratedContent(
            ai_summary=None,
            ai_key_aspects=[],
            ai_skills_recommendations=[],
            ai_achievements=[],
            ai_intro_letter=None
        )

    def _generate_experiencia_profesional_markdown(self, candidate_data: Optional[Dict[str, Any]]) -> str:
        """Genera la sección de Experiencia Profesional en markdown usando SOLO datos reales"""
        if not candidate_data:
            return ""

        experiences = candidate_data.get('experiences', [])
        if not experiences:
            return ""

        markdown_lines = []

        for exp in experiences:
            job_title = exp.get('job_title', '')
            company = exp.get('company', '')
            start_date = exp.get('start_date', '')
            end_date = exp.get('end_date', '')
            description = exp.get('description', '')
            is_current = exp.get('is_current', False)

            if not job_title or not company:
                continue

            # Formatear fechas
            date_range = ""
            if start_date:
                date_range = start_date
                if end_date:
                    date_range += f" - {end_date}"
                elif is_current:
                    date_range += " - Presente"

            # Título del trabajo
            markdown_lines.append(f"### {job_title}")
            markdown_lines.append(f"**{company}**")

            if date_range:
                markdown_lines.append(f"*{date_range}*")

            # Descripción si existe
            if description and description.strip():
                markdown_lines.append("")
                markdown_lines.append(description.strip())

            markdown_lines.append("")  # Separar experiencias

        return "\n".join(markdown_lines)

    def _generate_educacion_markdown(self, candidate_data: Optional[Dict[str, Any]]) -> str:
        """Genera la sección de Educación en markdown usando SOLO datos reales"""
        if not candidate_data:
            return ""

        educations = candidate_data.get('educations', [])
        if not educations:
            return ""

        markdown_lines = []

        for edu in educations:
            degree = edu.get('degree', '')
            institution = edu.get('institution', '')
            field_of_study = edu.get('field_of_study', '')
            start_date = edu.get('start_date', '')
            end_date = edu.get('end_date', '')
            description = edu.get('description', '')

            if not degree or not institution:
                continue

            # Formatear fechas
            date_range = ""
            if start_date:
                date_range = start_date
                if end_date:
                    date_range += f" - {end_date}"

            # Título de la educación
            title_parts = [degree]
            if field_of_study:
                title_parts.append(f"en {field_of_study}")

            markdown_lines.append(f"### {' '.join(title_parts)}")
            markdown_lines.append(f"**{institution}**")

            if date_range:
                markdown_lines.append(f"*{date_range}*")

            # Descripción si existe
            if description and description.strip():
                markdown_lines.append("")
                markdown_lines.append(description.strip())

            markdown_lines.append("")  # Separar educaciones

        return "\n".join(markdown_lines)

    def _generate_proyectos_markdown(self, candidate_data: Optional[Dict[str, Any]]) -> str:
        """Genera la sección de Proyectos en markdown usando SOLO datos reales"""
        if not candidate_data:
            return ""

        projects = candidate_data.get('projects', [])
        if not projects:
            return ""

        markdown_lines = []

        for project in projects:
            name = project.get('name', '')
            description = project.get('description', '')
            technologies = project.get('technologies', [])
            url = project.get('url', '')
            start_date = project.get('start_date', '')
            end_date = project.get('end_date', '')

            if not name:
                continue

            # Formatear fechas
            date_range = ""
            if start_date:
                date_range = start_date
                if end_date:
                    date_range += f" - {end_date}"

            # Título del proyecto
            markdown_lines.append(f"### {name}")

            if date_range:
                markdown_lines.append(f"*{date_range}*")

            # URL si existe
            if url and url.strip():
                markdown_lines.append(f"**URL:** {url}")

            # Descripción si existe
            if description and description.strip():
                markdown_lines.append("")
                markdown_lines.append(description.strip())

            # Tecnologías si existen
            if technologies:
                markdown_lines.append("")
                markdown_lines.append(f"**Tecnologías:** {', '.join(technologies)}")

            markdown_lines.append("")  # Separar proyectos

        return "\n".join(markdown_lines)

    def _generate_habilidades_markdown(self, candidate_data: Optional[Dict[str, Any]]) -> str:
        """Genera la sección de Habilidades en markdown usando SOLO datos reales"""
        if not candidate_data:
            return ""

        skills = candidate_data.get('skills', [])
        if not skills:
            return ""

        # Simplemente listar las habilidades como elementos de lista en markdown
        markdown_lines = []
        for skill in skills:
            if skill and skill.strip():
                markdown_lines.append(f"- {skill.strip()}")

        return "\n".join(markdown_lines)

    def _generate_datos_personales(self, candidate_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Genera los datos personales usando SOLO datos reales del candidato"""
        if not candidate_data:
            return {}

        datos_personales = {}

        # Solo incluir datos que existen
        if candidate_data.get('name'):
            datos_personales['name'] = candidate_data['name']

        if candidate_data.get('email'):
            datos_personales['email'] = candidate_data['email']

        if candidate_data.get('phone'):
            datos_personales['phone'] = candidate_data['phone']

        if candidate_data.get('location'):
            datos_personales['location'] = candidate_data['location']

        if candidate_data.get('linkedin_url'):
            datos_personales['linkedin_url'] = candidate_data['linkedin_url']

        return datos_personales

    # New methods for hybrid structure
    def _generate_general_data(self, candidate_data: Optional[Dict[str, Any]]) -> GeneralData:
        """Generate general data section using real candidate data"""
        if not candidate_data:
            return GeneralData()

        return GeneralData(
            cv_title=candidate_data.get('cv_title', 'Professional Resume'),
            name=candidate_data.get('name', ''),
            email=candidate_data.get('email', ''),
            phone=candidate_data.get('phone', '')
        )

    def _generate_variable_sections(self, candidate_data: Optional[Dict[str, Any]]) -> List[VariableSection]:
        """Generate variable sections with HTML content from candidate data"""
        sections = []

        # Professional Summary (basic, no AI for now)
        summary_content = self._generate_summary_html(candidate_data)
        if summary_content:
            sections.append(VariableSection(
                key='summary',
                title='Professional Summary',
                content=summary_content,
                order=1
            ))

        # Work Experience
        experience_content = self._generate_experience_html(candidate_data)
        if experience_content:
            sections.append(VariableSection(
                key='experience',
                title='Work Experience',
                content=experience_content,
                order=2
            ))

        # Education
        education_content = self._generate_education_html(candidate_data)
        if education_content:
            sections.append(VariableSection(
                key='education',
                title='Education',
                content=education_content,
                order=3
            ))

        # Skills
        skills_content = self._generate_skills_html(candidate_data)
        if skills_content:
            sections.append(VariableSection(
                key='skills',
                title='Skills',
                content=skills_content,
                order=4
            ))

        # Projects
        projects_content = self._generate_projects_html(candidate_data)
        if projects_content:
            sections.append(VariableSection(
                key='projects',
                title='Projects',
                content=projects_content,
                order=5
            ))

        return sections

    def _generate_summary_html(self, candidate_data: Optional[Dict[str, Any]]) -> str:
        """Generate basic professional summary in HTML"""
        if not candidate_data:
            return ""

        # Simple summary based on role and experience
        role = candidate_data.get('current_roles', ['Professional'])[0] if candidate_data.get(
            'current_roles') else 'Professional'
        location = candidate_data.get('location', '')

        summary_parts = []
        if role:
            summary_parts.append(f"Experienced {role}")
        if location:
            summary_parts.append(f"based in {location}")

        if summary_parts:
            return f"<p>{' '.join(summary_parts)}.</p>"
        return ""

    def _generate_experience_html(self, candidate_data: Optional[Dict[str, Any]]) -> str:
        """Generate work experience section in HTML"""
        if not candidate_data:
            return ""

        experiences = candidate_data.get('experiences', [])
        if not experiences:
            return ""

        html_parts = []

        for exp in experiences:
            job_title = exp.get('job_title', '')
            company = exp.get('company', '')
            start_date = exp.get('start_date', '')
            end_date = exp.get('end_date', '')
            description = exp.get('description', '')
            is_current = exp.get('is_current', False)

            if not job_title or not company:
                continue

            # Format dates
            date_range = ""
            if start_date:
                date_range = start_date
                if end_date:
                    date_range += f" - {end_date}"
                elif is_current:
                    date_range += " - Present"

            # Build HTML for this experience
            html_parts.append('<div class="experience-item">')
            html_parts.append(f'<h3>{job_title}</h3>')
            html_parts.append(f'<p><strong>{company}</strong></p>')

            if date_range:
                html_parts.append(f'<p><em>{date_range}</em></p>')

            if description and description.strip():
                html_parts.append(f'<p>{description.strip()}</p>')

            html_parts.append('</div>')

        return '\n'.join(html_parts)

    def _generate_education_html(self, candidate_data: Optional[Dict[str, Any]]) -> str:
        """Generate education section in HTML"""
        if not candidate_data:
            return ""

        educations = candidate_data.get('educations', [])
        if not educations:
            return ""

        html_parts = []

        for edu in educations:
            degree = edu.get('degree', '')
            institution = edu.get('institution', '')
            field_of_study = edu.get('field_of_study', '')
            start_date = edu.get('start_date', '')
            end_date = edu.get('end_date', '')
            description = edu.get('description', '')

            if not degree or not institution:
                continue

            # Format dates
            date_range = ""
            if start_date:
                date_range = start_date
                if end_date:
                    date_range += f" - {end_date}"

            # Build title
            title_parts = [degree]
            if field_of_study:
                title_parts.append(f"in {field_of_study}")

            html_parts.append('<div class="education-item">')
            html_parts.append(f'<h3>{" ".join(title_parts)}</h3>')
            html_parts.append(f'<p><strong>{institution}</strong></p>')

            if date_range:
                html_parts.append(f'<p><em>{date_range}</em></p>')

            if description and description.strip():
                html_parts.append(f'<p>{description.strip()}</p>')

            html_parts.append('</div>')

        return '\n'.join(html_parts)

    def _generate_skills_html(self, candidate_data: Optional[Dict[str, Any]]) -> str:
        """Generate skills section in HTML"""
        if not candidate_data:
            return ""

        skills = candidate_data.get('skills', [])
        if not skills:
            return ""

        # Create an unordered list of skills
        html_parts = ['<ul>']
        for skill in skills:
            if skill and skill.strip():
                html_parts.append(f'<li>{skill.strip()}</li>')
        html_parts.append('</ul>')

        return '\n'.join(html_parts)

    def _generate_projects_html(self, candidate_data: Optional[Dict[str, Any]]) -> str:
        """Generate projects section in HTML"""
        if not candidate_data:
            return ""

        projects = candidate_data.get('projects', [])
        if not projects:
            return ""

        html_parts = []

        for project in projects:
            name = project.get('name', '')
            description = project.get('description', '')
            technologies = project.get('technologies', [])
            url = project.get('url', '')
            start_date = project.get('start_date', '')
            end_date = project.get('end_date', '')

            if not name:
                continue

            # Format dates
            date_range = ""
            if start_date:
                date_range = start_date
                if end_date:
                    date_range += f" - {end_date}"

            html_parts.append('<div class="project-item">')
            html_parts.append(f'<h3>{name}</h3>')

            if date_range:
                html_parts.append(f'<p><em>{date_range}</em></p>')

            if url and url.strip():
                html_parts.append(f'<p><strong>URL:</strong> <a href="{url}" target="_blank">{url}</a></p>')

            if description and description.strip():
                html_parts.append(f'<p>{description.strip()}</p>')

            if technologies:
                html_parts.append(f'<p><strong>Technologies:</strong> {", ".join(technologies)}</p>')

            html_parts.append('</div>')

        return '\n'.join(html_parts)

    def _markdown_to_html(self, markdown_content: str) -> str:
        """Convert simple markdown to HTML (for legacy compatibility)"""
        if not markdown_content:
            return ""

        html = markdown_content

        # Convert headers
        html = html.replace('### ', '<h3>').replace('\n\n', '</h3>\n')
        html = html.replace('## ', '<h2>').replace('\n\n', '</h2>\n')
        html = html.replace('# ', '<h1>').replace('\n\n', '</h1>\n')

        # Convert bold and italic
        html = html.replace('**', '<strong>').replace('**', '</strong>')
        html = html.replace('*', '<em>').replace('*', '</em>')

        # Convert bullet points
        lines = html.split('\n')
        processed_lines = []
        in_list = False

        for line in lines:
            if line.strip().startswith('- '):
                if not in_list:
                    processed_lines.append('<ul>')
                    in_list = True
                processed_lines.append(f'<li>{line.strip()[2:]}</li>')
            else:
                if in_list:
                    processed_lines.append('</ul>')
                    in_list = False
                if line.strip():
                    processed_lines.append(f'<p>{line}</p>')

        if in_list:
            processed_lines.append('</ul>')

        return '\n'.join(processed_lines)
