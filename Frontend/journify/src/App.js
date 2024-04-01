import { BrowserRouter, Route, Routes } from 'react-router-dom';
import AuthCallbackPage from './pages/Callback';
import Home from './pages/Home';
import Login from './pages/Login';
import './styles/shared.module.scss';
import { AuthProvider } from './providers/AuthProvider';
import { useAuth } from './providers/AuthProvider';
import { Navigate } from 'react-router-dom';



function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/callback" element={
            <ProtectedRouteIfLoggedIn>
              <AuthCallbackPage />
            </ProtectedRouteIfLoggedIn>
          } />
          <Route path="/home" element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          } />
          <Route path="/" index element={
            <ProtectedRouteIfLoggedIn>
              <Login />
            </ProtectedRouteIfLoggedIn>
          } />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export const ProtectedRoute = ({ children }) => {
  const { token } = useAuth();
  if (!token) {
    return <Navigate to="/" />
  }
  return children;
};

export const ProtectedRouteIfLoggedIn = ({ children }) => {
  const { token } = useAuth();
  if (token) {
    return <Navigate to="/home" />
  }
  return children;
};


export default App;
