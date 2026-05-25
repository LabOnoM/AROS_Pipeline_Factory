// =============================================================================
// index.ts — Remotion Entry Point
// =============================================================================
//
// PURPOSE:
//   Registers the root component for the Remotion programmatic rendering engine.
//
// PART OF: Multimedia_Generation_Pipeline (Templates/HelloWorld/)
// =============================================================================

import {registerRoot} from 'remotion';
import {Root} from './Root';

registerRoot(Root);
