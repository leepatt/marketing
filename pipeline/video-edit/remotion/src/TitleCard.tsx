import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig, AbsoluteFill} from 'remotion';
import {C, SAFE} from './brand';
import {FONT, useCraftonsFonts} from './fonts';

/** Section marker. Use a number ONLY when the content is genuinely a sequence. */
export type TitleCardProps = {
  text: string;
  step?: string;
};

export const TitleCard: React.FC<TitleCardProps> = ({text, step}) => {
  useCraftonsFonts();
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const enter = spring({frame, fps, config: {damping: 200, mass: 0.5}});
  const out = interpolate(frame, [55, 70], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        opacity: Math.min(enter, out),
        justifyContent: 'center',
        alignItems: 'center',
        paddingTop: SAFE.top,
        paddingBottom: SAFE.bottom,
      }}
    >
      <div style={{textAlign: 'center', transform: `translateY(${interpolate(enter, [0, 1], [20, 0])}px)`}}>
        {step ? (
          <div
            style={{
              fontFamily: FONT.mono,
              fontSize: 34,
              color: C.lineGreen,
              letterSpacing: '0.24em',
              marginBottom: 12,
            }}
          >
            {step}
          </div>
        ) : null}
        <div
          style={{
            fontFamily: FONT.condensed,
              fontWeight: 700,
            fontSize: 96,
            lineHeight: 0.95,
            color: C.white,
            textShadow: '0 4px 24px rgba(0,0,0,.6)',
            maxWidth: 860,
          }}
        >
          {text}
        </div>
      </div>
    </AbsoluteFill>
  );
};
