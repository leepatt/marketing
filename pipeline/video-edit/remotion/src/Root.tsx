import React from 'react';
import {Composition} from 'remotion';
import {CANVAS} from './brand';
import {SpecStamp} from './SpecStamp';
import {LowerThird} from './LowerThird';
import {TitleCard} from './TitleCard';
import {Endcard} from './Endcard';

/**
 * Every composition renders at the full reel frame (1080x1920) so overlays
 * composite 1:1 in CapCut with no repositioning.
 *
 * Overlays render with alpha (--codec=prores --prores-profile=4444).
 * Endcard is opaque and can render as plain h264.
 */
export const RemotionRoot: React.FC = () => {
  const base = {width: CANVAS.width, height: CANVAS.height, fps: CANVAS.fps};

  return (
    <>
      <Composition
        id="SpecStamp"
        component={SpecStamp}
        durationInFrames={90}
        {...base}
        defaultProps={{
          radius: 'R900',
          specs: ['2400mm', '17mm formply'],
          label: 'CUT TO',
          position: 0.62,
        }}
      />
      <Composition
        id="LowerThird"
        component={LowerThird}
        durationInFrames={90}
        {...base}
        defaultProps={{name: 'Samuel C.', role: 'Concreter, Geelong'}}
      />
      <Composition
        id="TitleCard"
        component={TitleCard}
        durationInFrames={75}
        {...base}
        defaultProps={{text: 'Set out the curve', step: 'STEP 01'}}
      />
      <Composition
        id="Endcard"
        component={Endcard}
        durationInFrames={45}
        {...base}
        defaultProps={{cta: 'Build it once.', url: 'craftons.com.au'}}
      />
    </>
  );
};
