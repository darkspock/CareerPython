/**
 * Stage Style types for visual customization of workflow stages
 */

export interface StageStyle {
  icon: string;
  color: string;
  background_color: string;
}

export interface UpdateStageStyleRequest {
  icon?: string;
  color?: string;
  background_color?: string;
}

// Default styles for different stage types
export const DEFAULT_STAGE_STYLE: StageStyle = {
  icon: "📋",
  color: "#374151",
  background_color: "#f3f4f6"
};

export const SUCCESS_STAGE_STYLE: StageStyle = {
  icon: "✅",
  color: "#065f46",
  background_color: "#d1fae5"
};

export const FAIL_STAGE_STYLE: StageStyle = {
  icon: "❌",
  color: "#991b1b",
  background_color: "#fee2e2"
};

export const PROCESS_STAGE_STYLE: StageStyle = {
  icon: "⚙️",
  color: "#1e40af",
  background_color: "#dbeafe"
};

export const REVIEW_STAGE_STYLE: StageStyle = {
  icon: "👀",
  color: "#92400e",
  background_color: "#fef3c7"
};

// Helper function to get default style based on stage type
export function getDefaultStyleForStageType(stageType: string): StageStyle {
  switch (stageType) {
    case 'SUCCESS':
      return SUCCESS_STAGE_STYLE;
    case 'FAIL':
      return FAIL_STAGE_STYLE;
    case 'PROCESS':
      return PROCESS_STAGE_STYLE;
    case 'REVIEW':
      return REVIEW_STAGE_STYLE;
    default:
      return DEFAULT_STAGE_STYLE;
  }
}

// Helper function to validate color format
export function isValidColor(color: string): boolean {
  const hexPattern = /^#[0-9A-Fa-f]{6}$/;
  const rgbPattern = /^rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)$/;
  const rgbaPattern = /^rgba\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*[\d.]+\s*\)$/;
  
  const cssColors = [
    'black', 'white', 'red', 'green', 'blue', 'yellow', 'orange', 'purple',
    'pink', 'brown', 'gray', 'grey', 'transparent', 'currentColor'
  ];
  
  return (
    hexPattern.test(color) ||
    rgbPattern.test(color) ||
    rgbaPattern.test(color) ||
    cssColors.includes(color.toLowerCase())
  );
}

// Helper function to validate icon
export function isValidIcon(icon: string): boolean {
  if (!icon || !icon.trim()) return false;
  if (icon.length > 1000) return false;
  if (icon.startsWith('<') && !icon.endsWith('>')) return false;
  return true;
}
