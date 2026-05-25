// =============================================================================
// HelloWorld.tsx — Remotion Composition Component
// =============================================================================
//
// PURPOSE:
//   Defines the video composition layout and animations for the HelloWorld template.
//
// PART OF: Multimedia_Generation_Pipeline (Templates/HelloWorld/)
// =============================================================================

import React from 'react';
import {
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

export const HelloWorld: React.FC<{
  titleText: string;
  titleColor: string;
}> = ({titleText, titleColor}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  // Animate opacity: fade in from frame 0 to 30
  const opacity = interpolate(frame, [0, 30], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Animate scale: scale up from frame 0 to 45 with a spring effect
  const scale = spring({
    frame,
    fps,
    config: {
      damping: 12,
    },
  });

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: '#0b0f19',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        fontFamily: 'system-ui, -apple-system, sans-serif',
      }}
    >
      <div
        style={{
          opacity,
          transform: `scale(${scale})`,
          textAlign: 'center',
        }}
      >
        <h1
          style={{
            fontSize: '80px',
            fontWeight: 'bold',
            color: titleColor,
            marginBottom: '20px',
            textShadow: '0 4px 20px rgba(79, 70, 229, 0.4)',
          }}
        >
          {titleText}
        </h1>
        <p
          style={{
            fontSize: '40px',
            color: '#94a3b8',
            fontWeight: 300,
          }}
        >
          Multimedia Generation Pipeline (MGP) Active
        </p>
      </div>
    </div>
  );
};
