import { BrowserRouter as Router } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import AuthProvider from './contexts/AuthProvider';
import AppRoutes from './routes';
import 'react-toastify/dist/ReactToastify.css';
import './style/main.scss';

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppRoutes />
        <ToastContainer
          position="top-right"
          autoClose={3000}
          newestOnTop={false}
        />
      </AuthProvider>
    </Router>
  );
}

export default App;
