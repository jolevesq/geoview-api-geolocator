import { TypeTileGrid, TypeWindow} from 'geoview-core-types';
import Grid from '@mui/material/Grid';
import {
  List,
  ListItem,
  ExpandMoreIcon,
  ExpandLessIcon,
  Tooltip,
  IconButton,
} from 'geoview-core-types';

const w = window as TypeWindow;

const cgpv = w['cgpv'];

const { react } = cgpv;

/**
 * Data Grid Content Properties
 */
interface GeolocatorDataContentProps {
  mapId: string;
  tileGrid: TypeTileGrid;
}
/**
 * Create a new Data content
 *
 * @param {GeolocatorDatalContentProps} props data content properties
 * @returns {JSX.Element} the new create data content
 */

export const GeolocatorDataContent = (props: GeolocatorDataContentProps): JSX.Element => {
  const { tileGrid, mapId } = props;

  const { ui, react } = cgpv;

  const { useState, useEffect, useMemo } = react;
  const { TextField, Select, Autocomplete, Button } = ui.elements;

  return (
    <>
      <label htmlFor="Grid">Grid</label>
      <div style={{display: "grid", padding: "10px"}}>
        <label htmlFor="grid info">Info</label>
      </div>
    </>
  );
};
