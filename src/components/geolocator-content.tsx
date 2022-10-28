import { TypeButtonPanel, TypeWindow } from 'geoview-core-types';

const w = window as TypeWindow;

const cgpv = w['cgpv'];

const { react } = cgpv;

/**
 * Panel Content Properties
 */
interface GeolocatorPanelContentProps {
  mapId: string;
  buttonPanel: TypeButtonPanel;
}

/**
 * Create a new panel content
 *
 * @param {GeolocatorPanelContentProps} props panel content properties
 * @returns {JSX.Element} the new create panel content
 */
export const GeolocatorPanelContent = (props: GeolocatorPanelContentProps): JSX.Element => {
  const { buttonPanel, mapId } = props;

  const { ui, react } = cgpv;

  const { useState, useEffect, useMemo } = react;


  return (
    <div>This is the comming soon content!</div>
  );
};
