/**
 * Craftons brand tokens for motion graphics.
 * Mirrors pipeline/tokens.css and .claude/skills/craftons-design/BRAND.md.
 * Change them there first, then here.
 */
export const C = {
  green: '#194431',
  green700: '#123022',
  green900: '#0a1c14',
  lineGreen: '#2d8a5b',
  black: '#000000',
  ink: '#0e0e0c',
  white: '#ffffff',
  paper: '#F6F4F0',
} as const;

/** Reel canvas. Overlays render at full frame so they composite 1:1 in CapCut. */
export const CANVAS = { width: 1080, height: 1920, fps: 30 } as const;

/**
 * Meta consolidated Stories + Reels into one 9:16 safe zone, March 2026.
 * Nothing that must be read goes outside the central area.
 */
export const SAFE = {
  top: 270,
  side: 65,
  bottom: 672,
  get centreY() {
    return this.top + (CANVAS.height - this.top - this.bottom) / 2;
  },
} as const;

/** Type faces live in fonts.ts — they must be LOADED, not just named. */
export {FONT} from './fonts';
