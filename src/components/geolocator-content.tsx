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
  const { TextField, Select, Autocomplete, Button } = ui.elements;

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
    console.log(query);
    console.log(language);
    console.log(services);
    let qConst: string = "q=";
    let langConst: string = "&lang=";
    var servConst: string = "";
    if (services.length > 0) {
      servConst = "&keys=";
    }
    var queryString = qConst.concat(query, langConst, language, servConst, services)
    console.log(queryString)
    getConvertedData(queryString);
  }

  async function getConvertedData(query: string): Promise<any> {
    let url: string = 'https://fr59c5usw4.execute-api.ca-central-1.amazonaws.com/dev?'
    var strToFetch = url.concat(query)
    console.log(strToFetch)
    const response = await fetch(strToFetch);
    const result: any = await response.json();
    console.log(result)
    return result;
  };

  function handleServices(event: Event, newValue: string[]) {
    setServices(newValue.map((x) => x[1]).join(','));
  }

  return (
    <>
      <label htmlFor="filter">Search filter</label>
      <TextField id="filter" type="text" onChange={(e: any) => setQuery(e.target.value)} />
      <div style={{display: "grid", padding: "10px"}}>
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
        style={{display: "grid", paddingBottom: "20px"}}
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
    </>
  );
};
