import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig, AbsoluteFill} from 'remotion';
import {C, SAFE} from './brand';
import {FONT, useCraftonsFonts} from './fonts';

/**
 * The Craftons signature move: real job specs stamped on real footage.
 * A competitor can't fake this — the numbers come off an actual job.
 *
 * ONLY EVER REAL FIGURES. Never a plausible-looking placeholder.
 */
export type SpecStampProps = {
  /** e.g. "R900" — the headline figure */
  radius: string;
  /** supporting specs, e.g. ["2400mm", "17mm formply"] */
  specs: string[];
  /** small label above, e.g. "CUT TO" */
  label?: string;
  /** vertical placement as a fraction of the safe band. 0.5 = centred */
  position?: number;
};

export const SpecStamp: React.FC<SpecStampProps> = ({
  radius,
  specs,
  label = 'CUT TO',
  position = 0.62,
}) => {
  useCraftonsFonts();
  const frame = useCurrentFrame();
  const {fps, height} = useVideoConfig();

  // Settle-in, not a bounce. Trade audience, not a toy brand.
  const enter = spring({frame, fps, config: {damping: 200, mass: 0.6}});
  const slide = interpolate(enter, [0, 1], [28, 0]);

  // Rule sweeps out under the numbers
  const rule = interpolate(frame, [6, 22], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Hold, then fade. Duration comes from the composition.
  const out = interpolate(frame, [70, 85], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const usable = height - SAFE.top - SAFE.bottom;
  const top = SAFE.top + usable * position;

  return (
    <AbsoluteFill style={{opacity: Math.min(enter, out)}}>
      <div
        style={{
          position: 'absolute',
          left: SAFE.side + 24,
          top,
          transform: `translateY(${slide}px)`,
        }}
      >
        {label ? (
          <div
            style={{
              fontFamily: FONT.condensed,
              fontWeight: 700,
              fontSize: 30,
              letterSpacing: '0.22em',
              color: C.lineGreen,
              marginBottom: 6,
            }}
          >
            {label}
          </div>
        ) : null}

        <div
          style={{
            fontFamily: FONT.mono,
            fontVariantNumeric: 'tabular-nums',
            fontWeight: 700,
            fontSize: 112,
            lineHeight: 0.92,
            color: C.white,
            textShadow: '0 3px 18px rgba(0,0,0,.55)',
          }}
        >
          {radius}
        </div>

        <div
          style={{
            height: 4,
            width: `${rule * 100}%`,
            maxWidth: 420,
            background: C.lineGreen,
            margin: '14px 0 12px',
          }}
        />

        <div style={{display: 'flex', gap: 14, flexWrap: 'wrap', maxWidth: 620}}>
          {specs.map((s) => (
            <span
              key={s}
              style={{
                fontFamily: FONT.mono,
                fontWeight: 400,
                fontVariantNumeric: 'tabular-nums',
                fontSize: 34,
                color: C.white,
                background: C.green,
                padding: '8px 16px',
                borderRadius: 6,
                textShadow: 'none',
              }}
            >
              {s}
            </span>
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};
