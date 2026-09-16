// ============================================================
// INKSIDE DIGITAL — COLOR PALETTE
// ============================================================

export const colors = {
  // Background
  background: '#0B0F14',      // Main background
  card: '#131A22',            // Card background
  panel: '#1A2530',           // Panel background
  sidebar: '#0F141B',         // Sidebar background
  hover: '#18212B',           // Hover state

  // Border
  border: '#26313D',          // Main border
  borderLight: '#3A4A5A',     // Light border

  // Text
  text: '#E8EDF2',            // Primary text
  textSecondary: '#8D9AAA',   // Secondary text
  textMuted: '#5F6B78',       // Muted text

  // Accent
  primary: '#3B82F6',         // Blue
  success: '#10B981',         // Green
  warning: '#F59E0B',         // Amber
  danger: '#EF4444',          // Red
  purple: '#8B5CF6',          // Purple
  cyan: '#22D3EE',            // Cyan
} as const;

export type ColorKey = keyof typeof colors;
