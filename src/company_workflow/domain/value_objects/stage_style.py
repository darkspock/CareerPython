"""
Stage Style Value Object - Estilos visuales para workflow stages
"""
import re
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class StageStyle:
    """Value object para estilos visuales de workflow stages"""
    
    icon: str
    color: str
    background_color: str
    
    def __post_init__(self) -> None:
        """Validar los valores después de la inicialización"""
        self._validate_icon()
        self._validate_color(self.color, "color")
        self._validate_color(self.background_color, "background_color")
        self._validate_contrast()
    
    def _validate_icon(self) -> None:
        """Validar que el icono sea válido"""
        if not self.icon or not self.icon.strip():
            raise ValueError("Icon cannot be empty")
        
        if len(self.icon) > 1000:
            raise ValueError("Icon cannot exceed 1000 characters")
        
        # Validar que sea emoji válido o HTML válido
        if self.icon.startswith('<') and not self.icon.endswith('>'):
            raise ValueError("Invalid HTML icon format")
    
    def _validate_color(self, color: str, field_name: str) -> None:
        """Validar formato de color"""
        if not color or not color.strip():
            raise ValueError(f"{field_name} cannot be empty")
        
        # Patrones válidos para colores
        hex_pattern = r'^#[0-9A-Fa-f]{6}$'
        rgb_pattern = r'^rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)$'
        rgba_pattern = r'^rgba\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*[\d.]+\s*\)$'
        
        # Nombres de colores CSS comunes
        css_colors = {
            'black', 'white', 'red', 'green', 'blue', 'yellow', 'orange', 'purple',
            'pink', 'brown', 'gray', 'grey', 'transparent', 'currentColor'
        }
        
        if not (
            re.match(hex_pattern, color) or
            re.match(rgb_pattern, color) or
            re.match(rgba_pattern, color) or
            color.lower() in css_colors
        ):
            raise ValueError(f"Invalid {field_name} format: {color}")
    
    def _validate_contrast(self) -> None:
        """Validar que haya suficiente contraste entre color y background"""
        # Esta es una validación básica - en producción se podría usar una librería
        # como contrast-ratio para validaciones más precisas
        if self.color.lower() == self.background_color.lower():
            raise ValueError("Color and background color cannot be the same")
    
    @staticmethod
    def create(
        icon: str = "📋",
        color: str = "#374151",
        background_color: str = "#f3f4f6"
    ) -> "StageStyle":
        """
        Crear un StageStyle con valores por defecto
        
        Args:
            icon: Icono del stage (emoji, HTML icon, o SVG)
            color: Color del texto
            background_color: Color de fondo
            
        Returns:
            StageStyle: Nueva instancia con estilos
            
        Raises:
            ValueError: Si los valores no son válidos
        """
        return StageStyle(
            icon=icon,
            color=color,
            background_color=background_color
        )
    
    def update(
        self,
        icon: Optional[str] = None,
        color: Optional[str] = None,
        background_color: Optional[str] = None
    ) -> "StageStyle":
        """
        Crear una nueva instancia con estilos actualizados
        
        Args:
            icon: Nuevo icono (opcional)
            color: Nuevo color (opcional)
            background_color: Nuevo color de fondo (opcional)
            
        Returns:
            StageStyle: Nueva instancia con estilos actualizados
        """
        return StageStyle(
            icon=icon if icon is not None else self.icon,
            color=color if color is not None else self.color,
            background_color=background_color if background_color is not None else self.background_color
        )
    
    def to_dict(self) -> dict[str, str]:
        """Convertir a diccionario para serialización"""
        return {
            "icon": self.icon,
            "color": self.color,
            "background_color": self.background_color
        }
    
    @staticmethod
    def from_dict(data: dict[str, str]) -> "StageStyle":
        """Crear desde diccionario para deserialización"""
        return StageStyle(
            icon=data["icon"],
            color=data["color"],
            background_color=data["background_color"]
        )
    
    def __str__(self) -> str:
        """Representación string del estilo"""
        return f"StageStyle(icon='{self.icon}', color='{self.color}', bg='{self.background_color}')"


# Estilos por defecto basados en tipo de stage
DEFAULT_STAGE_STYLE = StageStyle.create()

SUCCESS_STAGE_STYLE = StageStyle.create(
    icon="✅",
    color="#065f46",  # green-800
    background_color="#d1fae5"  # green-100
)

FAIL_STAGE_STYLE = StageStyle.create(
    icon="❌",
    color="#991b1b",  # red-800
    background_color="#fee2e2"  # red-100
)

PROCESS_STAGE_STYLE = StageStyle.create(
    icon="⚙️",
    color="#1e40af",  # blue-800
    background_color="#dbeafe"  # blue-100
)

REVIEW_STAGE_STYLE = StageStyle.create(
    icon="👀",
    color="#92400e",  # amber-800
    background_color="#fef3c7"  # amber-100
)
