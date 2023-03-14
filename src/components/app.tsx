// import React, { useEffect, createContext, useState, useMemo } from 'react';
import React, { useEffect } from 'react';

import makeStyles from '@mui/styles/makeStyles';

import { GeolocatorPanelContent } from './geolocator-content';

import translationEn from '../../public/locales/en/translation.json';
import translationFr from '../../public/locales/fr/translation.json';

import {
  TypeIconButtonProps,
  TypePanelProps,
  TypeWindow,
} from 'geoview-core-types';

// get reference to window object
const w = window as TypeWindow;

// get reference to geoview apis
const cgpv = w['cgpv'];

/**
 * main container and map styling
 */
const useStyles = makeStyles((theme) => ({
  container: {
    height: '100vh',
  },
}));

/**
 * Create a container containing a leaflet map using the GeoView viewer
 *
 * @returns {JSX.Elemet} the element that creates the container and the map
 */
const App = (): JSX.Element => {
  const classes = useStyles();

  /**
   * initialize the map after it has been loaded
   */
  useEffect(() => {
    cgpv.init(() => {
      /**
       * translations object to inject to the viewer translations
       */
      const translations = {
        'en': translationEn,
        'fr': translationFr,
      };

      // get map instance
      const mapInstance = cgpv.api.map('mapWM');

      // add custom languages
      mapInstance.i18nInstance.addResourceBundle(
        'en',
        'translation',
        translations['en'],
        true,
        false,
      );
      mapInstance.i18nInstance.addResourceBundle(
        'fr',
        'translation',
        translations['fr'],
        true,
        false,
      );

      // get language
      //  const { language }: { language: 'en-CA' | 'fr-CA' } = mapInstance;
      const language = 'en';

      const MapIcon = cgpv.ui.elements.MapIcon;

      // button props
      const geolocatorButton: TypeIconButtonProps = {
        // set ID so that it can be accessed from the core viewer
        id: 'geolocatorButtonPanel',
        tooltip: translations[language].custom.geolocatorPanelTitle,
        tooltipPlacement: 'right',
        children: <MapIcon />,
        visible: true,
      };

      // panel props
      const geolocatorPanel: TypePanelProps = {
        title: translations[language].custom.geolocatorPanelTitle,
        icon: <MapIcon />,
        width: 500,
      };

      // create a new button panel on the appbar
      const geolocatorButtonPanel = cgpv.api
        .map('mapWM')
        .appBarButtons.createAppbarPanel(geolocatorButton, geolocatorPanel, null);

      // set panel content
      geolocatorButtonPanel?.panel?.changeContent(
        <GeolocatorPanelContent buttonPanel={geolocatorButtonPanel} mapId={'mapWM'} />,
      );
    });
  }, []);

  return (
    <div
      id="mapWM"
      className={`llwp-map ${classes.container}`}
      style={{
        height: '100vh',
        zIndex: 0,
      }}
      data-lang="en"
      data-config="{
        'map': {
          'interaction': 'dynamic',
          'viewSettings': {
            'zoom': 4,
            'center': [-100, 60],
            'projection': 3857
          },
          'basemapOptions': {
            'basemapId': 'transport',
            'shaded': false,
            'labeled': true
          }
        },
        'theme': 'dark',
        'components': ['app-bar'],
        'suportedLanguages': ['en', 'fr']
        }"
    ></div>
  );
};

export default App;
