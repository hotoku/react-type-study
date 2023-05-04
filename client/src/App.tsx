import "./App.css";
import ClientList from "./components/ClientList";
import ErrorBoundary from "./ErrorBoundary";

function App() {
  return (
    <div className="App">
      <div>sample application</div>
      <ErrorBoundary>
        <ClientList />
      </ErrorBoundary>
    </div>
  );
}

export default App;
