import { render } from 'react-dom';
import { createContext } from 'react';

import App from './components/app';
import { Provider } from 'react-redux';
import store from './store';

const container = document.getElementById('root');
// render(<Provider store={store}><App /></Provider>, container);

export const AppContext = createContext({store});

function AppWrapper() {
    // const store = createStore(rootReducer);
  
    return (<>
      <Provider store={store}>
        <App />
      </Provider>
    </>)
  }

  render(AppWrapper(), container);
export default AppWrapper;