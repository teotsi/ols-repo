import TermTable from "./components/TermTable";
import ErrorMessage from "./components/ErrorMessage";
import useTerms from "./hooks/useTerms";
import "./App.css";

function App() {
  const { pageData, setPageData, data, fetching, error } = useTerms();

  const handlePageChange = (pagination) => {
    setPageData(pagination);
  };
  return (
    <div className="App">
      <div className="centered">
        <div className="table-wrapper">
          <TermTable
            data={data}
            onChange={handlePageChange}
            fetching={fetching}
            pageData={pageData}
          />
        </div>
        {error && <ErrorMessage error={error} />}
      </div>
    </div>
  );
}

export default App;
