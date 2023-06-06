import { TypeButtonPanel, TypeWindow } from 'geoview-core-types';
import { useLocation, BrowserRouter } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { useState, useContext } from 'react';



import { AppContext } from '../index';

const w = window as TypeWindow;

const cgpv = w['cgpv'];

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

  const appContext = useContext(AppContext);
  const dispatch = appContext.store.dispatch; //useDispatch();
  const { buttonPanel, mapId } = props;
  const { ui } = cgpv;

  const { TextField, Select, Autocomplete, Button, List, ListItem, ListItemText } = ui.elements;

  const [layerData, setLayerData] = useState([]);
  const [query, setQuery] = useState('');
  const [language, setLanguage] = useState('en');
  const [services, setServices] = useState('');
  const languages = [
    ['en', 'English'],
    ['fr', 'French'],
  ];
  const serviceKeys = [
    ['nominatim', 'nominatim'],
    ['geonames', 'geonames'],
    ['locate', 'locate'],
    ['nts', 'nts'],
  ];

  function callGeolocator() {
    const qConst: string = 'q=';
    const langConst: string = '&lang=';
    let servConst: string = '';
    if (services.length > 0) {
      servConst = '&keys=';
    }
    const queryString = qConst.concat(query, langConst, language, servConst, services);
    getConvertedData(queryString).then((res) => {
      setLayerData(res);
    });
  }

  async function getConvertedData(query: string): Promise<any> {
    const url: string = 'https://znwaxif9m9.execute-api.ca-central-1.amazonaws.com/stage/geolocator?';
    const strToFetch = url.concat(query);
    console.log(strToFetch);
    const response = await fetch(strToFetch);
    const result: any = await response.json();
    console.log(result);
    return result;
  }

  function handleServices(event: Event, newValue: string[]) {
    setServices(newValue.map((x) => x[1]).join(','));
  }

  function zoomItem(coords: [number, number]) {
    console.log(`lat ${coords[1]}, long ${coords[0]}`);
    const coordsProj = (cgpv.api.projection as any).LngLatToWm([coords[0], coords[1]])[0];
    cgpv.api.maps.mapWM.getView().animate({ center: coordsProj, duration: 500, zoom: 11 });
  }

  return (
    <>
      <BrowserRouter>
        <label htmlFor="filter">Search filter</label>
        <TextField id="filter" type="text" onChange={(e: any) => setQuery(e.target.value)} />
        <div style={{ display: 'grid', padding: '10px' }}>
          <label htmlFor="language">Language filter (optional)</label>
          <Select
            id="language"
            value={language}
            onChange={(e: any) => setLanguage(e.target.value)}
            inputLabel={{
              id: 'select-variable',
            }}
            menuItems={languages.map(([value, label]) => ({
              key: value,
              item: {
                value,
                children: label,
              },
            }))}
          />
        </div>
        <Autocomplete
          style={{ display: 'grid', paddingBottom: '20px' }}
          fullWidth
          multiple={true}
          disableCloseOnSelect
          disableClearable={false}
          id="service-key"
          options={serviceKeys}
          getOptionLabel={(option) => `${option[1]} (${option[0]})`}
          renderOption={(props, option) => <span {...props}>{option[1]}</span>}
          onChange={handleServices as any}
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          renderInput={(params) => <TextField {...params} label="Select Service keys" />}
        />
        <Button tooltip="Process Data" tooltipPlacement="right" type="text" variant="contained" onClick={() => callGeolocator()}>
          Process Data
        </Button>
        <List>
          {layerData.map((layerData) => {
            return (
              <div key={layerData}>
                <ListItem onClick={() => zoomItem([(layerData as any).lng, (layerData as any).lat])}>
                  <ListItemText primary={(layerData as any).name} nonce={undefined} />
                </ListItem>
              </div>
            );
          })}
        </List>
      </BrowserRouter>
    </>
  );
};
