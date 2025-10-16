import i18n from 'i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import { initReactI18next } from 'react-i18next';

// Translation resources defined inline to avoid import issues
const resources = {
  en: {
    translation: {
      "common": {
        "save": "Save",
        "cancel": "Cancel",
        "edit": "Edit",
        "delete": "Delete",
        "add": "Add",
        "update": "Update",
        "loading": "Loading...",
        "search": "Search",
        "back": "Back",
        "continue": "Continue",
        "yes": "Yes",
        "no": "No",
        "confirm": "Confirm",
        "close": "Close",
        "name": "Name",
        "email": "Email",
        "phone": "Phone",
        "description": "Description",
        "startDate": "Start Date",
        "endDate": "End Date",
        "current": "Current",
        "inProgress": "In Progress",
        "saving": "Saving...",
        "unsavedChanges": "Unsaved changes",
        "lastSaved": "Last saved"
      },
      "experience": {
        "jobTitle": "Job Title",
        "company": "Company",
        "description": "Description",
        "startDate": "Start Date",
        "endDate": "End Date",
        "currentJob": "This is my current job",
        "addExperience": "Add Experience",
        "editExperience": "Edit Experience",
        "addNewExperience": "Add New Experience",
        "experienceAdded": "Experience added successfully",
        "experienceUpdated": "Experience updated successfully",
        "experienceDeleted": "Experience deleted successfully",
        "deleteConfirm": "Are you sure you want to delete this experience?",
        "errorLoading": "Error loading work experience",
        "errorSaving": "Error saving experience",
        "errorDeleting": "Error deleting experience",
        "jobTitlePlaceholder": "e.g. Senior Developer",
        "companyPlaceholder": "e.g. Tech Solutions Corp",
        "descriptionPlaceholder": "Describe your responsibilities, achievements and technologies used..."
      },
      "education": {
        "degree": "Degree / Title",
        "institution": "Institution",
        "description": "Description",
        "startDate": "Start Date",
        "endDate": "End Date",
        "currentStudies": "Currently studying",
        "addEducation": "Add Education",
        "editEducation": "Edit Education",
        "addNewEducation": "Add New Education",
        "educationAdded": "Education added successfully",
        "educationUpdated": "Education updated successfully",
        "educationDeleted": "Education deleted successfully",
        "deleteConfirm": "Are you sure you want to delete this education?",
        "errorLoading": "Error loading education",
        "errorSaving": "Error saving education",
        "errorDeleting": "Error deleting education",
        "degreePlaceholder": "e.g. Computer Engineering",
        "institutionPlaceholder": "e.g. Polytechnic University",
        "descriptionPlaceholder": "Describe your education, specialization, academic achievements...",
        "noEducation": "No education added",
        "startAddingEducation": "Start by adding your academic background",
        "leaveEmptyIfCurrentStudies": "Leave empty if currently studying"
      },
      "projects": {
        "name": "Project Name",
        "description": "Description",
        "startDate": "Start Date",
        "endDate": "End Date",
        "inProgress": "In progress",
        "addProject": "Add Project",
        "editProject": "Edit Project",
        "addNewProject": "Add New Project",
        "projectAdded": "Project added successfully",
        "projectUpdated": "Project updated successfully",
        "projectDeleted": "Project deleted successfully",
        "deleteConfirm": "Are you sure you want to delete this project?",
        "errorLoading": "Error loading projects",
        "errorSaving": "Error saving project",
        "errorDeleting": "Error deleting project",
        "namePlaceholder": "e.g. Inventory Management System",
        "descriptionPlaceholder": "Describe the project, technologies used, objectives achieved, challenges overcome...",
        "personalProject": "Personal Project",
        "noProjects": "No projects added",
        "startAddingProjects": "Start by adding your personal or professional projects",
        "leaveEmptyIfInProgress": "Leave empty if project is in progress"
      },
      "resume": {
        "generalInformation": "General Information",
        "resumeSections": "Resume Sections",
        "cvTitle": "CV Title",
        "fullName": "Full Name",
        "addSection": "Add Section",
        "addNewSection": "Add New Section",
        "sectionKey": "Section Key",
        "sectionTitle": "Section Title",
        "initialContent": "Initial Content (Optional)",
        "editTitle": "Edit title",
        "moveUp": "Move up",
        "moveDown": "Move down",
        "dragToReorder": "Drag to reorder",
        "removeSection": "Remove section",
        "sectionKeyPlaceholder": "e.g., certifications",
        "sectionTitlePlaceholder": "e.g., Certifications",
        "sectionContentPlaceholder": "Enter initial content for this section...",
        "enterContentPlaceholder": "Enter content for {{title}}...",
        "noSectionsFound": "No sections found. Add a section to get started.",
        "sectionAlreadyExists": "A section with this key already exists",
        "removeSectionConfirm": "Are you sure you want to remove this section?",
        "loadingEditor": "Loading resume editor...",
        "editGeneralInfo": "Edit general information",
        "cvTitlePlaceholder": "Professional Resume",
        "noTitleSet": "No title set",
        "noNameSet": "No name set",
        "noEmailSet": "No email set",
        "noPhoneSet": "No phone set",
        "hidePreview": "Hide Preview",
        "showPreview": "Show Preview",
        "revertChanges": "Revert Changes",
        "failedToLoadResumeData": "Failed to load resume data. Please try again.",
        "failedToSaveResume": "Failed to save resume. Please try again.",
        "resumeNotFound": "Resume not found",
        "tryAgain": "Try Again",
        "sections": {
          "experience": "Professional Experience",
          "education": "Education",
          "skills": "Skills",
          "projects": "Projects",
          "addExperienceHere": "Add your professional experience here...",
          "addEducationHere": "Add your academic background here...",
          "addSkillsHere": "Add your skills here",
          "addProjectsHere": "Add your projects here..."
        }
      },
      "profile": {
        "workExperience": "Work Experience",
        "noExperience": "No work experience added",
        "startAddingExperience": "Start by adding your professional experience"
      },
      "language": {
        "english": "English",
        "spanish": "Spanish",
        "selectLanguage": "Select Language"
      },
      "admin": {
        "header": {
          "title": "CareerPython Admin",
          "subtitle": "Admin Panel",
          "logout": "Logout"
        },
        "nav": {
          "dashboard": "Dashboard",
          "users": "Users",
          "candidates": "Candidates",
          "companies": "Companies",
          "jobPositions": "Job Positions",
          "interviewTemplates": "Interview Templates"
        }
      },
      "candidateProfile": {
        "header": {
          "title": "My Profile",
          "subtitle": "Candidate Dashboard"
        },
        "nav": {
          "dashboard": "Dashboard",
          "dashboardDesc": "General overview",
          "profile": "My Profile",
          "profileDesc": "Personal information",
          "experience": "Experience",
          "experienceDesc": "Work experience",
          "education": "Education",
          "educationDesc": "Academic background",
          "projects": "Projects",
          "projectsDesc": "Completed projects",
          "resumes": "My CVs",
          "resumesDesc": "Generate and manage CVs",
          "applications": "Applications",
          "interviews": "Interviews",
          "settings": "Settings",
          "comingSoon": "Coming soon..."
        },
        "footer": {
          "brandName": "CareerPython",
          "version": "v1.0 MVP"
        }
      },
      "adminLogin": {
        "title": "Administration Panel",
        "subtitle": "Restricted access for administrators only",
        "errors": {
          "noPermissions": "You don't have administrator permissions",
          "invalidCredentials": "Invalid credentials"
        },
        "form": {
          "adminEmail": "Administrator Email",
          "emailPlaceholder": "admin@company.com",
          "password": "Password",
          "securityNotice": "Restricted access. Only authorized personnel.",
          "verifyingAccess": "Verifying access...",
          "accessPanel": "Access Panel"
        },
        "footer": {
          "candidateQuestion": "Are you a candidate?",
          "candidateAccess": "Candidate Access"
        },
        "features": {
          "title": "Administration panel includes:",
          "userManagement": "User management",
          "candidateManagement": "Candidate management",
          "companyManagement": "Company management",
          "interviewTemplates": "Interview templates"
        }
      }
    }
  },
  es: {
    translation: {
      "common": {
        "save": "Guardar",
        "cancel": "Cancelar",
        "edit": "Editar",
        "delete": "Eliminar",
        "add": "Añadir",
        "update": "Actualizar",
        "loading": "Cargando...",
        "search": "Buscar",
        "back": "Atrás",
        "continue": "Continuar",
        "yes": "Sí",
        "no": "No",
        "confirm": "Confirmar",
        "close": "Cerrar",
        "name": "Nombre",
        "email": "Email",
        "phone": "Teléfono",
        "description": "Descripción",
        "startDate": "Fecha de Inicio",
        "endDate": "Fecha de Fin",
        "current": "Actual",
        "inProgress": "En curso",
        "saving": "Guardando...",
        "unsavedChanges": "Cambios sin guardar",
        "lastSaved": "Guardado por última vez"
      },
      "experience": {
        "jobTitle": "Cargo / Posición",
        "company": "Empresa",
        "description": "Descripción",
        "startDate": "Fecha de Inicio",
        "endDate": "Fecha de Fin",
        "currentJob": "Es mi trabajo actual",
        "addExperience": "Añadir Experiencia",
        "editExperience": "Editar Experiencia",
        "addNewExperience": "Añadir Nueva Experiencia",
        "experienceAdded": "Experiencia añadida correctamente",
        "experienceUpdated": "Experiencia actualizada correctamente",
        "experienceDeleted": "Experiencia eliminada correctamente",
        "deleteConfirm": "¿Estás seguro de que quieres eliminar esta experiencia?",
        "errorLoading": "Error al cargar la experiencia laboral",
        "errorSaving": "Error al guardar la experiencia",
        "errorDeleting": "Error al eliminar la experiencia",
        "jobTitlePlaceholder": "ej. Desarrollador Senior",
        "companyPlaceholder": "ej. Tech Solutions Corp",
        "descriptionPlaceholder": "Describe tus responsabilidades, logros y tecnologías utilizadas..."
      },
      "education": {
        "degree": "Título / Grado",
        "institution": "Institución",
        "description": "Descripción",
        "startDate": "Fecha de Inicio",
        "endDate": "Fecha de Finalización",
        "currentStudies": "Estoy estudiando actualmente",
        "addEducation": "Añadir Educación",
        "editEducation": "Editar Educación",
        "addNewEducation": "Añadir Nueva Educación",
        "educationAdded": "Educación añadida correctamente",
        "educationUpdated": "Educación actualizada correctamente",
        "educationDeleted": "Educación eliminada correctamente",
        "deleteConfirm": "¿Estás seguro de que quieres eliminar esta educación?",
        "errorLoading": "Error al cargar la educación",
        "errorSaving": "Error al guardar la educación",
        "errorDeleting": "Error al eliminar la educación",
        "degreePlaceholder": "ej. Ingeniería Informática",
        "institutionPlaceholder": "ej. Universidad Politécnica",
        "descriptionPlaceholder": "Describe tu formación, especialización, logros académicos...",
        "noEducation": "No has añadido educación",
        "startAddingEducation": "Comienza añadiendo tu formación académica",
        "leaveEmptyIfCurrentStudies": "Deja vacío si estás estudiando actualmente"
      },
      "projects": {
        "name": "Nombre del Proyecto",
        "description": "Descripción",
        "startDate": "Fecha de Inicio",
        "endDate": "Fecha de Finalización",
        "inProgress": "En curso",
        "addProject": "Añadir Proyecto",
        "editProject": "Editar Proyecto",
        "addNewProject": "Añadir Nuevo Proyecto",
        "projectAdded": "Proyecto añadido correctamente",
        "projectUpdated": "Proyecto actualizado correctamente",
        "projectDeleted": "Proyecto eliminado correctamente",
        "deleteConfirm": "¿Estás seguro de que quieres eliminar este proyecto?",
        "errorLoading": "Error al cargar los proyectos",
        "errorSaving": "Error al guardar el proyecto",
        "errorDeleting": "Error al eliminar el proyecto",
        "namePlaceholder": "ej. Sistema de Gestión de Inventario",
        "descriptionPlaceholder": "Describe el proyecto, tecnologías utilizadas, objetivos alcanzados, desafíos superados...",
        "personalProject": "Proyecto Personal"
      },
      "resume": {
        "generalInformation": "Información General",
        "resumeSections": "Secciones del Currículum",
        "cvTitle": "Título del CV",
        "fullName": "Nombre Completo",
        "addSection": "Añadir Sección",
        "addNewSection": "Añadir Nueva Sección",
        "sectionKey": "Clave de Sección",
        "sectionTitle": "Título de Sección",
        "initialContent": "Contenido Inicial (Opcional)",
        "editTitle": "Editar título",
        "moveUp": "Mover arriba",
        "moveDown": "Mover abajo",
        "dragToReorder": "Arrastra para reordenar",
        "removeSection": "Eliminar sección",
        "sectionKeyPlaceholder": "ej. certificaciones",
        "sectionTitlePlaceholder": "ej. Certificaciones",
        "sectionContentPlaceholder": "Ingresa el contenido inicial para esta sección...",
        "enterContentPlaceholder": "Ingresa contenido para {{title}}...",
        "noSectionsFound": "No se encontraron secciones. Añade una sección para comenzar.",
        "sectionAlreadyExists": "Una sección con esta clave ya existe",
        "removeSectionConfirm": "¿Estás seguro de que quieres eliminar esta sección?",
        "loadingEditor": "Cargando editor de currículum...",
        "editGeneralInfo": "Editar información general",
        "cvTitlePlaceholder": "Currículum Profesional",
        "noTitleSet": "Sin título establecido",
        "noNameSet": "Sin nombre establecido",
        "noEmailSet": "Sin email establecido",
        "noPhoneSet": "Sin teléfono establecido",
        "hidePreview": "Ocultar Vista Previa",
        "showPreview": "Mostrar Vista Previa",
        "revertChanges": "Revertir Cambios",
        "failedToLoadResumeData": "Error al cargar los datos del currículum. Por favor, inténtalo de nuevo.",
        "failedToSaveResume": "Error al guardar el currículum. Por favor, inténtalo de nuevo.",
        "resumeNotFound": "Currículum no encontrado",
        "tryAgain": "Intentar de Nuevo",
        "sections": {
          "experience": "Experiencia Profesional",
          "education": "Educación",
          "skills": "Habilidades",
          "projects": "Proyectos",
          "addExperienceHere": "Agrega tu experiencia profesional aquí...",
          "addEducationHere": "Agrega tu formación académica aquí...",
          "addSkillsHere": "Agrega tus habilidades aquí",
          "addProjectsHere": "Agrega tus proyectos aquí..."
        }
      },
      "profile": {
        "workExperience": "Experiencia Laboral",
        "noExperience": "No has añadido experiencia laboral",
        "startAddingExperience": "Comienza añadiendo tu experiencia profesional"
      },
      "language": {
        "english": "Inglés",
        "spanish": "Español",
        "selectLanguage": "Seleccionar Idioma"
      },
      "admin": {
        "header": {
          "title": "CareerPython Admin",
          "subtitle": "Panel de Administración",
          "logout": "Cerrar Sesión"
        },
        "nav": {
          "dashboard": "Panel de Control",
          "users": "Usuarios",
          "candidates": "Candidatos",
          "companies": "Empresas",
          "jobPositions": "Ofertas de Trabajo",
          "interviewTemplates": "Plantillas de Entrevista"
        }
      },
      "candidateProfile": {
        "header": {
          "title": "Mi Perfil",
          "subtitle": "Dashboard Candidato"
        },
        "nav": {
          "dashboard": "Dashboard",
          "dashboardDesc": "Resumen general",
          "profile": "Mi Perfil",
          "profileDesc": "Información personal",
          "experience": "Experiencia",
          "experienceDesc": "Experiencia laboral",
          "education": "Educación",
          "educationDesc": "Formación académica",
          "projects": "Proyectos",
          "projectsDesc": "Proyectos realizados",
          "resumes": "Mis CVs",
          "resumesDesc": "Generar y gestionar CVs",
          "applications": "Candidaturas",
          "interviews": "Entrevistas",
          "settings": "Configuración",
          "comingSoon": "Próximamente..."
        },
        "footer": {
          "brandName": "CareerPython",
          "version": "v1.0 MVP"
        }
      },
      "adminLogin": {
        "title": "Panel de Administración",
        "subtitle": "Acceso restringido solo para administradores",
        "errors": {
          "noPermissions": "No tienes permisos de administrador",
          "invalidCredentials": "Credenciales inválidas"
        },
        "form": {
          "adminEmail": "Email de Administrador",
          "emailPlaceholder": "admin@empresa.com",
          "password": "Contraseña",
          "securityNotice": "Acceso restringido. Solo personal autorizado.",
          "verifyingAccess": "Verificando acceso...",
          "accessPanel": "Acceder al Panel"
        },
        "footer": {
          "candidateQuestion": "¿Eres candidato?",
          "candidateAccess": "Acceso Candidatos"
        },
        "features": {
          "title": "Panel de administración incluye:",
          "userManagement": "Gestión de usuarios",
          "candidateManagement": "Gestión de candidatos",
          "companyManagement": "Gestión de empresas",
          "interviewTemplates": "Plantillas de entrevistas"
        }
      }
    }
  }
};

i18n
  // Detect user language
  .use(LanguageDetector)
  // Pass the i18n instance to react-i18next
  .use(initReactI18next)
  // Initialize i18next
  .init({
    resources,
    fallbackLng: 'en',
    debug: process.env.NODE_ENV === 'development',

    interpolation: {
      escapeValue: false, // React already does escaping
    },

    // Language detection options
    detection: {
      // Order and from where user language should be detected
      order: ['localStorage', 'navigator', 'htmlTag'],

      // Keys or params to lookup language from
      lookupLocalStorage: 'i18nextLng',

      // Cache user language on
      caches: ['localStorage'],

      // Optional expire and versions
      checkWhitelist: true,
    },

    // React i18next options
    react: {
      useSuspense: false, // Disable suspense to avoid loading issues
    },
  });

export default i18n;