import { useMemo } from "react";
import { Table } from "antd";

const TermTable = ({ data, pageData, onChange, fetching }) => {
  const columns = useMemo(
    () => [
      {
        title: "Label",
        dataIndex: "label",
      },
      {
        title: "Description",
        dataIndex: "description",
      },
      {
        title: "Synonyms",
        dataIndex: "synonyms",
        align: "center",
        render: (_, { synonyms }) => <>{synonyms.join(", ") || "-"}</>,
      },
      {
        title: "Parents",
        dataIndex: "parents",
        align: "center",
        render: (_, { parents }) => <>{parents.join(", ")}</>,
      },
    ],
    []
  );

  return (
    <>
      <h1 className="centered-text">EFO Terms Index</h1>
      <Table
        columns={columns}
        dataSource={data}
        pagination={{ ...pageData, showSizeChanger: false }}
        onChange={onChange}
        loading={fetching}
        scroll={{ y: "75vh" }}
      />
    </>
  );
};

export default TermTable;
