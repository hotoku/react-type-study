import { BrowserRouter, Route, Routes } from "react-router-dom";
import "./App.css";
import ClientEditor from "./components/ClientEditor";
import ClientList from "./components/ClientList";
import ErrorBoundary from "./ErrorBoundary";

function MyRoutes(): JSX.Element {
  return (
    <Routes>
      <Route index element={<ClientList />} />,
      <Route path="/clients/new" element={<ClientEditor />} />
    </Routes>
  );
}

function App(): JSX.Element {
  return (
    <div className="App">
      <header>sample application</header>
      <main>
        <ErrorBoundary>
          <BrowserRouter>
            <MyRoutes />
          </BrowserRouter>
        </ErrorBoundary>
      </main>
    </div>
  );
}

export default App;
