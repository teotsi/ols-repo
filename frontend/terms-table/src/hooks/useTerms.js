import { useEffect, useState } from "react";
import { DOMAIN } from "../config";
import { formatTermData } from "../helpers/formatting";

/**
 * Hook that fetches terms by page, and stores pagination data for our table
 * @returns [pagination data, pagination data setter, table data, fetching flag]
 */
const useTerms = () => {
  const [data, setData] = useState([]);
  const [fetching, setFetching] = useState(false);
  const [error, setError] = useState();
  const [pageData, setPageData] = useState({
    current: 1,
    total: 1,
    pageSize: 20,
  });
  const abortController = new AbortController();

  const fetcher = async () => {
    setFetching(true);
    try {
      const response = await fetch(
        `${DOMAIN}/terms/?page=${pageData.current}`,
        {
          signal: abortController.signal,
        }
      );
      const data = await response.json();
      setData(formatTermData(data.terms));
      setFetching(false);
      const { current, total, size: pageSize } = data.pagination;
      setPageData({ current, total, pageSize });
    } catch (error) {
      console.error(error);
      setError(error);
      setData([]);
      setFetching(false);
      setPageData({ current: 0, total: 0, pageSize: 0 });
    }
  };

  useEffect(() => {
    fetcher();
    return () => {
      abortController.abort();
    };
  }, [pageData.current]);

  return {pageData, setPageData, data, fetching, error};
};

export default useTerms;
