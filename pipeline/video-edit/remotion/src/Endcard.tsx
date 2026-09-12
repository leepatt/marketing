import React from 'react';
import {interpolate, useCurrentFrame, AbsoluteFill} from 'remotion';
import {C} from './brand';
import {FONT, useCraftonsFonts} from './fonts';

/**
 * 1.5s sign-off. Opaque — this one is a clip, not an overlay.
 * Soft CTA only. The value-first law forbids a hard sell here.
 */
export type EndcardProps = {
  cta?: string;
  url?: string;
};

export const Endcard: React.FC<EndcardProps> = ({
  cta = 'Build it once.',
  url = 'craftons.com.au',
}) => {
  useCraftonsFonts();
  const frame = useCurrentFrame();
  const fade = interpolate(frame, [0, 8], [0, 1], {extrapolateRight: 'clamp'});

  // The brand's curved-line motif — wood grain abstracted, used as a watermark
  const draw = interpolate(frame, [4, 30], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{background: C.green, opacity: fade, justifyContent: 'center', alignItems: 'center'}}>
      <svg
        width={1080}
        height={700}
        viewBox="0 0 400 260"
        style={{position: 'absolute', opacity: 0.18}}
      >
        <g stroke={C.lineGreen} strokeWidth={1.1} fill="none">
          {[106, 118, 130, 142, 154, 166, 178].map((y, i) => (
            <path
              key={y}
              d={`M20 ${y} C ${58 + i * 2} ${y - 112}, ${138 + i * 2} ${y - 112}, ${178 + i * 2} ${y} S ${298 + i * 2} ${y + 112}, ${338 + i * 2} ${y}`}
              pathLength={1}
              strokeDasharray={1}
              strokeDashoffset={1 - draw}
            />
          ))}
        </g>
      </svg>

      <div style={{textAlign: 'center', zIndex: 1}}>
        <div style={{fontFamily: FONT.condensed,
              fontWeight: 700, fontSize: 104, color: C.white, lineHeight: 1}}>
          CRAFTONS
        </div>
        <div
          style={{
            fontFamily: FONT.body,
            fontSize: 34,
            color: C.lineGreen,
            marginTop: 18,
            letterSpacing: '0.04em',
          }}
        >
          {cta}
        </div>
        <div style={{fontFamily: FONT.mono, fontSize: 26, color: C.white, marginTop: 40, opacity: 0.85}}>
          {url}
        </div>
      </div>
    </AbsoluteFill>
  );
};
