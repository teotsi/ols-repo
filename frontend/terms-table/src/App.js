import { Table } from "antd";
import useTerms from "./hooks/useTerms";
import "./App.css";

function App() {
  const [pageData, setPageData, data, fetching] = useTerms();

  const columns = [
    {
      title: "Label",
      dataIndex: "label",
      key: "label",
    },
    {
      title: "Description",
      dataIndex: "description",
      key: "description",
    },
    {
      title: "Synonyms",
      key: "synonyms",
      dataIndex: "synonyms",
      render: (_, { synonyms }) => <>{synonyms.join(", ")}</>,
    },
    {
      title: "Parents",
      key: "parents",
      dataIndex: "parents",
      render: (_, { parents }) => <>{parents.join(", ")}</>,
    },
  ];

  const formattedData =
    data?.map((term, index) => ({
      ...term,
      key: index,
    })) ?? [];

  const handlePageChange = (pagination) => {
    setPageData(pagination);
  };
  return (
    <div className="App">
      <div className="centered">
        <Table
          columns={columns}
          dataSource={formattedData}
          pagination={{ ...pageData, showSizeChanger: false }}
          onChange={handlePageChange}
          loading={fetching}
        />
      </div>
    </div>
  );
}

export default App;
