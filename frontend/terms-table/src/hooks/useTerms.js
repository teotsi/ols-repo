import { useEffect, useState } from "react";

const useTerms = () => {
  const [data, setData] = useState([]);
  const [pageData, setPageData] = useState({
    current: 1,
    total: 1,
    pageSize: 20,
  });
  const abortController = new AbortController();

  const fetcher = async () => {
    const response = await fetch(
      `http://localhost:8000/terms?page=${pageData.current}`,
      {
        signal: abortController.signal,
      }
    );
    const data = await response.json();
    setData(data.terms);
    const { current, pages: total, size: pageSize } = data.pagination;
    setPageData({ current, total, pageSize });
  };

  useEffect(() => {
    fetcher();
    return () => {
      abortController.abort();
    };
  }, [pageData.current]);

  return [pageData, setPageData, data];
};

export default useTerms;
