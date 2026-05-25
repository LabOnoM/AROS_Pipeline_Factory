// =============================================================================
// Root.tsx — Remotion Composition Root
// =============================================================================
//
// PURPOSE:
//   Registers the Remotion composition for the HelloWorld template.
//
// PART OF: Multimedia_Generation_Pipeline (Templates/HelloWorld/)
// =============================================================================

import React from 'react';
import {Composition} from 'remotion';
import {HelloWorld} from './HelloWorld';

export const Root: React.FC = () => {
  return (
    <>
      <Composition
        id="HelloWorld"
        component={HelloWorld}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          titleText: "Welcome to AROS",
          titleColor: "#4f46e5",
        }}
      />
    </>
  );
};
