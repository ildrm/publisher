import {createRoot} from 'react-dom/client';
import App from './App';
import {LocaleProvider} from '../../../packages/i18n/index';
import './styles.css';
createRoot(document.getElementById('root')!).render(<LocaleProvider><App/></LocaleProvider>);
