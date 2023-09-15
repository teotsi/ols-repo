import { useEffect, useState } from "react";
import { DOMAIN } from "../config";

/**
 * Hook that fetches terms by page, and stores pagination data for our table
 * @returns [pagination data, pagination data setter, table data, fetching flag]
 */
const useTerms = () => {
  const [data, setData] = useState([]);
  const [fetching, setFetching] = useState(false);
  const [pageData, setPageData] = useState({
    current: 1,
    total: 1,
    pageSize: 20,
  });
  const abortController = new AbortController();

  const fetcher = async () => {
    setFetching(true);
    const response = await fetch(
      `${DOMAIN}/terms/?page=${pageData.current}`,
      {
        signal: abortController.signal,
      }
    );
    const data = await response.json();
    setData(data.terms);
    setFetching(false);
    const { current, total, size: pageSize } = data.pagination;
    setPageData({ current, total, pageSize });
  };

  useEffect(() => {
    fetcher();
    return () => {
      abortController.abort();
    };
  }, [pageData.current]);

  return [pageData, setPageData, data, fetching];
};

export default useTerms;
