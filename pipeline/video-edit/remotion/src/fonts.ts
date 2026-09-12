/**
 * Craftons faces, bundled locally in public/fonts.
 *
 * Two lessons are baked in here:
 *  1. Declaring a font-family in CSS is not enough in Remotion — the font must be
 *     LOADED or it silently falls back to a generic. The first render of the spec
 *     stamp came out in a default sans and looked nothing like the brand.
 *  2. Loading from Google's CDN at render time adds a network dependency that can
 *     fail (it did, behind a proxy). Local files always render the same.
 *
 * Aeonik is the official display face but is licensed and not distributable here.
 * Big Shoulders Display is the documented fallback in BRAND.md.
 */
import React from 'react';
import {continueRender, delayRender, staticFile} from 'remotion';

const FACES = [
  {family: 'Big Shoulders Display', weight: 700, file: 'BigShouldersDisplay-700.woff2'},
  {family: 'Big Shoulders Display', weight: 900, file: 'BigShouldersDisplay-900.woff2'},
  {family: 'JetBrains Mono', weight: 400, file: 'JetBrainsMono-400.woff2'},
  {family: 'JetBrains Mono', weight: 700, file: 'JetBrainsMono-700.woff2'},
  {family: 'Inter', weight: 400, file: 'Inter-400.woff2'},
  {family: 'Inter', weight: 600, file: 'Inter-600.woff2'},
];

let loaded: Promise<void> | null = null;

const loadAll = (): Promise<void> => {
  if (loaded) return loaded;
  loaded = Promise.all(
    FACES.map(async ({family, weight, file}) => {
      const face = new FontFace(family, `url(${staticFile('fonts/' + file)})`, {
        weight: String(weight),
      });
      await face.load();
      // lib.dom's FontFaceSet type omits add(); it exists at runtime.
      (document.fonts as unknown as {add: (f: FontFace) => void}).add(face);
    }),
  ).then(() => undefined);
  return loaded;
};

/**
 * Blocks the render until every face is ready. Without this, Remotion can
 * screenshot a frame mid-load and bake in the fallback.
 */
export const useCraftonsFonts = (): void => {
  const [handle] = React.useState(() => delayRender('Loading Craftons fonts'));
  React.useEffect(() => {
    loadAll()
      .then(() => continueRender(handle))
      .catch((e) => {
        // Fail loudly. A silent fallback ships off-brand video.
        throw new Error(`Craftons fonts failed to load: ${(e as Error).message}`);
      });
  }, [handle]);
};

export const FONT = {
  condensed: '"Big Shoulders Display", Impact, sans-serif',
  mono: '"JetBrains Mono", ui-monospace, Consolas, monospace',
  body: '"Inter", system-ui, sans-serif',
} as const;
