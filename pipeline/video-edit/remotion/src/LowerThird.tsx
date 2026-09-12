import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig, AbsoluteFill} from 'remotion';
import {C, SAFE} from './brand';
import {FONT, useCraftonsFonts} from './fonts';

/** Name + trade for a builder on camera. First name + last initial, per brand rules. */
export type LowerThirdProps = {
  name: string;
  role: string;
};

export const LowerThird: React.FC<LowerThirdProps> = ({name, role}) => {
  useCraftonsFonts();
  const frame = useCurrentFrame();
  const {fps, height} = useVideoConfig();

  const enter = spring({frame, fps, config: {damping: 200, mass: 0.5}});
  const wipe = interpolate(enter, [0, 1], [0, 1]);
  const out = interpolate(frame, [70, 85], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{opacity: Math.min(1, out)}}>
      <div
        style={{
          position: 'absolute',
          left: SAFE.side + 24,
          top: height - SAFE.bottom - 150,
          display: 'flex',
        }}
      >
        <div style={{width: 6, background: C.lineGreen, transform: `scaleY(${wipe})`, transformOrigin: 'top'}} />
        <div
          style={{
            background: C.green,
            padding: '16px 26px',
            clipPath: `inset(0 ${(1 - wipe) * 100}% 0 0)`,
          }}
        >
          <div style={{fontFamily: FONT.condensed,
              fontWeight: 700, fontSize: 52, color: C.white, lineHeight: 1}}>
            {name}
          </div>
          <div
            style={{
              fontFamily: FONT.body,
              fontSize: 26,
              color: C.lineGreen,
              letterSpacing: '0.06em',
              marginTop: 4,
            }}
          >
            {role}
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
